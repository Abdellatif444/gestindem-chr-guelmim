---
type: parcours-walkthrough
date: 2026-09-02
produit: GESTINDEM (CHR de Guelmim)
scenarios: 3
ecrans: 19
constats-bloquants: 0
constats-ralentissent: 4
constats-genent: 4
---

# Walkthrough — GESTINDEM : saisie des gardes, ordre de mission, validation d'un lot

## Résumé

Les trois scénarios **aboutissent** pour l'utilisateur type, et le plus sensible (la validation d'un lot de 18 450 DH) est le mieux traité : confirmation explicite, succès annulable pendant 5 minutes, lot suivant proposé, état vide avec sorties. Aucun constat bloquant. Les quatre points qui ralentissent sont tous du même ordre : **des actions dont le résultat n'est pas dessiné** (création et clôture d'un ordre de mission, liste complète des lignes d'un lot) et **une fin de parcours muette** pour l'agent de saisie, qui ne sait pas quand son mois est « terminé » ni ce qui se passe ensuite. Trois corrections rentables : dessiner les retours de l'écran Missions et du rejet, ajouter la vue des lignes du lot, donner à l'agent de saisie un indicateur d'avancement et de clôture du mois.

## Scénarios évalués

| # | Utilisateur type | Objectif | Étapes | Aboutit ? |
|---|---|---|---|---|
| S1 | A. Tazi, agent de saisie, première semaine | Saisir les gardes d'août pour le service Urgences | 8 | Oui — mais sans savoir qu'il a fini |
| S2 | A. Tazi, agent de saisie | Créer un ordre de mission pour le Dr Saidi (Agadir, 2 jours) | 6 | Oui — sans confirmation visible |
| S3 | N. El Fassi, validateur récurrent | Traiter le lot LOT-2026-0142 puis vérifier le tableau de bord | 8 | Oui — parcours exemplaire |

## Carte des parcours

Voir `carte-parcours.md` (diagramme Mermaid, nœuds absents en rouge).

## Parcours pas à pas

### S1 — Saisir les gardes du mois

| Étape | Écran | Action correcte | Q1 quoi faire | Q2 visible | Q3 la bonne | Q4 retour | Constat |
|---|---|---|---|---|---|---|---|
| 1 | Connexion | Identifiant, mot de passe, « Se connecter » | ✓ | ✓ | ✓ | ✓ Main | — |
| 2 | Main | Sidebar « Plannings » | ✓ sous-titre « Gardes, astreintes… » visible seulement après | ✓ | ✗ hésitation possible entre « Plannings » et « Indemnités » pour un débutant | ✓ Planning | W-07 |
| 3 | Planning | Vérifier mois (Août 2026) et service (Urgences) | ✓ | ✓ un seul contrôle de période | ✓ | ✓ | — |
| 4 | Planning | « Nouvelle saisie » | ✓ | ✓ action primaire unique | ✓ | ✓ PlanningSaisie | — |
| 4b | Planning | (alternative) cliquer une case du calendrier | ? | ? aucun signifiant | ? | ? non dessiné | W-08 |
| 5 | PlanningSaisie | Type Garde, agent, date, durée, service | ✓ ordre logique | ✓ | ✓ | ✓ doublon signalé en direct, « Enregistrer » désactivé avec la raison | — |
| 6 | PlanningSaisie | Changer la date, « Enregistrer la garde » | ✓ | ✓ | ✓ verbe + objet | ✓ PlanningEnregistre (toast + chip) | — |
| 7 | PlanningEnregistre | Continuer : « Saisir le 14/08 → » | ✓ | ✓ | ✗ la case « saisie en série » promettait un formulaire resté ouvert ; on obtient un formulaire fermé et un lien | ✓ | W-04 |
| 8 | Planning | Fin du mois : constater que c'est terminé | ✗ rien ne dit « mois complet » ni ce qui suit | ✗ | — | ✗ aucun état de clôture | W-03 |

### S2 — Créer un ordre de mission

| Étape | Écran | Action correcte | Q1 | Q2 | Q3 | Q4 | Constat |
|---|---|---|---|---|---|---|---|
| 1 | Main | Sidebar « Missions » | ✓ | ✓ | ✓ | ✓ Missions | — |
| 2 | Missions | « Nouvel ordre de mission » | ✓ | ✓ | ✓ | ✓ MissionSaisie | — |
| 3 | MissionSaisie | Agent, départ, retour | ✓ | ✓ | ✓ | ✓ durée déduite (2 ×) dans le calcul | — |
| 4 | MissionSaisie | Destination, distance, motif | ✓ | ✓ | ✓ distance « calculée — modifiable » | ✓ coefficient × 1,5 et total mis à jour | — |
| 5 | MissionSaisie | « Créer l'ordre de mission » | ✓ | ✓ | ✓ | ✗ aucun écran après création | W-01 |
| 6 | Missions | Plus tard : « Clôturer et envoyer au calcul » | ✓ libellé explicite | ✓ | ✗ « À valider » (mission) et « En validation » (lot) : deux validations pour l'utilisateur | ✗ résultat non dessiné | W-01, W-07 |

### S3 — Valider un lot puis vérifier le tableau de bord

| Étape | Écran | Action correcte | Q1 | Q2 | Q3 | Q4 | Constat |
|---|---|---|---|---|---|---|---|
| 1 | Main | Aller à Validation | ✓ badge « 12 » + tuile « 12 lots · 98 640 DH » | ✓ | ✓ | ✓ Validation | — |
| 1b | Main | (alternative) cliquer la tuile « 12 lots » | ✓ | ? pas de signifiant | ? | ? | W-08 |
| 2 | Validation | Sélectionner LOT-2026-0142 | ✓ tri par délai, ligne mise en avant | ✓ | ✓ | ✓ détail à droite | — |
| 3 | Validation | Contrôler les lignes : « Voir les 12 lignes du lot » | ✓ | ✓ | ✓ | ✗ écran absent — 3 lignes visibles sur 12 | W-02 |
| 4 | Validation | « Valider le lot » | ✓ | ✓ action primaire | ✓ | ✓ ValidationConfirm : montant, agents, conséquence | — |
| 5 | ValidationConfirm | « Confirmer la validation » | ✓ | ✓ | ✓ même verbe qu'à l'étape 4 | ✓ ValidationSucces : toast, annulation 5 min, lot suivant, compteurs | — |
| 6 | Validation | (alternative) motif puis « Rejeter » | ✓ libellé + aide « obligatoire pour rejeter » | ✓ bouton grisé tant que vide | ✓ | ✗ résultat du rejet non dessiné | W-05 |
| 7 | Validation | Retrouver les lots « Prêt pour paiement » | ✗ étape 4 non cliquable, aucun filtre | ✗ | — | ✗ seulement depuis l'état vide | W-06 |
| 8 | ValidationSucces | Sidebar « Tableau de bord » | ✓ | ✓ | ✓ | ✓ Main | — |

## Après chaque action, que voit l'utilisateur ?

| Écran | Action | Résultat visible dans les maquettes | Dessiné ? |
|---|---|---|---|
| Connexion | Se connecter | Tableau de bord | oui |
| Connexion | Mot de passe oublié ? | — | non |
| Main | Exporter en PDF | — | non (hors scénarios) |
| Main | Tout voir (lots) | Validation (implicite) | partiel |
| Planning | Nouvelle saisie | Tiroir de saisie | oui |
| Planning | Importer (Excel) | — | non |
| Planning | Corriger (bandeau doublon) | — | non |
| Planning | Clic sur une case | — | non |
| PlanningSaisie | Enregistrer la garde | Toast + chip + lien série | oui |
| PlanningSaisie | Voir la saisie existante | — | non |
| PlanningSaisie | Annuler | Planning | oui (implicite) |
| PlanningEnregistre | Saisir le 14/08 → | Tiroir au jour suivant | partiel (contradiction W-04) |
| Missions | Nouvel ordre de mission | Tiroir OM | oui |
| MissionSaisie | Créer l'ordre de mission | — | **non** |
| Missions | Modifier | — | non |
| Missions | Clôturer et envoyer au calcul | — | **non** |
| Missions | Historique complet des déplacements | — | non |
| Missions | Exporter (Excel) | — | non |
| Validation | Voir les 12 lignes du lot | — | **non** |
| Validation | Valider le lot | Confirmation | oui |
| ValidationConfirm | Confirmer la validation | Succès + lot suivant + compteurs | oui |
| ValidationSucces | Annuler (5 min) | Retour à l'état précédent (implicite) | partiel |
| Validation | Rejeter | — | **non** |
| Validation | Afficher tout | — | non |
| ValidationVide | Voir les lots prêts pour paiement (24) | — | non |
| Personnel | Importer depuis Excel | Résultat d'import avec erreurs | oui |
| PersonnelImportErreur | Importer les 12 lignes valides | — | non |
| Calcul | Lancer le calcul / Recalculer cet agent | — | non (hors scénarios) |
| Etats | Générer le rapport (PDF) | — | non (hors scénarios) |

Les « non » en gras touchent directement les scénarios évalués ; les autres sont l'inventaire des états à prévoir avant le développement (ils deviendront des cas de test).

## Constats

### [Ralentit] W-01 · Les actions de l'écran Missions n'ont pas de résultat
- **Type** : RETOUR-ABSENT
- **Où** : S2 étapes 5–6 — MissionSaisie « Créer l'ordre de mission », Missions « Clôturer et envoyer au calcul », « Modifier »
- **Preuve** : aucune capture ne montre l'après ; la liste Missions contient déjà OM-2026-088 « En cours », mais rien ne relie ce résultat à l'action du formulaire
- **Effet sur l'utilisateur type** : l'agent ne sait pas si l'ordre est créé, ni ce que « envoyer au calcul » a produit (un lot ? une ligne dans Calcul ?)
- **Heuristique** : Nielsen #1 (visibilité de l'état), Shneiderman #4 (clôture des dialogues)
- **Correction proposée** : toast « Ordre OM-2026-089 créé — En cours » + ligne ajoutée en tête et sélectionnée ; après clôture : toast « Mission clôturée — 1 200 DH envoyés au calcul d'août » + état « Clôturée », lien vers Calcul · **Effort** : S (même mécanique que PlanningEnregistre)

### [Ralentit] W-02 · Le validateur ne voit pas ce qu'il valide
- **Type** : ECRAN-ABSENT
- **Où** : S3 étape 3 — Validation, lien « Voir les 12 lignes du lot »
- **Preuve** : 3 lignes affichées sur 12 ; le lien n'a pas de destination dessinée
- **Effet sur l'utilisateur type** : un validateur consciencieux hésite à confirmer 18 450 DH sans avoir vu les 9 autres lignes — c'est précisément le contrôle que le cahier des charges lui confie (M9)
- **Heuristique** : Nielsen #6 (reconnaissance plutôt que rappel), G-P #8
- **Correction proposée** : vue « Lignes du lot » (tableau agent · nombre · taux · montant · lien vers le planning) en tiroir ou en modale, avec « Valider le lot » accessible depuis cette vue · **Effort** : S

### [Ralentit] W-03 · La fin du mois est muette pour l'agent de saisie
- **Type** : CUL-DE-SAC (fin de parcours)
- **Où** : S1 étape 8 — Planning
- **Preuve** : le calendrier montre des chips, rien n'indique combien de saisies sont attendues, si le mois est complet, ni ce qui suit (le PDF prévoit une intégration automatique dans le calcul, mais l'interface ne le dit pas)
- **Effet sur l'utilisateur type** : « Et maintenant ? » — l'agent cherche un bouton « Envoyer » qui n'existe pas, ou doute d'avoir fini
- **Heuristique** : Nielsen #1, Peak-End (la fin du parcours est ce qu'on retient)
- **Correction proposée** : ligne d'état sous la barre d'outils : « Août 2026 · 41 saisies · intégrées au prochain calcul (planifié le 31/08) » ; à la clôture de période par l'administrateur : bandeau « Période clôturée le 31/08 — saisies verrouillées » · **Effort** : S

### [Ralentit] W-04 · « Saisie en série » ne tient pas sa promesse
- **Type** : CONTEXTE-PERDU
- **Où** : S1 étape 7 — PlanningSaisie (case « après enregistrement, passer au jour suivant pour le même agent ») vs PlanningEnregistre (formulaire fermé, lien « Saisir le 14/08 → » dans un toast)
- **Preuve** : les deux captures se contredisent sur ce qui suit « Enregistrer »
- **Effet sur l'utilisateur type** : pour saisir 20 gardes, l'agent s'attend à rester dans le formulaire ; s'il doit rouvrir à chaque fois, la tâche la plus fréquente de l'application devient la plus lente
- **Heuristique** : Nielsen #7 (efficacité pour l'utilisateur fréquent), Norman : modèle conceptuel
- **Correction proposée** : choisir un seul comportement — recommandé : le tiroir reste ouvert, date passée au 14/08, agent conservé, bandeau discret « Garde du 13/08 enregistrée » dans le tiroir ; le toast disparaît · **Effort** : S

### [Gêne] W-05 · Le rejet n'a pas de résultat dessiné
- **Type** : RETOUR-ABSENT · **Où** : S3 étape 6 — Validation
- **Preuve** : bouton « Rejeter » (correctement conditionné au motif) sans capture de l'après
- **Effet** : le validateur ne sait pas si l'agent de saisie a été prévenu ni où le lot est parti (retour en « Saisie » ?)
- **Correction proposée** : toast « Lot renvoyé à la saisie — motif transmis à A. Tazi » + étape 1 « Saisie » qui passe à 9 lots · **Effort** : S

### [Gêne] W-06 · Les lots « Prêt pour paiement » sont un cul-de-sac en état normal
- **Type** : CUL-DE-SAC · **Où** : S3 étape 7 — Validation, ValidationVide
- **Preuve** : la carte « 4 · Prêt pour paiement · 24 lots » est une progression non cliquable (décision de l'audit précédent) ; seul l'état vide propose « Voir les lots prêts pour paiement (24) »
- **Effet** : un validateur qui veut retrouver un lot validé hier ne sait pas où aller
- **Correction proposée** : chips de filtre au-dessus de la liste : « En attente (12) · Prêts pour paiement (24) · Rejetés (2) » — même composant que les filtres de Missions · **Effort** : S

### [Gêne] W-07 · Trois flottements de vocabulaire
- **Type** : VOCABULAIRE · **Où** : sidebar « Indemnités » → page « Calcul des indemnités » ; mission « À valider » vs lot « En validation » ; étape 2 « Vérification » alors que les 4 profils (Administration) n'ont pas de vérificateur
- **Effet** : un débutant hésite entre « Plannings » et « Indemnités » pour saisir une garde ; il ne sait pas si valider une mission et valider un lot sont la même chose ni qui « vérifie »
- **Heuristique** : Nielsen #2, Content #5 (un terme par concept)
- **Correction proposée** : sidebar « Calcul » (au lieu d'« Indemnités ») ; missions : « À clôturer » au lieu d'« À valider » si c'est l'agent qui clôture ; Administration : préciser sur le profil Validateur « vérifie et valide » ou ajouter « Vérificateur » aux profils (à trancher avec le client : le PDF dit « quatre profils au minimum ») · **Effort** : S

### [Gêne] W-08 · Deux affordances non signalées
- **Type** : ACTION-INVISIBLE · **Où** : Planning (cases du calendrier), Main (tuile « 12 lots · 98 640 DH »)
- **Preuve** : rien n'indique qu'un clic sur une case ouvre la saisie au bon jour, ni que la tuile mène à Validation — comportements non évaluables sur capture (marqués ?)
- **Correction proposée** : décider et dessiner : « + » au survol de la case (et raccourci clavier), tuile cliquable avec chevron « Traiter → » · **Effort** : S

## Niveau parcours

- **Transitions et contexte** : la navigation, la structure et la période restent visibles d'un écran à l'autre ; l'élément sélectionné (lot, agent, mission) est rappelé dans le panneau de détail. Seule exception assumée : sur Plannings la période vit dans la barre d'outils du calendrier et non dans la barre supérieure (décision de l'audit UX, cohérente en valeur).
- **Charge mémoire** : faible — identifiants et montants sont répétés là où l'utilisateur agit (confirmation, toast).
- **Vocabulaire** : solide sur les statuts de lot et les verbes d'action ; trois flottements (W-07).
- **Fin de parcours** : S3 exemplaire (succès, annulation, suivant, vide) ; S2 sans retour ; S1 sans clôture.
- **Sorties** : Annuler présent sur tiroirs et modale ; annulation 5 minutes après validation. Non dessiné : que devient un formulaire de saisie abandonné (brouillon ?).

## Ce qui rend le parcours fluide (à conserver)

- **[F-01]** Validation : confirmation → succès annulable → lot suivant → état vide. À reproduire pour Missions et le rejet.
- **[F-02]** Doublon détecté au moment de la saisie, bouton désactivé avec la raison et une sortie (« Voir la saisie existante »).
- **[F-03]** Calcul prévisionnel de l'ordre de mission mis à jour à chaque champ, plafond affiché.
- **[F-04]** La sidebar et son badge « 12 » sont un déclencheur permanent (Fogg : prompt) — le validateur sait toujours qu'il a du travail.
- **[F-05]** Import Excel : cause + correction par ligne, choix entre importer les valides ou tout corriger.
- **[F-06]** Même anatomie liste + détail + actions en bas sur tous les écrans : un utilisateur apprend une fois.

## Non évaluable sur captures statiques

Survol des cases du calendrier ; comportement des listes déroulantes (agent, service) ; ordre de tabulation et focus dans les tiroirs ; défilement du tiroir de saisie à 900 px ; délai d'apparition et de disparition des toasts ; conservation d'un brouillon de saisie.

## Trois corrections prioritaires

1. **Dessiner les retours manquants** (W-01, W-05) : création et clôture d'ordre de mission, rejet d'un lot — 3 planches, même mécanique toast + mise à jour que ValidationSucces.
2. **Vue « Lignes du lot »** (W-02) : le contrôle que fait réellement le validateur avant de signer.
3. **Fin de parcours de la saisie** (W-03 + W-04) : indicateur d'avancement/clôture du mois et un seul comportement pour la saisie en série (tiroir qui reste ouvert).

Puis, à coût nul : W-06 (chips de filtre), W-07 (trois libellés), W-08 (deux signifiants).
