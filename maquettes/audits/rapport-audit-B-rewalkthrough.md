# Audit B — re-walkthrough après corrections W-01 → W-08 — 2026-09-03

Objectif : vérifier, sur les captures corrigées (`audits/captures/`), que chaque constat du walkthrough du 2026-09-02 est résolu **et** qu'aucune régression n'est apparue sur les 3 scénarios. Méthode : rejouer les étapes qui portaient un ✗, avec les 4 questions du cognitive walkthrough.

## 1. Vérification constat par constat

| Constat | Correction attendue | Preuve sur capture | Q1 | Q2 | Q3 | Q4 | Résolu ? |
|---|---|---|---|---|---|---|---|
| W-01 retours Missions | Création et clôture dessinées | `MissionCree` : toast « Ordre OM-2026-088 créé… En cours » ; `MissionCloturee` : badge Clôturée, encart « Clôturée le 27/08 … 1 200 DH envoyés au calcul », lien « Voir dans Calcul », compteurs 4 / 7 | ✓ | ✓ | ✓ | ✓ | **Oui** |
| W-02 lignes du lot | Vue des 12 lignes | `ValidationLignes` : 12 agents, dates, taux, montants, total 18 450 DH, « Valider le lot » dans la modale | ✓ | ✓ | ✓ | ✓ | **Oui** |
| W-03 fin de mois muette | Indicateur d'avancement | `Planning` : « Août 2026 — période ouverte · 41 saisies … intégrées automatiquement au calcul du mois, planifié le 31/08 » + « Voir le calcul » | ✓ | ✓ | ✓ | ✓ | **Oui** |
| W-04 série contradictoire | Tiroir resté ouvert | `PlanningEnregistre` : tiroir ouvert, bandeau « Garde du 13/08 enregistrée », date 14/08 « jour suivant, modifiable », « Terminer la série » / « Enregistrer la garde » | ✓ | ✓ | ✓ | ✓ | **Oui** |
| W-05 rejet | Résultat du rejet | `ValidationRejete` : toast « renvoyé à la saisie — motif transmis à A. Tazi », Saisie 9 lots, lot suivant sélectionné, « Annuler (5 min) » | ✓ | ✓ | ✓ | ✓ | **Oui** |
| W-06 lots prêts | Filtres | `Validation` : « En attente (12) · Prêts pour paiement (23) · Rejetés (2) · Tous (37) », cohérents sur succès / rejet / vide | ✓ | ✓ | ✓ | ✓ | **Oui** |
| W-07 vocabulaire | Calcul / À clôturer / rôle validateur | Sidebar « Calcul » sur 22 écrans ; Missions « À clôturer (3) » ; Administration : « Le validateur assure la vérification (étape 2) puis la validation (étape 3) » | ✓ | ✓ | ✓ | — | **Oui** (décision client en suspens) |
| W-08 affordances | Signifiants | `Planning` : case du 20 « + Saisir une garde · au survol · touche N » ; `Main` : « Traiter → » sur la tuile d'attente | ✓ | ✓ | ✓ | ? | **Oui** (survol non évaluable sur image) |

## 2. Recherche de régressions (parcours complets rejoués)
- **S1 saisie** : Connexion → Main → Plannings → Nouvelle saisie → doublon → date corrigée → Enregistrer → série → fin de mois : 8 étapes, aucun ✗. La ligne d'avancement répond à « et maintenant ? ».
- **S2 mission** : Missions → Nouvel ordre → champs → Créer → toast → plus tard Clôturer → clôturée : 6 étapes, aucun ✗.
- **S3 validation** : Main (« Traiter → ») → Validation → lignes du lot → Valider → Confirmer → Succès → suivant → vide → Tableau de bord : 9 étapes, aucun ✗. Variante rejet : motif → Rejeter → toast : ✓.
- **Contexte conservé** : structure et période visibles partout (Plannings : période dans la barre du calendrier, décision documentée) ; lot et agent rappelés dans les panneaux et les toasts.
- **Vocabulaire** : « Calcul » (nav) = « Calcul des indemnités » (page) ; « À clôturer » ne se confond plus avec « En validation ».

## 3. Nouveaux constats apparus
Aucun au niveau parcours. Les constats d'écran relevés en parallèle sont dans l'audit A (A-01 à A-07) — aucun ne bloque un scénario.

## 4. Tableau « après chaque action » — mise à jour
Les 7 « non » qui touchaient les scénarios sont devenus « oui » (créer OM, clôturer OM, lignes du lot, rejeter, série, fin de mois, tuile tableau de bord). Restent « non », hors scénarios : Mot de passe oublié, Importer (Excel) planning, Corriger (bandeau), Voir la saisie existante, Modifier (mission), Historique complet, Exporter, Restaurer, Nouvel utilisateur, Lancer le calcul, Générer le rapport — soit **la liste des états à prévoir en phase de développement**, dont 3 sont prioritaires (audits A et F : recalcul, restauration, fiche utilisateur).

## 5. Verdict
Les 8 constats du walkthrough sont résolus, sans régression. Les 3 scénarios du cahier des charges sont réalisables par un nouvel utilisateur avec les maquettes actuelles.

## 6. Validation humaine
- W-07 : rôle « vérificateur » — à confirmer avec le client.
- W-08 : comportement au survol et raccourci « N » — à valider dans le prototype WPF (non évaluable sur image).
