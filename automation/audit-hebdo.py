#!/usr/bin/env python3
"""
AUDIT HEBDOMADAIRE INTEGRAL du site public de Virginie Deconinck.

Pourquoi ce fichier existe (demande de Virginie, 02/08/2026) : « si c'est une
fois par semaine, ca doit vraiment tout couvrir, tous les aspects », et non
regarder trois erreurs techniques et se dire que c'est bon.

Il applique sa definition d'un audit, qui est INTEGRAL ou n'est pas :
véracité réelle des références, rattachement référence/affirmation, exactitude,
cohérence interne et entre pages, forme, style, puis pour un site : liens, SEO,
GEO, et la même exigence de fond dans les FAQ et le JSON-LD que dans le corps.

Place dans le dispositif, sans recouvrement :
  monitoring.py  : est-ce CASSE ?              (quotidien, panne)
  seo-geo.py     : que cherche-t-on DEHORS ?   (Google, demande reelle)
  maillage.py    : comment le jus circule-t-il DEDANS ?
  audit-hebdo.py : le contenu est-il JUSTE, COHERENT et BIEN ECRIT ?  <- ici

Ce que la machine ne peut PAS faire, et qu'elle ne pretend donc pas faire : dire
si une etude soutient reellement l'affirmation a laquelle elle est accrochee. Le
script verifie que le DOI EXISTE et sort le titre reel de l'article ; la lecture
du rattachement reste un travail humain, signale comme tel.

Lecture seule. Ne modifie ni le site, ni aucun contenu.

Usage :  python3 automation/audit-hebdo.py [--markdown] [--sans-reseau]
"""

import re, sys, json, html, argparse, collections, datetime, unicodedata
import urllib.request, urllib.error, urllib.parse

SITE = "https://virginiedeconinck.com"
TIMEOUT = 30
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# --- Formules qui trahissent une redaction automatique. Virginie les traque
#     depuis longtemps : elles cassent la voix incarnee qui fait sa difference.
TICS = [
    "il est important de", "il convient de", "il est essentiel de", "force est de constater",
    "dans un monde où", "plongeons", "décryptage", "n'est plus à démontrer",
    "au cœur de", "véritable allié", "de nombreux experts", "il ne s'agit pas seulement",
    "bien plus qu'un", "la clé réside", "sans plus attendre", "vous l'aurez compris",
    "en un mot", "en résumé,", "il est crucial", "joue un rôle clé", "joue un rôle crucial",
    "révolutionnaire", "incontournable", "in fine",
]

# --- Marqueurs de PROTOCOLE. La ligne editoriale du site est d'expliquer les
#     mecanismes sans livrer la methode applicable : dosages, frequences, durees
#     et sequences appartiennent aux offres payantes. Ces motifs ne sont pas des
#     fautes en soi, ce sont des endroits a RELIRE.
PROTOCOLE = [
    (r"\b\d+\s?(mg|µg|mcg|g|UI|ui)\b", "dosage chiffre"),
    (r"\b\d+\s?(fois|x)\s?(par|/)\s?(jour|semaine|mois)", "frequence prescrite"),
    (r"\bpendant\s+\d+\s+(jours|semaines|mois)", "duree de cure"),
    (r"\bmatin et soir\b", "moment de prise"),
    (r"\bà jeun\b", "condition de prise"),
    (r"\bcure de\b", "cure"),
    (r"\bprotocole\s+(suivant|ci-dessous|en \d)", "protocole annonce"),
]

# --- Tutoiement. Le site vouvoie, strictement, partout.
TUTOIEMENT = [r"\btu\s", r"\btoi\b", r"\bton\s+(corps|âge|peau|sommeil|organisme|métabolisme)",
              r"\btes\s+(cellules|hormones|muscles|résultats)", r"\bvas-y\b", r"\btu\b\s*[,.]"]

erreurs, alertes, revues, infos = [], [], [], []
_sauts = []   # hierarchie de titres : suivie, sans action (voir audit_forme)
def ERREUR(cat, m): erreurs.append((cat, m))
def ALERTE(cat, m): alertes.append((cat, m))
def REVUE(cat, m):  revues.append((cat, m))      # a lire par un humain, pas un defaut
def INFO(m):        infos.append(m)

_cache = {}
def http(url, method="GET"):
    cle = (url, method)
    if cle in _cache:
        return _cache[cle]
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            res = (r.status, r.read().decode("utf-8", "replace") if method == "GET" else "", r.url)
    except urllib.error.HTTPError as e:
        res = (e.code, "", url)
    except Exception:
        res = (0, "", url)
    _cache[cle] = res
    return res


def texte(s):
    s = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>", " ", s)
    # Les balises INLINE ne produisent AUCUN espace a l'ecran : « l'<a>inflammation</a> »
    # se lit « l'inflammation ». Les remplacer par une espace, comme les balises de
    # bloc, fabriquait un « l' inflammation » introuvable dans le JSON-LD, donc un
    # faux ecart signale sur chaque reponse de FAQ contenant un lien. Mesure du
    # 02/08/2026, sur la FAQ de l'accueil ou trois liens contextuels venaient d'etre
    # poses : 2 reponses sur 3 declarees divergentes a tort.
    s = re.sub(r"(?is)</?(a|em|strong|b|i|span|sup|sub|small)\b[^>]*>", "", s)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def corps_visible(brut):
    return re.sub(r"(?is)<(script|style|nav|footer|head)\b[^>]*>.*?</\1\s*>", " ", brut)


def sansaccent(x):
    return "".join(c for c in unicodedata.normalize("NFD", x.lower())
                   if unicodedata.category(c) != "Mn")


def similitude(fragment, page):
    """Part des mots du fragment qui se retrouvent dans la page, dans l'ordre.

    Une comparaison de chaine brute echoue sur un mot change ; ici un ecart de
    formulation donne un score eleve (a signaler doucement) et une absence reelle
    un score bas (a signaler fort). C'est la difference entre « ce texte n'existe
    pas » et « ce texte a ete reecrit d'un cote seulement ».
    """
    import difflib
    a = sansaccent(fragment).split()
    if not a:
        return 1.0
    b = sansaccent(page).split()
    # On cherche le meilleur alignement local plutot que de comparer toute la page
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    communs = sum(bloc.size for bloc in m.get_matching_blocks())
    return communs / len(a)


# Verbes qui transforment une information en INSTRUCTION. Sans l'un d'eux a
# proximite, « a jeun » dans « glycemie a jeun » ou « pendant 12 mois » dans la
# definition de la menopause sont de la description clinique, pas un protocole.
# Mesure du 02/08/2026 : sans ce filtre, l'audit signalait ces deux phrases-la
# comme des fuites de contenu payant. Une fausse alerte repetee tue un audit.
VERBES_INSTRUCTION = (
    "prenez", "prendre", "consommez", "consommer", "faites", "appliquez", "suivez",
    "commencez", "augmentez", "reduisez", "visez", "ajoutez", "supplementez",
    "supplementation", "dosage recommande", "il faut prendre", "a raison de",
)


def protocoles_dans(txt):
    """Renvoie les extraits qui ressemblent VRAIMENT a une methode applicable."""
    out = []
    n = sansaccent(txt)
    for motif, quoi in PROTOCOLE:
        for m in re.finditer(motif, txt, re.I):
            autour = n[max(0, m.start() - 110):m.end() + 110]
            if any(v in autour for v in VERBES_INSTRUCTION):
                out.append((txt[max(0, m.start() - 70):m.end() + 70].strip(), quoi))
                break
    return out


# ====================================================================== COLLECTE
def collecte():
    code, sm, _ = http(f"{SITE}/sitemap.xml")
    if code != 200:
        print(f"ECHEC : sitemap inaccessible (HTTP {code})")
        sys.exit(1)
    pages = {}
    lastmods = dict(re.findall(r"<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]*)</lastmod>)?", sm))
    for u in re.findall(r"<loc>([^<]+)</loc>", sm):
        code, brut, _ = http(u)
        if code != 200:
            ERREUR("disponibilite", f"{u} renvoie HTTP {code}")
            continue
        vis = corps_visible(brut)
        pages[u.replace(SITE, "") or "/"] = {
            "url": u, "brut": brut, "visible": vis,
            "texte": texte(vis), "lastmod": lastmods.get(u, ""),
        }
    return pages


# ============================================ 1. FIDELITE JSON-LD <-> VISIBLE
def audit_json_ld(pages):
    """Le point que Virginie designe elle-meme comme le plus risque : « appliquer
    la meme regle de FOND dans les FAQ et le JSON-LD, pas seulement le corps,
    c'est la que les protocoles se cachent ».

    Une reponse presente UNIQUEMENT dans le JSON-LD est invisible pour la
    lectrice mais servie aux moteurs et aux IA. C'est du contenu hors controle :
    ni relu a l'ecran, ni soumis aux memes exigences.
    """
    for c, p in pages.items():
        vis_norm = sansaccent(p["texte"])
        for bloc in re.findall(r"(?is)<script[^>]*application/ld\+json[^>]*>(.*?)</script>", p["brut"]):
            try:
                d = json.loads(bloc)
            except Exception:
                continue                       # invalidite deja traitee par monitoring.py
            for item in (d if isinstance(d, list) else [d]):
                if not isinstance(item, dict):
                    continue
                t = item.get("@type", "")
                t = t if isinstance(t, list) else [t]

                if "FAQPage" in t:
                    for q in item.get("mainEntity", []):
                        nom = texte(str(q.get("name", "")))
                        rep = texte(str(q.get("acceptedAnswer", {}).get("text", "")))
                        if nom and sansaccent(nom)[:40] not in vis_norm:
                            ERREUR("json-ld", f"{c} : la question FAQ « {nom[:70]} » est servie "
                                              f"aux moteurs mais ABSENTE de la page visible")
                        if rep:
                            # Comparaison par SIMILARITE, jamais par prefixe exact.
                            # Mesure du 02/08/2026 : la page SHBG affiche « une part plus
                            # importante DE VOS hormones » quand son JSON-LD dit « DES
                            # hormones ». Le test par prefixe concluait « reponse
                            # invisible pour la lectrice », ce qui etait faux et
                            # alarmiste : le texte est bien la, c'est le vouvoiement qui
                            # n'a pas ete reporte dans les donnees structurees. Trois
                            # niveaux, pour que la gravite annoncee soit la vraie.
                            score = similitude(rep, p["texte"])
                            if score < 0.45:
                                ERREUR("json-ld", f"{c} : la REPONSE a « {nom[:45]} » est servie aux "
                                                  f"moteurs mais ne figure PAS sur la page visible "
                                                  f"(concordance {score:.0%})")
                            elif score < 0.95:
                                ALERTE("json-ld", f"{c} : la reponse a « {nom[:45]} » differe entre le "
                                                  f"JSON-LD et le texte affiche (concordance {score:.0%}) "
                                                  f"— verifier le vouvoiement et les chiffres")
                            for extrait, quoi in protocoles_dans(rep):
                                REVUE("frontiere", f"{c} : reponse FAQ du JSON-LD, {quoi} — "
                                                   f"«…{extrait}…»")

                if {"Article", "BlogPosting", "NewsArticle"} & set(t):
                    head = texte(str(item.get("headline", "")))
                    h1 = [texte(x) for x in re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", p["brut"])]
                    ti = re.search(r"(?is)<title[^>]*>(.*?)</title>", p["brut"])
                    ti = texte(ti.group(1)) if ti else ""
                    if head and ti and sansaccent(head) != sansaccent(ti):
                        # tolere si le headline est contenu dans le title ou l'inverse
                        if sansaccent(head) not in sansaccent(ti) and sansaccent(ti) not in sansaccent(head):
                            ALERTE("json-ld", f"{c} : headline JSON-LD « {head[:45]} » ne correspond "
                                              f"ni au title « {ti[:45]} » ni au H1")
                    d_pub = item.get("datePublished", "")
                    d_mod = item.get("dateModified", "")
                    if d_pub and d_mod and d_mod < d_pub:
                        ERREUR("json-ld", f"{c} : dateModified ({d_mod}) anterieure a "
                                          f"datePublished ({d_pub})")


# ==================================================== 2. REFERENCES REELLES
def audit_references(pages, reseau=True):
    """Verifie que les DOI cites EXISTENT et sort leur titre reel.

    Virginie l'a paye : « le contenu existant contient parfois des references
    inventees par IA ». Un DOI qui ne resout pas est une reference fabriquee.
    Un DOI qui resout mais dont le titre parle d'autre chose est une attribution
    deformee : le script sort le titre, la comparaison au propos reste humaine.
    """
    dois = collections.defaultdict(set)
    for c, p in pages.items():
        for d in re.findall(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", p["texte"]):
            dois[d.rstrip(".,);]")].add(c)
        for pm in re.findall(r"PMID\s*:?\s*(\d{6,9})", p["texte"], re.I):
            dois["PMID:" + pm].add(c)
    if not dois:
        INFO("aucun DOI ni PMID cite dans le texte visible des pages")
        return
    if not reseau:
        INFO(f"{len(dois)} references trouvees, non verifiees (--sans-reseau)")
        return
    for ref, ou in sorted(dois.items()):
        pages_str = ", ".join(sorted(ou))
        if ref.startswith("PMID:"):
            pm = ref.split(":")[1]
            code, corps, _ = http("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                                  f"?db=pubmed&retmode=json&id={pm}")
            titre = ""
            if code == 200:
                try:
                    j = json.loads(corps)
                    titre = j["result"][pm].get("title", "")
                except Exception:
                    titre = ""
            if not titre:
                ERREUR("references", f"PMID {pm} introuvable dans PubMed — cite sur {pages_str}")
            else:
                REVUE("references", f"PMID {pm} existe : « {titre[:110]} » — cite sur {pages_str}. "
                                    f"A relire : dit-il bien ce que la page lui fait dire ?")
        else:
            # On interroge CROSSREF, pas doi.org. Mesure du 02/08/2026 : le DOI
            # 10.2337/dc23-1630 renvoyait 403 via doi.org parce que le site de
            # l'editeur bloque les robots, et l'audit l'accusait d'etre une
            # reference inventee. Il existe : « Longitudinal Changes in SHBG and
            # Risk of Incident Diabetes (SWAN) », Diabetes Care 2024. Accuser a
            # tort une vraie source est la pire sortie possible pour cet audit,
            # puisqu'elle pousse a supprimer du contenu juste. Crossref est le
            # registre lui-meme : il repond sur la donnee, pas sur la page.
            code, corps, _ = http("https://api.crossref.org/works/" + urllib.parse.quote(ref))
            if code == 200:
                try:
                    msg = json.loads(corps)["message"]
                    titre = (msg.get("title") or ["(sans titre)"])[0]
                    revue = (msg.get("container-title") or ["?"])[0]
                    an = msg.get("issued", {}).get("date-parts", [["?"]])[0][0]
                    REVUE("references", f"DOI {ref} EXISTE : « {titre[:95]} » ({revue}, {an}) — "
                                        f"cite sur {pages_str}. A relire : l'article soutient-il "
                                        f"bien l'affirmation, sur la bonne population ?")
                except Exception:
                    REVUE("references", f"DOI {ref} existe (reponse Crossref illisible) — {pages_str}")
            elif code == 404:
                ERREUR("references", f"DOI {ref} INTROUVABLE dans Crossref — cite sur {pages_str}. "
                                     f"Reference probablement inventee : a verifier a la main "
                                     f"avant toute suppression.")
            else:
                ALERTE("references", f"DOI {ref} : Crossref n'a pas repondu (HTTP {code}), "
                                     f"existence NON tranchee — cite sur {pages_str}")


# ============================================= 3. COHERENCE DES CHIFFRES
def audit_chiffres(pages):
    """Un meme fait chiffre doit etre dit pareil partout. Virginie l'exige :
    « chiffres repetes identiques ». On regroupe les nombres par le sujet qui les
    entoure et on signale les valeurs divergentes pour un meme sujet."""
    par_sujet = collections.defaultdict(set)
    for c, p in pages.items():
        for m in re.finditer(r"(\d+(?:[,.]\d+)?)\s*(%|ans|kg|g de protéines|grammes)", p["texte"]):
            val, unite = m.group(1), m.group(2)
            gauche = sansaccent(p["texte"][max(0, m.start() - 60):m.start()])
            mots = [w for w in re.findall(r"[a-z]{5,}", gauche)][-3:]
            if mots:
                par_sujet[(" ".join(mots), unite)].add((val, c))
    for (sujet, unite), vals in sorted(par_sujet.items()):
        valeurs = {v for v, _ in vals}
        if len(valeurs) > 1 and len({c for _, c in vals}) > 1:
            det = " / ".join(f"{v} {unite} sur {c}" for v, c in sorted(vals))
            REVUE("coherence", f"chiffres differents sur un contexte proche («…{sujet}») : {det}")


# ======================================== 4. FORME, STYLE, VOUVOIEMENT
def audit_forme(pages):
    for c, p in pages.items():
        t = p["texte"]

        # Tirets cadratin et demi-cadratin : bannis partout par Virginie.
        for tiret, nom in (("—", "cadratin"), ("–", "demi-cadratin")):
            n = t.count(tiret)
            if n:
                ex = [x for x in re.findall(r".{30}" + tiret + r".{30}", t)][:1]
                ERREUR("forme", f"{c} : {n} tiret(s) {nom} dans le texte" +
                       (f" — «…{ex[0].strip()}…»" if ex else ""))

        # Ponctuation double francaise : espace insecable attendu AVANT ; : ! ?
        for signe in (";", ":", "!", "?", "»"):
            n = len(re.findall(r"[^\s  ]" + re.escape(signe), t))
            if n > 2:
                ALERTE("forme", f"{c} : {n} fois « {signe} » sans espace avant "
                                f"(typographie francaise)")

        # Hierarchie des titres : signale, mais en INFO seulement.
        # Verifie a la source le 02/08/2026 dans la documentation Google : l'ordre
        # des titres n'est PAS un facteur de classement, Google ecrit qu'il n'a
        # aucune importance qu'ils soient dans le desordre. Le seul enjeu reel est
        # l'accessibilite aux lecteurs d'ecran. Or sur ce site le CSS cible la
        # BALISE h4 et non une classe : renommer les h4 en h3 sur les 12 pages
        # concernees casserait leur rendu. Le faire couterait donc un risque
        # visuel reel pour un gain nul en referencement. On le sait, on ne le
        # traite pas, et surtout on n'encombre pas le rapport hebdomadaire avec
        # 12 lignes qui n'appellent aucune action.
        niveaux = [int(x) for x in re.findall(r"(?i)<h([1-6])[^>]*>", p["brut"])]
        prec = 0
        for n in niveaux:
            if prec and n > prec + 1:
                _sauts.append(f"{c} (H{prec}->H{n})")
                break
            prec = n

        # Tutoiement residuel
        for motif in TUTOIEMENT:
            for m in re.finditer(motif, t, re.I):
                ERREUR("style", f"{c} : TUTOIEMENT — «…{t[max(0,m.start()-40):m.start()+40]}…»")
                break

        # Tics de redaction automatique
        trouves = [tic for tic in TICS if tic in sansaccent(t)]
        if trouves:
            ALERTE("style", f"{c} : formule(s) de remplissage — {', '.join(trouves[:4])}")

        # Staccato : rafales de phrases tres courtes, tic d'IA que Virginie rejette
        phrases = [s.strip() for s in re.split(r"[.!?]\s", t) if s.strip()]
        rafale = 0
        for s in phrases:
            rafale = rafale + 1 if len(s.split()) <= 4 else 0
            if rafale >= 4:
                ALERTE("style", f"{c} : au moins 4 phrases tres courtes d'affilee (staccato)")
                break

        # Images : alt absent ou vide de sens
        for tag in re.findall(r"<img[^>]*>", p["visible"], re.I):
            m = re.search(r'alt\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
            src = re.search(r'src\s*=\s*(["\'])(.*?)\1', tag, re.I)
            src = src.group(2).split("/")[-1] if src else "?"
            if not m or not m.group(2).strip():
                ALERTE("images", f"{c} : image sans alt utile ({src})")
            elif len(m.group(2).split()) < 2:
                ALERTE("images", f"{c} : alt trop court « {m.group(2)} » ({src})")


def bilan_titres():
    if _sauts:
        INFO(f"hierarchie des titres : {len(_sauts)} page(s) sautent un niveau. Sans effet "
             f"sur le referencement (documentation Google, verifiee le 02/08/2026) ; conserve "
             f"tel quel car le CSS cible la balise h4 et renommer casserait le rendu.")


# ================================= 5. FRONTIERE GRATUIT / PAYANT (visible)
def audit_frontiere(pages):
    n = 0
    for c, p in pages.items():
        for extrait, quoi in protocoles_dans(p["texte"]):
            REVUE("frontiere", f"{c} : {quoi} — «…{extrait}…»")
            n += 1
    INFO(f"frontiere gratuit/payant : {n} passage(s) a relire "
         f"(un marqueur ne compte que s'il porte une instruction, pas une description)")


# ============================================ 6. RECIPROCITE ET SITEMAP
def audit_liens_structure(pages):
    sortants = {}
    for c, p in pages.items():
        s = set()
        for m in re.finditer(r'(?is)<a\b[^>]*?href\s*=\s*(["\'])(.*?)\1', p["visible"]):
            href = html.unescape(m.group(2)).strip()
            if href.startswith(("mailto:", "tel:", "#", "javascript:")):
                continue
            a = urllib.parse.urljoin(p["url"], href).split("#")[0].split("?")[0]
            if a.startswith(SITE):
                cible = a.replace(SITE, "") or "/"
                if cible.rstrip("/") != c.rstrip("/"):
                    s.add(cible.rstrip("/") or "/")
        sortants[c] = s
    INFO(f"{sum(len(v) for v in sortants.values())} liens internes distincts analyses")

    # lastmod du sitemap : une date figee fait passer une page pour abandonnee
    auj = datetime.date.today()
    for c, p in pages.items():
        lm = p.get("lastmod", "")[:10]
        if not lm:
            ALERTE("sitemap", f"{c} : aucune date lastmod dans le sitemap")
            continue
        try:
            d = datetime.date.fromisoformat(lm)
            if (auj - d).days > 200:
                ALERTE("sitemap", f"{c} : lastmod du {lm}, soit {(auj-d).days} jours "
                                  f"(page percue comme dormante)")
            if d > auj:
                ERREUR("sitemap", f"{c} : lastmod {lm} est dans le FUTUR")
        except ValueError:
            ERREUR("sitemap", f"{c} : lastmod illisible « {lm} »")


# ====================================================================== RAPPORT
def rapport(markdown):
    tampon = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    L = []
    t = ("# Audit hebdomadaire integral — virginiedeconinck.com" if markdown
         else "=== AUDIT HEBDOMADAIRE INTEGRAL — virginiedeconinck.com ===")
    L.append(t)
    L.append((f"\n_Mesure du {tampon}, sur le site en ligne._\n" if markdown
              else f"Mesure du {tampon}\n"))
    L.append(f"**{len(erreurs)} erreur(s)**, **{len(alertes)} point(s) a corriger**, "
             f"**{len(revues)} point(s) a relire par un humain**." if markdown else
             f"{len(erreurs)} erreurs, {len(alertes)} a corriger, {len(revues)} a relire.")

    def bloc(titre, items, vide):
        if markdown:
            L.append(f"\n## {titre}\n")
            L.extend([f"- `{c}` {m}" for c, m in items] or [f"_{vide}_"])
        else:
            L.append(f"\n--- {titre} ---")
            L.extend([f"  [{c}] {m}" for c, m in items] or [f"  {vide}"])

    bloc("Erreurs (quelque chose est faux, casse ou invisible)", erreurs, "aucune")
    bloc("A corriger (forme, style, structure)", alertes, "aucun")
    bloc("A RELIRE par un humain (la machine ne peut pas trancher)", revues,
         "aucun point de jugement souleve")
    if markdown:
        L.append("\n## Perimetre couvert\n")
        L.extend([f"- {m}" for m in infos])
    else:
        L.append("\n--- PERIMETRE ---")
        L.extend([f"  {m}" for m in infos])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--sans-reseau", action="store_true",
                    help="ne verifie pas les DOI/PMID aupres de doi.org et PubMed")
    args = ap.parse_args()

    pages = collecte()
    INFO(f"{len(pages)} pages du sitemap chargees et analysees integralement")
    audit_json_ld(pages)
    audit_references(pages, reseau=not args.sans_reseau)
    audit_chiffres(pages)
    audit_forme(pages)
    bilan_titres()
    audit_frontiere(pages)
    audit_liens_structure(pages)

    txt = rapport(args.markdown)
    print(txt)
    if args.markdown:
        open("rapport-audit-hebdo.md", "w", encoding="utf-8").write(txt + "\n")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
