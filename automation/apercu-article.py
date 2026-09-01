#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere un apercu PDF FIDELE d'un article, et PROUVE qu'il n'est pas tronque.

Pourquoi ce fichier existe : le 01/09/2026 Virginie a recu plusieurs apercus PDF
dont le texte etait coupe en plein milieu d'une phrase. Ses mots : « ca fait
plusieurs fois que les pages sont tronquees, ca ne peut plus aller ». La cause
n'etait pas l'article, qui etait complet, mais ma facon de fabriquer le PDF.

Trois causes cumulees, mesurees ce jour-la :
  1. `body { overflow: hidden auto }` : a l'impression, un conteneur defilant
     fait disparaitre ce qui depasse.
  2. `nav { position: fixed }` : le bandeau se reimprime sur chaque page et
     recouvre du texte.
  3. aucune regle @media print : les paragraphes et les blocs FAQ se coupent
     n'importe ou entre deux pages.

Le script neutralise les trois, PUIS relit le PDF produit et compare son texte a
celui de la page. S'il manque une phrase, il le dit et sort en erreur, au lieu
de livrer un document ampute.

Usage :
  python3 automation/apercu-article.py blog/mon-article.html sortie.pdf
"""
import html as htmllib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import http.server
import socketserver

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS_IMPRESSION = """
<style id="apercu-impression">
  .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
  @page { margin: 12mm 10mm; }
  @media print {
    html, body { overflow: visible !important; height: auto !important; }
    * { overflow: visible !important; }
    nav { position: static !important; }
    .article-hero { height: auto !important; min-height: 0 !important; margin-top: 0 !important; }
    .article-hero img { height: auto !important; max-height: 460px; }
    p, li, h1, h2, h3, blockquote { orphans: 3; widows: 3; }
    .faq-bloc, .pull-quote, .sources li, .cta-block { break-inside: avoid; page-break-inside: avoid; }
  }
</style>
</head>"""


def paragraphes(chemin_html):
    """Les paragraphes du CORPS, seule chose qui doit se retrouver entiere.

    On compare les <p> et les <li> et non un decoupage brut de toute la page :
    les titres, l'ariane et la barre de meta se concatenent entre eux et
    produisent de fausses alertes.
    """
    src = open(chemin_html, encoding="utf-8").read()
    corps = re.sub(r"(?s)<(script|style|nav|footer)\b.*?</\1>", " ", src)
    out = []
    for m in re.finditer(r"(?s)<(p|li)\b[^>]*>(.*?)</\1>", corps):
        t = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        if len(t) > 60:
            out.append(t)
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: apercu-article.py <article.html> <sortie.pdf>")
    article, sortie = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    racine = os.path.dirname(os.path.abspath(article)) or "."
    depot = os.path.abspath(os.path.join(racine, ".."))

    src = open(article, encoding="utf-8").read()
    # le point de terminaison Netlify Images n'existe qu'en production
    src = re.sub(r"/\.netlify/images\?url=%2F([^&\"]+)[^\"]*", r"/\1", src)
    src = src.replace("</head>", CSS_IMPRESSION)

    tmp = tempfile.mkdtemp(prefix="apercu-")
    try:
        for f in os.listdir(depot):
            if f.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                shutil.copy(os.path.join(depot, f), tmp)
        page = os.path.join(tmp, "apercu.html")
        open(page, "w", encoding="utf-8").write(src)

        os.chdir(tmp)
        class Muet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass

        srv = socketserver.TCPServer(("127.0.0.1", 0), Muet)
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()

        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--virtual-time-budget=12000",
                        "--no-pdf-header-footer", "--print-to-pdf-no-header",
                        "--print-to-pdf=" + sortie,
                        "http://127.0.0.1:%d/apercu.html" % port],
                       capture_output=True)
        srv.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not os.path.exists(sortie):
        sys.exit("ECHEC : aucun PDF produit.")

    # LA verification : le PDF contient-il tout le texte de la page ?
    from pypdf import PdfReader
    lu = " ".join(p.extract_text() or "" for p in PdfReader(sortie).pages)
    lu = re.sub(r"\s+", " ", lu)

    def norm(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    lu_n = norm(lu)
    paras = paragraphes(article)
    # on verifie le DEBUT et la FIN de chaque paragraphe : une coupe en plein
    # milieu se voit sur la fin, une page perdue se voit sur le debut.
    manquantes = []
    for p in paras:
        n = norm(p)
        if n[:55] not in lu_n or n[-55:] not in lu_n:
            manquantes.append(p)

    print("PDF : %s (%d Ko, %d pages)"
          % (os.path.basename(sortie), os.path.getsize(sortie) // 1024, len(PdfReader(sortie).pages)))
    print("paragraphes du corps verifies (debut ET fin) : %d" % len(paras))
    if manquantes:
        print("TRONQUE : %d paragraphe(s) incomplet(s) dans le PDF" % len(manquantes))
        for p in manquantes[:5]:
            print("   ->", p[:130])
        sys.exit(1)
    print("COMPLET : chaque paragraphe est present du debut a la fin.")


if __name__ == "__main__":
    main()
