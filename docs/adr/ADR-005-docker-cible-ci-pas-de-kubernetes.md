# ADR-005 : Docker limité à l'intégration continue ; pas de Kubernetes

**Status:** Accepted
**Date:** 2026-09-03
**Deciders:** Abdellatif (chef de projet / développeur)
**Related:** ADR-002 (couches), ADR-004 (tests : SQL Server Express réel)

## Context

Avant de préparer l'environnement de développement, la question a été posée : faut-il standardiser l'environnement avec Docker, et Kubernetes serait-il pertinent ? Les faits qui pèsent :

- Le client est une application **WPF** : une interface graphique Windows ne s'exécute pas dans un conteneur. Seuls l'API et la base sont conteneurisables.
- La cible de production est **un serveur Windows au CHR de Guelmim**, administré par une DSI hospitalière, avec un **installeur Windows et un guide d'installation exigés** par le cahier des charges (§7). Une DSI hospitalière exploite des services Windows et SQL Server ; rien n'indique qu'elle exploite Docker.
- SQL Server Express est retenu (D4) et les tests d'intégration doivent tourner contre le vrai moteur (ADR-004). SQL Server existe en conteneur **Linux** : même moteur T-SQL, mais collation par défaut, chemins et procédures de sauvegarde diffèrent de l'Express Windows de production.
- Un serveur, quelques centaines d'utilisateurs, aucune équipe d'exploitation, livraison en 5 jours après notification.
- L'intégration continue (GitHub Actions, ADR-004) doit exécuter les tests d'intégration à chaque push ; installer SQL Server Express sur un exécuteur à chaque exécution prend plusieurs minutes.

Principe adopté : **une technologie se justifie par un problème nommé**, jamais par sa popularité.

## Decision

1. **Docker est utilisé pour un seul problème nommé : exécuter les tests d'intégration en CI.** Le workflow GitHub Actions démarre un conteneur `mcr.microsoft.com/mssql/server` (édition Express via `MSSQL_PID=Express`) comme service, les tests `[Trait("Category","Integration")]` s'exécutent contre lui.
2. **Le développement local se fait sur .NET SDK + SQL Server Express installés nativement**, identiques à la production : ce que le développeur teste est ce que le CHR exploitera. Docker Desktop n'est **pas requis** sur le poste ; il pourra être installé plus tard, uniquement pour rejouer la CI en local (`act`) ou pour une base jetable, sans devenir une dépendance du projet.
3. **La livraison ne contient aucun conteneur** : API en service Windows, base SQL Server Express, client WPF, installeur unique + guide (§7).
4. **Kubernetes n'est pas utilisé** sur ce projet. Il n'y a pas de problème d'orchestration, de mise à l'échelle ni de haute disponibilité à résoudre. Cette décision est prise pour ne pas rouvrir le débat ; elle n'empêche pas un apprentissage personnel ultérieur, hors périmètre client.

## Options Considered

### Docker
| Option | Problème résolu | Coût | Retenue |
|---|---|---|---|
| **Ciblé CI** | tests d'intégration reproductibles à chaque push | un fichier de workflow ; conteneur Linux ≈ fidèle (écarts documentés) | **Oui** |
| Aucun Docker | — | CI lente (installation d'Express à chaque exécution) ou tests d'intégration hors CI, donc oubliés | Non |
| Docker partout (dev + livraison) | environnement identique partout | impose Docker à la DSI ; contredit l'installeur exigé ; WPF hors conteneur de toute façon | Non |

### Kubernetes
| Option | Problème résolu | Coût | Retenue |
|---|---|---|---|
| **Non** | aucun problème à résoudre (un serveur, un service) | — | **Oui** |
| Laboratoire personnel plus tard | apprentissage | hors périmètre, après livraison | Possible, non planifié |
| Intégrer maintenant | — | cluster, stockage persistant pour la base, secrets, certificats, réseau — à apprendre avant une livraison en 5 jours | Non |

## Trade-off Analysis

Le seul compromis réel est la **fidélité du conteneur SQL Server Linux** en CI par rapport à l'Express Windows de production : même moteur, mêmes contraintes, mêmes plans ; écarts sur la collation par défaut (à fixer explicitement dans les migrations : `French_CI_AS`), les chemins de sauvegarde (non testés en CI) et l'absence de FILESTREAM (non utilisé). En échange : une CI de moins d'une minute qui exécute *tous* les tests, y compris l'immuabilité et les contraintes d'unicité d'ADR-003. La fidélité totale reste garantie localement par l'Express natif du poste de développement.

Kubernetes apporterait mise à l'échelle et auto-réparation à un système qui n'a besoin ni de l'une ni de l'autre, contre plusieurs jours d'apprentissage et une plateforme que le CHR n'exploiterait pas. Le meilleur moment pour l'apprendre est un projet qui en a le besoin — ou un laboratoire personnel sans échéance.

## Consequences

- **Plus facile** : environnement de développement simple (deux installations), production identique au poste de développement, CI complète et rapide, installeur conforme au cahier des charges.
- **Plus difficile** : SQL Server Express doit être installé sur chaque poste de développement (une fois) ; la CI ne teste pas les procédures de sauvegarde/restauration Windows — elles sont testées manuellement en recette (§9 : « sauvegarde et restauration opérationnelles »).
- **À revisiter** : si le CHR ou la direction régionale demandait un hébergement centralisé multi-sites avec haute disponibilité, un ADR dédié réévaluerait la conteneurisation de l'API — sans toucher au code, l'API étant sans état (ADR-002).

## Action Items
1. [ ] Installer localement : .NET SDK (LTS courant), SQL Server Express + SQL Server Management Studio (ou Azure Data Studio), Git — selon l'inventaire du poste
2. [ ] Fixer la collation `French_CI_AS` dans la première migration (fidélité CI ↔ prod)
3. [ ] Workflow GitHub Actions avec service SQL Server (`MSSQL_PID=Express`) pour les tests d'intégration
4. [ ] Livraison : API en service Windows + installeur (ADR à venir sur le format d'installeur : MSIX vs Inno Setup vs WiX)
