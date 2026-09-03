# Audit D — cohérence mécanique des maquettes

Généré par `verifier_coherence.py` sur 29 planches. Chaque constat est vérifiable en rouvrant le fichier cité.

## 1. Couleurs hors palette documentée

Aucune : toutes les couleurs utilisées sont documentées.

Palette documentée : 50 couleurs · utilisées : 49 · inconnues : 0

## 2. Tailles de texte sous le seuil (règle F-06 : ≥ 12 px, 11 px toléré en capitales)

Aucune taille sous le seuil.

## 3. Composants : un rôle = une signature de style ?

### Bouton primaire — 3 signature(s) de style
- `background: #10554A; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #FFFFFF; font-family: 'IBM Plex Sans', 'Seg` — 20 fichier(s) : Administration.dc.html, Baremes.dc.html, Calcul.dc.html, Etats.dc.html, MissionCloturee.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, MotDePasse.dc.html, Personnel.dc.html, PersonnelImportErreur.dc.html, Planning.dc.html, PlanningEnregistre.dc.html,
- `background: #10554A; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #FFFFFF; font-family: 'IBM Plex Sans', 'Seg` — 11 fichier(s) : Identite.dc.html, MissionCree.dc.html, MissionSaisie.dc.html, Missions.dc.html, Personnel.dc.html, PersonnelImportErreur.dc.html, Validation.dc.html, ValidationConfirm.dc.html, ValidationLignes.dc.html, ValidationRejete.dc.html, ValidationSucces.dc.html
- `background: #10554A; color: #FFFFFF; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; font-family: 'IBM Plex Sans', 'Seg` — 1 fichier(s) : Connexion.dc.html

### Bouton secondaire — 2 signature(s) de style
- `background: #FFFFFF; border: 1px solid #C9D3CD; border-radius: 8px; font-size: 13px; font-weight: 600; color: #182420; font-family: 'IBM Ple` — 23 fichier(s) : Administration.dc.html, Baremes.dc.html, Calcul.dc.html, Main.dc.html, MissionCloturee.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, MotDePasse.dc.html, Notifications.dc.html, Personnel.dc.html, PersonnelImportErreur.dc.html, Planning.dc.html, Plann
- `background: #FFFFFF; border: 1px solid #C9D3CD; border-radius: 8px; font-size: 13px; font-weight: 600; color: #182420; font-family: 'IBM Ple` — 1 fichier(s) : Identite.dc.html

### Badge de statut (padding neutralisé) — 4 signature(s) de style
- `background: #FBEEDC; color: #92400E; font-size: 12px; font-weight: 600; border-radius: 20px;` — 15 fichier(s) : Calcul.dc.html, Identite.dc.html, Main.dc.html, MissionCloturee.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, MotDePasse.dc.html, Notifications.dc.html, Validation.dc.html, ValidationConfirm.dc.html, ValidationLignes.dc.html, ValidationRejete.dc.htm
- `background: #E4F2E9; color: #17663F; font-size: 12px; font-weight: 600; border-radius: 20px;` — 15 fichier(s) : Administration.dc.html, Identite.dc.html, Main.dc.html, MissionCloturee.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, MotDePasse.dc.html, Notifications.dc.html, Personnel.dc.html, PersonnelImportErreur.dc.html, RestaurationConfirm.dc.html, Structure
- `background: #E8EDEA; color: #5B6660; font-size: 12px; font-weight: 600; border-radius: 20px;` — 9 fichier(s) : Administration.dc.html, Calcul.dc.html, Identite.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, RestaurationConfirm.dc.html, UtilisateurFiche.dc.html
- `background: #FADEDC; color: #A61B1B; font-size: 12px; font-weight: 600; border-radius: 20px;` — 4 fichier(s) : Identite.dc.html, Main.dc.html, MotDePasse.dc.html, Notifications.dc.html

### Champ de formulaire — 1 signature(s) de style
- une seule signature : composant cohérent sur tous les écrans

## 4. Barre latérale et barre supérieure identiques ?

- Connexion.dc.html : pas de barre latérale (écran plein : Connexion / Identité)
- Identite.dc.html : pas de barre latérale (écran plein : Connexion / Identité)
- Barre latérale : 1 variante(s) après neutralisation de l'élément actif
  - `1c4fcae2` : Main.dc.html, Planning.dc.html, Validation.dc.html, Administration.dc.html, Baremes.dc.html, Calcul.dc.html, Etats.dc.html, MissionCloturee.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, MotDePasse.dc.html, Notifications.dc.html, Personnel.dc.html, PersonnelImportErreur.dc.html, PlanningEnregistre.dc.html, PlanningSaisie.dc.html, RestaurationConfirm.dc.html, Statistiques.dc.html, Structures.dc.html, UtilisateurFiche.dc.html, ValidationConfirm.dc.html, ValidationLignes.dc.html, ValidationRejete.dc.html, ValidationSucces.dc.html, ValidationVide.dc.html
- Barre supérieure : 2 variante(s) après neutralisation du nom, du rôle et du texte de recherche
  - `c9fabcbd` : Main.dc.html, Validation.dc.html, Administration.dc.html, Baremes.dc.html, Calcul.dc.html, Etats.dc.html, MissionCloturee.dc.html, MissionCree.dc.html, MissionPlafonnee.dc.html, MissionSaisie.dc.html, Missions.dc.html, MotDePasse.dc.html, Notifications.dc.html, Personnel.dc.html, PersonnelImportErreur.dc.html, RestaurationConfirm.dc.html, Statistiques.dc.html, Structures.dc.html, UtilisateurFiche.dc.html, ValidationConfirm.dc.html, ValidationLignes.dc.html, ValidationRejete.dc.html, ValidationSucces.dc.html, ValidationVide.dc.html
  - `7e8cbe62` : Planning.dc.html, PlanningEnregistre.dc.html, PlanningSaisie.dc.html
