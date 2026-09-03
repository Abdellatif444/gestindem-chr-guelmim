# Audit A — `ux-audit` des 15 planches non encore auditées — 2026-09-03

Périmètre : Calcul, États & rapports, Statistiques, Administration, et les 11 états (PlanningSaisie, PlanningEnregistre, MissionSaisie, MissionCree, MissionCloturee, PersonnelImportErreur, ValidationConfirm, ValidationSucces, ValidationVide, ValidationLignes, ValidationRejete). Même grille que l'audit du 2026-09-02 (Nielsen, Norman, Gestalt, WCAG statique, contenu), même échelle de sévérité (0–4). Captures : `audits/captures/`.

## 1. Éléments corrects (à conserver)
- **[P-01] Calcul** : détail du calcul par agent (dates, taux, barème appliqué, total), alerte « planning modifié » avec nouveau total prévisionnel — transparence exigée par le cahier des charges (M6) — Nielsen #1, G-P #7.
- **[P-02] États & rapports** : le format choisi se répercute dans le libellé du bouton (« Générer le rapport (PDF) »), aperçu du contenu avant génération, archive horodatée avec auteur — Content #3, Nielsen #1.
- **[P-03] Administration** : profils et droits lisibles en une table, encart qui nomme les 4 profils et le rôle du validateur, journal d'audit non modifiable, sauvegardes avec dernière restauration testée — M1/M12 rendus visibles.
- **[P-04] Import Excel** : chaque erreur donne la ligne, la cause et la correction ; choix explicite entre importer les lignes valides ou tout corriger ; « Aucune donnée n'a encore été enregistrée » rassure — Nielsen #9, Content #6.
- **[P-05] Confirmation de validation** : montant, agents, vérificateur, conséquence (« n'est plus modifiable »), journalisation — puis succès avec annulation 5 min — Nielsen #5, Shneiderman #6.
- **[P-06] Ordre de mission** : calcul prévisionnel mis à jour à chaque champ, distance pré-calculée et modifiable, note sur le barème appliqué à la date du départ.
- **[P-07] États vides et succès** : chaque action principale a désormais un résultat dessiné (correctif W-01/W-05/W-07 vérifié).

## 2. Problèmes détectés

| ID | Sév. | Écran | Vérification | Constat | Heuristiques |
|---|---|---|---|---|---|
| A-01 | 2 | Calcul | CTA-AMBIGUITY | « Lancer le calcul — Août 2026 » alors qu'un calcul existe déjà (31/08) : rien ne dit ce qu'il advient des lots déjà validés ou en validation (recalcul = écrasement ?) | Nielsen #5, G-P #2 |
| A-02 | 2 | Administration | STATE-GAP | « Restaurer… » (action destructive : remplace la base) sans confirmation dessinée ; « Nouvel utilisateur » et la fiche des droits **par module et par structure** (cœur de M1) non dessinées | Nielsen #5, Shneiderman #6 |
| A-03 | 1 | ValidationVide | Content | Le panneau de droite dit « Sélectionnez un lot… » alors qu'il n'y a aucun lot à sélectionner | Nielsen #2, Content #7 |
| A-04 | 1 | Etats | FAKE-AFFORDANCE | Bouton « régénérer » en icône seule dans l'archive, sans libellé ni info-bulle visible | Norman : signifiants, WCAG 4.1.2 |
| A-05 | 1 | Calcul | Lisibilité | En-tête du panneau : badge « À recalculer » et matricule « M-04512 » passent à la ligne (largeur insuffisante) | B&S : Lisibilité |
| A-06 | 1 | Etats | Fitts | Le bouton « Générer le rapport (PDF) » est en bas d'une carte largement vide, loin des champs qu'il conclut | Fitts, Gestalt : proximité |
| A-07 | 1 | Main / Calcul / Statistiques | PATTERN-DRIFT | Trois formulations de l'export : « Exporter en PDF », « Exporter (Excel) », « Exporter (PDF) » | Content #5 |

Aucun constat de sévérité 3 ou 4.

## 3. Niveau de priorité
- **À corriger avant de clore** : A-01 (une décision métier à afficher), A-02 (deux écrans manquants sur une exigence centrale).
- **Finitions** (effort S, à faire en même temps) : A-03 à A-07.

## 4. Améliorations recommandées et corrections
- **A-01** : renommer « Relancer le calcul — Août 2026 » et ajouter une confirmation : « Recalcule 248 agents avec le barème v3. Les lots déjà validés (23) ne sont pas modifiés ; les lots en validation (12) seront recalculés et repasseront en vérification. » — la règle exacte est **à confirmer avec le client** (voir §6).
- **A-02** : dessiner (a) la modale de confirmation de restauration (point de restauration choisi, avertissement de perte des saisies postérieures, double confirmation), (b) la fiche utilisateur avec la matrice **modules × structures** (cases à cocher), profil, statut, réinitialisation du mot de passe.
- **A-03** : texte « Aucun lot à afficher » et masquer les actions.
- **A-04** : libellé « Régénérer » à côté de l'icône, ou info-bulle + nom accessible.
- **A-05** : panneau à 400 px ou sous-titre sur deux lignes explicites.
- **A-06** : bouton directement sous l'aperçu du contenu.
- **A-07** : forme unique « Exporter (PDF) » / « Exporter (Excel) » — le tableau de bord passe à « Exporter (PDF) ».

## 5. Corrections appliquées
A-03, A-05, A-06, A-07 : appliquées dans cette itération (générateur + Main). A-01, A-02, A-04 : nouveaux écrans / règle métier — inscrits dans la liste « à ajouter » avec le changement de mot de passe, la mission plafonnée et les notifications (audit F).

## 6. Éléments nécessitant une validation humaine
- **A-01** : que fait un recalcul sur les lots déjà validés ? (recommandation : jamais modifiés ; un écart crée un lot de régularisation). Décision métier à prendre avec le CHR.
- **A-02** : la restauration d'une sauvegarde est-elle réservée à la DSI (hors application) ou offerte à l'administrateur dans l'interface ?
