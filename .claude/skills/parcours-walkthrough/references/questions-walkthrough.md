# Les quatre questions du cognitive walkthrough

Source : Wharton, Rieman, Lewis & Polson, *The Cognitive Walkthrough Method: A Practitioner's Guide* (1994) ; version simplifiée de Spencer (2000). À poser dans l'ordre, pour chaque étape, en se mettant à la place de l'utilisateur type du scénario.

## Q1 — L'utilisateur essaiera-t-il d'obtenir le bon effet ?

Il ne s'agit pas encore de l'interface : est-ce que, à ce moment du parcours, l'utilisateur **pense** à faire ce qu'il faut ? Il y a un problème si le sous-objectif n'est pas évident (l'utilisateur ne sait pas qu'il doit d'abord ouvrir une période avant de saisir), si l'écran le pousse vers autre chose, ou si la tâche suppose une connaissance interne (« il faut vérifier avant de valider »).

- ✓ si l'écran rend le prochain sous-objectif évident (titre, étape courante, élément mis en avant, action primaire unique).
- ✗ si l'utilisateur doit savoir quelque chose que l'interface ne lui a pas dit.

## Q2 — Verra-t-il que l'action correcte est disponible ?

L'élément à actionner est-il **visible sans chercher** ? Problème s'il est masqué dans un menu, hors de la zone où l'utilisateur regarde, noyé parmi des éléments de même poids, ou s'il ne ressemble pas à quelque chose d'actionnable (Norman : signifiants).

- ✓ si l'action est dans le champ de vision naturel et ressemble à ce qu'elle est (bouton, lien, champ).
- ✗ si elle est cachée, ambiguë ou en concurrence avec d'autres actions de même poids.

## Q3 — Associera-t-il l'action correcte à l'effet voulu ?

Parmi les actions visibles, l'utilisateur choisira-t-il **la bonne** ? Problème si le libellé est vague (« Exporter » sans objet), si un autre élément semble tout aussi plausible, si l'icône seule porte le sens, ou si le vocabulaire n'est pas celui de l'utilisateur (Nielsen #2, Content #3).

- ✓ si le libellé dit ce qui va se passer, dans les mots du métier, et qu'aucun concurrent ne prête à confusion.
- ✗ si deux actions se ressemblent, ou si le nom de l'action ne correspond pas à ce que l'utilisateur veut obtenir.

## Q4 — Après l'action, verra-t-il que la tâche a progressé ?

Le **retour** est-il immédiat, visible et cohérent avec l'attente ? Problème si rien ne change visiblement, si le changement est ailleurs que là où l'utilisateur regarde, si le résultat n'est pas dessiné dans les maquettes, ou si le vocabulaire change entre l'action et son résultat (« Publier » → « Enregistré »).

- ✓ si l'écran ou l'état suivant existe dans les captures et montre sans ambiguïté que l'action a réussi (ou échoué, avec la cause et le remède).
- ✗ si le résultat n'est pas dessiné : constat `RETOUR-ABSENT`, jamais une supposition.
- ? si le retour est une animation, un délai ou un focus clavier — non évaluable sur image, à lister en fin de rapport.

## Rappels de calibrage

- Répondre du point de vue de **l'utilisateur type du scénario**, pas du concepteur. Un administrateur expérimenté et un agent de saisie le premier jour ne répondent pas pareil à Q1.
- Une réponse ✓ doit pouvoir pointer un élément précis de la capture. « Ça semble clair » n'est pas une preuve.
- Quand une étape cumule plusieurs ✗, le premier dans l'ordre Q1→Q4 est la cause ; les suivants sont souvent des conséquences.
