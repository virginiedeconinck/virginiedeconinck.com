# LOOP-STATE, monitoring site public virginiedeconinck.com

> ✅ **CYCLE DU 2026-09-01 PUBLIÉ.** Article « Mélasma et traitement hormonal : ce qu'on ne vous
> dit pas » en ligne, vérifié à 21h46 (HTTP 200, sitemap à 21 URLs, `index, follow`, 0 lien cassé).
> Virginie a demandé son indexation dans Search Console le soir même. **N'écris plus le SHA de `main` ici : c'est un piège structurel.** Ce fichier est versionné, donc tout SHA qu'il note désigne forcément le commit d'AVANT celui qui l'enregistre, et le run suivant croit trouver une divergence. Corrigé deux fois pour rien (02/09 puis 03/09, `27e7a72` → `04ab13c` → `bcd9a63`). La seule mesure valable est `git rev-parse origin/main`, à faire sur place.
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
> - **Reste à décider par Virginie** : le domaine ci-dessus ; les 17 pages sur 20 encore sans bloc
>   de sources ; et si elle veut la date de septembre sur tout le site plutôt que sur les 6 pages
>   réellement modifiées. **RETIRÉ le 14/09 : « un rond gris à la place de son portrait ».** Ce
>   disque (64 px, accent à 30 %) est dans le code depuis le premier commit du 14/05, sans jamais
>   aucune image à cet endroit : c'est un ornement de la maquette. Virginie ne l'a jamais vu comme
>   un manque. C'était une supposition, jamais mesurée, portée ici pendant deux semaines.

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
- Page RGPD (`politique-de-confidentialite`) : hors sitemap ET en `noindex, follow`, depuis le
  commit `b1e4658` du 31/07/2026, « Politique de confidentialite retiree de l'index ». **Cette ligne
  disait « reste indexable » : c'etait FAUX**, mesure sur la page en ligne le 07/09/2026. La page
  leviers `/blog/les-4-leviers-biologiques` est dans le meme cas (commit `4abaa18`, meme jour).
  Ce sont les deux seules pages en `noindex` du site avec la 404. C'est VOULU : quand Search Console
  signale « exclue par balise noindex », ne pas partir en chasse.

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
- **`LOOP-STATE.md` et `automation/cycle-log.json` sont VERSIONNÉS sur `main` depuis le 01/09/2026**
  (commit `04ab13c`, mesuré par `git ls-files` le 12/09). Cette ligne disait encore « cinq fichiers
  gitignorés » : c'était vrai jusqu'au 01/09 et c'est ce qui a rendu irrécupérable l'écrasement du
  02/08 décrit plus haut. Restent ignorés, et c'est voulu : les quatre `rapport-*.md` (vestiges figés,
  la vraie sortie est l'artefact du run cloud).
- Réglage Netlify = « Deploy only the production branch » : SEULE `main` déclenche un déploiement.
  Pousser une autre branche ne publie rien, donc pas de préversion Netlify de branche : valider en
  local avant de fusionner.
- Convention couverture blog : image **portrait ~4:5** (ex. 1122×1402),
  `<a class="card"><img src="/xxx.png" loading="lazy">`. Le blog accepte des photos
  **lifestyle/street-style** (validé par Virginie le 26/06/2026) : ne PAS les juger « hors charte ».

## Mesures du 07/09/2026 (lundi)

- **INDEXATION : les 21 URLs du sitemap sont « Envoyee et indexee ».** Mesure API `urlInspection`
  du 07/09 a 07h, une par une, 21 sur 21, zero exception. Explorations les plus recentes :
  `/muscle-longevite-feminine` le 06/09, `/` le 04/09, l'article melasma le 01/09 (jour de sa
  publication). **Donc toute ligne « non indexee » de Search Console porte sur une URL HORS
  sitemap, et les quatre cas sont voulus** : `virginiedck.netlify.app` (301 vers le vrai site,
  verifie page par page le 07/09), la 404, `/politique-de-confidentialite` et
  `/blog/les-4-leviers-biologiques` (noindex assume). Ne plus traiter ces lignes comme un defaut.
- **`virginiedck.netlify.app` : rien a faire, c'est deja regle.** Il renvoie un 301 vers
  `virginiedeconinck.com` sur la racine ET sur une page interne. Il n'y a donc aucun contenu
  duplique servi a Google, seulement des redirections, ce qui est exactement la categorie
  « Page avec redirection » de son email. `virginiedeconinck.netlify.app` (l'autre orthographe)
  n'existe pas : 404.
- **`/shbg` A BOUGE depuis le 02/08, contrairement a ce que dit le SKILL.** 4 commits (26/08 et
  01/09). MAIS les 4 lignes de references sont **identiques a l'octet pres** entre `41af613`
  (02/08) et HEAD : memes 4 DOI, memes effectifs, memes revues. La verification du 02/08 tient
  donc toujours. **Le bon controle n'est pas « le fichier a-t-il bouge » mais « le bloc de
  references a-t-il bouge »** : diff cible sur les lignes DOI, pas `git log` du fichier.
- ⚠️ **CORRIGE le 07/09 a 07h30 : la note precedente sur le « nettoyage virgule avant et » etait
  FAUSSE sur le fond ET citait une phrase inexistante.** Elle affirmait que 73 retraits etaient
  fautifs « la ou les deux propositions ont des sujets differents ». Regle de Virginie relue a la
  source (`rcf-regles-redaction.md`, 01/09), verbatim : « **La regle est absolue, y compris quand
  la grammaire l'autoriserait (deux propositions a sujets differents)** ». Ces retraits sont donc
  CORRECTS, il n'y a rien a defaire. Mesure du 07/09 : le lot `e53c41d` a touche **164 phrases**
  sur 23 pages plus llms.txt (et non 195/230).
  **La phrase donnee en exemple, « C'est une conversation, pas une liste et elle se tient avec
  votre dermatologue », n'est PAS sur le site** : le mot « conversation » y apparait UNE fois, dans
  la politique de confidentialite, sur un sujet sans rapport. Cette phrase est citee dans la
  MEMOIRE comme un exemple que Virginie avait releve le 01/09, et elle a ete reecrite depuis. Le
  passage precedent l'a lue dans la memoire et l'a annoncee « lue sur la page en ligne ».
  **C'est la faute du substitut prise en flagrant delit : lire une note et l'annoncer comme une
  page chargee.**
- ✅ **Ce qui reste vrai, et c'est le seul reste :** la seconde branche de la regle (« quand la
  phrase devient longue, on coupe avec un point ») n'a pas ete appliquee. Mesure du 07/09 sur les
  pages actuelles, avec les signes que Virginie ecrit elle-meme (enumeration de plus de trois
  elements, deux « et » dans la meme phrase, chute en « pas ceci, pas cela ») : **8 phrases** de
  30 mots et plus portent au moins deux de ces signes. 3 sur `/perimenopause`, 2 sur `/peptides`,
  1 sur `/biohacking-feminin`, 1 sur l'article estrobolome, 1 sur la page RGPD (enumeration
  juridique, noindex, a laisser). **REJUGE le 14/09 : ce sont des ENUMERATIONS, lisibles telles
  quelles ; les couper au point les abimerait.** Le seul vrai defaut cree par le retrait des
  virgules, c'est le « X et Y et Z » ou le lecteur ne sait plus ce qui va avec quoi : 3 phrases
  (`/collagene-peau` microbiote, `/shbg` testosterone/oestradiol, `/inflammaging` CRP), reparees
  par une parenthese ou un point sur `optim-2026-09-14`. Chantier CLOS, ne plus le rouvrir.
- ⚠️ **`/peptides-longevite-feminine` dit DEUX FOIS la meme chose** (verifie sur la page en ligne
  le 07/09). « Le geste sous-cutane se ressemble, mais l'analogie ne va pas plus loin : l'insuline
  est un medicament approuve, dose et controle, tandis que les peptides... » et, plus loin, « Le
  geste sous-cutane ressemble a celui que les femmes diabetiques pratiquent pour l'insuline, mais
  l'analogie s'arrete la : une insuline est un medicament approuve, dose et controle, alors que
  les peptides... ». Meme comparaison, memes trois enjeux (purete, sterilite, dosage), deux fois.
  **REJUGE le 14/09 : ce n'est PAS un defaut.** La seconde occurrence est la REPONSE FAQ (ligne
  371, miroir JSON-LD ligne 73). Une reponse de FAQ se lit seule, par Google comme par une
  lectrice qui saute au bloc : elle doit redire le point. Fusionner casserait la FAQ. CLOS.

## Audit du lundi 07/09/2026 (run cloud 34109421105, 10h04 UTC)

- **Site : 0 erreur, 0 point a optimiser.** 21 pages, 29 liens, 6 images, 8 crawlers IA en 200.
- **Les 6 « formules de remplissage » sont 6 FAUX POSITIFS**, chaque phrase ouverte sur la page
  en ligne. « Le muscle squelettique est bien plus qu'un tissu contractile », « Le collagene :
  bien plus qu'une proteine de beaute » (c'est un H2), « bien plus qu'une liste appliquee telle
  quelle » (comparatif normal), « au coeur de tout ce que je fais » (bloc de voix). **Ce detecteur
  n'a jamais produit un seul vrai positif en 3 passages (17/08, 07/09).** A envisager de le
  retirer du moteur plutot que de le relire chaque semaine.
- **Les 3 DOI « non tranches (HTTP 429) » EXISTENT tous les trois**, reinterroges le 07/09 :
  10.1111/j.1471-0528.1987.tb02338.x (Brincat, BJOG 1987, collagene cutane et menopause),
  10.2337/dc23-1630 (Diabetes Care 2024), 10.3390/biom16081136 (Biomolecules 2026, DAO).
  Le 429 de Crossref est passager, il ne dit rien sur la reference. **Piege d'outil rencontre en
  chemin : le resume Crossref contient des caracteres de controle, `json.loads` echoue en mode
  strict et fait croire a un DOI mort. Toujours parser avec `strict=False`.**
  **Detecteur de « formules de remplissage » : corrige dans le moteur le 14/09 (`955815d`).**
  « au cœur de » et « bien plus qu'un » retires (4 passages, 0 vrai positif), et un bug trouve
  en chemin : la liste comparait des tics ACCENTUES a un texte DESACCENTUE, six formules ne
  pouvaient jamais sortir. Version corrigee mesuree sur les 21 pages : 0 alerte.
- **Les 4 references de l'article melasma (01/09) confrontees a leur resume Europe PMC : justes.**
  Les chiffres « 36,4 % a 75 % » et « jusqu'a 30 % persistent, parfois dix ans plus tard » sont
  VERBATIM dans le resume de CCID.S488663. Les deux travaux IJMS disent bien ce que la page leur
  fait dire, sur la bonne nature de preuve (revue, puis cellules et peau). **Une seule reserve :
  la page attribue aux auteurs de DSS.0000000000005032 « les donnees se composent essentiellement
  de cas rapportes » ; le resume public dit « poorly researched » et ne montre pas cette phrase.
  Le fond est juste, l'attribution precise n'est pas verifiee.**
- ⚠️ **HYPOTHESE FAUSSE, corrigee par la mesure : /histamine-perimenopause NE decroche PAS.**
  Le rapport montrait la requete « histamine perimenopause » passant de la position 7.4 a 10.6 et
  j'ai cru a une regression de la page. Mesure GSC semaine par semaine sur 8 semaines : la PAGE
  tient entre 6.1 et 7.3 sans tendance, et ses impressions montent de 34 a 70. **Une position de
  requete sur 11 impressions est du bruit ; seule la position de la PAGE se lit.**
- **Les -16 % de clics ne sont pas un probleme de contenu.** Ils viennent de la requete de marque
  « virginie deconinck », 94 -> 64 impressions. Les impressions de sujet, elles, montent de 19 %.
- **Maillage : 0 orpheline, 0 sous-maillee.** Sur les 25 « occasions manquees », 10 pointent vers
  le seul article melasma : appliquer ce lot ferait entrer 10 liens d'un coup vers un article a
  17 impressions, exactement le remaniement que Google lit comme du bruit. Ne pas le faire.
- **/shbg : 76 impressions, 0 clic, position 8.2.** Formellement au-dessus du seuil, mais a cette
  position 76 impressions donnent 1 a 2 clics attendus : **0 est dans le bruit, ce n'est pas la
  preuve d'un mauvais titre.** Le seul manque reel et verifiable : le titre ne contient pas le mot
  « femme », present dans 3 des 5 requetes qui l'amenent (« shbg elevee femme », « shbg femme »,
  « shbg eleve femme »). Rien d'autre a y toucher. **Depasse le 14/09 : 131 impressions, 0 clic,
  le titre est prepare (voir audit du 14/09).**

## Audit du lundi 14/09/2026 (run cloud 34809323010, lance a la main a 05h21 UTC)

- **Pourquoi un run a la main** : a 07h20 Luxembourg le passage planifie n'etait pas parti (il
  part entre 09h et 10h30 UTC, mesure sur 6 jours). `workflow_dispatch` calcule les 4 rapports sur
  les memes 28 jours GSC et le meme site, sans email. L'email planifie du lundi arrive ensuite
  avec les memes chiffres. Aucun recalcul local.
- **Site : 0 erreur, 0 point a optimiser.** 21 pages, 29 liens, 6 images, 8 crawlers IA en 200.
  Rendu regarde a 375 px et desktop (accueil, histamine, article melasma) : aucun debordement,
  images chargees. Les 9 a 11 px mesures sont les surtitres capitales espacees, voulus.
- **AUCUNE page HTML n'a bouge depuis le 07/09** (`git diff --stat 7d21408..HEAD` vide).
- **LES 19 DOI DU SITE SONT MAINTENANT TOUS VERIFIES A LA SOURCE, resume contre affirmation :**
  4 `/shbg` (02/08, bloc DOI identique a l'octet), 4 melasma (07/09), 1 `/glp1` (01/09), et les
  **10 restants ouverts le 14/09 sur Europe PMC** : Kendall 2022 (7+11+10 femmes, keratinocytes),
  Pordab 2026 (38 femmes 40-61, 28 tirees au sort 12 semaines, 5 en echographie 8 semaines, plus
  de rougeurs a 0,247 %), He & Zhuo 2026 (revue, « shortage of rigorous human studies »),
  Brincat 1987 (69 non traitees + 37 sous hormones, collagene de la cuisse), Wang 2026 (in vitro
  et sous-cutane, topique a demontrer), Janus 2026 (revue, modeles in vivo), Hwang 2026
  (pharmacologie de reseau + toxicite dose unique rat), Lei 2026 (heterogeneite, petits
  effectifs), Zybul 2026 (DAO muqueuse contre circulante, limites du dosage serique), Valerieva
  2026 (mastocytes, permeabilite vasculaire, recommandations peri/post-menopause absentes).
  **Chaque description de source sur les pages dit ce que le resume dit.** Une seule nuance non
  tranchable sans le texte integral : sur `/regeneration-cellulaire`, « exploratoire » est
  attribue au volet echographique de Pordab ; dans le resume, le mot suit les resultats du volet
  tape-stripping (IL-1). Les deux volets font 5 femmes. Ne rien changer sur la foi d'un resume.
- **`/shbg` : 131 impressions, 0 clic, position 7,6.** La semaine derniere 76/0/8,2, « dans le
  bruit ». A 131 impressions en position 7,6, 3 a 4 clics etaient attendus : 0 ne l'est plus.
  Requetes reelles : « shbg elevee femme » 15, « shbg femme » 6, « shbg eleve femme » 6, et le
  titre ne contenait pas « femme ». **Prepare sur `optim-2026-09-14` (`9df4767`)** : « SHBG
  elevee chez la femme : ce que dit votre prise de sang » (58 car.), title + og + twitter +
  headline ensemble, dateModified/lastmod/date visible passes au 14/09. « ou basse » sort du
  titre (2 impressions sur « shbg faible femme »), reste dans la description. ATTEND « publie ».
- **Estrobolome : 103 impr., 1 clic, pos 9,1, « estrobolome definition » 48 impr.** Le titre est
  deja une definition ; a cette position 1 a 2 clics sont attendus. Rien a toucher.
- **Maillage : memes 25 occasions que le 07/09, 10 vers melasma.** Meme decision : non.
- **GEO : « est-ce que les soins dits regenerant cellulaire ont des preuves scientifiques ? »
  5 impr. en position 8,8**, c'est la seule question GEO deja a portee. `/regeneration-cellulaire`
  y repond en corps de texte ; un H2 mot pour mot est le geste GEO classique. Pas fait ce jour :
  un H2 de plus sur une page qui va bien est un remaniement, a decider avec Virginie.
- **Instagram dans Search Console : aucun CSV dans `~/Downloads` le 14/09.** A lui demander.
- **Piege local repare : `main` local avait diverge** (commit `35e6605`, doublon de `61f9f08`
  avec d'autres mots dans les commentaires, jamais pousse). Remis sur `origin/main`, le doublon
  garde sous la branche `stale-main-35e6605`. Toujours `git fetch` puis comparer avant d'ecrire.

## AUDIT RÉEL DES 21 PAGES, soir du 14/09/2026 (demandé par Virginie : « pas un audit par sondage »)

**Méthode, à reproduire chaque lundi (elle est dans le SKILL depuis ce soir) :** Chrome headless piloté
par DevTools (`scratchpad/capture.mjs`, à recréer au besoin : `Emulation.setDeviceMetricsOverride`
375x812 DPR 2 puis 1280x800, `.reveal` forcé visible, transitions coupées, `captureScreenshot` par
tranches de 1568 px). 280 captures relues, `innerText` des 21 pages lu de la première à la dernière
lettre. Plus un détecteur de conflits CSS (`cssclash.mjs` : classe déclarant un font-size dont
le calculé diffère). **Ce que le rapport du matin appelait « rendu regardé » (3 pages) n'avait rien
vu de ce qui suit.** **PUBLIÉ le 14/09 à 21h07 sur « correction alors. Fais-le. » de Virginie**, après lui avoir montré
4 panneaux avant/après (`~/Downloads/audit-site-14-09/`). Fusion `ea04dcf`, déploiement Netlify
`ready`, relu EN LIGNE : bloc de voix pleine largeur à 375 px, scores DunedinPACE à 36 px, titre
SHBG servi, 0 conflit CSS sur les 21 pages, 0 « transition hormonales ». Run cloud post-déploiement
34885410265 : 0 erreur, 0 point à optimiser, audit 0 point à corriger (le détecteur de tics ne crie
plus). **Réserve dite à Virginie** : l'espace ajouté sous le bandeau noir est un jugement de mise en
page, pas une casse ; si elle le préfère collé, on le retire.

- **Le bloc de voix (bandeau noir, disque, citation) était illisible sur iPhone sur les 16 pages
  piliers.** Section inline `padding:48px 80px` + grille `80px 1fr` gap 40 : colonne de texte de
  95 px, la citation en 20 lignes de trois mots, depuis le 15/06. Personne ne l'a vu en trois mois
  parce que personne n'a ouvert une page pilier à 375 px jusqu'en bas du bandeau.
- **`.content` avait `padding-top:0` depuis le premier commit** : le H2 collait au bandeau noir,
  desktop et mobile. Le bandeau a été ajouté après, personne n'a réajusté.
- **`.article p` écrasait 14 classes** (spécificité 0,1,1 contre 0,1,0) : scores DunedinPACE
  dessinés à 36 px rendus à 15 px, noms d'horloges à 13 px (plus petits que le texte courant),
  étiquettes à 13-15 px au lieu de 9. Sur toutes les pages à cartes.
- **Accueil, témoignages : carrousel de 215 px sur 375** (section inline `padding:120px 80px`).
- **Texte, 16 corrections**, les plus lourdes : `/perimenopause` portait trois vestiges d'un
  remplacement automatique périménopause → transition hormonale (« La transition hormonale est la
  période de transition hormonale », « symptômes de transition hormonales » x2, FAQ + JSON-LD) ;
  `/shbg` et `/nad` répétaient mot pour mot leur phrase d'intro dans le bloc de voix juste dessous ;
  `/shbg` disait « 1 à 3 % » puis « 1 à 2 % » dans le même paragraphe et sa référence Hammond
  n'avait ni revue ni DOI (J Endocrinol 2016, 10.1530/JOE-16-0070) ; `/glp1` prêtait à Neeland
  « non toxique » là où le résumé dit « adaptive » ; la FAQ de `/cellules-senescentes` parlait
  « d'essais cliniques publiés » pour un essai exploratoire de 13 participants ; l'accueil disait
  « 1 à 2 % par an dès 25 ans » contre « environ 1 % dès la vingtaine » sur `/collagene-peau` ;
  temps de lecture mélasma 8 min sur la carte, 7 sur l'article ; l'article glycémie affichait
  Août 2026 alors que la carte et `datePublished` disent juin.
- **Vérifié en local avant de proposer** : 0 conflit CSS restant, 104/104 réponses FAQ identiques
  à leur miroir JSON-LD, JSON-LD valides, captures mobile et desktop relues sur 4 pages corrigées.
- **Pas touché, à décider par Virginie** : les 4 pages sans bloc de sources qui citent quand même des études
  (`/peptides` Leyden 2002 = résumé de congrès, `/nad`, `/cellules-senescentes`, `/muscle`,
  `/age-biologique`) ; les pieds de page différents entre l'accueil et le reste ; l'ordre des cartes
  du blog (sept, août, juin, juillet). « 20K+ » sur l'accueil : 25 982 abonnés mesurés à l'API
  Instagram le 14/09, le chiffre reste vrai.
- **Ce qui n'est PAS un défaut, pour ne pas le rouvrir** : les gros espaces après les points dans
  les paragraphes (c'est la fonte Didact Gothic, espace de 6,8 px à 16 px, source à un seul
  espace) ; les 9-11 px mesurés sur les surtitres capitales ; la réponse FAQ de `/peptides` qui
  redit le corps (une FAQ se lit seule) ; l'image `leviers-hero` « cassée » en headless mobile
  (charge en 1 s dans le vrai navigateur, lazy-loading).
- **Externe revérifié le 14/09** : rétatrutide TRIUMPH-1 (2 339 participants, 28,3 % à 80 semaines,
  21/05/2026) et orforglipron (FDA, 01/04/2026), tels que `/glp1` les cite.

## Publication du 20/09/2026 (hors cycle, demande de Virginie, « publie » à 07h46)

- **Perte musculaire par décennie : « 3 à 5 % » → « 3 à 8 % »**, aligné sur la formation RCF
  (`piliers-rcf/espace-prive/protocole-1.html` et son miroir autoguidé, lus à la source : « À partir
  de 35 ans, une femme perd en moyenne 3 à 8 % de sa masse musculaire par décennie »). 4 occurrences,
  les seules du site (grep des 21 pages) : `/glp1` x3 (JSON-LD FAQPage, corps, FAQ visible, changées
  ENSEMBLE) et `/muscle-longevite-feminine` x1. `dateModified` + `lastmod` au 2026-09-20 sur les deux.
- **NON touché, sur consigne de Virginie : « jusqu'à 1 à 2 % par an après la ménopause » sur `/glp1`.**
  Pas vérifié dans cette recherche, à contrôler séparément si besoin. Compté intact : 3 avant, 3 après.
- **Limite dite** : la source classique du chiffre (Volpi 2004, PMID 15192443) n'a pas pu être ouverte
  en texte intégral, son résumé Europe PMC ne porte pas le chiffre. Correction fondée sur la cohérence
  avec la formation, pas sur une lecture de l'article.
- Fusion `d6a8e73`, Netlify `ready`, les deux pages relues EN LIGNE (0 « 3 à 5 », FAQ 4/4 et 5/5
  concordantes avec le JSON-LD, sitemap au 20/09). Run cloud post-déploiement 35492553743 : 0 erreur,
  0 point à optimiser. Aucune capture d'écran : changement d'un chiffre dans une phrase, pas de mise en page.

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
**Note du 20/09/2026 (filet quotidien) :** le run du 19/09 mesure « valide encore 4 jours, expire le
24/09 ». Le moteur ouvre une Issue à `jours < 3`, donc le 22/09 et le 23/09 SI OVH n'a pas encore
repoussé la date (OVH renouvelle dans la semaine qui précède). Conduite à tenir ce jour-là, sans
rouvrir le sujet : interroger RDAP (`curl -s https://rdap.org/domain/virginiedeconinck.com`) ; si
l'expiration est passée à 2027, l'Issue est périmée, proposer sa fermeture en une ligne ; si la date
n'a pas bougé le 23/09 au soir, c'est le SEUL cas où l'on alerte Virginie. Tout ça est dans le
rapport de surveillance d'hier, rien n'a été recalculé ici.
**21/09/2026, 19h41 :** l'Issue #9 s'est ouverte au run de 10h34 UTC (2,86 jours arrondis à 2). RDAP registre
(Verisign) ET registrar (OVH) interrogés à 17h41 UTC : expiration toujours au 24/09/2026 09h21, pas encore
renouvelé, statuts normaux (delete/transfer prohibited), DNS OVH intacts. Remonté à Virginie avec la seule
preuve qui compte : l'état du renouvellement automatique dans son espace OVH. Le moteur rouvrira une Issue
le 22 et le 23/09 tant que la date n'a pas bougé : c'est le filet voulu, pas une panne.
**21/09, 19h55 : RENOUVELÉ CÔTÉ OVH.** Capture de l'espace client envoyée par Virginie : « Date d'expiration
24 sept. 2027 », fréquence « tous les ans », statut Enregistré / Actif. Le registre Verisign, réinterrogé à
17h55 UTC, affiche ENCORE 2026 : OVH pousse la commande au registre à l'échéance, pas avant. Donc les
Issues des 22-23/09 seront des faux positifs à fermer sans un mot ; ne rouvrir que si le registre
affiche toujours 2026 le 25/09.
**23/09/2026 : LE MOTEUR EST CORRIGE, sujet clos pour de bon (commit `5215059`, fusionne sur `main`
sur « publie » de Virginie).** Les Issues #9, #10 et #11 (21, 22, 23/09) etaient TROIS fausses alertes
d'affilee pour la meme cause, et les runs passaient en rouge avec elles : trois emails par jour pour
un domaine qui va bien. Cause de fond : le moteur lit le REGISTRE (RDAP Verisign), or OVH ne lui pousse
le renouvellement qu'a l'echeance. Avant l'echeance, le moteur ne peut donc PAS distinguer un domaine
renouvele d'un domaine abandonne, et tout seuil positif fabrique du bruit garanti, plusieurs jours de
suite, une fois par an. Seuil passe de `jours < 3` a `jours < 0` (expiration reellement depassee et non
repoussee), message reecrit (il affirmait « le renouvellement automatique n'a pas eu lieu », ce qu'il ne
mesurait pas). Simule sur les vraies dates : rien les 21 au 24/09, alerte le 25/09 seulement si OVH n'a
pas paye, rien une fois la date a 2027. Run de controle 35847610678 : 0 erreur, 0 point a optimiser.
Les 3 Issues fermees avec l'explication. **Ne jamais remettre de seuil positif sur ce controle.**

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

## Filet quotidien du 24/09/2026 (05h20 UTC) : le jour J de l'echeance du domaine

Les trois controles du filet sont normaux : dernier run termine **success** (35847610678, run de
controle du 23/09 a 10h14 UTC, il y a 19 h), **0 Issue ouverte**, accueil charge en 200 avec son
contenu reel (title servi, 1 seul H1 « Virginie Deconinck », canonical, `index, follow`,
« Mis a jour en septembre 2026 »). Pas de rattrapage editorial : `nextPlanned` = 2026-10-01.
`choix-sujet-article-mensuel` est armee et part aujourd'hui a 06h39 UTC : le sujet d'octobre se
decide avec Virginie ce matin, ce n'est pas mon travail. Rien remonte a Virginie, comme prevu.

⚠️ **Prevision a verifier demain, PAS une alerte : aujourd'hui est le jour exact de l'echeance.**
RDAP interroge a 05h21 UTC, registre Verisign ET registrar OVH : expiration **2026-09-24T07:21:11Z**,
soit 09h21 Luxembourg, toujours en 2026, statuts normaux. Or le run planifie part entre 09h et
10h30 UTC, donc **apres** l'heure d'expiration. Avec le seuil corrige hier (`jours < 0`), si OVH n'a
pas encore pousse le renouvellement au registre a cette minute-la, le moteur mesurera une expiration
depassee et ouvrira une Issue : ce serait la **4e fausse alerte** du meme mecanisme, le domaine etant
renouve chez OVH (capture de son espace client du 21/09 : « Date d'expiration 24 sept. 2027 »,
statut Enregistre / Actif).
**Conduite a tenir demain, sans rouvrir le sujet avec Virginie :** reinterroger RDAP. Si le registre
affiche 2027, l'Issue eventuelle est perime, on la ferme sans un mot. Si le registre affiche ENCORE
2026 le 25/09, c'est le seul cas ou on alerte.
**Correctif du moteur volontairement NON fait aujourd'hui.** La grace a ajouter serait d'attendre
24 h apres l'expiration avant d'alerter (le temps que le registrar pousse au registre), jamais un
seuil positif. Mais je ne corrige pas sur une hypothese : si l'Issue s'ouvre ce matin, la mesure
existe et on propose la grace demain ; si elle ne s'ouvre pas, le moteur est bon et il n'y a rien
a faire. Fabriquer l'optimisation avant la mesure, c'est exactement ce que la section 4 interdit.

## Filet quotidien du 25/09/2026 (11h42 UTC) : la prevision d'hier s'est realisee

- **Issue #12 (24/09, run 35983537418) = 4e fausse alerte domaine, PERIMEE.** RDAP Verisign
  interroge a 11h42 UTC : expiration **2027-09-24**, « last changed » **2026-09-25T08:06:40Z**.
  Le registre a donc ete mis a jour **25 h apres** l'echeance (24/09 07h21 UTC). Run du jour
  36122054899 : success, 0 erreur, 0 point a optimiser, « valide encore 363 jours ». Accueil charge
  a 11h42 UTC : title, H1 « Virginie Deconinck », « Mis a jour en septembre 2026 ».
- **Correctif prepare sur `optim-2026-09-25` (`3569e45`), ATTEND « publie »** : alerte seulement
  48 h apres l'echeance REELLE (heure comprise ; la date etait tronquee au jour, donc le moteur criait
  des minuit le jour J). Simule sur les vraies dates : rien le 24/09 ni le 25/09 matin, alerte le 26/09
  si le registre n'a pas bouge. Fermeture de l'Issue #12 proposee a Virginie, pas faite.
- `automation/cycle-log.json` porte une modification NON commitee (sujet d'octobre « Sommeil »,
  valide le 24/09 par une autre session). Pas touchee, pas commitee par moi : a la session du sujet.
