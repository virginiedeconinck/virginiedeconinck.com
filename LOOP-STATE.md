# LOOP-STATE, monitoring site public virginiedeconinck.com

> ✅ **CYCLE DU 2026-09-01 PUBLIÉ.** Article « Mélasma et traitement hormonal : ce qu'on ne vous
> dit pas » en ligne, vérifié à 21h46 (HTTP 200, sitemap à 21 URLs, `index, follow`, 0 lien cassé).
> Virginie a demandé son indexation dans Search Console le soir même. `origin/main` = **`04ab13c`** (mesure du 02/09/2026 07h25 ; ce fichier portait `27e7a72`, qui est le commit d'AVANT celui qui l'a versionné lui-même).
> - **PÉRIMÉ, corrigé par Virginie le 01/09/2026 au soir : la cadence N'A JAMAIS été suspendue.**
>   Ce fichier portait « cadence suspendue depuis le 17/08 » : c'était MA suspension en attendant
>   SON arbitrage, jamais sa décision, et je l'ai lue comme un acquis. Ses mots : « C'est un article
>   par mois, tous les premiers du mois. » Le sujet se décide désormais AVEC elle le 24 du mois
>   précédent (tâche `choix-sujet-article-mensuel`, prochain passage le 24/09). La 21e page EXISTE.
> - Le travail de fond va là où une demande RÉELLE monte : la peau.
>   « régénération cellulaire peau et collagène » passe de 26 à 51 impressions en un mois, et les
>   3 questions GEO relevées par Search Console portent toutes les trois sur la peau.
> - **Correction de fond la plus importante : `/glp1` faisait dire à sa source le contraire de ce
>   qu'elle dit.** La page écrivait « de la masse maigre, c'est-à-dire principalement du muscle »
>   en l'attribuant à Neeland 2024. Résumé ouvert à la source (PMID 38937282), verbatim : *changes
>   in lean mass may not always reflect changes in muscle mass as the former measure includes not
>   only muscle but also organs, bone, fluids, and water in fat tissue*. Corrigé aux 3 endroits.
>   Le message de fond ne bouge pas, l'attribution devient exacte.
> - **Les 44 nœuds `Person` du site n'avaient AUCUN `@id`.** Pour un moteur de réponse, ce n'est
>   pas une personne décrite 44 fois, ce sont 44 homonymes possibles. Identifiant canonique
>   `#virginie` ajouté sur les 44, en purement additif.
> - **13 pages avaient un bloc `Article` sans `datePublished` ni `image`.** Complétées, dates
>   prises dans l'historique git de chaque fichier, jamais inventées.
> - **`/histamine` : titre et structure NON touchés.** 3 clics sur 14 impressions, c'est le
>   meilleur taux de clic du site. On n'y touche pas. Seulement un garde-fou ajouté sur le dosage
>   DAO, la case vide de la grille comblée, et le CTA changé (il promettait un résultat esthétique
>   à une lectrice venue faire un diagnostic différentiel, et il était identique MOT POUR MOT à
>   celui de `/glp1`).
> - **Moteur corrigé, pas seulement le rapport.** `automation/maillage.py` reproposait le 31/08,
>   mot pour mot, les 2 propositions écartées à la main le 02/08. La correction n'avait jamais été
>   faite dans le code, donc elle revenait chaque mois. `corps_liable()` retire désormais les
>   citations et le bloc de voix, et `CONTEXTES_TROMPEURS` écarte le contresens « entraînement en
>   résistance » vers `/resistance-insuline`. **Leçon générale : une correction faite dans un
>   rapport et pas dans le moteur n'est pas une correction, c'est un report.**
> - ⚠️ **Six affirmations d'agents étaient fausses et ont été rattrapées par mesure** : la page
>   collagène ne parle nulle part de collagène oral (0 occurrence) ; le mot mastocyte EST dans
>   `/histamine` ligne 301 ; le « TEWL augmenté » n'est pas dans le résumé de l'étude ; les deux
>   propositions de méta parlaient de « froid » et de « déficit calorique », absents de la page ;
>   4 blocs `Article` incomplets annoncés contre 13 mesurés ; « doubler la dose » généralisait un
>   rapport de 2,4 en rapport de 2. **Un rapport d'agent est un indice, jamais une preuve.**
> - **Reste à décider par Virginie** : le domaine ci-dessus ; une photo pour les 5 pages piliers
>   (elles n'ont AUCUNE image, le bloc de citation affiche un rond gris de 64 px à la place de son
>   portrait) ; les 17 pages sur 20 encore sans bloc de sources ; et si elle veut la date de
>   septembre sur tout le site plutôt que sur les 6 pages réellement modifiées.

> ✅ **CYCLE ÉDITORIAL DU 2026-08-01 PUBLIÉ EN PROD** (sur « publie » de Virginie). `main` = **`b2a4976`**. Dernière surveillance du site en ligne, 20h49 : **0 erreur, 0 point à optimiser**, 20 pages, 24 liens et 5 images testés un par un, 8 crawlers IA en 200.
> - **Article Estrobolome EN LIGNE** (200, sitemap 20 URLs, photo `estrobolome-hero.jpg` présente, og dédiée). Sa date visible est passée en **Août 2026** et `datePublished` au 2026-08-01 : il n'avait jamais été réellement accessible avant.
> - **5 corrections de fond.** La plus importante : l'essai cité dans l'Estrobolome était mal restitué. Article original ouvert (DOI 10.1089/jmf.2023.k.0320) : **111 femmes de 45-55 ans** (pas « un effectif limité »), **formule de 3 souches** en ratio 2:1:1 (pas « une souche précise »), et les auteurs écrivent **n'avoir trouvé aucune corrélation entre les taux d'œstrogènes et les symptômes**, les deux groupes s'améliorant pareillement. Ce résultat manquait. Ajouté. Les 4 autres : rapamycine reclassée **sénomorphique** (elle était étiquetée « Sénolytique 02 » alors que la page définit le mot juste avant) ; perfusions NAD+ sorties de l'encadré « ce que la science soutient réellement » ; contradiction peptides « ne pénètre pas dans une veine » / « entre directement dans la circulation » levée aux 3 occurrences dont le JSON-LD ; SHBG « le libre qui agit » corrigé en « la fraction biodisponible ».
> - **Maillage.** `/regeneration-cellulaire` avait 26 liens entrants, **tous** menu, encart ou liste, et **zéro depuis une phrase**. Elle en a maintenant **5 en corps de texte** (accueil, biohacking, peptides, nad, cellules-sénescentes) et sort vers `/collagene-peau`. L'article Estrobolome passe de 3 à 5 liens sortants en prose (il nommait SHBG et inflammaging sans les lier) et reçoit 2 entrants contextuels.
> - **Fraîcheur, premier lot :** seules les 4 pages réellement modifiées étaient passées en août. **DÉCISION DE VIRGINIE le 01/08 : tout le site passe en août** (voir lot du soir ci-dessous). J'avais recommandé de ne dater que les pages touchées, pour ne pas envoyer un faux signal de fraîcheur à Google. Elle a tranché autrement, c'est son appel et c'est appliqué. Argument à ne pas re-servir chaque mois.
> - **Correctif post-publication** (`445df6e`) : la surveillance a détecté que le retitrage SHBG du matin avait changé le `<title>` sans les titres de partage. og:title et twitter:title réalignés.
>
> ✅ **LOT DU SOIR (commits `1b2e164` et `b2a4976`), publié et vérifié en ligne à 20h49 : surveillance 0 erreur / 0 point à optimiser.**
> - **Août 2026 sur TOUT le site**, sur demande de Virginie : 19 pages sur 20 affichent « août 2026 », les 20 ont `dateModified 2026-08-01` et `lastmod 2026-08-01`. La 20e est `/blog/`, qui **n'a jamais eu** de ligne de fraîcheur visible (vérifié par recherche dans tout l'historique git) : c'est une page de listing, sa fraîcheur est portée par les articles. Ne pas lui en ajouter une par réflexe d'uniformité.
> - **Les dates d'études citées ne sont PAS des marqueurs de fraîcheur.** « Menopause, juillet 2026 » et « Maturitas, juillet 2026 » sur `/shbg` sont des dates de publication scientifique. Ne jamais les passer en août.
> - **og:image de `/regeneration-cellulaire` : FAIT.** C'était la seule page sur 20 sans visuel social alors qu'elle déclare `summary_large_image`. Carte générée avec `hero.jpg`. Cette photo n'est QUE sur la vignette de partage, pas sur l'article de blog.
> - **Cadrage de cette carte, leçon à garder.** Les 20 cartes partagent la même géométrie (photo à 44 %, x=672) : quand un sujet « prend trop de place », le problème n'est jamais la largeur, c'est l'échelle du sujet dans la photo source. Deux méthodes écartées après contrôle à l'écran : le miroir des bords duplique un bras et la tête ; un fond étendu à bord net laisse une couture rectangulaire. **Méthode qui marche : marbre du haut de la photo étiré et flouté en arrière-plan, fondu large de 110 px.** Le fichier `hero.jpg` n'est pas modifié, le recul est fabriqué à la volée.
> - **Title de `/blog` :** 61 car. et « Biohacking Féminin » en doublon direct avec `/biohacking-feminin` qui, elle, a du trafic. Remplacé par « Blog : biologie féminine et longévité après 35 ans » (50 car.).
> - **Contrôle qualité complet des 21 pages**, fait par moi et non délégué : title ≤ 60, description ≤ 155, 1 H1, og 5/5, twitter 4/4, FAQPage, BreadcrumbList (sauf accueil, normal), disclaimer médical, **au moins un CTA vers une offre**, canonical. HTML sans balise non fermée, tous les blocs JSON-LD valides, sitemap valide, **zéro lien interne cassé**.
> - **Orthographe et typographie : mesurées sur le texte AFFICHÉ dans le navigateur**, pas sur le code source. Zéro double espace, zéro espace avant ponctuation, zéro mot répété, apostrophes homogènes. ⚠️ Piège à ne pas refaire : un contrôle sur le code HTML remonte des dizaines de faux « doubles espaces », car le navigateur fusionne les espaces. Toujours mesurer `innerText`.
>
> ✅ **LIENS EN CORPS DE TEXTE : 73 liens sortaient en BLEU NAVIGATEUR, corrigé le 02/08.**
> Défaut **antérieur** aux liens ajoutés le 01/08 : aucune page n'avait de règle CSS pour les liens
> contextuels. Mesuré à l'écran (couleur calculée `rgb(0,0,238)`), pas dans le code. Règle unique
> ajoutée aux 23 pages, reprenant la convention DÉJÀ en place (16 liens l'écrivaient à la main) :
> texte encre, fin soulignement `--accent-light`, survol qui passe le trait au doré. `--accent-light`
> ajoutée dans les 4 pages du blog, 404 et RGPD où elle n'était pas définie (les liens stylisés à la
> main y tombaient sur un soulignement noir). Vérifié en ligne sur les 21 pages : **0 lien bleu**.
> ⚠️ **Leçon de méthode.** Ma première version mettait les liens en doré : ça inventait une troisième
> convention. Toujours chercher comment le site fait DÉJÀ avant d'écrire une règle de style.
> Et toujours mesurer la couleur CALCULÉE dans le navigateur : le code ne dit pas ce qui s'affiche.
>
> ✅ **POIDS DES PHOTOS : rien à faire, vérifié le 02/08.** Livré en webp par le CDN Netlify :
> 183 Ko (article estrobolome), 144 Ko (shbg), 137 Ko (leviers), 49 Ko (glycémie). Correct pour des
> photos plein écran. **Hypothèse fausse à ne pas refaire :** j'ai cru que demander `w=1200` sur des
> sources de 1024 px les agrandissait inutilement. Mesuré : le CDN plafonne à la taille source,
> `w=1200` et `w=1024` livrent exactement le même poids. Aucun gain à changer quoi que ce soit.
>
> ✅ **COLLISION DE TÂCHES PLANIFIÉES : CORRIGÉE le 01/08.** Ce jour-là, `monitoring-site-public-vdck` (section 4, rattrapage) et `cycle-editorial-mensuel` ont exécuté le MÊME cycle en parallèle sur le même dépôt : condition de déclenchement identique, et aucune ne réservait le cycle avant de travailler (`lastCycleMonth` n'était écrit qu'à la fin). Effet mesuré : des audits ont lu des fichiers pendant leur réécriture et produit 2 fausses alertes, démenties 3 minutes plus tard.
> **Ce qui a été changé, dans les deux SKILL.md :** (1) le rattrapage exige une date **strictement** postérieure à `nextPlanned`, donc il ne peut plus se déclencher le jour J, qui appartient à la tâche mensuelle ; (2) les deux lisent et écrivent un verrou `cycleEnCours` (avec `expireISO` à +4 h) **avant** toute écriture, et l'effacent en posant `lastCycleMonth` ; (3) quand le rattrapage lance la tâche mensuelle, il lui dit explicitement de sauter garde-fou et verrou, sinon elle verrait la réservation du rattrapage et s'arrêterait aussitôt.
> Simulé sur l'état réel du journal : au 01/09 la mensuelle démarre et la quotidienne s'arrête ; au 02/09, si la mensuelle a échoué, le filet se déclenche.
>
> ⚠️ **FAUSSE ALERTE DU 01/08, à ne pas propager : « 9 requêtes SHBG sans page dédiée » était un BUG D'OUTIL.** `seo-geo.py` cherchait les mots de 5 lettres et plus (`[a-z]{5,}`), donc le mot « shbg » n'était **jamais** testé et les recherches « shbg prise de sang », « shbg élevée », « shbg comment augmenter », « shbg basse » étaient annoncées comme du terrain non couvert, alors que `/shbg-hormones-actives-femme` existe et venait justement d'être enrichie sur ces questions exactes. Corrigé le 02/08 (seuil à 4 caractères, mots outils exclus) et **vérifié par mesure comparative** : les 4 requêtes passent de « non couvert » à « couvert ». Même piège potentiel pour « nad » et « glp1 ». Leçon : avant de conclure à un trou de contenu, vérifier que l'outil sait lire le mot-clé.
>
> ✅ **Citation SHBG VÉRIFIÉE le 02/08 : elle est correcte, dossier clos.** L'étude WHI SHBG/sarcopénie est bien parue dans *Menopause*, volume 33 numéro 7, **juillet 2026**, pages 775-788 (epub 01/07/2026, PMID 41701631, Osmancevic, Daka, Larson, Allison, Burney, Shadyab, Cauley, Crandall). Une recherche web la datait à tort du 17/02/2026 : c'est le résultat de recherche qui était faux, pas la page. Ne pas rouvrir ce point.
>
> 🛑 **Préversion locale dans le panneau : SUJET CLOS le 02/08, ne plus le rouvrir, ne plus en parler à Virginie.**
> Elle ne fonctionne pas et ne fonctionnera pas : tout processus lancé par le panneau se voit refuser
> la lecture du dossier Téléchargements. Épuisé le 02/08 : l'accès « Fichiers et dossiers » était déjà
> donné, l'« Accès complet au disque » aussi, et l'app a été redémarrée. Toujours refusé. Ce n'est donc
> pas un réglage manquant côté Virginie, c'est la façon dont l'app lance ces serveurs.
> **Ne jamais lui redemander de cocher quoi que ce soit là-dessus.** Elle y a déjà passé du temps pour rien.
> **Méthode à utiliser directement, sans essayer le panneau :** servir le dossier depuis un shell, puis
> rendre avec Chrome headless. `--print-to-pdf` pour un article entier (rendu fidèle), `--screenshot`
> pour une vue. Attention, une capture pleine hauteur déforme la page : le bandeau est en `70vh` et
> enfle avec la fenêtre. Pour montrer une page à Virginie, passer par le PDF.


---

> ⚠️ **AVERTISSEMENT DE RECONSTRUCTION (02/08/2026, 08h25).** Tout ce qui suit cette ligne a été
> **effacé par erreur** puis **reconstruit de mémoire de lecture**. Cause : une réécriture en Python
> a pris « tout le texte à partir de la note d'outillage jusqu'à la fin » et l'a remplacé, emportant
> l'historique et la structure. Le fichier est passé de 16 204 à 8 858 octets. Il est gitignoré,
> aucune sauvegarde n'existait. La reconstruction s'appuie sur la lecture intégrale faite le même
> jour à 07h22, elle est fidèle sur le fond mais **pas garantie mot pour mot**. Les blocs d'historique
> antérieurs au 28/06 n'ont pas pu être restitués. En cas de doute sur un détail ancien, se fier au
> dépôt git et à `automation/cycle-log.json`, pas à ce fichier.

## Historique publié (reconstruit)

- **2026-06-28** : lot complet publié en prod (corrections scientifiques, vouvoiement, frontière
  gratuit/payant, SEO/GEO, maillage, cohérence navigation accueil=menu et SHBG, a-propos avec l'âge
  biologique 39,7 TruDiagnostic) + workflow de surveillance GitHub Actions. Déploiement Netlify depuis
  `main`. **Correction du 29/06** : l'article Estrobolome embarqué par erreur dans ce lot a été retiré
  de la prod (commit `c414519`). Il est désormais **EN LIGNE depuis le 01/08/2026**, voir en tête.
- **2026-07-29, lot SEO/GEO** : 18 titles ramenés sous 60 caractères, suffixe « | Virginie Deconinck »
  retiré sauf accueil et /a-propos ; 13 pages avaient 2 blocs JSON-LD `Article`, dont 5 aux `headline`
  contradictoires, fusionnés ; og:image dédiée par page (une seule servait 16 pages) ; BreadcrumbList
  sur les 18 pages internes ; FAQPage sur 19/19 ; /blog enrichi de 178 à 685 mots ;
  /blog/les-4-leviers-biologiques de 587 à 881 mots. Défauts trouvés en chemin et corrigés : l'article
  des 4 leviers TUTOYAIT (10 occurrences), 10 tirets cadratins, 3 pages sans aucun style de lien.
- **2026-07-31** : accès Search Console résolu (clé de compte de service
  `alien-bruin-504108-s7-93c4f22e43bb.json` dans `~/Downloads`, lue par `automation/seo-geo.py`).
  Titres de `/age-biologique-age-chronologique` et `/cellules-senescentes-vieillissement` retitrés sur
  mesure réelle. **Formulation corrigée le 03/08** après relecture des commits : cette note disait
  « ne pas revenir à un titre "la différence / vs" », ce qui se lit à l'envers de la réalité. Le titre
  ÉCARTÉ est **« Âge biologique et âge chronologique : la différence »** ; le titre RETENU, en ligne
  depuis le commit `dc2dee8` du 31/07, est **« Âge biologique vs chronologique : comment mesurer le
  vôtre »**. Le mot « vs » fait partie du titre gagnant, il ne fait pas partie de ce qu'on écarte.
  ⚠️ **Conséquence à ne pas rater : le CTR de 0,79 % de cette page mesure l'ANCIEN titre** (le nouveau
  n'était en ligne que le 31/07, dernier jour de la fenêtre). Ne pas rouvrir ce titre avant une
  fenêtre de 28 jours pleine sur le nouveau, soit **à partir du 31/08/2026**.
  3 sous-sections bouffées de chaleur ajoutées à `/perimenopause`. Page `/regeneration-cellulaire`
  créée. **http vers https vérifié : redirections 301 propres, ce n'est PAS un bug, ne pas rouvrir.**

## Charte (objectif & règles)

- **Objectif** : (1) veille constante sur le contenu du site public et mises à jour nécessaires ;
  (2) publier **1 article de blog tous les 30 jours**.
- **Méthode** : un seul élément à la fois, terminé complètement avant le suivant. Suivre les
  conventions des fichiers existants, ne pas inventer de patterns.
- **Garde-fou décisions** : si un élément exige une décision réservée à Virginie (dépenser, publier,
  contacter quelqu'un) → STOP sur cet élément, le mettre en « besoin de validation », passer au suivant.
- **Vérification** : après chaque élément, relire le livrable et confirmer l'objectif atteint. Échec →
  corriger et revérifier. Max 3 tentatives, sinon « bloqué » et on passe.
- **Arrêt** : quand tout est fait ou bloqué → rapport court (fait / bloqué / besoin de décision).

## Cadence & convention monitoring

- **Technique + SEO + GEO = GitHub Actions QUOTIDIEN** (cron `0 5 * * *`, soit 07h00 Luxembourg),
  workflow `surveillance-site-public.yml`, moteur `automation/monitoring.py`. Lançable à la main :
  `python3 automation/monitoring.py`. Couvre les 20 pages : disponibilité, TLS, gestionnaire 404,
  chaque lien et chaque image un par un, title/description/canonical/H1/viewport/lang, doublons,
  `noindex`, validité du JSON-LD et blocs `Article` contradictoires, intégrité de llms.txt, et accès
  réel des crawlers IA testé avec leur propre User-Agent. Deux niveaux : **ERREUR** ouvre une Issue,
  **À OPTIMISER** figure au rapport sans faire de bruit.
- Battement de cœur hebdomadaire conservé : GitHub désactive un workflow planifié après 60 jours sans
  commit sur le dépôt.
- **Fond = MENSUEL, le 1er du mois.** Voir le verrou anti-collision décrit en tête de ce fichier.
- **Convention fraîcheur** : harmoniser la date visible « Mis à jour en <mois> <année>», le
  `dateModified` du JSON-LD et le `lastmod` du sitemap. `datePublished` = première publication, à NE
  PAS changer. **Ne jamais toucher aux années dans les citations d'études.**
- Page RGPD (`politique-de-confidentialite`) : volontairement HORS sitemap, reste indexable.

## Règle photos blog

**À chaque nouvel article de blog : DEMANDER une photo à Virginie** (numéro du fichier dans
`~/Downloads`), la convertir au format bandeau des autres articles, ne jamais publier avec un
placeholder. **Rappel à l'ordre du 01/08/2026 : la demander AVANT de déployer, pas après.**
Voir la mémoire `blog-article-photo-rule`.

## Contexte projet (faits stables)

- Dossier local : `~/Downloads/Pages SEO` (SITE PUBLIC, ne pas confondre avec les 2 espaces privés).
- Netlify siteId : `7acdb5d6-8bb1-49b6-9ed0-27ce566d4403` (projet `virginiedck`).
- **Déploiement = AUTOMATIQUE via Git. PLUS AUCUN jeton Netlify.** Netlify publie la prod depuis la
  branche `main` du dépôt `virginiedeconinck/virginiedeconinck.com`. Publier = pousser sur `main`.
  Le jeton intégré dans `.git/config` était MORT. `gh auth setup-git` est configuré, donc
  `git push origin HEAD:main` suffit. Repli :
  `git push "https://x-access-token:$(gh auth token)@github.com/virginiedeconinck/virginiedeconinck.com.git" main`.
- **Cinq fichiers d'état sont gitignorés** (vérifié le 02/08) : `LOOP-STATE.md`,
  `automation/cycle-log.json`, `rapport-surveillance.md`, `rapport-seo-geo.md`, `rapport-maillage.md`.
  Jamais déployés, donc **aucun historique git en cas de perte**. C'est ce qui a rendu irrécupérable
  l'écrasement du 02/08 décrit plus haut.
- Réglage Netlify = « Deploy only the production branch » : SEULE `main` déclenche un déploiement.
  Pousser une autre branche ne publie rien, donc pas de préversion Netlify de branche : valider en
  local avant de fusionner.
- Convention couverture blog : image **portrait ~4:5** (ex. 1122×1402),
  `<a class="card"><img src="/xxx.png" loading="lazy">`. Le blog accepte des photos
  **lifestyle/street-style** (validé par Virginie le 26/06/2026) : ne PAS les juger « hors charte ».

## Pour le prochain run (cycle de septembre 2026)

- **Sujet recommandé : une page SOMMEIL.** C'est le seul thème des domaines d'expertise RCF sans
  aucune page, et celui où le rapport preuve / concurrence éditoriale francophone est le plus
  favorable (méta-analyse de 11 ECR sur 973 femmes ménopausées, essai randomisé 2026 pile dans la
  cible d'âge avec 53,6 ans de moyenne, deux molécules non hormonales homologuées avec bénéfice
  sommeil documenté). Revérifier la science le jour même avant d'écrire.
- **Mises à jour scientifiques identifiées le 01/08, par valeur décroissante** : `peptides` (vote du
  comité FDA du 24/07/2026, non contraignant, contre l'avis des scientifiques de l'agence, et 6 des 8
  membres récemment nommés exploitent des cliniques de peptides ; plus le conflit d'intérêts sur le
  chiffre GHK-Cu) ; `inflammaging` (non-universalité, *Nature Aging* juillet 2025) ; `glp1` (chiffres
  de l'essai BELIEVE, *Nature Medicine* 2026) ; `perimenopause` (le paysage thérapeutique a bougé
  quatre fois en neuf mois et la page n'en dit rien) ; `collagene-peau` (le collagène oral en
  complément n'est traité nulle part, alors que c'est la question numéro un des lectrices).
- **Frontière gratuit/payant, point à trancher** : l'ordre des leviers est reconstituable en agrégeant
  quatre endroits (accueil, article des 4 leviers, PDF). Le point de coupe le moins coûteux est
  l'article des 4 leviers, qui est en `noindex` donc sans enjeu SEO.
- **Maillage restant** : `peptides` (0 entrant, 0 sortant en prose), `biohacking-feminin` (0 sortant
  alors qu'elle est parente de 5 fils d'Ariane), `graisse-abdominale`, `cellules-senescentes` et
  `glp1` (0 sortant chacune).
- **GEO** : aucune citation vers une source primaire sur tout le site (0 occurrence de pubmed, doi.org,
  ncbi, nih.gov). Poser 2 à 3 liens sources sur les pages aux affirmations les plus fortes, pas partout.
  Et deux nœuds `Person` concurrents dans `a-propos.html`, sans `@id`, à fusionner.

## SOIRÉE DU 01/09/2026 : ce qui a été tranché, et ce qui reste

**Qui fait quoi (décision de Virginie).** La mise à jour du site est au VEILLEUR
`monitoring-site-public-vdck`, à lui seul. `cycle-editorial-mensuel` ne fait plus que l'article du
mois et son raccordement. Ses mots : « C'est uniquement toi qui es responsable de la mise à jour de
mon site. L'autre session est juste responsable de créer un article de blog par mois, rien d'autre. »
Les deux SKILL.md ont été corrigés en conséquence le soir même.

**Le nom de domaine : SUJET CLOS, ne plus jamais le remonter.** Il est en renouvellement automatique
chez OVH. Le moteur criait dès 45 jours avant l'échéance, six semaines par an. `monitoring.py`
corrigé sur `main` (`61f9f08`) : palier d'alerte supprimé, filet abaissé de 14 à 3 jours.

**Les deux titres à réécrire : ABANDONNÉ APRÈS MESURE, et c'est le bon geste.** Le rapport désignait
`/biohacking-feminin` (51 impr, 1 clic) et `/resistance-insuline` (31 impr, 0 clic) comme des pages à
retitrer. Une mesure ajoutée au moteur ce soir (`27e7a72`, bloc « SUR QUOI CES PAGES SORTENT ») montre
que la demande derrière n'existe pas : 6 des 51 impressions de biohacking sont sur le nom de Virginie,
3 sur une requête de veille, et `/resistance-insuline` n'a AUCUNE requête isolée. Les retitrer, c'était
inventer à quoi elles répondent. **Ne pas rouvrir ce chantier sans une demande mesurée.**

**Ce que Virginie a dit sur le niveau de détail.** Les micro-corrections (un effectif de 5 au lieu de
38, une décimale, une virgule) se vérifient AVANT d'écrire, en silence. Elles ne font jamais l'objet
d'un rapport : « c'est des petits détails qui ne vont pas enlever de la crédibilité à ce que je
raconte ». Ce jour-là, 50 % des lignes du lot n'étaient qu'une virgule devant « et » retirée, et deux
« faits faux corrigés » portaient sur du texte qui n'avait JAMAIS été publié.

**LA PISTE, et elle est unique.** `/histamine-perimenopause`, position 10.3 sur « histamine
périménopause », meilleur taux de clic du site. C'est la seule veine où gagner des places rapporte.
Et les 4 questions GEO réellement tapées, dont « pourquoi ma peau est plus sensible aux soins depuis
que j'ai passé 40 ans ? » : la réponse EXISTE déjà sur `/collagene-peau` et sort quand même en
position 87. Comprendre pourquoi est le prochain vrai sujet.

**Chantier proposé, non tranché : l'incarnation des pages.** Mesuré page par page le 01/09 : le « je »
des pages piliers est interchangeable (« À un moment donné, ma peau a changé »), sans date ni chiffre.
`/graisse-abdominale` n'a aucun vécu, seulement des CTA. `/perimenopause` est la seule avec un fait daté
(« les premières fluctuations à 38 ans »). Le 39,7 de TruDiagnostic n'est sur AUCUNE page pilier.
Commencer par 3 pages (histamine, périménopause, collagène), jamais par les 20 : modifier tout un site
qui va bien produit du bruit que Google traite comme tel.
