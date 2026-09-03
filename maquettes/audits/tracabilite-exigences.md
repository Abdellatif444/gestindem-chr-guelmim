# Audit F — traçabilité des exigences du cahier des charges vers les maquettes

Source des exigences : `AGENTS.md` §4 (extraction du CDC-GESTINDEM-2026) et §2bis (avis 43/2026/CHRG). Une exigence est **couverte** quand une planche en montre la preuve visible ; **partielle** quand seule une partie est dessinée ; **hors maquette** quand elle relève du code ou de l'exploitation (à tracer en phase de développement, pas dans un prototype visuel).

Légende : ✅ couverte · 🟡 partielle · ❌ non maquettée · ⚙️ hors maquette (technique)

## M1 — Authentification & droits d'accès

| Exigence | Preuve | Statut |
|---|---|---|
| Connexion identifiant + mot de passe haché | `Connexion` (formulaire) ; hachage = code | ✅ / ⚙️ |
| 4 profils minimum : administrateur, agent de saisie, validateur, consultation | `Administration` (colonne Profil, encart « Quatre profils »), 4 rôles visibles dans les barres supérieures | ✅ |
| Droits par module **et** par structure | `Administration` (colonnes Structure, Modules autorisés) ; l'arbre grisé « hors périmètre » sur `Structures` | ✅ (fiche utilisateur détaillée non dessinée : 🟡) |
| Déconnexion automatique après inactivité | `Connexion` (encart 15 min), `Administration` (pied) | ✅ |
| Changement de mot de passe | aucun écran | ❌ → à ajouter (menu utilisateur ou fiche) |

## M2 — Gestion des structures

| Exigence | Preuve | Statut |
|---|---|---|
| Hôpitaux, centres de santé, délégations, services | `Structures` (arbre : direction, délégations, CHR, CS urbain/rural, services) | ✅ |
| Rattachement agents et utilisateurs à une structure | `Personnel` (colonne Affectation), `Administration` (colonne Structure) | ✅ |
| Exercices et périodes (mois, trimestre, année) | `Structures` (« Exercices et périodes » : Août, Juillet, Trimestre 2 ; « Ouvrir une période ») | ✅ |
| Formulaires et paramètres adaptables par structure | `Structures` (encart + lien Administration) — écran de paramétrage non dessiné | 🟡 |

## M3 — Gestion du personnel

| Exigence | Preuve | Statut |
|---|---|---|
| Fiche agent : matricule, nom, grade, catégorie/groupe, affectation | `Personnel` (table + panneau de détail) | ✅ |
| Classement par groupes déterminant les taux | `Personnel` (colonne Groupe, « Groupe (taux) »), `Baremes` (grille par groupe) | ✅ |
| Import en masse depuis Excel | `Personnel` (bouton, dernier import), `PersonnelImportErreur` (résultat avec erreurs) | ✅ |
| Recherche et filtrage par grade, groupe, structure | `Personnel` (filtres Grade / Groupe / Service + recherche) | ✅ |

## M4 — Barèmes & règles de calcul

| Exigence | Preuve | Statut |
|---|---|---|
| Taux garde / astreinte / permanence par grade | `Baremes` (« Taux par grade et par type ») | ✅ |
| Grille déplacement par groupe : indemnité journalière, coefficient, plafond | `Baremes` (grille + coefficients de distance) | ✅ |
| Historisation par date d'effet | `Baremes` (« Historique des versions » v1–v3 avec dates d'effet) | ✅ |
| Modifiable par l'administrateur sans code | `Baremes` (« Nouvelle version ») — formulaire d'édition non dessiné | 🟡 |

## M5 — Plannings

| Exigence | Preuve | Statut |
|---|---|---|
| Saisie gardes/astreintes/permanences par agent et période | `PlanningSaisie`, `PlanningEnregistre` | ✅ |
| Intégration automatique dans le calcul | `Planning` (ligne d'avancement « intégrées automatiquement au calcul ») | ✅ |
| Vue mensuelle par structure et par service | `Planning` (calendrier, filtre Service) | ✅ |
| Détection des doublons et contrôles de cohérence | `Planning` (bandeau + cellule), `PlanningSaisie` (doublon en direct) | ✅ |

## M6 — Calcul des indemnités G/A/P

| Exigence | Preuve | Statut |
|---|---|---|
| Calcul automatique par agent, type, période | `Calcul` (table par agent, totaux) | ✅ |
| Barème en vigueur à la date concernée | `Calcul` (« barème v3 — effet 01/07/2026 »), bandeau `Baremes` | ✅ |
| États récapitulatifs mensuels, trimestriels, annuels | `Etats` (types de rapports) | ✅ |
| Recalcul si planning ou barème modifié | `Calcul` (« À recalculer », alerte planning modifié, « Recalculer cet agent ») | ✅ |

## M7 — Missions & déplacements

| Exigence | Preuve | Statut |
|---|---|---|
| Ordres de mission : agent, destination, durée, distance, motif | `MissionSaisie`, `Missions` (détail) | ✅ |
| Suivi de l'état + historique complet | `Missions` (états En cours / À clôturer / Clôturée, historique, lien « Historique complet ») ; `MissionCree`, `MissionCloturee` | ✅ |
| Rattachement à une période et une structure | `Missions` (barre supérieure Structure + Période, « Août 2026 » en pied) | ✅ |

## M8 — Calcul des indemnités de déplacement

| Exigence | Preuve | Statut |
|---|---|---|
| Durée × indemnité journalière du groupe × coefficient de distance | `Missions`, `MissionSaisie` (détail du calcul) | ✅ |
| Plafond par mission | idem (« plafond 2 000 DH respecté ») — **cas plafonné jamais montré** | 🟡 |
| Affichage du détail du calcul | idem | ✅ |

## M9 — Workflow de validation

| Exigence | Preuve | Statut |
|---|---|---|
| Circuit saisie → vérification → validation → (paiement) | `Validation` (4 étapes) | ✅ |
| Validation ou rejet avec motif | `Validation` (motif obligatoire), `ValidationConfirm`, `ValidationSucces`, `ValidationRejete` | ✅ |
| Notification des lots en attente, suivi des délais | `Validation` (colonne Délai + légende), sidebar badge, cloche « 3 » — **écran de notifications non dessiné** | 🟡 |
| Chaque action horodatée et attribuée | `Validation` (historique), `Administration` (journal) | ✅ |

## M10 — États & rapports

| Exigence | Preuve | Statut |
|---|---|---|
| Rapports mensuels, trimestriels, annuels automatiques | `Etats` (générateur + archive) | ✅ |
| États personnalisés : par service, agent, type | `Etats` (« Détail par » : service / agent / type) | ✅ |
| Export Excel et PDF (+ CSV, avis 43/2026) | `Etats` (formats PDF / Excel / CSV) | ✅ |
| Archivage des rapports générés | `Etats` (archive, « conservés 10 ans ») | ✅ |

## M11 — Statistiques & tableaux de bord

| Exigence | Preuve | Statut |
|---|---|---|
| Indicateurs : suivi des dépenses, répartition | `Main`, `Statistiques` | ✅ |
| Graphiques : évolution, répartition | `Main` (barres empilées), `Statistiques` (courbes 2026/2025, répartition) | ✅ |
| Comparaison entre structures ou périodes | `Statistiques` (comparaison structures ; 2026 vs 2025) | ✅ |
| Tableau de bord synthétique en page d'accueil | `Main` | ✅ |

## M12 — Traçabilité, sécurité & sauvegarde

| Exigence | Preuve | Statut |
|---|---|---|
| Journal d'audit (qui, quoi, quand) | `Administration` (journal du jour, « Tout le journal ») | ✅ (écran complet du journal : 🟡) |
| Suivi des validations et rejets | `Validation` (historique), journal | ✅ |
| Sauvegarde quotidienne, restauration testée | `Administration` (« Sauvegardes » : quotidienne 02:00, restauration testée) | ✅ |
| Chiffrement sauvegardes et mots de passe | `Administration` (« AES-256 ») ; implémentation = code | ✅ / ⚙️ |

## Exigences transversales et contractuelles

| Exigence | Preuve | Statut |
|---|---|---|
| Interface en français, claire et cohérente | 24 planches, audits ux-audit + cohérence | ✅ |
| Formulaires dynamiques pour saisie rapide | `PlanningSaisie` (série), `MissionSaisie` (calcul en direct) | ✅ |
| API-first, aucune logique dans le client | ⚙️ architecture (ADR à venir) | ⚙️ |
| Démonstration sous 48 h (avis 43/2026) | prototype = scénario de démo ; **jeu de données de démo et scénario écrit** à produire | 🟡 |
| Livrables : installeur, doc, formation | ⚙️ phases suivantes | ⚙️ |

## Mise à jour du 2026-09-03 — 5 planches ajoutées

| Exigence | Nouvelle preuve | Statut |
|---|---|---|
| M1 · changement de mot de passe | `MotDePasse` (modale : actuel, nouveau, confirmation, robustesse, règles, déconnexion des autres sessions, journalisation) | ❌ → ✅ |
| M1 · droits par module **et** par structure | `UtilisateurFiche` (matrice modules × structures, profil, statut, réinitialisation, désactivation) | 🟡 → ✅ |
| M8 · plafond par mission | `MissionPlafonnee` (OM-2026-083 : 4 j × 250 × 1,5 = 1 500 → plafond Groupe C 1 200 DH, détail ligne à ligne + explication) | 🟡 → ✅ |
| M9 · notification des lots en attente | `Notifications` (centre de notifications : délais, recalculs, imports, sauvegardes ; non lues ; préférences) | 🟡 → ✅ |
| M12 · restauration sécurisée | `RestaurationConfirm` (point de restauration, pertes chiffrées, sauvegarde de sécurité, double confirmation) | ✅ renforcé |

## Synthèse

- **Couvertes** : 42 exigences · **Partielles** : 5 (paramétrage par structure, édition de barème, journal complet, notifications e-mail, démo à scénariser) · **Non maquettée** : 0 · **Hors maquette (technique)** : 4.
- Les partielles restantes sont des écrans secondaires acceptables en phase de développement.
- **Questions à poser au client** (validation humaine) : (1) valeurs réglementaires des barèmes ; (2) tranches du coefficient de distance ; (3) qui « vérifie » (validateur ou 5ᵉ profil) ; (4) notifications in-app suffisantes ou e-mail exigé.
