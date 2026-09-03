# ADR-002 : Découpage en couches et localisation de la logique de calcul

**Status:** Accepted
**Date:** 2026-09-03
**Deciders:** Abdellatif (chef de projet / développeur)
**Supersedes / Related:** ADR-001 (prototype de référence)

## Context

Le cahier des charges CDC-GESTINDEM-2026 (§3) impose une architecture **API-first** : « la logique métier (calcul des indemnités, barèmes, règles) est centralisée dans une API REST ; les clients ne font qu'afficher les données et appeler l'API ; aucune logique de calcul n'est dupliquée ; aucun accès direct du client à la base ». Il recommande .NET (ASP.NET Core Web API, WPF, EF Core, SQL Server, JWT) et prévoit une **application mobile ultérieure** (.NET MAUI ou Flutter) consommant la même API.

Décisions déjà prises : client WPF (D3), SQL Server Express + EF Core (D4), prototype de 29 planches comme référence de l'interface (ADR-001). Les maquettes imposent deux comportements à prendre en compte : un **calcul prévisionnel mis à jour à chaque champ** (formulaire d'ordre de mission) et une **détection de doublon en direct** (formulaire de planning).

Forces en présence : conformité contractuelle et recette (§9 : « les calculs appliquent les barèmes paramétrés », « intégrité des calculs garantie par une couche métier unique ») ; délai de livraison très court (5 jours après notification) ; démonstration exigée ; réutilisation par un futur client mobile ; équipe d'une personne montant en compétence sur .NET.

## Decision

**Option A — monolithe modulaire côté API, client WPF léger, Clean Architecture.**

1. Toute la logique métier (moteurs de calcul garde/astreinte/permanence et déplacement, application des barèmes à date, plafonds, règles de validation, détection de doublons, workflow de validation, journal d'audit) vit dans l'API. Le client WPF n'a **aucune règle métier** : il affiche, saisit, appelle.
2. La solution est découpée selon la **règle de dépendance** (les dépendances pointent vers l'intérieur) :

```
Gestindem.Domain          entités, objets-valeurs, règles pures, interfaces        → (aucune dépendance)
Gestindem.Application     cas d'usage, moteurs de calcul, validation, ports       → Domain
Gestindem.Infrastructure  EF Core / SQL Server, exports Excel-PDF-CSV, sauvegardes → Application
Gestindem.Api             ASP.NET Core, JWT, endpoints REST versionnés, OpenAPI    → Application, Infrastructure
Gestindem.Contracts       DTO de requête/réponse partagés — ZÉRO logique          → (aucune dépendance)
Gestindem.Desktop         WPF MVVM, client HTTP typé                              → Contracts uniquement
tests/                    Domain.Tests, Application.Tests (moteurs en priorité), Api.Tests (intégration)
```

3. Le **calcul prévisionnel en direct** est servi par un endpoint de simulation (`POST /api/v1/deplacements/simulation`, `POST /api/v1/plannings/controle`) appelé par le client avec un délai de 300 ms après la dernière frappe : l'expérience « instantanée » des maquettes est préservée avec **un seul moteur de calcul**.
4. Le projet `Gestindem.Contracts` est le seul code partagé entre l'API et les clients — c'est le partage de DTO explicitement autorisé par le cahier des charges.

### Exigence complémentaire : backend réutilisable par un futur client mobile

Décision de l'utilisateur lors de l'arbitrage. Elle se traduit par des règles que l'API respecte **dès la première ligne de code** :

| Règle | Pourquoi |
|---|---|
| API **versionnée** (`/api/v1/…`) ; les changements incompatibles créent `/v2` | Un mobile déployé sur des téléphones ne se met pas à jour en même temps que l'API |
| **Aucune hypothèse sur le client** dans l'API : pas de HTML, pas de mise en forme, pas de libellés d'écran ; l'API renvoie des données et des codes d'erreur stables | Le mobile et le web afficheront différemment |
| Authentification **JWT sans état** avec jeton de rafraîchissement | Fonctionne pour desktop, mobile et web ; pas de session serveur |
| **Pagination, tri et filtres** normalisés sur toutes les listes (`?page=&size=&sort=&filtre=`) | Un écran mobile charge peu d'éléments à la fois |
| Contrat **OpenAPI** généré et versionné dans le dépôt ; les DTO de `Contracts` publiés en **paquet NuGet interne** | Un client MAUI référence le même paquet ; un client Flutter génère ses modèles depuis OpenAPI |
| Messages d'erreur **identifiés par un code** (`PLANNING_DOUBLON`, `BAREME_ABSENT_A_DATE`…) + texte FR ; structure prête pour d'autres langues | Le client choisit l'affichage ; l'arabe est possible plus tard sans toucher l'API |
| Endpoints **idempotents** pour les créations sensibles (clé d'idempotence sur la validation d'un lot) | Réseau mobile instable : un double envoi ne valide pas deux fois |
| Réponses **compactes** (pas de graphes d'objets profonds), dates en ISO 8601 UTC + fuseau, montants en décimal | Bande passante mobile, cohérence des calculs |

## Options Considered

### Option A : Monolithe modulaire API + client WPF léger (retenue)
| Dimension | Assessment |
|-----------|------------|
| Complexity | Low — une seule application serveur, un client d'affichage |
| Cost | Faible : un serveur (SQL Server Express + API) ; pas de licence |
| Scalability | Suffisante pour une région (quelques centaines d'utilisateurs) ; l'API sans état se réplique si besoin |
| Team familiarity | Bonne : parcours d'apprentissage linéaire (Domain → Application → API → WPF) |

**Pros :** conforme mot pour mot au cahier des charges ; un seul moteur de calcul à tester ; barèmes et audit centralisés ; l'API est déjà « le backend mobile » ; délai le plus court.
**Cons :** dépend du réseau du CHR (pas de hors-ligne) ; chaque simulation est un aller-retour HTTP (négligeable en réseau local, à surveiller en mobile).

### Option B : Bibliothèque métier partagée (NuGet) entre API et client
| Dimension | Assessment |
|-----------|------------|
| Complexity | Medium — versionnage du paquet, réplication des barèmes côté client |
| Cost | Faible |
| Scalability | Bonne |
| Team familiarity | Moyenne : deux contextes d'exécution du même code |

**Pros :** calcul prévisionnel local instantané ; fonctionne sans réseau pour la simulation.
**Cons :** « aucune logique dupliquée » n'est respecté que si tous les postes ont exactement la même version du paquet **et** les mêmes barèmes — c'est précisément le risque que le cahier des charges veut éliminer ; un client non mis à jour affiche un montant faux ; double surface de test.

### Option C : Client autonome (SQLite) avec synchronisation
| Dimension | Assessment |
|-----------|------------|
| Complexity | High — deux bases, résolution de conflits, files de synchronisation |
| Cost | Moyen (temps) |
| Scalability | Faible : la cohérence régionale (objectif n°1 du projet) devient difficile |
| Team familiarity | Faible |

**Pros :** mode hors-ligne complet.
**Cons :** contredit « base de données centralisée » et « aucun accès direct à la base » ; conflits de saisie entre postes ; + 5 à 10 jours ; audit fragmenté.

## Trade-off Analysis

Le compromis central est **réactivité locale (B, C) contre unicité de la logique (A)**. Le cahier des charges tranche explicitement pour l'unicité (§3.1, §6.3), et la recette la vérifiera. L'argument de réactivité de B est neutralisé par un endpoint de simulation en réseau local (latence de l'ordre de 20–50 ms, invisible avec un délai de saisie de 300 ms). Le hors-ligne de C n'est demandé nulle part ; s'il apparaissait pour le mobile, il se traiterait par un cache de lecture côté client, pas par une duplication du calcul. L'exigence de réutilisation mobile renforce A : plus l'API contient de métier, moins le futur mobile en réécrit.

## Consequences

- **Plus facile** : tests des moteurs de calcul en un seul endroit (priorité du PDF §8) ; démonstration avec un serveur et un poste ; ajout du mobile = un nouveau client, zéro réécriture ; conformité vérifiable en recette.
- **Plus difficile** : l'application ne fonctionne pas sans serveur — prévoir un message d'état réseau clair dans le client (Nielsen #1) et un poste serveur fiable au CHR ; la simulation « à chaque champ » demande un délai de saisie et une annulation des requêtes obsolètes côté client.
- **À revisiter** : si le CHR exige un mode hors-ligne, écrire un ADR dédié (cache de lecture + file d'envoi), sans remettre en cause l'unicité du calcul ; si la charge dépasse une région, envisager la réplication de l'API (sans état, donc simple).

## Action Items
1. [ ] ADR-003 — modèle de données (entités du PDF §5 affinées, historisation des barèmes, lots et workflow, journal d'audit) et endpoints REST v1 par module
2. [ ] ADR-004 — stratégie de tests (moteurs de calcul en priorité, jeux de cas « golden », tests d'intégration API)
3. [ ] Créer la solution `.NET` avec les 7 projets et la règle de dépendance vérifiée (références de projets **et** analyseur)
4. [ ] Générer OpenAPI dès le premier endpoint ; versionner `/api/v1`
5. [ ] Écrire le client HTTP typé WPF à partir de `Contracts` ; interdire toute référence de `Desktop` vers `Domain`/`Application`
