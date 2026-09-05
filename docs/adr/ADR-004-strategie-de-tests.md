# ADR-004 : Stratégie de tests

**Status:** Accepted
**Date:** 2026-09-03
**Deciders:** Abdellatif (chef de projet / développeur)
**Related:** ADR-002 (couches), ADR-003 (modèle et formules)

## Context

Le cahier des charges fait des tests une exigence explicite : les moteurs de calcul sont « à tester en priorité » (§8, phase 2), l'intégrité des calculs doit être « garantie par une couche métier unique » (§6.3), et la recette vérifiera que « les calculs sont exacts et appliquent les barèmes paramétrés » (§9). L'application manipule de l'argent public : une branche de calcul non testée est une erreur de paiement potentielle.

Contraintes : une personne, délai court, SQL Server Express déjà choisi (D4), WPF en MVVM (D3), Clean Architecture avec `Desktop` ne référençant que `Contracts` (ADR-002). Le prototype (ADR-001) fournit déjà des valeurs de référence (barème v3, lots, missions dont un cas plafonné) et trois parcours validés par walkthrough.

## Decision

### Principes

1. **Tests avant le code sur le métier** : chaque moteur de calcul est écrit après ses cas golden, jamais l'inverse. Un cas golden = une ligne d'un tableau `[Theory]` : entrées → montant attendu → source (PDF, maquette, règle).
2. **Une seule source de données de référence** : le seed de démonstration (`Gestindem.Infrastructure.Seed`) alimente la démo **et** les tests d'intégration. Ce que la démo montre, les tests l'ont prouvé.
3. **Jamais de fournisseur EF « InMemory »** : il n'applique ni contraintes d'unicité ni transactions ; un test qui passe dessus ne prouve rien sur SQL Server.
4. **Immuabilité testée** : un test tente un `UPDATE` sur une ligne d'indemnité, une étape de validation, une entrée d'audit et une version de barème archivée — et vérifie l'échec.

### Pyramide par couche

| Couche | Type | Outils | Cible de couverture |
|---|---|---|---|
| `Domain` | unitaires purs (invariants, objets-valeurs) | xUnit, FluentAssertions | ≥ 90 % |
| `Application` — moteurs de calcul | **golden tabulaires**, écrits d'abord | xUnit `[Theory]` + `[MemberData]` | **100 % des branches** (bloquant) |
| `Application` — cas d'usage | unitaires avec doubles sur les ports | xUnit, NSubstitute | ≥ 90 % |
| `Infrastructure` | intégration sur base réelle | SQL Server Express, base `Gestindem_Test` recréée à chaque exécution (`EnsureDeleted` + migrations), Respawn pour le nettoyage entre tests | contraintes et migrations : 100 % des invariants d'ADR-003 |
| `Api` | intégration HTTP | `WebApplicationFactory`, base de test ci-dessus, JWT de test | ≥ 70 % ; contrat OpenAPI vérifié par test de non-régression (le fichier généré est comparé à celui versionné) |
| `Desktop` — ViewModels | unitaires (client HTTP simulé) | xUnit, NSubstitute | ≥ 60 % |
| `Desktop` — interface | (a) scénarios manuels scriptés ; (b) **automatisation FlaUI** sur les 3 parcours du walkthrough | script de recette ; FlaUI + xUnit | (b) : 3 scénarios verts = critère de livraison |

**Décision de l'utilisateur sur le client** : ViewModels + scénarios manuels **et** automatisation FlaUI. Phasage retenu pour tenir le délai : les tests de ViewModels et le script manuel accompagnent chaque écran ; l'automatisation FlaUI est écrite **une fois les écrans stabilisés** (fin de phase 4), limitée aux 3 parcours de référence (saisie → mission → validation) qui servent de test de fumée avant chaque livraison. Toute extension au-delà des 3 parcours fera l'objet d'une décision séparée (coût de maintenance élevé).

### Cas golden des moteurs de calcul (liste initiale, à compléter avant le code)

| # | Cas | Entrées | Attendu | Source |
|---|---|---|---|---|
| G-01 | Gardes spécialiste, barème v3 | 6 gardes, Médecin spécialiste, août 2026 | 3 600 DH | maquette `ValidationLignes` |
| G-02 | Mix gardes + astreintes | 6 gardes + 2 astreintes, spécialiste | 4 400 DH | maquette `Personnel` |
| G-03 | Mois à cheval sur deux versions | 2 gardes le 28/06 (v2 : 550) + 4 le 05/07 (v3 : 600) | 1 100 + 2 400 = 3 500 DH, deux instantanés | M6 « barème à la date » |
| G-04 | Aucun barème à la date | planning au 01/01/2020 | erreur `BAREME_ABSENT_A_DATE` | ADR-003 |
| G-05 | Agent sans groupe | mission d'un agent sans `GroupeId` | erreur `AGENT_SANS_GROUPE` | ADR-003 |
| D-01 | Déplacement standard | 2 j, 452 km, Groupe A (400, plafond 2 000) | 2 × 400 × 1,5 = 1 200 DH, non plafonné | maquette `Missions` |
| D-02 | **Déplacement plafonné** | 4 j, 642 km, Groupe C (250, plafond 1 200) | brut 1 500, final **1 200**, `PlafondApplique` renseigné | maquette `MissionPlafonnee` |
| D-03 | Borne de tranche | 150 km exactement | coefficient de la tranche 50–150 (× 1,2), pas × 1,5 | tranches d'ADR-003 |
| D-04 | Courte distance | 1 j, 42 km, Groupe C | 1 × 250 × 1,0 = 250 DH | maquette `Missions` |
| D-05 | Mission non clôturée | mission `EnCours` | exclue du calcul | ADR-003 |
| D-06 | Dates invalides | retour < départ | erreur `MISSION_DATES_INVALIDES` | ADR-003 |
| W-01 | Période close | saisie sur période `Cloturee` | erreur `PERIODE_CLOTUREE` | M2 |
| W-02 | Doublon | même agent, même date, même type | erreur `PLANNING_DOUBLON` | M5 |
| W-03 | Recalcul | second calcul sur la même période | nouveau `Calcul`, ancien `Obsolete`, lignes anciennes intactes | ADR-003 |
| W-04 | Idempotence | deux validations avec la même `Idempotency-Key` | une seule `EtapeValidation` | ADR-002 |
| W-05 | Rejet sans motif | `POST /lots/{id}/rejet` sans motif | erreur `LOT_MOTIF_REQUIS` | M9 |
| W-06 | Annulation expirée | annulation à 5 min 01 s | erreur `ANNULATION_EXPIREE` | maquette `ValidationSucces` |

### Outillage et intégration continue

> **Amendement du 2026-09-05** — FluentAssertions est passé sous licence commerciale à partir de la version 8 (usage professionnel payant). Le projet étant un marché public, on utilise **AwesomeAssertions** (fork communautaire sous licence Apache 2.0, même API ; depuis sa version 9 l'espace de noms est `AwesomeAssertions` — vérifié dans le paquet 9.6.0) : un `using` à changer, aucune redevance. Le reste de la décision est inchangé.

- **xUnit** (standard .NET, parallélisme natif), **FluentAssertions** (messages d'échec lisibles), **NSubstitute** (doubles), **coverlet** + `reportgenerator` (couverture), **Respawn** (remise à zéro de la base de test), **FlaUI** (UI Automation Windows).
- Commande unique : `dotnet test` exécute tout ; les tests d'intégration sont marqués `[Trait("Category","Integration")]` pour pouvoir n'exécuter que l'unitaire en local (`--filter Category!=Integration`).
- **GitHub Actions** (gratuit pour ce dépôt) : à chaque push, unitaires + couverture ; l'échec d'un cas golden ou une couverture < 100 % sur les moteurs **bloque la fusion** vers `main`. Les tests d'intégration SQL Server tournent sur un exécuteur Windows avec SQL Server Express installé dans le workflow ; FlaUI reste local (nécessite une session graphique).

## Options Considered

### Base des tests d'intégration
| Option | Fidélité | Vitesse | Prérequis | Retenue |
|---|---|---|---|---|
| **SQL Server Express réel** | Totale (même dialecte, mêmes contraintes) | Moyenne (~1 s par test avec Respawn) | Express local — déjà requis par D4 | **Oui** |
| SQLite en mémoire | Partielle (décimaux, dates, index filtrés diffèrent) | Excellente | Aucun | Non — un vert SQLite ne prouve rien pour Express |
| Testcontainers | Totale | Moyenne | Docker Desktop, image 1,5 Go | Non pour le poste ; possible plus tard en CI |

### Client WPF
| Option | Confiance | Coût | Retenue |
|---|---|---|---|
| ViewModels + scénarios manuels | Bonne sur la logique d'écran | Faible | **Oui** |
| + automatisation FlaUI | Élevée sur les parcours réels | Élevé (fragile aux changements d'écran) | **Oui, limitée aux 3 parcours, après stabilisation** |
| Manuel seul | Faible | Nul à court terme, élevé à chaque régression | Non |

### Couverture
| Option | Retenue |
|---|---|
| **Ciblée par couche** (moteurs 100 % bloquant, Application/Domain ≥ 90 %, API ≥ 70 %, ViewModels ≥ 60 %) | **Oui** |
| Globale 80 % | Non — masque une faiblesse sur le calcul derrière du code trivial |
| Aucun seuil | Non — rien n'alerte sur une branche de calcul jamais exécutée |

## Trade-off Analysis

Le choix structurant est **fidélité contre vitesse** sur l'intégration : Express réel coûte quelques secondes par exécution mais fait des tests une preuve opposable en recette ; SQLite aurait été plus rapide et moins fiable — sur un logiciel de paiement, la fiabilité l'emporte. Pour le client, l'automatisation FlaUI est retenue mais **bornée** : trois parcours, écrits après stabilisation, sinon elle consommerait le délai en maintenance de tests cassés par chaque ajustement d'écran. Les seuils par couche coûtent un peu de configuration mais empêchent la seule tricherie facile de la couverture globale.

## Consequences

- **Plus facile** : la recette « calculs exacts » se démontre par le rapport de tests ; le jeu de démo est fiable par construction ; un changement de barème ou de formule est protégé par 17 cas golden.
- **Plus difficile** : SQL Server Express doit être installé sur tout poste qui exécute les tests d'intégration ; les tests FlaUI exigent une session Windows ouverte (pas de CI sans agent graphique) ; la discipline « tests d'abord » ralentit le premier jour et accélère tous les suivants.
- **À revisiter** : étendre FlaUI au-delà des 3 parcours ; passer l'intégration continue à Testcontainers si le dépôt migre vers des exécuteurs Linux.

## Action Items
1. [ ] Créer `tests/Gestindem.Domain.Tests`, `Application.Tests`, `Infrastructure.Tests`, `Api.Tests`, `Desktop.Tests` avec xUnit, FluentAssertions, NSubstitute, coverlet
2. [ ] Écrire les 17 cas golden ci-dessus **avant** `Gestindem.Application` (ils échouent, puis passent)
3. [ ] Script de création de la base `Gestindem_Test` + Respawn ; test d'immuabilité (principe 4)
4. [ ] Workflow GitHub Actions : `dotnet test` unitaire + couverture bloquante sur les moteurs
5. [ ] Après phase 4 : FlaUI sur les 3 parcours du walkthrough ; script de recette manuelle dérivé de `maquettes/walkthrough/rapport-walkthrough.md`
