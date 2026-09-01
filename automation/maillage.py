#!/usr/bin/env python3
"""
MAILLAGE INTERNE du site public de Virginie Deconinck.

Ce qu'il n'est PAS :
  - monitoring.py, qui verifie que les liens ne sont pas CASSES. Un site peut
    n'avoir aucun lien casse et un maillage catastrophique : ce sont deux choses
    sans rapport.
  - seo-geo.py, qui lit la demande reelle chez Google. Lui regarde le dehors,
    celui-ci regarde le dedans.

Ce qu'il EST : la mesure du jus interne. Quelles pages en recoivent, lesquelles
sont abandonnees, et OU ajouter un lien pour que ca change quelque chose.

Le point central, souvent rate : un lien de MENU ne vaut presque rien. Il est sur
les 20 pages, il ne transmet aucun contexte, et les moteurs le savent. Ce qui
compte est le lien EN CORPS DE TEXTE, entoure de phrases sur le sujet. Ce script
ne compte donc que ceux-la : il retire d'abord <nav>, <footer>, <head>, <script>
et <style> de chaque page, et travaille sur ce qui reste.

Il ne se contente pas de compter. Sa section la plus utile est OCCASIONS
MANQUEES : les pages qui parlent deja du sujet d'une autre page, dans leur texte,
sans lier vers elle. Ce sont des liens a poser ce matin, pas des statistiques.

Croise avec Google Search Console quand la cle est disponible, pour trier par
enjeu reel plutot que par ordre alphabetique : une page sous-maillee que
personne ne cherche n'est pas une urgence, une page sous-maillee qui plafonne en
9e position en est une.

Lecture seule. Ne modifie ni le site, ni aucun contenu.

Usage :  python3 automation/maillage.py [--markdown] [--jours 28]
"""

import re, sys, json, html, argparse, collections, datetime, time
import urllib.request, urllib.error, urllib.parse
import os.path

SITE = "https://virginiedeconinck.com"
TIMEOUT = 30
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# En dessous, une page ne recoit pas assez de contexte pour peser. Seuil bas
# assume : sur un site de 20 pages, exiger 5 liens entrants par page produirait
# un maillage artificiel, et Google traite le sur-maillage comme du bruit.
SEUIL_ENTRANTS = 3

# Ancres qui ne disent rien de la destination. Elles gaspillent le seul signal
# que le lien transmet : le mot sur lequel on veut que la page cible sorte.
ANCRES_PAUVRES = {
    "ici", "cliquez ici", "cliquer ici", "en savoir plus", "savoir plus", "lire",
    "lire la suite", "lire plus", "voir", "voir plus", "cette page", "ce lien",
    "la page", "decouvrir", "decouvrez", "acceder", "y acceder", "plus", "suite",
    "commencer", "continuer", "lien",
}

# Mots qui n'identifient aucune page en particulier. Deux familles, toutes deux
# mesurees sur la sortie reelle du 02/08/2026, qui proposait sans cela de poser
# un lien sur « ans », sur « propos » ou sur « age » :
#   - les mots de structure du site (femme, feminin, apres) ;
#   - le vocabulaire de fond present sur TOUTES les pages d'un site qui parle de
#     rajeunissement cellulaire feminin : cellules, hormones, longevite. Un lien
#     pose sur ces mots-la ne dit rien a Google, il dilue.
MOTS_VIDES = {
    "femme", "femmes", "feminin", "feminine", "apres", "avant", "pour", "avec",
    "blog", "index", "sans", "dans", "plus", "chez", "vers", "cellulaire",
    "propos", "cellules", "hormones", "actives", "longevite", "corps", "sante",
    "biologique", "chronologique", "vieillissement", "rajeunissement",
}

# En dessous de 5 caracteres, un mot tire d'une adresse est presque toujours un
# mot courant du francais (age, ans, peau) et non un sujet. Exception faite des
# sigles, reconnus parce qu'ils apparaissent en majuscules dans le titre de la
# page : SHBG, NAD, GLP-1 sont au contraire les termes les plus distinctifs du site.
LONGUEUR_MIN_TERME = 5

# CONTEXTES TROMPEURS. Un mot tire d'une adresse peut exister dans le francais
# courant avec un tout autre sens : le trouver dans une phrase ne prouve donc pas
# que la phrase parle de la page cible. Sans ce garde-fou, le rapport propose un
# CONTRESENS, et il le repropose chaque mois tant que le moteur n'apprend rien.
# Mesure : le 02/08/2026 le rapport proposait de lier « l'entrainement en
# RESISTANCE » (de la musculation) vers /resistance-insuline. Ecarte a la main.
# Le 01/09/2026, un mois plus tard, il proposait exactement la meme chose, parce
# que la correction n'avait ete faite que dans le rapport, jamais dans le code.
# Meme famille : « reveils NOCTURNES », dans une liste de symptomes, propose vers
# un article sur la glycemie nocturne et la peau.
# Regle : le terme ne compte pas s'il apparait dans l'une de ces expressions.
CONTEXTES_TROMPEURS = {
    "resistance": ("entrainement en resistance", "entrainement de resistance",
                   "exercice en resistance", "exercices en resistance",
                   "travail en resistance", "resistance musculaire",
                   "bandes de resistance"),
    "nocturne": ("reveils nocturnes", "reveil nocturne", "sueurs nocturnes",
                 "insomnies nocturnes"),
}


def terme_present(terme, texte):
    """Le terme apparait-il AILLEURS que dans un contexte trompeur ?

    On efface d'abord les expressions qui detournent le mot, puis on cherche.
    Effacer plutot que compter evite le faux negatif : une page qui emploie le
    mot deux fois, une fois a tort et une fois a raison, reste eligible.
    """
    for expr in CONTEXTES_TROMPEURS.get(terme, ()):
        texte = texte.replace(expr, " ")
    return terme in texte

# GARDE-FOUS DE DENSITE. Un maillage qui part dans tous les sens est pire que pas
# de maillage : la page devient un annuaire, la lecture casse, et Google dilue le
# poids entre trop de sorties. Mesure du site le 02/08/2026 : 29 261 mots pour 219
# liens de corps, soit 1 lien pour 133 mots en moyenne, ce qui est sain. Les seules
# pages denses sont l'accueil (1/72) et /blog (1/55), et c'est normal : ce sont des
# index, leur role EST de distribuer. A l'oppose, /shbg-hormones-actives-femme
# affiche 3 518 mots pour 10 liens (1/351) : c'est la qu'il reste de la place.
#
# On n'ajoute donc un lien QUE si la page source garde au moins 1 lien pour 110
# mots apres ajout, et jamais plus de 2 ajouts sur la meme page en une fois.
MOTS_PAR_LIEN_MIN = 110
AJOUTS_MAX_PAR_SOURCE = 2

# Les pages d'INDEX echappent au seuil : leur metier EST de distribuer vers le
# reste du site, pas de retenir la lectrice. Leur appliquer la meme regle qu'a un
# article ferait retirer des liens utiles pour satisfaire un chiffre.
PAGES_INDEX = {"/", "/blog"}


# ------------------------------------------------------------------ RESEAU
_cache = {}

# Une panne PASSAGERE ne doit pas faire tomber tout le rapport de la semaine.
# Mesure du 03/08/2026 : le job SEO a echoue sur un sitemap.xml en HTTP 500,
# servi pendant la propagation d'un deploiement Netlify. Rechargee 40 secondes
# plus tard, la meme adresse repondait 200 avec ses 20 URLs. Sans relance, un
# hoquet d'une seconde prive Virginie de tout le rapport hebdomadaire.
#
# On ne relance QUE les coupures reseau et les erreurs SERVEUR (5xx). Un 404 ou
# un 410 n'est jamais rejoue : une page vraiment absente doit rester absente,
# c'est precisement le defaut que ce script cherche a trouver. Masquer un 404
# derriere une relance reviendrait a rendre le controle aveugle.
TENTATIVES = 3
ATTENTES = (2, 5)   # secondes avant la 2e puis la 3e tentative


def passagere(code):
    return code == 0 or 500 <= code < 600


def http(url):
    if url in _cache:
        return _cache[url]
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    res = (0, "")
    for essai in range(TENTATIVES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                res = (r.status, r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            res = (e.code, "")
        except Exception:
            res = (0, "")
        if not passagere(res[0]):
            break
        if essai < TENTATIVES - 1:
            print(f"  {url} : HTTP {res[0]}, nouvelle tentative dans {ATTENTES[essai]} s "
                  f"({essai + 2}/{TENTATIVES})", file=sys.stderr)
            time.sleep(ATTENTES[essai])
    # L'echec definitif est mis en cache lui aussi : inutile de re-tenter trois
    # fois la meme adresse a chaque appel suivant dans le meme passage.
    _cache[url] = res
    return res


def sansaccent(x):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", x.lower())
                   if unicodedata.category(c) != "Mn")


def chemin(url):
    c = url.split("#")[0].split("?")[0]
    c = c.replace("https://virginiedeconinck.com", "").replace(
        "http://virginiedeconinck.com", "")
    return (c.rstrip("/") or "/")


def corps_utile(brut):
    """Le HTML prive de tout ce qui se repete sur chaque page.

    Sans ce nettoyage, chaque page recevrait ~20 liens entrants venant du menu
    et du pied de page, et TOUTES paraitraient parfaitement maillees. Le rapport
    dirait que tout va bien en permanence, ce qui est exactement le defaut qu'on
    cherche a eviter.
    """
    return re.sub(r'(?is)<(script|style|nav|footer|head)\b[^>]*>.*?</\1\s*>', " ", brut)


def corps_liable(brut):
    """Le corps ou l'on a le droit d'aller CHERCHER une ancre.

    Plus etroit que corps_utile : on retire en plus les citations de Virginie
    (`div.highlight`, `blockquote`) ET son bloc de voix a la premiere personne,
    repere par le commentaire `<!-- VOICE INTRO -->` : c'est sa parole, pas de
    la prose d'article. Y planter un lien casse la voix du texte et se voit.
    Mesure du 02/08/2026 : le rapport proposait de poser un lien dans un
    temoignage, ecarte a la main ; le 01/09/2026 il proposait « ma glycemie et ma
    recuperation », tire de la citation de /muscle-longevite-feminine. Ecarte a la
    main une deuxieme fois, faute d'avoir corrige le moteur la premiere.
    """
    sans_voix = re.sub(r'(?is)<!--\s*VOICE INTRO\s*-->.*?</section\s*>', " ",
                       corps_utile(brut))
    sans_cit = re.sub(
        r'(?is)<div[^>]*class="[^"]*\bhighlight\b[^"]*"[^>]*>.*?</div\s*>',
        " ", sans_voix)
    return re.sub(r'(?is)<(blockquote)\b[^>]*>.*?</\1\s*>', " ", sans_cit)


def texte_seul(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


# ------------------------------------------------------------------ COLLECTE
LIEN = re.compile(r'(?is)<a\b[^>]*?href\s*=\s*(["\'])(.*?)\1[^>]*>(.*?)</a\s*>')


def collecte():
    code, sm = http(f"{SITE}/sitemap.xml")
    if code != 200 or not sm:
        print(f"ECHEC : sitemap.xml inaccessible (HTTP {code}) apres {TENTATIVES} tentatives.")
        sys.exit(1)
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    pages = {}
    for u in urls:
        c = chemin(u)
        code, brut = http(u)
        if code != 200:
            print(f"  (page ignoree, HTTP {code} : {c})")
            continue
        corps = corps_utile(brut)
        txt = texte_seul(corps)
        h1 = re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", brut)
        sortants = []
        for _, href, ancre in LIEN.findall(corps):
            href = html.unescape(href).strip()
            if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            absolu = urllib.parse.urljoin(u, href)
            if not absolu.startswith(("https://virginiedeconinck.com",
                                      "http://virginiedeconinck.com")):
                continue                      # lien externe : hors sujet ici
            cible = chemin(absolu)
            if cible == c:
                continue                      # lien vers soi-meme
            sortants.append((cible, texte_seul(ancre)))
        pages[c] = {
            "url": u,
            "titre": texte_seul(h1[0]) if h1 else "",
            "texte": sansaccent(txt),
            # Texte ou l'on a le droit de CHERCHER une ancre : citations retirees.
            # Distinct de "texte", qui sert au comptage de mots et doit rester
            # comparable d'un mois sur l'autre.
            "texte_liable": sansaccent(texte_seul(corps_liable(brut))),
            "mots": len(txt.split()),
            "sortants": sortants,
        }
    return pages


def termes_distinctifs(pages):
    """Le ou les mots par lesquels une page se reconnait dans une phrase.

    Un mot present dans plusieurs adresses n'identifie personne : le retenir
    ferait proposer n'importe quel lien vers n'importe quelle page. On ne garde
    donc que les mots propres a UNE seule page, assez longs pour etre un sujet
    et non un mot outil, plus les sigles ecrits en majuscules dans le titre.
    """
    freq = collections.Counter()
    par_page = {}
    for c, p in pages.items():
        titre = p.get("titre", "")
        mots = []
        for m in re.findall(r"[a-z0-9]+", sansaccent(c)):
            if m in MOTS_VIDES or m in mots:          # dedoublonne : "/age-...-age-..."
                continue
            # Le titre est compare TEL QUEL, sans passage en majuscules : c'est
            # justement le fait d'etre ecrit en capitales qui distingue un sigle
            # d'un mot courant. Mesure du 02/08/2026 : avec titre.upper(), le
            # « ans » de « apres 40 ans » etait pris pour un sigle et le rapport
            # proposait serieusement de poser un lien sur le mot « ans ».
            sigle = len(m) <= 4 and m.isalpha() and m.upper() in titre
            if len(m) >= LONGUEUR_MIN_TERME or sigle:
                mots.append(m)
        par_page[c] = mots
        for m in set(mots):
            freq[m] += 1
    return {c: [m for m in mots if freq[m] == 1] for c, mots in par_page.items()}


# ------------------------------------------------- SEARCH CONSOLE (optionnel)
def donnees_google(jours):
    """Reutilise le moteur de seo-geo.py plutot que de redupliquer son
    authentification. Si la cle manque, on continue sans : la structure du
    maillage reste mesurable, seul le classement par enjeu est perdu."""
    ici = os.path.dirname(os.path.abspath(__file__))
    chemin_seo = os.path.join(ici, "seo-geo.py")
    if not os.path.exists(chemin_seo):
        return None, "seo-geo.py introuvable"
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("seogeo", chemin_seo)
        mod = importlib.util.module_from_spec(spec)
        sys.argv = [sys.argv[0]]          # le module lit argparse a l'import de main()
        spec.loader.exec_module(mod)
        tok = mod.jeton()
        fin = datetime.date.today() - datetime.timedelta(days=mod.LATENCE)
        debut = fin - datetime.timedelta(days=jours - 1)
        lignes = mod.interroge(tok, debut.isoformat(), fin.isoformat(), ["page"])
        out = {}
        for r in lignes:
            c = chemin(r["keys"][0])
            if c in out:                   # http et https fusionnes sur le meme chemin
                out[c]["impressions"] += r["impressions"]
                out[c]["clics"] += r["clicks"]
            else:
                out[c] = {"impressions": r["impressions"], "clics": r["clicks"],
                          "position": r["position"]}
        return out, None
    except SystemExit:
        return None, "cle Search Console absente"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ------------------------------------------------------------------ ANALYSE
def analyse(jours):
    pages = collecte()
    if not pages:
        print("ECHEC : aucune page collectee.")
        sys.exit(1)

    entrants = collections.defaultdict(list)      # cible -> [(source, ancre)]
    for c, p in pages.items():
        for cible, ancre in p["sortants"]:
            entrants[cible].append((c, ancre))

    sc, err_sc = donnees_google(jours)
    termes = termes_distinctifs(pages)

    def enjeu(c):
        """Impressions Google si connues. Sert a trier par ce que ca rapporte."""
        return (sc or {}).get(c, {}).get("impressions", 0)

    sections = []
    ajoute = sections.append

    # ---------- 0. ETAT DES LIEUX ----------
    total_liens = sum(len(p["sortants"]) for p in pages.values())
    total_mots = sum(p["mots"] for p in pages.values())
    moy = total_liens / len(pages) if pages else 0
    dens = total_mots / total_liens if total_liens else 0
    tete = [
        f"{len(pages)} pages, {total_mots} mots, {total_liens} liens internes EN CORPS DE "
        f"TEXTE (moyenne {moy:.1f} par page).",
        "Les liens de menu et de pied de page sont volontairement exclus : presents",
        "partout, ils ne transmettent aucun contexte et fausseraient toute la mesure.",
        "",
        f"DENSITE GLOBALE : 1 lien pour {dens:.0f} mots. Reference : 1 pour 100 a 150 reste",
        "naturel ; sous 70, la page se lit comme un annuaire.",
    ]
    # Les pages les plus longues et les moins liees sont celles ou il reste de la
    # place. Les nommer evite d'aller charger celles qui sont deja pleines.
    marges = sorted(((p["mots"] / len(p["sortants"]), c) for c, p in pages.items()
                     if p["sortants"]), reverse=True)[:4]
    tete.append("Le plus de marge : " + ", ".join(f"{c} (1/{d:.0f})" for d, c in marges) + ".")
    tete.append("Donnees Google croisees : " + (
        f"oui, {jours} derniers jours." if sc else f"NON ({err_sc}). Classement par structure seule."))
    ajoute(("ETAT DES LIEUX", tete))

    # ---------- 1. ORPHELINES ----------
    orphelines = sorted([c for c in pages if not entrants.get(c)],
                        key=lambda c: -enjeu(c))
    ajoute((f"PAGES ORPHELINES ({len(orphelines)})", [
        "Aucune autre page ne pointe vers elles autrement que par le menu. Pour Google",
        "elles sont des culs-de-sac : rien n'indique de quoi elles parlent ni qu'elles",
        "comptent. C'est le defaut de maillage le plus couteux, et le plus simple a corriger.",
        ""] + [
        f"  {c}   ({enjeu(c):.0f} impr./{jours}j)" if sc else f"  {c}"
        for c in orphelines] or ["  aucune"]))

    # ---------- 2. SOUS-MAILLEES A ENJEU ----------
    sous = []
    for c, p in pages.items():
        n = len(entrants.get(c, []))
        if 0 < n < SEUIL_ENTRANTS:
            sous.append((c, n))
    sous.sort(key=lambda x: (-enjeu(x[0]), x[1]))
    ajoute((f"SOUS-MAILLEES (moins de {SEUIL_ENTRANTS} liens entrants) ({len(sous)})", [
        "Triees par impressions reelles : celles du haut sont deja vues par Google et",
        "plafonnent, un lien de plus les fait bouger. Celles du bas ne cherchent personne,",
        "les mailler ne rapporterait rien aujourd'hui.",
        ""] + [
        (f"  {n} entrant(s)  {c}   ({enjeu(c):.0f} impr., pos "
         f"{(sc or {}).get(c, {}).get('position', 0):.1f})") if sc else
        f"  {n} entrant(s)  {c}"
        for c, n in sous] or ["  aucune"]))

    # ---------- 3. OCCASIONS MANQUEES ----------
    # Le coeur du fichier : des liens a poser, pas des chiffres a regarder.
    # Une occasion n'a de valeur que si la CIBLE en a besoin. Proposer quatre
    # liens de plus vers une page qui en compte deja dix-huit ne la fera pas
    # monter d'un rang : ca dilue le maillage et ca remplit le rapport de travail
    # inutile. Trois situations, et trois seulement, justifient un lien de plus :
    besoins = {}
    for c in pages:
        n = len(entrants.get(c, []))
        d = (sc or {}).get(c, {})
        if n < SEUIL_ENTRANTS:
            besoins[c] = f"{n} lien(s) entrant(s) seulement"
        elif sc and d.get("impressions", 0) == 0:
            besoins[c] = "page muette : aucune impression Google sur la periode"
        elif sc and 4 <= d.get("position", 0) <= 20:
            besoins[c] = (f"a portee : position {d['position']:.1f} pour "
                          f"{d['impressions']:.0f} impressions, un rang gagne se voit")

    occasions = []
    for cible in besoins:
        mots = termes.get(cible, [])
        if not mots:
            continue
        deja = {s for s, _ in entrants.get(cible, [])}
        for source, p_src in pages.items():
            if source == cible or source in deja:
                continue
            trouves = [m for m in mots
                       if terme_present(m, p_src["texte_liable"])]
            if trouves:
                # Une source qui recoit deja du trafic transmet davantage qu'une
                # page que personne ne visite : elle passe en premier.
                occasions.append((enjeu(cible), enjeu(source), cible, source, trouves))
    occasions.sort(key=lambda x: (-x[0], -x[1], x[3]))

    # Filtre de densite : on retient les propositions une par une, en tenant a jour
    # le nombre de liens que chaque page source porterait APRES ajout. Une page qui
    # tomberait sous le seuil est ecartee, et on le DIT, plutot que de la charger.
    charge = {c: len(p["sortants"]) for c, p in pages.items()}
    ajouts = collections.Counter()
    retenues, ecartees = [], []
    for _, _, cible, source, mots in occasions:
        futur = charge[source] + 1
        densite = pages[source]["mots"] / futur if futur else 0
        if densite < MOTS_PAR_LIEN_MIN and source not in PAGES_INDEX:
            ecartees.append((source, cible, f"deviendrait 1 lien / {densite:.0f} mots"))
        elif ajouts[source] >= AJOUTS_MAX_PAR_SOURCE:
            ecartees.append((source, cible, f"deja {AJOUTS_MAX_PAR_SOURCE} ajouts prevus ici"))
        else:
            charge[source] = futur
            ajouts[source] += 1
            retenues.append((cible, source, mots))

    par_cible = collections.OrderedDict()
    for cible, source, mots in retenues:
        par_cible.setdefault(cible, []).append((source, mots))
    lignes = []
    for cible, liste in par_cible.items():
        n = len(entrants.get(cible, []))
        det = f"{enjeu(cible):.0f} impr., {n} entrant(s)" if sc else f"{n} entrant(s)"
        lignes.append(f"  VERS {cible}   ({det})")
        lignes.append(f"      pourquoi elle : {besoins[cible]}")
        for source, mots in liste:
            d = pages[source]["mots"] / charge[source]
            lignes.append(f"      depuis {source}  (ancre : {', '.join(mots)}"
                          f"  |  cette page resterait a 1 lien / {d:.0f} mots)")
    if ecartees:
        lignes.append("")
        lignes.append(f"  ECARTEES pour ne pas surcharger ({len(ecartees)}) :")
        for source, cible, motif in ecartees[:8]:
            lignes.append(f"      {source} -> {cible}   ({motif})")
    ajoute((f"OCCASIONS MANQUEES ({len(occasions)} liens possibles, "
            f"{len(par_cible)} pages concernees)", [
        "Ces pages parlent DEJA du sujet d'une autre page, dans leur corps de texte,",
        "sans lier vers elle. Le contexte est en place : il ne manque que le lien.",
        "Le mot indique est celui a transformer en ancre, tel quel, dans la phrase",
        "qui existe. Ne jamais ecrire une phrase artificielle juste pour caser un lien.",
        "",
        "Deux filtres, pour que le maillage ne parte pas dans tous les sens :",
        "  - la CIBLE doit avoir un besoin mesure (sous-maillee, muette chez Google, ou",
        "    a portee d'un gain de position). Les autres sont deja servies.",
        f"  - la SOURCE doit garder au moins 1 lien pour {MOTS_PAR_LIEN_MIN} mots apres ajout, et ne",
        f"    recoit jamais plus de {AJOUTS_MAX_PAR_SOURCE} liens en une fois. Une page trop liee devient un",
        "    annuaire : la lecture casse et le poids se dilue entre trop de sorties.",
        ""] + (lignes or ["  aucune"])))

    # ---------- 4. ANCRES PAUVRES ----------
    pauvres, nues = [], []
    for c, p in pages.items():
        for cible, ancre in p["sortants"]:
            a = sansaccent(ancre).strip(" .,:;!?»« ")
            if not a:
                nues.append((c, cible, "(ancre vide : lien sur une image ou un bouton nu)"))
            elif a in ANCRES_PAUVRES:
                pauvres.append((c, cible, ancre))
            elif a.startswith("http") or a.startswith("www."):
                pauvres.append((c, cible, ancre))
    ajoute((f"ANCRES QUI NE DISENT RIEN ({len(pauvres) + len(nues)})", [
        "Le texte cliquable est le seul indice que le lien donne aux moteurs sur la page",
        "d'arrivee. « en savoir plus » gaspille ce signal. A remplacer par les mots sur",
        "lesquels vous voulez que la page cible sorte.",
        ""] + [
        f"  {src} -> {cible}   ancre : « {a} »" for src, cible, a in (pauvres + nues)[:20]
    ] or ["  aucune"]))

    # ---------- 5. PROFONDEUR ----------
    # Distance en clics depuis l'accueil, par les liens de CORPS uniquement.
    # Le menu masque completement ce probleme : il met tout a 1 clic en apparence,
    # alors que le poids reel transmis suit les liens contextuels.
    dist = {"/": 0}
    file = ["/"]
    while file:
        cur = file.pop(0)
        for cible, _ in pages.get(cur, {}).get("sortants", []):
            if cible in pages and cible not in dist:
                dist[cible] = dist[cur] + 1
                file.append(cible)
    loin = sorted([(d, c) for c, d in dist.items() if d >= 3], reverse=True)
    jamais = sorted([c for c in pages if c not in dist], key=lambda c: -enjeu(c))
    ajoute((f"PROFONDEUR DEPUIS L'ACCUEIL ({len(jamais)} inatteignables, {len(loin)} a 3 clics ou plus)", [
        "Chemin le plus court depuis la page d'accueil en ne suivant QUE les liens de",
        "corps de texte. Une page inatteignable par ce chemin ne recoit du poids que par",
        "le menu, c'est-a-dire presque rien.",
        ""] + [f"  INATTEIGNABLE  {c}" + (f"   ({enjeu(c):.0f} impr.)" if sc else "")
               for c in jamais]
        + [f"  {d} clics  {c}" for d, c in loin] or ["  tout est a moins de 3 clics"]))

    return sections, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--jours", type=int, default=28)
    args = ap.parse_args()

    sections, pages = analyse(args.jours)
    tampon = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    if args.markdown:
        out = [f"# Maillage interne virginiedeconinck.com\n",
               f"_Mesure du {tampon}, sur le site en ligne_\n"]
        for titre, lignes in sections:
            out.append(f"\n## {titre}\n")
            out.append("```\n" + "\n".join(lignes) + "\n```\n")
        txt = "\n".join(out)
        open("rapport-maillage.md", "w", encoding="utf-8").write(txt)
        print(txt)
    else:
        print(f"\n{'='*70}\n  MAILLAGE INTERNE virginiedeconinck.com   ({tampon})\n{'='*70}")
        for titre, lignes in sections:
            print(f"\n--- {titre} ---")
            for l in lignes:
                print(("  " + l) if not l.startswith(" ") else l)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
