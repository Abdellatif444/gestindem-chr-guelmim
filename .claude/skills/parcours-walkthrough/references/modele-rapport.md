# Modèle de rapport — parcours walkthrough

Utiliser ce gabarit tel quel (langue et conventions de l'utilisateur ; nombres avec espaces insécables).

```markdown
---
type: parcours-walkthrough
date: {AAAA-MM-JJ}
produit: {Produit}
scenarios: {n}
ecrans: {n}
constats-bloquants: {n}
constats-ralentissent: {n}
constats-genent: {n}
---

# Walkthrough — {Produit} : {liste courte des scénarios}

## Résumé
{3 à 5 phrases : les scénarios aboutissent-ils pour l'utilisateur type ? Où se situent les blocages ? Les trois corrections les plus rentables. Écrit pour quelqu'un qui ne lira que ce paragraphe.}

## Scénarios évalués
| # | Utilisateur type | Objectif | Étapes | Aboutit ? |
|---|---|---|---|---|

## Carte des parcours
{diagramme Mermaid, nœuds absents marqués}

## Parcours pas à pas
### Scénario {n} — {titre}
| Étape | Écran | Action correcte | Q1 quoi faire | Q2 visible | Q3 la bonne | Q4 retour | Constat |
|---|---|---|---|---|---|---|---|
{une ligne par étape ; ✓ / ✗ / ? ; la colonne Constat renvoie à un identifiant W-nn}

## Après chaque action, que voit l'utilisateur ?
| Écran | Action | Résultat visible dans les maquettes | Dessiné ? |
|---|---|---|---|
{toutes les actions primaires et secondaires des écrans du parcours ; « Dessiné ? » = oui / non / partiel. Les « non » sont la liste des états à produire.}

## Constats
### [{Bloquant|Ralentit|Gêne}] W-{nn} · {titre}
- **Type** : {ECRAN-ABSENT | RETOUR-ABSENT | ACTION-INVISIBLE | LIBELLE-AMBIGU | CONTEXTE-PERDU | VOCABULAIRE | CUL-DE-SAC | SANS-RETOUR-ARRIERE | CHARGE-MEMOIRE}
- **Où** : {scénario, étape, écran, élément}
- **Preuve** : {ce qui est visible, ou ce qui manque, sur la capture}
- **Effet sur l'utilisateur type** : {ce qu'il fait ou ne fait pas à ce moment}
- **Heuristique** : {Nielsen #n, Norman : …, Content #n — si applicable}
- **Correction proposée** : {concrète} · **Effort** : S/M/L

## Niveau parcours
- Transitions et conservation du contexte : …
- Charge mémoire entre écrans : …
- Vocabulaire d'un bout à l'autre : …
- Fin de parcours et suite proposée : …
- Sorties et retours arrière : …

## Ce qui rend le parcours fluide (à conserver)
- [F-01] …

## Non évaluable sur captures statiques
{focus clavier, délais, animations, comportements au survol…}

## Trois corrections prioritaires
1. …
2. …
3. …
```

## Types de constats (identifiants stables)

| Type | Signification |
|---|---|
| ECRAN-ABSENT | Une étape du scénario n'a pas d'écran dessiné |
| RETOUR-ABSENT | Le résultat d'une action (succès, erreur, vide) n'est pas dessiné |
| ACTION-INVISIBLE | L'action correcte existe mais n'est pas là où l'utilisateur regarde, ou ne ressemble pas à une action |
| LIBELLE-AMBIGU | Le libellé ne permet pas de choisir la bonne action, ou une autre semble aussi plausible |
| CONTEXTE-PERDU | Un changement d'écran fait perdre la période, la structure ou la sélection en cours |
| VOCABULAIRE | Un même concept porte deux noms sur le parcours |
| CUL-DE-SAC | Un écran ou un état sans action suivante ni sortie |
| SANS-RETOUR-ARRIERE | Impossible d'annuler ou de revenir sans perdre son travail |
| CHARGE-MEMOIRE | L'utilisateur doit retenir une information d'un écran à l'autre |
