# Audit C — accessibilité (WCAG 2.1 AA, sous-ensemble transposable à WPF) — 2026-09-03

Objectif : vérifier ce qui peut l'être **sur des maquettes** — contraste, tailles de cibles, libellés, information portée par la couleur seule, ordre de lecture, lisibilité — et lister explicitement ce qui ne pourra être vérifié que dans l'application WPF. Outils : `verifier_contrastes.py` (ratio WCAG calculé sur 68 paires texte/fond extraites des 24 fichiers), lecture des captures, grille de la skill `accessibility-audit` (4 principes). Cible : AA.

## Méthode et limites (règle « données indisponibles »)
- **Calculé** : contraste de chaque couleur de texte contre les fonds où elle apparaît (formule WCAG 2.x, luminance relative).
- **Observé** : cibles, libellés, couleur seule, ordre de lecture, cohérence de navigation.
- **Non évaluable ici** (à tester dans WPF, listé §5) : focus clavier, ordre de tabulation, lecteur d'écran (Narrateur / NVDA via UI Automation), zoom 200 %, mouvement.

## 1. Éléments corrects
- **Contraste (1.4.3 / 1.4.11)** : 68 paires testées, **0 échec** après correction — gris secondaire porté à `#5C6B64` (4,9:1 sur le fond `#ECF1EE`, 5,4:1 sur blanc), texte des jours hors mois relevé, wordmark bicolore réservé aux fonds sombres (4,6:1), or foncé `#8F6A1F` pour le titre sur fond clair (4,3:1, grand texte). Deux exemptions documentées : texte de bouton désactivé et flèches décoratives (`#AEB9B2`).
- **Couleur jamais seule (1.4.1)** : statuts = couleur + libellé ; types d'indemnité = pastille + lettre G/A/P + légende ; délais = chiffre ; doublon = bordure + icône + texte ; nœuds hors périmètre = cadenas + texte.
- **Libellés (3.3.2)** : tous les champs de formulaire ont un libellé visible permanent (Motif du rejet corrigé à l'audit UX). Erreurs identifiées avec cause et correction (import Excel, doublon).
- **Cibles (2.5.5)** : boutons 38–48 px de haut, lignes de tableau 37 px, chips 30 px, pager 30 px — tous au-dessus du plancher 24 px (desktop, souris).
- **Cohérence (3.2.3 / 3.2.4)** : navigation identique sur 22 écrans (vérifié mécaniquement, audit D) ; mêmes composants pour les mêmes fonctions.
- **Ordre de lecture (1.3.2)** : barre latérale → barre supérieure → titre → filtres → contenu → panneau de détail ; identique partout.
- **Lisibilité** : plancher 12 px (11 px en capitales espacées), chiffres tabulaires, espaces insécables.

## 2. Problèmes détectés

| ID | P | Critère | Écrans | Constat |
|---|---|---|---|---|
| C-01 | P1 | 1.4.3 | 22 écrans | Gris secondaire `#66746D` à **4,29:1** sur le fond de l'application (250 occurrences) — **corrigé** (`#5C6B64`) |
| C-02 | P2 | 1.4.3 | Planning ×3 | Jours hors mois en `#AEB9B2` à 2:1 — **corrigé** (`#5C6B64`, la cellule grise garde la distinction) |
| C-03 | P2 | 1.4.3 | Identité | « DEM » en or `#B98A2F` à 2,7:1 sur fond clair — **corrigé** (`#8F6A1F`, règle : bicolore sur fond sombre seulement) |
| C-04 | P2 | 2.5.5 | tiroirs, modales, barre supérieure | Icônes de fermeture (16 px) et cloche (19 px) sans zone de clic dessinée ≥ 24 px | 
| C-05 | P2 | 4.1.2 / 3.3.2 | 22 écrans | Champ de recherche identifié par son seul texte indicatif ; bouton « régénérer » (États) en icône seule — pas de nom accessible visible |
| C-06 | P1 | 2.4.7 | tous | **Aucun style de focus défini** dans la planche Identité avant cette itération — **corrigé** (règle ajoutée : contour 2 px `#10554A` décalé de 2 px) ; reste à implémenter |
| C-07 | P2 | 1.4.10 / 1.4.4 | tous | Maquettes à 1440 × 900 fixes ; comportement à 1366 × 768 (portables courants) et au zoom 125 % Windows non défini |
| C-08 | P3 | 1.3.1 | graphiques | Graphiques sans alternative tabulaire dessinée (recommandation `dataviz`) |

## 3. Priorité
- **P1** : C-01 (fait), C-06 (règle fixée, implémentation WPF).
- **P2** : C-02, C-03 (faits) ; C-04, C-05, C-07 (à traiter au développement — règles ci-dessous).
- **P3** : C-08.

## 4. Recommandations et corrections
- **C-04** : en WPF, zone de clic minimale 32 × 32 px sur toute icône interactive (`Padding` du bouton), même si le glyphe fait 16 px.
- **C-05** : `AutomationProperties.Name` sur tous les contrôles sans texte (recherche : « Rechercher un agent ou un lot » ; régénérer : « Régénérer le rapport ») + `ToolTip`. Règle à inscrire dans le guide de développement.
- **C-06** : `FocusVisualStyle` global dans `Theme.xaml` ; ordre de tabulation = ordre de lecture ; focus renvoyé au déclencheur à la fermeture d'un tiroir ou d'une modale ; Échap ferme.
- **C-07** : décision de résolution minimale (recommandation : **1366 × 768 à 100 %**, mise en page fluide au-delà ; tester 125 % de mise à l'échelle Windows). Le panneau de détail passe alors sous la liste, ou devient un tiroir.
- **C-08** : bouton « Voir les données » sous chaque graphique, ouvrant le tableau des valeurs (sert aussi à l'export).

## 5. Non évaluable sur maquettes — plan de test WPF
| Test | Outil | Quand |
|---|---|---|
| Navigation clavier complète des 3 scénarios (Tab, Entrée, Espace, Échap, flèches dans les listes) | manuel | fin de chaque module |
| Lecteur d'écran : structure, libellés, erreurs annoncées, modales | Narrateur Windows + NVDA (UI Automation) | fin de phase client |
| Zoom / mise à l'échelle 125 % et 150 % | Windows | fin de phase client |
| Contraste réel des rendus (anticrénelage) | Accessibility Insights for Windows (gratuit, Microsoft) | fin de phase client |

## 6. Validation humaine
- **Résolution minimale** et prise en charge de la mise à l'échelle (C-07) : décision à prendre avec le CHR selon le parc de postes.
- Lecteur d'écran : le cahier des charges ne l'exige pas explicitement ; recommandé d'en faire un critère de recette (postes publics, agents en situation de handicap).
