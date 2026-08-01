#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere une og:image 1200x630 au gabarit de marque du site public.

Pourquoi ce fichier existe : les 18 og:image du lot du 29/07/2026 ont ete
fabriquees sans laisser de script. Le 01/08/2026, il a fallu remesurer le
gabarit au pixel sur une image existante pour en produire une de plus.
Ce script fige cette geometrie pour que ca ne se reproduise pas.

Gabarit (mesure sur og/nad-vieillissement-feminin.jpg) :
  panneau blanc 0-672 (56%), photo 672-1200 (528 px)
  eyebrow y 45-64 | titre L1 y 131-201 | titre L2 y 229-299 (dore)
  sous-titre y 350-366 | url y 570-590 | marge gauche 88

Usage :
  python3 automation/og-image.py --photo estrobolome-hero.jpg \
      --eyebrow MICROBIOTE --l1 "Le microbiote" --l2 ESTROBOLOME \
      --sub "IL DECIDE COMBIEN D'OESTROGENES CIRCULENT" \
      --out og/blog-estrobolome-microbiote-femme.jpg
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
SPLIT = 672           # ou commence la photo
MARGE = 88
ACCENT = (196, 168, 130)   # --accent #c4a882
INK = (14, 14, 14)         # --ink #0e0e0e
GRIS = (138, 138, 138)
BLANC = (255, 255, 255)

SERIF = "/System/Library/Fonts/Supplemental/Didot.ttc"
SANS = "/System/Library/Fonts/Supplemental/Futura.ttc"


def espace(draw, xy, texte, font, fill, interlettre):
    """PIL n'a pas de letter-spacing : on dessine caractere par caractere."""
    x, y = xy
    for c in texte:
        draw.text((x, y), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + interlettre
    return x


def ajuste(texte, chemin, cible_px, depart=76, mini=30):
    """Plus grande taille de police telle que le texte tienne dans cible_px."""
    taille = depart
    while taille > mini:
        f = ImageFont.truetype(chemin, taille)
        if f.getbbox(texte)[2] <= cible_px:
            return f
        taille -= 1
    return ImageFont.truetype(chemin, mini)


def photo_cadree(chemin, larg, haut, ancrage=0.2):
    """Remplit larg x haut sans deformer (equivalent object-fit:cover)."""
    im = Image.open(chemin).convert("RGB")
    r = max(larg / im.width, haut / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    gx = (im.width - larg) // 2
    gy = int((im.height - haut) * ancrage)   # object-position: center 20%
    return im.crop((gx, gy, gx + larg, gy + haut))


def construire(photo, eyebrow, l1, l2, sub, sortie, ancrage=0.2):
    img = Image.new("RGB", (W, H), BLANC)
    img.paste(photo_cadree(photo, W - SPLIT, H, ancrage), (SPLIT, 0))
    d = ImageDraw.Draw(img)

    dispo = SPLIT - MARGE - 40    # largeur utile du panneau texte

    espace(d, (MARGE, 45), eyebrow.upper(), ImageFont.truetype(SANS, 17), GRIS, 4.5)

    f1 = ajuste(l1, SERIF, dispo, depart=78)
    d.text((MARGE, 131 - f1.getbbox(l1)[1]), l1, font=f1, fill=INK)

    f2 = ajuste(l2.upper(), SERIF, dispo - 30, depart=76)
    espace(d, (MARGE, 229 - f2.getbbox(l2.upper())[1]), l2.upper(), f2, ACCENT, 3)

    espace(d, (MARGE, 350), sub.upper(), ImageFont.truetype(SANS, 15), GRIS, 3.2)
    d.text((MARGE, 570), "virginiedeconinck.com",
           font=ImageFont.truetype(SANS, 18), fill=INK)

    img.save(sortie, "JPEG", quality=88, optimize=True)
    return sortie


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for a in ("photo", "eyebrow", "l1", "l2", "sub", "out"):
        p.add_argument("--" + a, required=True)
    p.add_argument("--ancrage", type=float, default=0.2)
    a = p.parse_args()
    print("ecrit :", construire(a.photo, a.eyebrow, a.l1, a.l2, a.sub,
                                a.out, a.ancrage))
