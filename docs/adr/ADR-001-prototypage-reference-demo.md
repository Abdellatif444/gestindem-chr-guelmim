# ADR-001 — Le prototype visuel (29 planches) est la référence de la démonstration et de l'interface WPF

- **Statut** : Accepté — 2026-09-03
- **Décideurs** : Yassine (chef de projet / développeur)
- **Format** : ADR (Architecture Decision Record, style MADR) — un fichier par décision structurante, jamais modifié après acceptation ; une décision ultérieure qui le contredit crée un nouvel ADR qui le « remplace ».

## Contexte

Le cahier des charges CDC-GESTINDEM-2026 impose une application Windows desktop couvrant 12 modules, et l'avis d'achat 43/2026/CHRG exige une **démonstration sous 48 h** conditionnant l'attribution, puis une livraison en 5 jours. Avant tout développement, nous avons choisi de prototyper l'intégralité de l'interface (décisions D2, D5) pour valider l'expérience utilisateur et disposer d'un scénario de démo.

Au 2026-09-03, le prototype compte **29 planches** (identité visuelle, 12 écrans de modules, 16 états : formulaires, confirmations, succès, vides, erreurs, rejet, plafond, notifications, restauration, fiche des droits). Il a passé **six audits** documentés dans `maquettes/audits/` et `maquettes/walkthrough/` :

| Audit | Méthode | Résultat final |
|---|---|---|
| Écrans (×2) | `ux-audit` — heuristiques citées, sévérité 0–4 | 0 critique, 0 majeur restant |
| Parcours (×2) | `parcours-walkthrough` — cognitive walkthrough, 3 scénarios | 8/8 constats résolus, 0 régression |
| Cohérence | `verifier_coherence.py` (lint) | 0 couleur hors palette, 0 taille < 12 px, 1 variante de navigation |
| Graphiques | `dataviz` | conforme (couleurs de type réservées aux types) |
| Accessibilité | `accessibility-audit` + `verifier_contrastes.py` | 69/69 paires de contraste conformes ; focus, cibles, noms accessibles reportés au développement |
| Traçabilité | matrice exigence → écran | 42/42 exigences maquettées, 5 partielles secondaires |

## Décision

1. Les 29 planches du canvas Claude Design (sources : `maquettes/lot1/`, `maquettes/lot2/`, `maquettes/canvas.json`) constituent **la référence de l'interface** : le client WPF reproduit ces écrans, leurs libellés, leurs états et leurs transitions. Tout écart en développement doit être justifié et reporté dans les maquettes.
2. La **planche Identité** (`lot1/Identite.dc.html`) est le contrat visuel : palette (49 tokens), typographie (IBM Plex Serif titres / IBM Plex Sans interface, replis Georgia / Segoe UI), tailles (plancher 12 px), boutons (38 / 42 / 48 px), signature khatam, règle de focus, règles des graphiques. En WPF elle devient un `ResourceDictionary` unique ; aucune couleur ni taille en dur dans les vues.
3. Les **conventions d'interaction** validées par les audits sont figées : anatomie liste + panneau de détail, tiroir latéral pour la saisie, modale pour les confirmations, toast avec annulation 5 min après une action financière, états vides avec sorties, motif obligatoire avant rejet, saisie en série au jour suivant.
4. Le **scénario de démonstration** suit les 3 parcours du walkthrough (saisie des gardes → ordre de mission → validation d'un lot → tableau de bord), dans cet ordre.
5. Les deux **scripts de vérification** (`verifier_coherence.py`, `verifier_contrastes.py`) sont conservés et rejoués après toute modification des maquettes.

## Options considérées

| Option | Avantages | Inconvénients | Retenue ? |
|---|---|---|---|
| A. Figer le prototype maintenant (cette décision) | Base stable pour l'architecture et la démo ; 42/42 exigences prouvées ; audits reproductibles | 5 écrans secondaires restent à dessiner pendant le développement | **Oui** |
| B. Continuer à itérer sur les maquettes jusqu'aux réponses du client | Zéro incertitude avant de coder | Bloque l'architecture sur 4 questions non bloquantes ; contraire au délai de l'avis d'achat | Non |
| C. Passer au prototype cliquable avant de figer | Test des transitions réelles | Coût élevé pour un gain marginal après 2 walkthroughs ; sera plus utile sur l'application WPF elle-même | Reporté (décision possible en phase développement) |

## Conséquences

- **Positives** : l'architecture (ADR-002 et suivants) peut s'appuyer sur des écrans stables pour définir les endpoints, les DTO et les états ; le jeu de données de démonstration est déjà spécifié par les maquettes (agents, lots, barème v3, missions) ; la recette pourra comparer écran par écran.
- **Négatives / à surveiller** : les maquettes sont statiques — focus clavier, survol, latence et lecteur d'écran seront vérifiés dans WPF (plan de test dans `rapport-audit-C-accessibilite.md`) ; les générateurs Python des maquettes sont de l'outillage jetable (D8) et ne servent pas de modèle pour le code.
- **Écrans encore partiels**, à produire au fil du développement : paramétrage des formulaires par structure, édition d'une version de barème, journal d'audit complet, préférences de notification.

## Questions ouvertes à trancher avec le client (n'invalident pas cette décision)

1. **Recalcul et lots validés** — proposition : un recalcul ne modifie jamais un lot validé ; un écart génère un lot de régularisation.
2. **Restauration d'une sauvegarde** — dans l'application (administrateur, double confirmation dessinée) ou réservée à la DSI ?
3. **Résolution minimale des postes** — proposition : 1366 × 768 à 100 %, mise à l'échelle Windows 125 % testée.
4. **Rôle de vérification** — le validateur vérifie puis valide (maquetté), ou 5ᵉ profil « Vérificateur » ?
5. **Barèmes et coefficients réels** — valeurs réglementaires à fournir ; le prototype utilise des valeurs de démonstration paramétrables.
6. **Notifications par e-mail** — in-app maquetté ; e-mail à confirmer.

## Références

- `AGENTS.md` §4 (exigences), §8 (décisions D1–D8), §9 (checklist de recette)
- `maquettes/audits/` : rapports A, B, C, D-E, traçabilité, `coherence.md`, `contrastes.md`
- `maquettes/walkthrough/` : carte des parcours, rapport
- Canvas : https://claude.ai/code/artifact/cb2c2395-6fcf-4499-a932-cfd6ad893c07
