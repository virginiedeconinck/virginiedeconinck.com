#!/usr/bin/env python3
"""Envoie un fichier Markdown a Virginie par email, via Brevo.

Ecrit le 31/07/2026 pour le rapport SEO/GEO hebdomadaire. Sort du code d'envoi
du fichier de workflow pour qu'il ne soit ecrit qu'a UN seul endroit : le job
d'alerte contient encore sa propre copie, testee et fonctionnelle le 31/07, qui
sera ramenee ici lors d'un lot separe plutot que touchee pendant qu'elle marche.

Un rapport que personne ne lit ne sert a rien : c'est la lecon de l'Issue #3,
restee ouverte et non lue pendant 25 jours. Tout ce qui est produit
automatiquement doit atterrir dans la boite mail de Virginie, pas dans un
tableau de bord qu'elle n'ouvre jamais.

Usage :  python3 automation/envoyer-email.py <fichier.md> "<sujet>"
La cle arrive par la variable d'environnement BREVO_API_KEY.
"""
import os, sys, json, html, urllib.request

EXPEDITEUR = {"name": "Site public", "email": "alertes@virginiedeconinck.com"}
DESTINATAIRE = [{"email": "virginiedeconinck@gmail.com", "name": "Virginie"}]


def markdown_en_html(texte):
    """Rendu volontairement minimal : titres, listes, blocs de code, gras.

    Pas de bibliotheque externe : le workflow n'installe que requests et
    cryptography, et une dependance de plus est une dependance de plus a casser.
    """
    sortie, dans_bloc = [], False
    for ligne in texte.splitlines():
        if ligne.startswith('```'):
            sortie.append('</pre>' if dans_bloc else
                          '<pre style="background:#f4f4f8;padding:12px;border-radius:8px;'
                          'white-space:pre-wrap;font-size:13px;line-height:1.5;'
                          'font-family:ui-monospace,Menlo,monospace">')
            dans_bloc = not dans_bloc
            continue
        if dans_bloc:
            sortie.append(html.escape(ligne))
            continue
        l = html.escape(ligne)
        if ligne.startswith('## '):
            sortie.append(f'<h2 style="font-size:18px;margin:26px 0 8px;color:#15243f">{l[3:]}</h2>')
        elif ligne.startswith('# '):
            sortie.append(f'<h1 style="font-size:22px;margin:0 0 6px;color:#15243f">{l[2:]}</h1>')
        elif ligne.startswith('- '):
            sortie.append(f'<div style="margin:2px 0 2px 14px">• {l[2:]}</div>')
        elif ligne.startswith('_') and ligne.endswith('_'):
            sortie.append(f'<p style="color:#666;font-size:14px;margin:2px 0">{l[1:-1]}</p>')
        elif not ligne.strip():
            sortie.append('<div style="height:6px"></div>')
        else:
            sortie.append(f'<p style="margin:4px 0">{l}</p>')
    return "\n".join(sortie)


def main():
    if len(sys.argv) < 3:
        print("usage : envoyer-email.py <fichier.md> \"<sujet>\"")
        return 1
    chemin, sujet = sys.argv[1], sys.argv[2]
    cle = os.environ.get('BREVO_API_KEY', '').strip()
    if not cle:
        print("::error::Secret BREVO_API_KEY absent : le rapport n'a PAS ete envoye.")
        return 0          # ne pas faire echouer le job pour autant : le rapport reste archive
    try:
        texte = open(chemin, encoding='utf-8').read()
    except Exception as e:
        print(f"::error::rapport introuvable ({chemin}) : {e}")
        return 0

    corps = ('<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;'
             'font-size:16px;line-height:1.6;color:#1a1a2e;max-width:640px">'
             + markdown_en_html(texte) +
             '<p style="color:#666;font-size:13px;margin-top:26px;border-top:1px solid #e5e5ec;'
             'padding-top:12px">Rapport automatique, en lecture seule : rien n\'a ete modifie '
             'ni publie sur le site. Les chiffres viennent de Google Search Console et des '
             'suggestions de recherche Google, mesures le jour de l\'envoi.</p></div>')

    req = urllib.request.Request(
        'https://api.brevo.com/v3/smtp/email',
        data=json.dumps({"sender": EXPEDITEUR, "to": DESTINATAIRE,
                         "subject": sujet, "htmlContent": corps}).encode(),
        headers={'api-key': cle, 'content-type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("Rapport envoye, Brevo a repondu", r.status)
    except Exception as e:
        detail = getattr(e, 'read', lambda: b'')().decode()[:300]
        print(f"::error::Brevo a REFUSE l'envoi du rapport : {e} {detail}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
