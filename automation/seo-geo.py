#!/usr/bin/env python3
"""
MOTEUR SEO + GEO du site public de Virginie Deconinck.

Ce qu'il n'est PAS : un controle de conformite technique. Ca, c'est monitoring.py
(titres, balises, donnees structurees, liens casses). Les deux sont complementaires
et ne se recouvrent pas.

Ce qu'il EST : le travail de fond, refait a chaque passage sur les donnees REELLES
de Google, jamais sur une intuition ni une liste de mots-cles ecrite une fois pour
toutes. Il repond aux questions qui decident du trafic :

  1. Sur quoi les femmes tombent-elles reellement sur ce site, aujourd'hui ?
  2. Quelles requetes sont A PORTEE (page 1 basse / page 2) et rapporteraient si on
     poussait ? C'est la que le travail paie, pas sur les mots ou on est 40e.
  3. Quelles pages sortent bien mais ne font PAS cliquer ? Probleme de titre et de
     description, pas de referencement : le trafic est deja la, il passe a cote.
  4. Quelles QUESTIONS les gens formulent ? C'est la matiere premiere du GEO :
     ChatGPT, Claude, Perplexity et Gemini citent les pages qui repondent a une
     question posee comme un humain la pose.
  5. Deux pages se disputent-elles la meme requete (cannibalisation) ?
  6. Quelles pages indexees ne rapportent AUCUNE impression (contenu muet) ?
  7. Qu'est-ce qui monte, qu'est-ce qui decroche par rapport a la periode d'avant ?

Lecture seule. Ne modifie ni le site, ni Search Console, ni quoi que ce soit.

Usage :  python3 automation/seo-geo.py [--jours 90] [--markdown]
"""
import json, time, base64, sys, argparse, datetime, urllib.parse, re
from collections import defaultdict

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

SITE = 'sc-domain:virginiedeconinck.com'
SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'
# Chemins possibles de la cle de compte de service, du plus specifique au plus general.
CLES = [
    '/Users/virginie/Downloads/cle-search-console-rcf.json',
    '/Users/virginie/Downloads/alien-bruin-504108-s7-93c4f22e43bb.json',
]
# Search Console publie ses donnees avec 2 a 3 jours de retard : on s'arrete a J-3
# pour ne jamais comparer une periode complete a une periode encore en cours.
LATENCE = 3

MOTS_QUESTION = ('comment', 'pourquoi', 'quel', 'quelle', 'quels', 'quelles', 'est-ce',
                 'peut-on', 'faut-il', 'combien', 'quand', 'qui ', 'que ', 'c est quoi',
                 "c'est quoi", 'difference', 'signe', 'symptome')


def cle_service():
    """Cle du compte de service, depuis l'environnement (cloud) ou le disque (Mac).

    En execution automatique (GitHub Actions), la cle arrive par la variable
    GOOGLE_SC_KEY : elle n'est JAMAIS ecrite dans le depot, qui est public, et
    Google desactive de toute facon automatiquement toute cle trouvee dans un
    depot public. En execution manuelle depuis le Mac de Virginie, on lit le
    fichier telecharge depuis Google Cloud.
    """
    import os
    brut = os.environ.get('GOOGLE_SC_KEY', '').strip()
    if brut:
        return json.loads(brut)
    for c in CLES:
        if os.path.exists(c):
            return json.load(open(c))
    print("ECHEC : aucune cle de compte de service trouvee.")
    print("  ni dans la variable d'environnement GOOGLE_SC_KEY,")
    for c in CLES:
        print("  ni dans", c)
    sys.exit(1)


def b64(d):
    if isinstance(d, dict):
        d = json.dumps(d, separators=(',', ':')).encode()
    return base64.urlsafe_b64encode(d).rstrip(b'=')


def jeton():
    info = cle_service()
    t = int(time.time())
    a_signer = b64({'alg': 'RS256', 'typ': 'JWT'}) + b'.' + b64({
        'iss': info['client_email'], 'scope': SCOPE,
        'aud': info['token_uri'], 'iat': t, 'exp': t + 3600})
    k = serialization.load_pem_private_key(info['private_key'].encode(), password=None)
    sig = k.sign(a_signer, padding.PKCS1v15(), hashes.SHA256())
    r = requests.post(info['token_uri'], timeout=30, data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': (a_signer + b'.' + b64(sig)).decode()})
    if r.status_code != 200:
        print("ECHEC de l'authentification Google :", r.status_code, r.text[:300])
        sys.exit(1)
    return r.json()['access_token']


def interroge(tok, debut, fin, dimensions=None, limite=25000):
    url = ('https://www.googleapis.com/webmasters/v3/sites/'
           + urllib.parse.quote(SITE, safe='') + '/searchAnalytics/query')
    corps = {'startDate': debut, 'endDate': fin, 'rowLimit': limite}
    if dimensions:
        corps['dimensions'] = dimensions
    r = requests.post(url, headers={'Authorization': 'Bearer ' + tok}, json=corps, timeout=90)
    if r.status_code != 200:
        print(f"  ERREUR API {r.status_code} : {r.text[:300]}")
        return []
    return r.json().get('rows', [])


def chemin(url):
    return url.replace('https://virginiedeconinck.com', '').replace(
        'http://virginiedeconinck.com', '[NON SECURISE]') or '/'


def analyse(jours):
    tok = jeton()
    fin = datetime.date.today() - datetime.timedelta(days=LATENCE)
    debut = fin - datetime.timedelta(days=jours - 1)
    # periode precedente de meme longueur, pour comparer des choses comparables
    fin_p = debut - datetime.timedelta(days=1)
    debut_p = fin_p - datetime.timedelta(days=jours - 1)
    S, F = debut.isoformat(), fin.isoformat()
    SP, FP = debut_p.isoformat(), fin_p.isoformat()

    sections = []
    ajoute = sections.append

    # ---------- 1. VUE D'ENSEMBLE ----------
    tot = interroge(tok, S, F)
    tot_p = interroge(tok, SP, FP)
    a = tot[0] if tot else {}
    b = tot_p[0] if tot_p else {}

    def ecart(x, y):
        if not y:
            return "(pas de point de comparaison)"
        d = (x - y) / y * 100
        return f"{d:+.0f}% vs les {jours} jours precedents"

    ajoute(("VUE D'ENSEMBLE", [
        f"periode analysee : du {S} au {F} ({jours} jours, arretee a J-{LATENCE} "
        f"car Google publie avec 2 a 3 jours de retard)",
        f"clics        : {a.get('clicks', 0):.0f}   {ecart(a.get('clicks', 0), b.get('clicks', 0))}",
        f"impressions  : {a.get('impressions', 0):.0f}   {ecart(a.get('impressions', 0), b.get('impressions', 0))}",
        f"CTR          : {a.get('ctr', 0)*100:.2f}%",
        f"position moy.: {a.get('position', 0):.1f}",
    ]))

    req = interroge(tok, S, F, ['query'])
    req_p = {r['keys'][0]: r for r in interroge(tok, SP, FP, ['query'])}
    pages = interroge(tok, S, F, ['page'])
    req_page = interroge(tok, S, F, ['query', 'page'])

    # CTR median du site par tranche de position : reference auto-calibree, plutot
    # que des "CTR attendus" tires d'un article de blog qui ne connait pas ce site.
    par_tranche = defaultdict(list)
    for r in req:
        if r['impressions'] >= 5:
            par_tranche[min(int(r['position']), 20)].append(r['ctr'])
    median = {}
    for p, v in par_tranche.items():
        v.sort()
        median[p] = v[len(v)//2]

    # ---------- 2. A PORTEE DE MAIN ----------
    portee = sorted([r for r in req if 4 <= r['position'] <= 20 and r['impressions'] >= 5],
                    key=lambda r: -r['impressions'])[:20]
    ajoute((f"A PORTEE DE MAIN ({len(portee)} requetes)", [
        "Requetes ou le site apparait deja entre la 4e et la 20e place, avec de la demande.",
        "C'est ICI que le travail paie : gagner 3 places sur ces mots rapporte plus que",
        "creer une page de plus sur un sujet ou personne ne cherche.",
        ""] + [
        f"{r['impressions']:>5} impr. {r['clicks']:>3} clics  pos {r['position']:>5.1f}  {r['keys'][0]}"
        for r in portee] or ["  aucune"]))

    # ---------- 3. SORT BIEN, NE FAIT PAS CLIQUER ----------
    mous = []
    for r in req:
        p = min(int(r['position']), 20)
        ref = median.get(p)
        if ref and r['impressions'] >= 10 and r['position'] <= 12 and r['ctr'] < ref * 0.5:
            mous.append((r, ref))
    mous.sort(key=lambda x: -x[0]['impressions'])
    ajoute((f"SORT BIEN MAIS NE FAIT PAS CLIQUER ({len(mous)})", [
        "Le referencement fonctionne, le titre non. Le trafic passe devant et va ailleurs.",
        "Action : reecrire le titre et la meta description de la page concernee.",
        ""] + [
        f"{r['impressions']:>5} impr. pos {r['position']:>4.1f}  CTR {r['ctr']*100:>5.2f}% "
        f"(median du site a cette place : {ref*100:.2f}%)  {r['keys'][0]}"
        for r, ref in mous[:15]] or ["  aucune"]))

    # ---------- 3bis. PAGES QUI SORTENT MAIS NE FONT PAS CLIQUER ----------
    # Corrige le 31/07/2026 : la detection ci-dessus, faite requete par requete, ne
    # voyait RIEN. Deux raisons. D'abord la plupart des requetes d'un petit site ont
    # zero clic, donc le CTR median par tranche de position tombe a zero et plus rien
    # ne peut passer sous "la moitie du median". Ensuite le probleme se joue au niveau
    # de la PAGE : c'est son titre et sa description que Google affiche, pas la requete.
    # Cas reel qui a revele le trou : /age-biologique-age-chronologique, 519 impressions
    # pour 11 clics, invisible pour l'ancienne detection.
    ctr_site = (a.get('clicks', 0) / a.get('impressions', 1)) if a.get('impressions') else 0
    froides = []
    for r in pages:
        c = chemin(r['keys'][0])
        if c.startswith('[NON') or r['impressions'] < 30:
            continue
        if r['position'] <= 15 and ctr_site and r['ctr'] < ctr_site * 0.5:
            froides.append((r, c))
    froides.sort(key=lambda x: -x[0]['impressions'])
    ajoute((f"PAGES QUI SORTENT MAIS NE FONT PAS CLIQUER ({len(froides)})", [
        f"Reference : le CTR moyen du site est de {ctr_site*100:.2f}%. Ces pages sont bien",
        "placees et vues, mais leur titre ne declenche pas le clic. Le trafic est deja la,",
        "il passe devant et va chez quelqu'un d'autre.",
        "Action : reecrire le title et la meta description, pas le contenu.",
        ""] + [
        f"{r['impressions']:>5} impr. {r['clicks']:>3} clics  CTR {r['ctr']*100:>5.2f}%  "
        f"pos {r['position']:>5.1f}  {c}" for r, c in froides[:12]] or ["  aucune"]))

    # ---------- 4. MATIERE GEO : LES QUESTIONS ----------
    questions = [r for r in req if any(m in r['keys'][0].lower() for m in MOTS_QUESTION)]
    questions.sort(key=lambda r: -r['impressions'])
    ajoute((f"MATIERE GEO : QUESTIONS REELLEMENT POSEES ({len(questions)})", [
        "Les moteurs de reponse (ChatGPT, Claude, Perplexity, Gemini) citent les pages qui",
        "repondent a une question formulee comme un humain la pose. Ces formulations-la sont",
        "REELLES : ce sont celles tapees par de vraies femmes pour arriver ici.",
        "Action : en faire des intertitres (H2) et des blocs FAQ, mot pour mot.",
        ""] + [
        f"{r['impressions']:>5} impr. pos {r['position']:>5.1f}  {r['keys'][0]}"
        for r in questions[:20]] or ["  aucune question detectee sur la periode"]))

    # ---------- 5. CANNIBALISATION ----------
    parreq = defaultdict(list)
    for r in req_page:
        parreq[r['keys'][0]].append((chemin(r['keys'][1]), r['impressions'], r['position']))
    canni = {q: v for q, v in parreq.items()
             if len({p for p, _, _ in v if not p.startswith('[NON')}) > 1
             and sum(i for _, i, _ in v) >= 10}
    lignes = []
    for q, v in sorted(canni.items(), key=lambda kv: -sum(i for _, i, _ in kv[1]))[:10]:
        lignes.append(f"  \"{q}\"")
        for p, i, pos in sorted(v, key=lambda x: -x[1]):
            lignes.append(f"      {i:>4} impr. pos {pos:>5.1f}  {p}")
    ajoute((f"CANNIBALISATION ({len(canni)} requetes disputees)", [
        "Deux pages du site se disputent la meme requete : elles s'affaiblissent l'une l'autre.",
        "Action : en designer UNE comme la page de reference, et faire pointer l'autre vers elle.",
        ""] + (lignes or ["  aucune"])))

    # ---------- 6. PAGES MUETTES ----------
    vues = {chemin(r['keys'][0]) for r in pages if r['impressions'] > 0}
    try:
        sm = requests.get('https://virginiedeconinck.com/sitemap.xml', timeout=30).text
        declarees = {chemin(u) for u in re.findall(r'<loc>(.*?)</loc>', sm)}
    except Exception as e:
        declarees, vues = set(), set()
        print("  (sitemap illisible :", e, ")")
    muettes = sorted(declarees - vues)
    ajoute((f"PAGES MUETTES ({len(muettes)})", [
        "Pages publiees et declarees a Google, mais qui n'ont declenche AUCUNE impression",
        "sur la periode. Elles ne repondent a aucune demande, ou Google ne les a pas retenues.",
        ""] + [f"  {p}" for p in muettes] or ["  aucune"]))

    # ---------- 6bis. TERRAIN NON COUVERT (veille, source gratuite) ----------
    # Search Console ne montre QUE ce sur quoi le site apparait deja. Elle est aveugle
    # a tout ce qui se cherche ailleurs. Cette section comble ce trou avec la source
    # de suggestions de Google : ce que de vrais gens tapent, mis a jour en permanence,
    # sans compte, sans cle, sans abonnement. On confronte ensuite ces demandes reelles
    # aux sujets deja couverts par le site pour faire ressortir les trous.
    themes = sorted({m for u in declarees for m in re.findall(r'[a-z]{5,}', u)
                     if m not in ('index', 'blog', 'https', 'about')})[:0] or []
    graines = [
        'périménopause', 'ménopause', 'âge biologique', 'collagène peau femme',
        'résistance à l\'insuline femme', 'inflammation chronique femme',
        'masse musculaire femme 40 ans', 'hormones femme 45 ans', 'peptides longévité',
        'NAD+ vieillissement', 'cellules sénescentes', 'histamine hormones',
        'GLP-1 femme', 'biohacking féminin', 'SHBG', 'glycémie peau',
        'graisse abdominale femme', 'rajeunissement cellulaire', 'longévité femme',
    ]
    prefixes = ['', 'comment ', 'pourquoi ', 'quel ', 'est-ce que ']
    # Les adresses des pages sont sans accents ("/perimenopause"), les recherches en
    # ont ("périménopause"). Sans cette normalisation, le rapport se remplissait de
    # faux positifs : des sujets DEJA couverts declares comme des trous.
    import unicodedata
    def sansaccent(x):
        return ''.join(c for c in unicodedata.normalize('NFD', x.lower())
                       if unicodedata.category(c) != 'Mn')
    couvert = sansaccent(' '.join(declarees))
    trouvees, a_reformuler, vues_sug = [], [], set()
    for g in graines:
        for pre in prefixes:
            try:
                rq = requests.get('https://suggestqueries.google.com/complete/search',
                                  params={'client': 'firefox', 'hl': 'fr', 'gl': 'fr',
                                          'q': pre + g}, timeout=15)
                sugg = rq.json()[1] if rq.status_code == 200 else []
            except Exception:
                sugg = []
            for s in sugg:
                s = s.strip().lower()
                if s in vues_sug or len(s) < 8:
                    continue
                vues_sug.add(s)
                # Seuil a 4 caracteres et non 5. Bug mesure le 02/08/2026 : avec
                # {5,}, le mot "shbg" n'etait JAMAIS teste, et les 8 recherches
                # "shbg prise de sang", "shbg elevee", "shbg comment augmenter"...
                # etaient annoncees comme des sujets SANS PAGE DEDIEE, alors que
                # /shbg-hormones-actives-femme existe et venait d'etre enrichie
                # exactement sur ces questions. Meme piege pour NAD et GLP-1.
                # Les mots outils sont retires a la main : sans cela "sang" ou
                # "prise" suffiraient a declarer une suggestion couverte.
                mots = [m for m in re.findall(r'[a-z0-9]{4,}', sansaccent(s))
                        if m not in ('dans', 'avec', 'pour', 'quoi', 'este', 'cest',
                                     'plus', 'sans', 'faire', 'quand', 'tout', 'toute')]
                # "non couvert" = aucun mot signifiant de la suggestion n'apparait
                # dans les adresses des pages publiees. On compare sur le mot entier
                # quand il est court, sur son prefixe quand il est long (pour que
                # "collagene" reconnaisse "collagenes").
                if mots and not any((m if len(m) <= 5 else m[:7]) in couvert for m in mots):
                    trouvees.append(s)          # sujet absent du site
                elif any(s.startswith(m) for m in ('comment','pourquoi','quel','est-ce','qu')):
                    # Question precise sur un theme DEJA couvert. Ce n'est pas un trou de
                    # contenu, c'est un trou de FORMULATION : la page existe mais ne repond
                    # pas a la question telle qu'elle est posee. C'est exactement ce qui
                    # decide qu'un moteur de reponse cite la page, ou ne la cite pas.
                    a_reformuler.append(s)
            time.sleep(0.15)   # rester poli avec le service de suggestions

    questions_neuves = [s for s in trouvees
                        if any(s.startswith(m) for m in ('comment', 'pourquoi', 'quel', 'est-ce'))]
    autres = [s for s in trouvees if s not in questions_neuves]
    ajoute((f"TERRAIN NON COUVERT ({len(trouvees)} demandes reelles sans page dediee)", [
        f"Source : suggestions de recherche Google, interrogees a l'instant sur "
        f"{len(graines)} themes ({len(vues_sug)} formulations relevees).",
        "Ce sont des recherches que de vraies personnes formulent MAINTENANT et sur",
        "lesquelles le site n'a aucune page. C'est la matiere pour les prochains contenus.",
        "",
        "-- formulees comme des QUESTIONS (matiere GEO prioritaire : c'est ainsi qu'on",
        "   interroge ChatGPT, Claude, Perplexity et Gemini) --"]
        + [f"   {s}" for s in questions_neuves[:25]]
        + ["", "-- autres demandes non couvertes --"]
        + [f"   {s}" for s in autres[:25]]
        + ["", f"-- QUESTIONS sur des sujets DEJA couverts ({len(a_reformuler)}) : la page",
           "   existe mais ne repond pas a la question telle qu'elle est posee.",
           "   A transformer en intertitres H2 et en blocs FAQ, mot pour mot. --"]
        + [f"   {s}" for s in a_reformuler[:30]]))

    # ---------- 7. CE QUI MONTE, CE QUI DECROCHE ----------
    monte, descend = [], []
    for r in req:
        q = r['keys'][0]
        av = req_p.get(q)
        if not av or (r['impressions'] < 10 and av['impressions'] < 10):
            continue
        d = r['impressions'] - av['impressions']
        (monte if d > 0 else descend).append((abs(d), q, av['impressions'], r['impressions'],
                                              av['position'], r['position']))
    monte.sort(reverse=True); descend.sort(reverse=True)
    ajoute(("CE QUI MONTE", [
        f"{a2} -> {a3} impr. (pos {p2:.1f} -> {p3:.1f})  {q}"
        for _, q, a2, a3, p2, p3 in monte[:10]] or ["  rien de significatif"]))
    ajoute(("CE QUI DECROCHE", [
        f"{a2} -> {a3} impr. (pos {p2:.1f} -> {p3:.1f})  {q}"
        for _, q, a2, a3, p2, p3 in descend[:10]] or ["  rien de significatif"]))

    return sections, S, F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jours', type=int, default=90)
    ap.add_argument('--markdown', action='store_true')
    args = ap.parse_args()

    sections, S, F = analyse(args.jours)

    if args.markdown:
        out = [f"# SEO + GEO virginiedeconinck.com\n", f"_Donnees Google du {S} au {F}_\n"]
        for titre, lignes in sections:
            out.append(f"\n## {titre}\n")
            out.append("```\n" + "\n".join(lignes) + "\n```\n")
        open('rapport-seo-geo.md', 'w', encoding='utf-8').write("\n".join(out))
        print("rapport-seo-geo.md ecrit")
    else:
        print(f"\n{'='*70}\n  SEO + GEO virginiedeconinck.com   (donnees Google du {S} au {F})\n{'='*70}")
        for titre, lignes in sections:
            print(f"\n--- {titre} ---")
            for l in lignes:
                print(("  " + l) if not l.startswith(' ') else l)
        print()


if __name__ == '__main__':
    main()
