# Carte des parcours — GESTINDEM (état des maquettes au 2026-09-02)

Un nœud = un écran ou un état visible (nom du fichier de capture). Une flèche = une action, étiquetée par le libellé exact. Les nœuds rouges n'ont pas de capture : c'est un résultat d'action qui n'est pas encore dessiné.

```mermaid
flowchart LR
  classDef absent fill:#FADEDC,stroke:#A61B1B,color:#7A1A1A
  classDef etat fill:#EDF4F1,stroke:#10554A,color:#10554A

  Connexion -->|Se connecter| Main

  subgraph S1 [S1 — Agent de saisie : saisir les gardes d'août, Urgences]
    Main -->|Sidebar : Plannings| Planning
    Planning -->|‹ › mois, Service, Type, Agent| Planning
    Planning -->|Nouvelle saisie| PlanningSaisie:::etat
    Planning -->|Importer Excel| Planning_Import:::absent
    Planning -->|Corriger, bandeau doublon| Planning_Doublon:::absent
    Planning -.->|Clic sur une case du calendrier| Planning_Case??:::absent
    PlanningSaisie -->|Agent, date, durée saisis, doublon détecté| PlanningSaisie
    PlanningSaisie -->|Voir la saisie existante| Planning_Existante:::absent
    PlanningSaisie -->|Annuler| Planning
    PlanningSaisie -->|Enregistrer la garde| PlanningEnregistre:::etat
    PlanningEnregistre -->|Saisir le 14/08 →| PlanningSaisie
    PlanningEnregistre -.->|Fin du mois : et ensuite ?| Planning_Cloture??:::absent
  end

  subgraph S2 [S2 — Agent de saisie : ordre de mission Dr Saidi, Agadir, 2 jours]
    Main -->|Sidebar : Missions| Missions
    Missions -->|Toutes, En cours, À valider, Clôturées| Missions
    Missions -->|Nouvel ordre de mission| MissionSaisie:::etat
    MissionSaisie -->|Champs saisis, calcul prévisionnel mis à jour| MissionSaisie
    MissionSaisie -->|Annuler| Missions
    MissionSaisie -->|Créer l'ordre de mission| Missions_Cree:::absent
    Missions -->|Sélectionner OM-2026-088| Missions
    Missions -->|Modifier| Missions_Modif:::absent
    Missions -->|Clôturer et envoyer au calcul| Missions_Cloture:::absent
    Missions -->|Historique complet des déplacements| Missions_Historique:::absent
  end

  subgraph S3 [S3 — Validateur : traiter LOT-2026-0142, puis tableau de bord]
    Main -->|Sidebar : Validation 12| Validation
    Main -.->|Clic sur 12 lots · 98 640 DH| Validation
    Validation -->|Sélectionner LOT-2026-0142| Validation
    Validation -->|Voir les 12 lignes du lot| Validation_Lignes:::absent
    Validation -->|Valider le lot| ValidationConfirm:::etat
    ValidationConfirm -->|Annuler| Validation
    ValidationConfirm -->|Confirmer la validation| ValidationSucces:::etat
    ValidationSucces -->|Annuler 5 min| Validation
    ValidationSucces -->|Dernier lot traité| ValidationVide:::etat
    Validation -->|Motif saisi puis Rejeter| Validation_Rejete:::absent
    ValidationVide -->|Voir les lots prêts pour paiement 24| Validation_Prets:::absent
    Validation -.->|Voir les lots prêts pour paiement, état normal| Validation_Prets
    ValidationSucces -->|Sidebar : Tableau de bord| Main
  end
```

## Lecture de la carte

| Nœud rouge | Signification | Constat |
|---|---|---|
| `Missions_Cree`, `Missions_Cloture`, `Missions_Modif` | Les trois actions de l'écran Missions n'ont pas de résultat dessiné | W-01 |
| `Validation_Lignes` | Le validateur ne peut pas voir les 12 lignes qu'il valide | W-02 |
| `Planning_Cloture??` | Rien n'indique à l'agent que le mois est terminé ni ce qui suit | W-03 |
| `Validation_Rejete` | Le résultat d'un rejet n'est pas dessiné | W-05 |
| `Validation_Prets` (flèche pointillée) | Les lots prêts pour paiement ne sont accessibles que depuis l'état vide | W-06 |
| `Planning_Case??` | On ignore si cliquer une case du calendrier ouvre la saisie | W-08 |
| `Planning_Import`, `Planning_Doublon`, `Planning_Existante`, `Missions_Historique` | Actions secondaires sans résultat dessiné | inventaire, tableau « après chaque action » |

Les nœuds verts (`PlanningSaisie`, `PlanningEnregistre`, `MissionSaisie`, `ValidationConfirm`, `ValidationSucces`, `ValidationVide`) sont les états produits par le mini-lot « saisie & états » : ils couvrent l'action principale de chaque scénario.
