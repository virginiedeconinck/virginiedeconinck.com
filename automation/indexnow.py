#!/usr/bin/env python3
"""
INDEXNOW : prevenir Bing (et donc ChatGPT) des qu'une page change.

Pourquoi ce fichier existe. Mesure du 31/07/2026 : Google avait deja le bon titre
de la page d'accueil, mais Bing servait encore l'ancien site, "Personal Coaching &
Fitness Programs", et une page /services/ supprimee depuis. Or ChatGPT s'appuie sur
Bing. Le residu "coach sportif" que Virginie subit vit donc surtout chez Bing, pas
chez Google, et rien ne poussait Bing a se mettre a jour.

IndexNow renverse le mecanisme : au lieu d'attendre le passage d'un robot, le site
ANNONCE ses changements. Gratuit, sans inscription, sans compte Webmaster Tools. Un
seul envoi touche Bing, Yandex, Seznam et Naver. La cle posee a la racine du site
sert de preuve de propriete : elle est PUBLIQUE par conception, ce n'est pas un secret.

Ne rien envoyer quand rien n'a change : le protocole demande de ne signaler que les
pages reellement modifiees. On se cale donc sur la date de derniere modification
declaree dans le sitemap, et on ne soumet que ce qui a bouge depuis le dernier envoi.

Usage :
    python3 automation/indexnow.py            # seulement les pages modifiees depuis le dernier envoi
    python3 automation/indexnow.py --tout     # toutes les pages du sitemap
"""
import json, re, sys, datetime, pathlib
import urllib.request

HOTE = 'virginiedeconinck.com'
SITEMAP = f'https://{HOTE}/sitemap.xml'
POINT_ENVOI = 'https://api.indexnow.org/indexnow'
ETAT = pathlib.Path(__file__).parent / 'indexnow-etat.json'


def cle():
    """La cle est le fichier <cle>.txt pose a la racine du depot."""
    racine = pathlib.Path(__file__).parent.parent
    for f in racine.glob('*.txt'):
        nom = f.stem
        if len(nom) == 32 and re.fullmatch(r'[0-9a-f]{32}', nom):
            return nom
    print("ECHEC : aucun fichier de cle IndexNow trouve a la racine du depot.")
    print("  attendu : un fichier <32 caracteres hexadecimaux>.txt contenant la meme chaine")
    sys.exit(1)


def sitemap():
    """Retourne [(url, date de derniere modification)] lu sur le site EN LIGNE."""
    with urllib.request.urlopen(SITEMAP, timeout=45) as r:
        xml = r.read().decode('utf-8')
    blocs = re.findall(r'<url>(.*?)</url>', xml, re.S)
    sortie = []
    for b in blocs:
        u = re.search(r'<loc>(.*?)</loc>', b)
        d = re.search(r'<lastmod>(.*?)</lastmod>', b)
        if u:
            sortie.append((u.group(1).strip(), (d.group(1).strip() if d else '')))
    return sortie


def main():
    tout = '--tout' in sys.argv
    k = cle()
    pages = sitemap()
    if not pages:
        print("ECHEC : sitemap vide ou illisible."); return 1

    connu = {}
    if ETAT.exists():
        try:
            connu = json.loads(ETAT.read_text(encoding='utf-8')).get('pages', {})
        except Exception:
            connu = {}

    if tout:
        a_envoyer = [u for u, _ in pages]
        raison = "envoi complet demande"
    else:
        a_envoyer = [u for u, d in pages if connu.get(u) != d]
        raison = "pages dont la date de modification a change depuis le dernier envoi"

    if not a_envoyer:
        print(f"Rien a signaler : les {len(pages)} pages du sitemap sont inchangees depuis le dernier envoi.")
        return 0

    print(f"{len(a_envoyer)} page(s) a signaler ({raison}) :")
    for u in a_envoyer:
        print("   ", u)

    corps = json.dumps({"host": HOTE, "key": k,
                        "keyLocation": f"https://{HOTE}/{k}.txt",
                        "urlList": a_envoyer}).encode()
    req = urllib.request.Request(POINT_ENVOI, data=corps,
                                 headers={'Content-Type': 'application/json; charset=utf-8'},
                                 method='POST')
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            code = r.status
        # 200 = pris en compte ; 202 = accepte, cle en cours de validation.
        if code in (200, 202):
            print(f"Accepte par IndexNow (code {code}). Bing, Yandex, Seznam et Naver sont prevenus.")
            ETAT.write_text(json.dumps(
                {"dernierEnvoi": datetime.datetime.now(datetime.timezone.utc)
                    .isoformat(timespec='seconds'),
                 "pages": {u: d for u, d in pages}}, indent=1, ensure_ascii=False), encoding='utf-8')
            print(f"Etat enregistre dans {ETAT.name} : les prochains envois ne porteront que sur les changements.")
        else:
            print(f"::error::IndexNow a repondu {code} : rien n'est confirme.")
            return 1
    except Exception as e:
        detail = getattr(e, 'read', lambda: b'')().decode()[:300]
        print(f"::error::envoi IndexNow refuse : {e} {detail}")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
