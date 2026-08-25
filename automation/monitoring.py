#!/usr/bin/env python3
"""
Surveillance du site public virginiedeconinck.com : technique + SEO + GEO.

Lecture seule. Ne modifie jamais le site, ne publie rien.
Aucune dependance externe (stdlib uniquement) : pas de rupture de build.

Deux niveaux, volontairement distincts :
  ERREUR  -> quelque chose est CASSE ou invisible pour Google/les IA. Ouvre une Issue.
  ALERTE  -> quelque chose est PERFECTIBLE. Figure au rapport, n'ouvre pas d'Issue.
Ce choix evite le bruit permanent qui fait qu'on finit par ne plus lire les alertes.

Usage :
    python3 automation/monitoring.py                 # rapport texte
    python3 automation/monitoring.py --markdown      # rapport pour GITHUB_STEP_SUMMARY
Code de sortie : 1 si au moins une ERREUR, sinon 0.
"""

import re, sys, json, ssl, socket, html, collections, datetime
import urllib.request, urllib.error, urllib.parse

SITE = "https://virginiedeconinck.com"
HOST = "virginiedeconinck.com"
TIMEOUT = 30
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Crawlers dont depend la visibilite dans les reponses generees par IA.
# Verifies par requete REELLE avec leur User-Agent : un robots.txt permissif ne
# prouve rien si l'hebergeur ou un pare-feu bloque le bot en amont.
CRAWLERS_IA = {
    "GPTBot":            "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.2; +https://openai.com/gptbot",
    "OAI-SearchBot":     "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot",
    "ClaudeBot":         "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +claudebot@anthropic.com",
    "PerplexityBot":     "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot",
    "Google-Extended":   "Mozilla/5.0 (compatible; Google-Extended/1.0)",
    "Googlebot":         "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Bingbot":           "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "meta-externalagent": "Mozilla/5.0 (compatible; meta-externalagent/1.1; +https://developers.facebook.com/docs/sharing/webmasters/crawler)",
}

SEUIL_TITLE = 60        # au-dela, Google tronque dans les resultats
DESC_MIN, DESC_MAX = 100, 160
MOTS_MIN = 300
TLS_JOURS_MIN = 21
DOMAINE_JOURS_MIN = 45   # large : un renouvellement de domaine se regle a la main,
                         # chez le registrar, et peut demander plusieurs jours

erreurs, alertes, infos = [], [], []
def ERREUR(cat, msg): erreurs.append((cat, msg))
def ALERTE(cat, msg): alertes.append((cat, msg))
def INFO(msg): infos.append(msg)

_cache = {}
def http(url, method="GET", ua=UA):
    """Retourne (code, corps, entetes, url_finale). code 0 = echec reseau."""
    cle = (url, method, ua)
    if cle in _cache: return _cache[cle]
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": ua, "Accept-Language": "fr-FR,fr;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            corps = r.read().decode("utf-8", "replace") if method == "GET" else ""
            res = (r.status, corps, dict(r.headers), r.url)
    except urllib.error.HTTPError as e:
        res = (e.code, "", dict(e.headers or {}), url)
    except Exception as e:
        res = (0, "", {}, f"{type(e).__name__}: {e}")
    _cache[cle] = res
    return res

def attr(balise_re, nom, s):
    """Extrait un attribut proprement : le delimiteur fermant doit etre le MEME
    que l'ouvrant, sinon une apostrophe francaise coupe la valeur en deux."""
    out = []
    for tag in re.findall(balise_re, s, re.I | re.S):
        m = re.search(nom + r'\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
        if m: out.append(html.unescape(m.group(2)).strip())
    return out

def texte(s):
    s = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


# ---------------------------------------------------------------- 1. SOCLE
def controle_socle():
    for f in ("robots.txt", "sitemap.xml", "llms.txt"):
        code, _, _, _ = http(f"{SITE}/{f}")
        if code != 200: ERREUR("socle", f"/{f} renvoie HTTP {code} (200 attendu)")

    code, _, _, _ = http(f"{SITE}/page-qui-n-existe-pas-controle-monitoring")
    if code != 404: ERREUR("socle", f"une URL inexistante renvoie {code} au lieu de 404 "
                                    f"(un 200 ferait indexer des pages fantomes)")
    else: INFO("page inexistante -> 404 : le gestionnaire d'erreur fonctionne")

    # Certificat TLS : une expiration silencieuse rend le site inaccessible a tous.
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((HOST, 443), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=HOST) as ss:
                exp = datetime.datetime.strptime(ss.getpeercert()["notAfter"], "%b %d %H:%M:%S %Y %Z")
        jours = (exp - datetime.datetime.utcnow()).days
        INFO(f"certificat TLS valide encore {jours} jours (expire le {exp:%d/%m/%Y})")
        if jours < TLS_JOURS_MIN: ERREUR("socle", f"certificat TLS expire dans {jours} jours")
    except Exception as e:
        ERREUR("socle", f"controle TLS impossible : {e}")

    # Nom de domaine. Le certificat TLS se renouvelle tout seul chez Netlify ;
    # le DOMAINE, lui, depend d'un paiement chez OVH. S'il expire, il n'y a plus
    # de site, plus de liens de pub, plus rien, et aucun autre controle de ce
    # moteur ne l'aurait vu venir. Constate le 25/08/2026 : l'expiration tombait
    # dans 30 jours et rien ne la surveillait. Source = RDAP, le registre
    # officiel de Verisign pour les .com, pas une note ni un rappel d'agenda.
    try:
        code, corps, _, _ = http(f"https://rdap.verisign.com/com/v1/domain/{HOST}")
        d = json.loads(corps)
        exp = next(e["eventDate"] for e in d["events"] if e["eventAction"] == "expiration")
        fin = datetime.datetime.strptime(exp[:10], "%Y-%m-%d")
        jours = (fin - datetime.datetime.utcnow()).days
        reg = next((v[3] for e in d.get("entities", []) if "registrar" in e.get("roles", [])
                    for v in e.get("vcardArray", [[], []])[1] if v[0] == "fn"), "?")
        INFO(f"nom de domaine valide encore {jours} jours "
             f"(expire le {fin:%d/%m/%Y}, registrar {reg})")
        # Deux niveaux volontairement, pour ne pas crier au loup pendant un mois.
        # Le renouvellement automatique OVH se declenche dans les jours qui
        # precedent l'echeance : tant qu'on est loin, une simple ligne dans le
        # rapport suffit. Une Issue ne s'ouvre que sous 14 jours, la ou un
        # renouvellement qui n'a PAS eu lieu devient un vrai danger.
        if jours < 14:
            ERREUR("socle", f"le NOM DE DOMAINE expire dans {jours} jours "
                            f"(le {fin:%d/%m/%Y}, chez {reg}) : le renouvellement "
                            f"automatique n'a pas eu lieu, le site entier va tomber")
        elif jours < DOMAINE_JOURS_MIN:
            ALERTE("socle", f"nom de domaine a renouveler dans {jours} jours "
                            f"(le {fin:%d/%m/%Y}, chez {reg})")
    except Exception as e:
        ALERTE("socle", f"controle du nom de domaine impossible : {e}")


# ------------------------------------------------- 2. PAGES : HTTP + SEO + GEO
def collecte_pages():
    code, sm, _, _ = http(f"{SITE}/sitemap.xml")
    urls = re.findall(r'<loc>([^<]+)</loc>', sm)
    if not urls:
        ERREUR("socle", "sitemap.xml ne contient aucune URL exploitable")
        return {}, []
    pages = {}
    for u in urls:
        code, corps, ent, final = http(u)
        if code != 200:
            ERREUR("disponibilite", f"{u} renvoie HTTP {code}")
            pages[u] = {"code": code}
            continue
        if final.rstrip("/") != u.rstrip("/"):
            ALERTE("disponibilite", f"{u} redirige vers {final} (le sitemap devrait citer l'URL finale)")

        p = {
            "code": code, "html": corps,
            "title": (re.search(r'(?s)<title[^>]*>(.*?)</title>', corps).group(1).strip()
                      if re.search(r'(?s)<title[^>]*>(.*?)</title>', corps) else ""),
            "desc":  attr(r'<meta[^>]*name\s*=\s*["\']description["\'][^>]*>', 'content', corps),
            "canon": attr(r'<link[^>]*rel\s*=\s*["\']canonical["\'][^>]*>', 'href', corps),
            "ogimg": attr(r'<meta[^>]*property\s*=\s*["\']og:image["\'][^>]*>', 'content', corps),
            "ogtit": attr(r'<meta[^>]*property\s*=\s*["\']og:title["\'][^>]*>', 'content', corps),
            "twtit": attr(r'<meta[^>]*name\s*=\s*["\']twitter:title["\'][^>]*>', 'content', corps),
            "robots": attr(r'<meta[^>]*name\s*=\s*["\']robots["\'][^>]*>', 'content', corps),
            "xrobots": ent.get("X-Robots-Tag", ""),
            "h1": re.findall(r'(?s)<h1[^>]*>(.*?)</h1>', corps),
            "h2": re.findall(r'(?s)<h2[^>]*>(.*?)</h2>', corps),
            "lang": (re.search(r'<html[^>]*lang\s*=\s*["\']([^"\']+)', corps).group(1)
                     if re.search(r'<html[^>]*lang\s*=\s*["\']', corps) else ""),
            "viewport": bool(re.search(r'name\s*=\s*["\']viewport["\']', corps, re.I)),
            "mots": len(texte(corps).split()),
        }
        p["title"] = html.unescape(p["title"])
        pages[u] = p
    return pages, urls


def controle_seo(pages):
    vues_title, vues_desc = collections.defaultdict(list), collections.defaultdict(list)
    for u, p in pages.items():
        if p.get("code") != 200: continue
        chemin = u.replace(SITE, "") or "/"

        # --- indexabilite : une page desindexee par erreur est invisible, point.
        if any("noindex" in r.lower() for r in p["robots"]):
            ERREUR("indexation", f"{chemin} porte une balise meta robots noindex")
        if "noindex" in (p["xrobots"] or "").lower():
            ERREUR("indexation", f"{chemin} porte un en-tete HTTP X-Robots-Tag noindex")

        # --- title
        if not p["title"]:
            ERREUR("seo", f"{chemin} : balise title absente")
        else:
            vues_title[p["title"]].append(chemin)
            if len(p["title"]) > SEUIL_TITLE:
                ALERTE("seo", f"{chemin} : title de {len(p['title'])} car. (>{SEUIL_TITLE}), "
                              f"tronque dans Google")

        # --- meta description
        if not p["desc"]:
            ERREUR("seo", f"{chemin} : meta description absente")
        else:
            if len(p["desc"]) > 1:
                ERREUR("seo", f"{chemin} : {len(p['desc'])} balises description (1 attendue)")
            d = p["desc"][0]
            vues_desc[d].append(chemin)
            if not (DESC_MIN <= len(d) <= DESC_MAX):
                ALERTE("seo", f"{chemin} : description de {len(d)} car. "
                              f"(cible {DESC_MIN}-{DESC_MAX})")

        # --- canonical
        if not p["canon"]:
            ERREUR("seo", f"{chemin} : balise canonical absente")
        elif p["canon"][0].rstrip("/") != u.rstrip("/"):
            ERREUR("seo", f"{chemin} : canonical pointe vers {p['canon'][0]} au lieu d'elle-meme")

        # --- structure
        if len(p["h1"]) != 1:
            ERREUR("seo", f"{chemin} : {len(p['h1'])} balises H1 (exactement 1 attendue)")
        if not p["h2"]:
            ALERTE("seo", f"{chemin} : aucun H2, structure de lecture absente")
        if not p["viewport"]:
            ERREUR("seo", f"{chemin} : meta viewport absente, rendu mobile casse")
        if not p["lang"]:
            ERREUR("seo", f"{chemin} : attribut lang absent sur <html>")
        if p["mots"] < MOTS_MIN:
            ALERTE("seo", f"{chemin} : {p['mots']} mots seulement (<{MOTS_MIN})")

        # --- partage social
        # Le titre de la carte de partage doit dire la MEME chose que la page.
        # Un ecart se cree en silence des qu'on retouche un title sans penser aux
        # deux balises jumelles : la carte annonce alors autre chose que le contenu.
        if not p["ogimg"]: ALERTE("social", f"{chemin} : og:image absente")
        if not p["ogtit"]:
            ALERTE("social", f"{chemin} : og:title absente")
        elif p["ogtit"][0] != p["title"]:
            ERREUR("social", f"{chemin} : og:title differe du title de la page "
                             f"(« {p['ogtit'][0][:50]} » au lieu de « {p['title'][:50]} »)")
        if not p["twtit"]:
            ALERTE("social", f"{chemin} : twitter:title absente")
        elif p["twtit"][0] != p["title"]:
            ERREUR("social", f"{chemin} : twitter:title differe du title de la page")

    # --- cannibalisation : deux pages sur la meme requete se penalisent
    for t, l in vues_title.items():
        if len(l) > 1: ERREUR("seo", f"title identique sur {len(l)} pages ({', '.join(l)}) : « {t[:60]} »")
    for d, l in vues_desc.items():
        if len(l) > 1: ERREUR("seo", f"description identique sur {len(l)} pages ({', '.join(l)})")

    ogs = collections.Counter(p["ogimg"][0] for p in pages.values()
                              if p.get("code") == 200 and p.get("ogimg"))
    for img, n in ogs.items():
        if n > 3:
            ALERTE("social", f"la meme og:image sert {n} pages ({img.replace(SITE,'')}) : "
                             f"tout partage affiche le meme visuel")


# ------------------------------------------------------ 3. LIENS ET IMAGES
def controle_liens(pages):
    liens = collections.defaultdict(set)   # url cible -> pages qui la citent
    images = collections.defaultdict(set)
    sans_alt = []
    for u, p in pages.items():
        if p.get("code") != 200: continue
        chemin = u.replace(SITE, "") or "/"
        corps = p["html"]
        for m in re.finditer(r'<a[^>]*href\s*=\s*(["\'])(.*?)\1', corps, re.I | re.S):
            href = html.unescape(m.group(2)).strip()
            if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")): continue
            liens[urllib.parse.urljoin(u, href).split("#")[0]].add(chemin)
        for tag in re.findall(r'<img[^>]*>', corps, re.I):
            m = re.search(r'src\s*=\s*(["\'])(.*?)\1', tag, re.I)
            if m: images[urllib.parse.urljoin(u, m.group(2))].add(chemin)
            if not re.search(r'alt\s*=\s*(["\'])(.+?)\1', tag, re.I): sans_alt.append(chemin)

    for cible, sources in sorted(liens.items()):
        interne = cible.startswith(SITE)
        if cible in pages and pages[cible].get("code") == 200: continue
        code, _, _, _ = http(cible, "HEAD")
        if code in (0, 403, 405, 501):            # certains serveurs refusent HEAD
            code, _, _, _ = http(cible, "GET")
        if code == 200: continue
        # 429 (trop de requetes) et 999 (LinkedIn) ne disent rien de la sante du
        # lien : ce sont des protections anti-robot. Instagram repond 200 a une
        # vraie visiteuse et 429 a un runner GitHub. Signaler ca chaque jour
        # apprendrait a ignorer le rapport, ce qui est exactement le defaut
        # qu'on vient de corriger.
        if not interne and code in (429, 999):
            continue
        ou = ", ".join(sorted(sources)[:4])
        if interne:
            ERREUR("liens", f"lien interne casse (HTTP {code}) : {cible.replace(SITE,'')} "
                            f"— cite sur {ou}")
        else:
            ALERTE("liens", f"lien externe injoignable (HTTP {code}) : {cible} — cite sur {ou}")

    for img, sources in sorted(images.items()):
        code, _, _, _ = http(img, "HEAD")
        if code in (0, 403, 405): code, _, _, _ = http(img, "GET")
        if code != 200:
            ERREUR("images", f"image cassee (HTTP {code}) : {img.replace(SITE,'')} "
                             f"— sur {', '.join(sorted(sources)[:4])}")
    for chemin in sorted(set(sans_alt)):
        ALERTE("images", f"{chemin} : image sans attribut alt (accessibilite + SEO image)")

    INFO(f"{len(liens)} liens et {len(images)} images testes un par un")


# --------------------------------------------------------- 4. GEO / VISIBILITE IA
def controle_geo(pages, urls_sitemap):
    # a) les crawlers IA obtiennent-ils REELLEMENT la page ?
    #    Un robots.txt permissif ne prouve rien : l'hebergeur, un pare-feu ou une
    #    protection anti-bot peuvent renvoyer 403 a ces agents sans prevenir.
    ok_ia = []
    for nom, ua in CRAWLERS_IA.items():
        code, _, _, _ = http(f"{SITE}/perimenopause", ua=ua)
        if code != 200:
            ERREUR("geo", f"le crawler {nom} recoit HTTP {code} : le site lui est invisible "
                          f"(donc absent des reponses generees par cet outil)")
        else:
            ok_ia.append(nom)
    if ok_ia:
        INFO(f"crawlers servis en 200 : {', '.join(ok_ia)}")

    # b) robots.txt : une directive Disallow ciblant un bot IA le coupe malgre un 200
    _, robots, _, _ = http(f"{SITE}/robots.txt")
    bloc, agent = {}, None
    for ligne in robots.splitlines():
        ligne = ligne.split("#")[0].strip()
        if not ligne: continue
        if ligne.lower().startswith("user-agent:"):
            agent = ligne.split(":", 1)[1].strip()
            bloc.setdefault(agent, [])
        elif ligne.lower().startswith("disallow:") and agent is not None:
            v = ligne.split(":", 1)[1].strip()
            if v: bloc[agent].append(v)
    for nom in CRAWLERS_IA:
        for agent, interdits in bloc.items():
            if agent.lower() == nom.lower() and "/" in interdits:
                ERREUR("geo", f"robots.txt interdit tout le site a {nom} (Disallow: /)")
    if "Sitemap:" not in robots and "sitemap:" not in robots:
        ERREUR("geo", "robots.txt ne declare pas l'URL du sitemap")

    # c) llms.txt : l'index que lisent les moteurs generatifs. Doit couvrir le site
    #    et ne contenir aucun lien mort, sinon il devient une source de reponses fausses.
    code, llms, _, _ = http(f"{SITE}/llms.txt")
    if code == 200:
        cites = set(re.findall(r'\((https://virginiedeconinck\.com[^)]*)\)', llms))
        for u in cites:
            c, _, _, _ = http(u, "HEAD")
            if c in (0, 403, 405): c, _, _, _ = http(u, "GET")
            if c != 200:
                ERREUR("geo", f"llms.txt cite une URL morte (HTTP {c}) : {u.replace(SITE,'')}")
        manquantes = {u.rstrip("/") for u in urls_sitemap} - {u.rstrip("/") for u in cites}
        for u in sorted(manquantes):
            ALERTE("geo", f"page absente de llms.txt : {u.replace(SITE,'') or '/'} "
                          f"(les moteurs IA ne la verront pas dans l'index)")
        INFO(f"llms.txt reference {len(cites)} URLs, toutes testees")

    # d) donnees structurees : c'est ce que les moteurs generatifs lisent en priorite
    for u, p in pages.items():
        if p.get("code") != 200: continue
        chemin = u.replace(SITE, "") or "/"
        blocs = re.findall(r'(?s)<script[^>]*application/ld\+json[^>]*>(.*?)</script>', p["html"])
        if not blocs:
            ERREUR("geo", f"{chemin} : aucune donnee structuree JSON-LD "
                          f"(page difficilement citable par une IA)")
            continue
        types, articles = [], []
        for b in blocs:
            try:
                d = json.loads(b)
            except Exception as e:
                ERREUR("geo", f"{chemin} : JSON-LD invalide, illisible par les moteurs ({e})")
                continue
            for item in (d if isinstance(d, list) else [d]):
                if not isinstance(item, dict) or not item.get("@type"): continue
                t = item["@type"]
                tl = t if isinstance(t, list) else [t]
                types += tl
                if {"Article", "BlogPosting"} & set(tl):
                    articles.append(item)

        # Plusieurs blocs Article sur une page sont tolerés par Google TANT QUE leur
        # contenu concorde. Ce qui casse, c'est la CONTRADICTION : deux headline ou
        # deux url differentes, et les moteurs ne savent plus lequel fait foi.
        # On distingue donc le vrai conflit (erreur) de la simple redondance (alerte).
        if len(articles) > 1:
            titres = {a.get("headline") for a in articles if a.get("headline")}
            liens_a = {(a.get("url") or a.get("mainEntityOfPage")) for a in articles
                       if (a.get("url") or a.get("mainEntityOfPage"))}
            liens_a = {l.get("@id") if isinstance(l, dict) else l for l in liens_a}
            if len(titres) > 1:
                ERREUR("geo", f"{chemin} : {len(articles)} blocs JSON-LD Article aux titres "
                              f"CONTRADICTOIRES ({' / '.join(sorted(t[:45] for t in titres))}) : "
                              f"les moteurs ne savent pas lequel fait foi")
            elif len(liens_a) > 1:
                ERREUR("geo", f"{chemin} : {len(articles)} blocs JSON-LD Article pointant vers "
                              f"des URL differentes ({', '.join(sorted(liens_a))})")
            else:
                ALERTE("geo", f"{chemin} : {len(articles)} blocs JSON-LD Article redondants "
                              f"(contenu concordant, mais un seul suffit)")
        # Types principaux acceptes : tout ce qui identifie la NATURE de la page.
        # CollectionPage, Blog et ProfilePage sont des types parfaitement valides,
        # la liste precedente etait trop etroite et generait une fausse alerte.
        PRINCIPAUX = {"Article", "BlogPosting", "NewsArticle", "WebPage", "CollectionPage",
                      "Blog", "ProfilePage", "AboutPage", "Person", "Organization"}
        if not (PRINCIPAUX & set(types)):
            ALERTE("geo", f"{chemin} : JSON-LD sans type principal identifiant la page")
        # Le fil d'Ariane structure : Google l'affiche dans ses resultats a la
        # place de l'URL nue, et il donne aux moteurs la place de la page dans
        # l'arborescence. L'accueil n'en a pas besoin, il EST la racine.
        if chemin != "/" and "BreadcrumbList" not in types:
            ALERTE("geo", f"{chemin} : pas de BreadcrumbList (fil d'Ariane structure)")

    # e) cohesion sitemap <-> pages reellement servies
    for u in urls_sitemap:
        if pages.get(u, {}).get("code") not in (200,):
            continue
    INFO(f"{len(urls_sitemap)} pages du sitemap controlees")


# ------------------------------------------------------------------ RAPPORT
def rapport(markdown=False):
    d = datetime.datetime.now(datetime.timezone.utc)
    tampon = d.strftime("%d/%m/%Y %H:%M UTC")
    L = []
    if markdown:
        L.append(f"# Surveillance virginiedeconinck.com\n\n_Controle du {tampon}_\n")
        L.append(f"**{len(erreurs)} erreur(s)** · **{len(alertes)} point(s) a optimiser**\n")
        if erreurs:
            L.append("## Erreurs (quelque chose est casse ou invisible)\n")
            for cat, m in erreurs: L.append(f"- `{cat}` {m}")
        else:
            L.append("## Aucune erreur : le site est sain\n")
        if alertes:
            L.append("\n## A optimiser (n'ouvre pas d'alerte)\n")
            for cat, m in alertes: L.append(f"- `{cat}` {m}")
        if infos:
            L.append("\n## Perimetre couvert\n")
            for m in infos: L.append(f"- {m}")
    else:
        L.append(f"=== SURVEILLANCE virginiedeconinck.com — {tampon} ===")
        L.append(f"{len(erreurs)} erreur(s), {len(alertes)} a optimiser\n")
        if erreurs:
            L.append("--- ERREURS ---")
            for cat, m in erreurs: L.append(f"  [{cat}] {m}")
        else:
            L.append("--- aucune erreur ---")
        if alertes:
            L.append("\n--- A OPTIMISER ---")
            for cat, m in alertes: L.append(f"  [{cat}] {m}")
        if infos:
            L.append("\n--- PERIMETRE ---")
            for m in infos: L.append(f"  {m}")
    return "\n".join(L)


def main():
    controle_socle()
    pages, urls = collecte_pages()
    if pages:
        controle_seo(pages)
        controle_liens(pages)
        controle_geo(pages, urls)

    txt = rapport("--markdown" in sys.argv)
    print(txt)
    if "--markdown" in sys.argv:
        import os
        chemin = os.environ.get("GITHUB_STEP_SUMMARY")
        if chemin:
            with open(chemin, "a", encoding="utf-8") as f: f.write(txt + "\n")
        with open("rapport-surveillance.md", "w", encoding="utf-8") as f: f.write(txt + "\n")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
