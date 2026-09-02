---
name: parcours-walkthrough
description: "Évalue un parcours utilisateur multi-écrans (scénario complet, pas un écran isolé) par la méthode du cognitive walkthrough (Wharton, Rieman, Lewis & Polson) : à chaque action, l'utilisateur sait-il quoi faire, voit-il l'action, comprend-il qu'elle est la bonne, reçoit-il un retour clair ? Utiliser cette skill dès que l'utilisateur parle de parcours, scénario, flux, enchaînement d'écrans, transitions, navigation entre pages, « ce qui se passe après une action », points de blocage ou de confusion, intuitivité pour un nouvel utilisateur, walkthrough, user flow, user journey, task flow — même s'il ne nomme pas la méthode. Entrées : captures d'écran des maquettes + carte des parcours (Mermaid). Ne pas utiliser pour auditer un écran seul (voir ux-audit) ni pour l'accessibilité technique (voir accessibility-audit)."
---

# Parcours walkthrough

Un audit d'écran dit si une page est bien faite. Un walkthrough dit si **une personne qui ne connaît pas l'application arrive au bout de sa tâche** en passant d'un écran à l'autre. On simule un utilisateur précis, avec un objectif précis, et on l'accompagne action par action en posant toujours les mêmes quatre questions. Les réponses négatives sont les points de confusion ou de blocage ; les actions dont le résultat n'est visible nulle part sont les états manquants.

Cette méthode est faite pour les maquettes : elle n'a besoin ni de code ni d'utilisateurs réels, seulement des écrans et d'un scénario. C'est ce qui la rend précieuse avant le développement — chaque blocage trouvé ici coûte dix fois moins qu'après.

## Entrées

1. **Les captures** des écrans (PNG), un fichier par écran. Si elles n'existent pas, les produire comme dans `ux-audit` (rendu des `.dc.html` avec un navigateur headless) — ne jamais évaluer un écran de mémoire.
2. **La carte des parcours** : un diagramme Mermaid où chaque flèche est une *action* et chaque nœud un *écran ou un état visible*. Format et exemple dans `references/carte-parcours.md`. Si elle n'existe pas, l'écrire d'abord à partir des captures et la faire relire : **rédiger la carte est la première évaluation** — une action dont on ne sait pas dessiner la destination est déjà un constat.
3. **Les scénarios** : pour chacun, un utilisateur type (rôle, niveau de familiarité), un objectif formulé en une phrase, et la séquence d'actions correctes attendue. Si l'utilisateur n'en donne pas, les proposer à partir du cahier des charges et **attendre sa confirmation** — la sévérité des constats dépend entièrement de l'objectif choisi.

## Procédure

### 1. Préparer
- Lister les écrans et lire la carte. Vérifier que chaque scénario est réalisable avec les écrans fournis ; sinon, noter les écrans manquants comme constats de type `ECRAN-ABSENT` avant même de commencer.
- Pour chaque scénario, décomposer la séquence d'actions correctes en étapes atomiques (un clic, une saisie, un choix). Une étape trop grosse (« saisir la garde ») cache des questions ; la découper (« ouvrir le formulaire », « choisir l'agent », « choisir le type », « valider »).

### 2. Parcourir (le cœur de la méthode)
Pour **chaque étape** de chaque scénario, regarder la capture de l'écran courant et répondre aux quatre questions de `references/questions-walkthrough.md` :

| # | Question | Ce qu'elle mesure |
|---|---|---|
| Q1 | L'utilisateur essaiera-t-il d'obtenir le bon effet ? | Sait-il **quoi faire** à ce moment ? |
| Q2 | Verra-t-il que l'action correcte est disponible ? | L'action est-elle **visible** ? |
| Q3 | Associera-t-il l'action correcte à l'effet voulu ? | Le libellé/l'icône dit-il **que c'est la bonne** ? |
| Q4 | Après l'action, verra-t-il que ça a progressé ? | Le **retour** est-il clair et prévisible ? |

Répondre ✓ (oui, preuve visible), ✗ (non, avec ce qui manque) ou ? (pas décidable sur capture statique — le dire, ne jamais deviner). Chaque ✗ devient un constat. Se mettre réellement à la place de l'utilisateur type : un validateur qui ouvre l'application pour la première fois ne sait pas ce qu'est un « lot » tant que l'interface ne le lui a pas montré.

Q4 est celle qui rattrape ce que les audits d'écran ratent : elle oblige à chercher l'écran ou l'état **suivant**. S'il n'existe pas dans les captures, c'est un constat `RETOUR-ABSENT` — pas une supposition sur ce que le développeur fera.

### 3. Relever le niveau parcours
Une fois les étapes passées, regarder le scénario dans son ensemble :
- **Transitions** : le contexte survit-il au changement d'écran (période, structure, élément sélectionné) ? L'utilisateur retrouve-t-il ses repères (même position de la navigation, même vocabulaire) ?
- **Charge mémoire** : doit-il retenir quelque chose d'un écran à l'autre (un numéro de lot, un montant) sans qu'il soit rappelé ?
- **Vocabulaire** : un même concept a-t-il un seul nom d'un bout à l'autre ?
- **Fin de parcours** : le dernier écran dit-il clairement « c'est fait » et propose-t-il la suite logique ?
- **Sorties** : à chaque étape, peut-on annuler ou revenir sans perdre son travail ?

### 4. Classer et rédiger
- Sévérité sur l'objectif : **Bloquant** (l'utilisateur type ne finit pas), **Ralentit** (il hésite, se trompe puis se rattrape), **Gêne** (il finit mais note une incohérence). Pondérer par la fréquence de la tâche : une hésitation sur la saisie quotidienne pèse plus qu'un blocage sur un paramétrage annuel.
- Fusionner les constats identiques trouvés à plusieurs étapes en un seul, avec la liste des occurrences.
- Citer une preuve visible (écran + élément) pour chaque constat, et l'heuristique correspondante quand elle existe (Nielsen, Norman, Content) — cela rend le constat discutable sur des faits, pas sur des goûts.
- Rédiger avec `references/modele-rapport.md`. Le tableau « après chaque action, que voit l'utilisateur ? » est obligatoire : ses cases vides sont la liste des états à dessiner.
- Terminer par les trois corrections les plus rentables et proposer à l'utilisateur de trancher — la décision de corriger lui appartient.

## Ce qu'on ne fait pas

- Inventer le comportement d'un bouton dont le résultat n'est pas dessiné : on marque `?` ou `RETOUR-ABSENT`.
- Juger l'esthétique ou le détail d'un écran : c'est le travail de `ux-audit` et de `frontend-design`.
- Produire vingt constats mineurs pour remplir : huit constats prouvés, ancrés sur l'objectif, valent mieux.
- Oublier les points forts : noter ce qui rend le parcours fluide, pour le conserver et le reproduire dans les écrans suivants.
