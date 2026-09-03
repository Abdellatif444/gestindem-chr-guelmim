# Audits D (cohérence mécanique) et E (graphiques) — 2026-09-03

Objectif : vérifier **objectivement** la cohérence du design entre les 24 planches et la conformité des graphiques aux règles `dataviz`, sans jugement de goût. Outils : `verifier_coherence.py` (script maison, rejouable) et le catalogue d'anti-patterns de la skill `dataviz`.

## Audit D — cohérence mécanique

### 1. Éléments corrects (après correction)
- **Palette** : 48 couleurs utilisées, 0 hors palette documentée (49 tokens dans la planche Identité + tokens sémantiques).
- **Barre latérale** : 1 seule variante sur les 22 écrans qui en ont une (après neutralisation de l'élément actif).
- **Barre supérieure** : 2 variantes — la seconde est **voulue** (Plannings n'a pas de sélecteur de période global, décision F-02 de l'audit UX).
- **Champs de formulaire** : 1 signature de style.
- **Badges de statut** : 4 signatures = exactement les 4 familles sémantiques (attente, ok, neutre, rejet), mêmes valeurs partout.
- **Boutons secondaires** : 1 signature (Identité incluse).

### 2. Problèmes détectés et gravité
| # | Constat | Gravité | Preuve |
|---|---|---|---|
| D-01 | L'icône « Structures » de la barre latérale du tableau de bord avait un tracé de plus que sur les 21 autres écrans | Gêne (cohérence) | hash de sidebar distinct pour `Main` |
| D-02 | Boutons primaires à **13,5 px** sur les 5 écrans Validation, 13 px ailleurs | Gêne | 4 signatures de police |
| D-03 | Badges du tableau de bord avec un style `inline-flex` propre à cet écran | Gêne | 3 signatures supplémentaires sur `Main` |
| D-04 | 3 couleurs hors palette : `#F2DDBB` (bordure bandeau Barèmes), `#F4F3EF` (chip du 13/08, ancien fond chaud), `#8A968F` (bouton désactivé, ancien gris) | Gêne | tableau 1 du lint |
| D-05 | Tailles sous 12 px : chips du calendrier (11,5), sous-titre sidebar (11), « AUJOURD'HUI » (9,5), compteur de cloche (10), libellés hex de l'Identité (11,5), logins Administration (11,5) | Ralentit (lisibilité, règle F-06) | tableau 2 du lint |
| D-06 | Hauteurs de boutons primaires variables (38 / 40 / 42 / 48) sans règle écrite | Gêne | signatures |

### 3. Corrections appliquées
- D-01 icône unifiée · D-02 police 13 px partout (15 px conservé sur l'écran de connexion, seul CTA plein écran) · D-03 badges de `Main` alignés sur le composant commun · D-04 les 3 couleurs remplacées par leurs tokens (`#F1D9B4`, `#ECF1EE`, `#66746D`) · D-05 plancher 12 px appliqué (11 px conservé pour les libellés en capitales et le compteur numérique de la cloche) · D-06 règle écrite dans la planche Identité : **38 px en barre d'outils, 42 px en pied de panneau, 48 px connexion**.
- Résidu accepté : le bouton primaire garde 2 signatures à 13 px — avec et sans icône (`display: flex; gap`) — c'est une variante fonctionnelle, pas une dérive.

### 4. Ce que ce script apporte pour la suite
C'est l'équivalent maquette d'un **linter** : rejouable après chaque modification (`python verifier_coherence.py`), il transforme « ça a l'air cohérent » en « 0 couleur hors palette, 1 variante de sidebar ». En WPF, le même contrôle sera fait par un analyseur XAML (couleurs uniquement via `StaticResource`).

## Audit E — graphiques (règles `dataviz`)

Graphiques examinés : tableau de bord (barres empilées 6 mois, tendance 6 mois, répartition), Statistiques (courbes 2026 vs 2025, comparaison structures, répartition par type, services les plus coûteux).

### 1. Éléments corrects
- **Une seule échelle par graphique**, jamais de double axe.
- **Légende présente dès 2 séries** et libellés directs en fin de courbe (« 2026 · 184 k », « 2025 · 171 k ») : l'identité n'est jamais portée par la couleur seule.
- **Palette catégorielle validée** (daltonisme, contraste) pour les 4 types ; texte des valeurs en encre, pas en couleur de série.
- Traits fins (2–2,2 px), grille discrète, marqueurs ≥ 8 px, chiffres tabulaires.
- Courbe avec axe débutant à 120 k : acceptable pour une courbe d'évolution (l'anti-pattern « axe tronqué » vise les barres).

### 2. Problème détecté
| # | Constat | Gravité | Règle |
|---|---|---|---|
| E-01 | Le **vert du type « Garde »** (`#0A8467`) servait aussi de couleur à la série « 2026 », à la tendance 6 mois du tableau de bord et aux barres « par structure » / « par service » — sur la même page que la répartition par type, un lecteur peut croire que ces courbes ne concernent que les gardes | Ralentit (lecture faussée) | `dataviz` : « la couleur suit l'entité ; les couleurs réservées ne sont jamais réutilisées pour une autre série » |

### 3. Correction appliquée
- Séries uniques et temporelles passées en **primaire `#10554A`** (courbe 2026, point, libellé, légende, tendance du tableau de bord, 9 barres structures/services). Le vert `#0A8467` ne désigne plus que le type Garde. Règle ajoutée à la planche Identité.

### 4. Non évaluable sur maquettes
Info-bulles au survol, mise en évidence d'une série au passage de la souris, vue « tableau » des données (à prévoir dans WPF : `dataviz` demande une alternative tabulaire pour l'accessibilité).

## Éléments nécessitant une validation humaine
- Aucune décision de design en suspens pour D et E : toutes les corrections sont des mises en conformité avec des règles déjà validées (Identité, F-06, `dataviz`).
- Une seule question de fond, hors périmètre de ces audits : le CHR veut-il des **info-bulles et une vue tableau** sur les graphiques (recommandé par `dataviz`) — à confirmer lors de la démo.
