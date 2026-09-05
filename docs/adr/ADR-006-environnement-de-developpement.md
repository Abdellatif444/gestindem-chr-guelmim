# ADR-006 : Environnement de développement

**Status:** Accepted
**Date:** 2026-09-04
**Deciders:** Abdellatif (chef de projet / développeur)
**Related:** ADR-002 (couches), ADR-004 (tests sur SQL Server Express réel), ADR-005 (pas de Docker en local)

## Context

Le poste de développement (Windows 11) ne disposait d'aucun SDK .NET ni d'instance SQL Server (inventaire du 2026-09-04 : `dotnet --list-sdks` vide, `Get-Service MSSQL*` vide, Git 2.53 présent). L'environnement doit être **reproductible** — la même procédure servira de base au guide d'installation exigé par le cahier des charges (§7) — et **fidèle à la production** (ADR-005 : développement sur les mêmes composants que le CHR exploitera).

## Decision

Installation par **winget** (gestionnaire de paquets intégré à Windows), une commande par composant, sans téléchargement manuel :

| Composant | Paquet winget | Version installée | Justification |
|---|---|---|---|
| SDK .NET | `Microsoft.DotNet.SDK.10` | 10.0.400 | **LTS**, supportée jusqu'en novembre 2028. .NET 8 (LTS) sort du support en novembre 2026, deux mois après la livraison : exclu. |
| SQL Server | `Microsoft.SQLServer.2022.Express` | 16.0.1000.6 RTM, instance `SQLEXPRESS`, moteur seul, authentification Windows | Édition gratuite (10 Go/base, bien au-delà du besoin), mûre, répandue dans les DSI hospitalières ; identique à la cible de production. 2025 Express existe mais moins familier aux équipes d'exploitation. |
| Administration | `Microsoft.SQLServerManagementStudio.21` (+ pilote ODBC 17) | 21.6.17 | Voir les tables et exécuter des requêtes à la main — indispensable pour comprendre ce que produisent les migrations EF Core. |
| Git | déjà présent | 2.53 | — |
| Docker | **non installé** | — | ADR-005 : Docker ne sert qu'en CI. |

Règles retenues :
1. **Service SQL Server en démarrage automatique** (état par défaut) : les tests d'intégration supposent une base disponible ; ~500 Mo de RAM au repos sur ce poste, acceptable. Option documentée pour plafonner la mémoire (`max server memory` = 512 Mo) ou passer le service en manuel avec `Start-Service` avant une session.
2. **Chaîne de connexion de développement** : `Server=localhost\SQLEXPRESS;Database=Gestindem;Trusted_Connection=True;TrustServerCertificate=True;` — base `Gestindem_Test` pour l'intégration (ADR-004). Jamais de chaîne en dur dans le code : `appsettings.Development.json` (hors dépôt pour les valeurs sensibles) ou `dotnet user-secrets`.
3. **Collation** `French_CI_AS` fixée par la première migration (fidélité CI ↔ prod, ADR-005).
4. **Médias d'installation conservés** : `C:\SQL2022\Express_ENU` (installeur Express hors ligne) — à copier dans le kit de livraison pour un CHR sans accès Internet ; appliquer la dernière mise à jour cumulative avant mise en production.
5. **Mise à jour** : `winget upgrade --id <paquet>` ; les versions mineures du SDK 10 sont adoptées au fil de l'eau, un changement de version majeure ferait l'objet d'un ADR.

## Options Considered

| Option | Retenue | Raison |
|---|---|---|
| **winget + composants natifs** | **Oui** | reproductible, scriptable, identique à la prod, une ligne par composant dans le guide d'installation |
| Installeurs téléchargés à la main | Non | non reproductible, versions non tracées |
| Visual Studio 2022/2026 Community | Non pour l'instant | le SDK + un éditeur suffisent ; VS pourra être ajouté pour le concepteur XAML (WPF) si le besoin apparaît — décision locale, sans impact sur le projet |
| SQL Server dans Docker en local | Non | ADR-005 |

## Consequences

- **Plus facile** : n'importe quel poste se prépare en quatre commandes ; le guide d'installation du CHR réutilise la même liste ; les tests d'intégration tournent contre le vrai moteur dès le premier jour.
- **Plus difficile / à surveiller** : ~500 Mo de RAM occupés en permanence par SQL Server ; SSMS pèse ~1 Go ; le SDK doit être mis à jour avec les correctifs de sécurité mensuels.
- **À revisiter** : ajout de Visual Studio si l'écriture du XAML à la main devient un frein ; passage à .NET 12 LTS (novembre 2027) après la fin du projet.

## Action Items
1. [ ] Créer la solution (script `scripts/creer-solution.ps1`, 11 projets, règle de dépendance par références de projets)
2. [ ] `Directory.Build.props` : `Nullable`, `TreatWarningsAsErrors`, `ImplicitUsings`, version C# — communs à tous les projets
3. [ ] `appsettings.Development.json` avec la chaîne de connexion locale ; `.gitignore` déjà prêt (`bin/`, `obj/`, `.vs/`, `*.user`)
