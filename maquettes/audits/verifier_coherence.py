# -*- coding: utf-8 -*-
"""Audit D — vérification mécanique de la cohérence des 24 maquettes.

Ce que fait ce script (et pourquoi) :
  1. Couleurs : toute couleur hexadécimale utilisée est comparée à la palette documentée
     dans la planche Identité + les tokens sémantiques listés ci-dessous. Une couleur
     inconnue est soit une dérive, soit un token à documenter — dans les deux cas un constat.
  2. Tailles de texte : la règle F-06 impose >= 12 px (11 px toléré pour les libellés en
     capitales). Tout font-size inférieur est listé.
  3. Composants : les boutons et badges sont regroupés par « signature de style ». Plusieurs
     signatures pour un même rôle = un composant qui dérive d'un écran à l'autre.
  4. Barre latérale et barre supérieure : leur HTML est comparé entre écrans après
     neutralisation de l'élément actif. Toute différence est signalée.
Usage : python verifier_coherence.py  (écrit coherence.md à côté du script)
"""
import io, os, re, glob, hashlib
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "lot1", "*.dc.html")) + glob.glob(os.path.join(ROOT, "lot2", "*.dc.html")))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coherence.md")

# --- Palette de référence (planche Identité + tokens sémantiques documentés) ---
PALETTE = {
    # marque et neutres (Identité)
    "#0B2E29": "encre teal", "#10554A": "primaire", "#B98A2F": "or (signature)", "#EDF4F1": "teinte claire",
    "#182420": "texte", "#61706A": "atténué", "#DBE3DE": "bordure", "#ECF1EE": "fond",
    "#5C6B64": "gris secondaire (4,9:1 sur fond)", "#8F6A1F": "or foncé (texte sur fond clair)", "#8BA39A": "libellés sur fond sombre", "#3A4741": "texte de libellé",
    "#C9D3CD": "bordure de champ", "#E7EDE9": "piste / désactivé", "#E9EEEA": "séparateur", "#E8EDEA": "badge neutre fond",
    "#EDF1EE": "bordure de ligne", "#F4F7F5": "cellule hors mois", "#F6F9F7": "surface secondaire", "#AEB9B2": "texte grisé",
    "#FFFFFF": "blanc", "#7E968D": "sidebar sous-titre", "#9DB8AF": "connexion eyebrow", "#C9D8D1": "connexion texte",
    "#B9CCC5": "sidebar texte", "#DCEBE6": "avatar fond", "#3A5C52": "info texte", "#5B6660": "badge neutre texte",
    # types d'indemnité (palette validée daltonisme)
    "#0A8467": "type Garde", "#D97706": "type Astreinte", "#2563EB": "type Permanence", "#C2255C": "type Déplacement",
    # statuts
    "#E4F2E9": "statut ok fond", "#17663F": "statut ok texte", "#C5E3CF": "alerte ok bordure",
    "#FBEEDC": "statut attente fond", "#92400E": "statut attente texte", "#F1D9B4": "alerte warn bordure", "#7A5210": "alerte warn texte",
    "#FADEDC": "statut rejet fond", "#A61B1B": "statut rejet texte", "#EFC4C0": "alerte err bordure", "#7A1A1A": "alerte err texte",
    "#E0B4B0": "bouton danger bordure", "#B3261E": "pastille notification", "#D8564C": "cellule doublon bordure", "#FDF3F2": "cellule doublon fond",
    # toasts (fond sombre)
    "#0F3B33": "toast fond", "#7CD4B4": "toast accent", "#FFC9C4": "toast erreur accent",
}
ALLOWED_11PX = True  # 11 px toléré pour les libellés en capitales (letter-spacing)

def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()

def short(p):
    return os.path.basename(p)

report = ["# Audit D — cohérence mécanique des maquettes", "",
          "Généré par `verifier_coherence.py` sur %d planches. Chaque constat est vérifiable en rouvrant le fichier cité." % len(FILES), ""]

# ---------------------------------------------------------------- 1. couleurs
color_use = defaultdict(lambda: defaultdict(int))
for p in FILES:
    for c in re.findall(r"#[0-9A-Fa-f]{6}\b", read(p)):
        color_use[c.upper()][short(p)] += 1
unknown = {c: u for c, u in color_use.items() if c not in PALETTE}
report += ["## 1. Couleurs hors palette documentée", ""]
if unknown:
    report += ["| Couleur | Occurrences | Fichiers |", "|---|---|---|"]
    for c, u in sorted(unknown.items(), key=lambda kv: -sum(kv[1].values())):
        report.append("| `%s` | %d | %s |" % (c, sum(u.values()), ", ".join("%s (%d)" % kv for kv in sorted(u.items()))))
else:
    report.append("Aucune : toutes les couleurs utilisées sont documentées.")
report += ["", "Palette documentée : %d couleurs · utilisées : %d · inconnues : %d" % (len(PALETTE), len(color_use), len(unknown)), ""]

# ---------------------------------------------------------------- 2. tailles
report += ["## 2. Tailles de texte sous le seuil (règle F-06 : ≥ 12 px, 11 px toléré en capitales)", ""]
small = []
for p in FILES:
    html = read(p)
    for m in re.finditer(r'font-size: (\d+(?:\.\d+)?)px', html):
        size = float(m.group(1))
        if size < 12:
            ctx = html[m.start():m.start() + 220]
            caps = "text-transform: uppercase" in ctx or "letter-spacing" in ctx
            numeric_badge = "font-weight: 700; display: flex" in ctx  # compteur de notifications (1-2 chiffres)
            if size < 11 or not (ALLOWED_11PX and (caps or numeric_badge) and size >= 11):
                small.append((short(p), size, "capitales" if caps else "texte courant"))
svg_small = []
for p in FILES:
    for m in re.finditer(r'font-size="(\d+(?:\.\d+)?)"', read(p)):
        if float(m.group(1)) < 11.5:
            svg_small.append((short(p), float(m.group(1))))
if small or svg_small:
    cnt = Counter((f, s, k) for f, s, k in small)
    report += ["| Fichier | Taille | Contexte | Occurrences |", "|---|---|---|---|"]
    for (f, s, k), n in sorted(cnt.items()):
        report.append("| %s | %s px | %s | %d |" % (f, s, k, n))
    for f, s in sorted(set(svg_small)):
        report.append("| %s | %s (SVG) | graphique | — |" % (f, s))
else:
    report.append("Aucune taille sous le seuil.")
report.append("")

# ---------------------------------------------------------------- 3. composants
def norm_style(style):
    style = re.sub(r"\s+", " ", style)
    style = re.sub(r"(padding|width|min-width|height|flex-grow|flex|margin[^;]*|justify-content|text-align|white-space): [^;]+;?", "", style)
    style = re.sub(r";\s*;", ";", style)
    return re.sub(r"\s+", " ", style).strip()

def group(pattern, label, role):
    sigs = defaultdict(set)
    for p in FILES:
        for m in re.finditer(pattern, read(p), flags=re.S):
            sigs[norm_style(m.group(1))].add(short(p))
    report.append("### %s — %d signature(s) de style" % (label, len(sigs)))
    if len(sigs) > 1:
        for sig, files in sorted(sigs.items(), key=lambda kv: -len(kv[1])):
            report.append("- `%s` — %d fichier(s) : %s" % (sig[:140], len(files), ", ".join(sorted(files))[:300]))
    else:
        report.append("- une seule signature : composant cohérent sur tous les écrans")
    report.append("")

report += ["## 3. Composants : un rôle = une signature de style ?", ""]
group(r'<button style="([^"]*background: #10554A[^"]*)"', "Bouton primaire", "primary")
group(r'<button style="([^"]*background: #FFFFFF; border: 1px solid #C9D3CD[^"]*)"', "Bouton secondaire", "secondary")
group(r'<span style="([^"]*border-radius: 20px[^"]*)">(?:Validé|Rejeté|En attente|En validation|En vérification|Actif|Clôturée|En cours|À clôturer|Prêt pour paiement|Brouillon|Désactivé|Ouverte|Calculé|À recalculer)</span>', "Badge de statut (padding neutralisé)", "badge")
group(r'<div style="([^"]*height: 42px; border: 1px solid #C9D3CD; border-radius: 8px[^"]*)"', "Champ de formulaire", "field")

# ---------------------------------------------------------------- 4. sidebar / topbar
def block(html, start, end):
    i = html.find(start); j = html.find(end, i)
    return html[i:j] if i >= 0 and j >= 0 else None

def neutral_sidebar(s):
    s = s.replace(' background: rgba(255,255,255,0.11);', '').replace('stroke="#FFFFFF"', 'stroke="#B9CCC5"')
    s = s.replace('font-weight: 600; color: #FFFFFF;', 'color: #B9CCC5;').replace('fill="#0B2E29"', 'fill="#0B2E29"')
    s = re.sub(r'>1[12]</span>', '>N</span>', s)  # badge validation 12/11
    s = re.sub(r'\s*<span style="min-width: 18px;[^>]*>N</span>', '', s)  # badge absent (état vide)
    return re.sub(r"\s+", " ", s)

report += ["## 4. Barre latérale et barre supérieure identiques ?", ""]
side = defaultdict(list); top = defaultdict(list)
for p in FILES:
    html = read(p)
    sb = block(html, "<!-- ===== Barre latérale ===== -->", "<!-- ===== Zone principale ===== -->")
    if sb is None:
        report.append("- %s : pas de barre latérale (écran plein : Connexion / Identité)" % short(p)); continue
    side[hashlib.md5(neutral_sidebar(sb).encode("utf-8")).hexdigest()[:8]].append(short(p))
    tb = block(html, "<!-- Barre supérieure -->", "<!-- Contenu -->")
    if tb:
        t = re.sub(r'(<span style="font-size: 13px; color: #5C6B64;">)[^<]*(</span>)', r'\1…\2', tb)  # texte de recherche
        t = re.sub(r'>[A-Z]{2}</div>', '>XX</div>', t)
        t = re.sub(r'>(N\. El Fassi|A\. Tazi|H\. Bouzid|M\. Raji)</span>', '>Nom</span>', t)
        t = re.sub(r'>(Validateur|Agent de saisie|Administrateur|Consultation)</span>', '>Rôle</span>', t)
        t = re.sub(r"\s+", " ", t)
        top[hashlib.md5(t.encode("utf-8")).hexdigest()[:8]].append(short(p))
report.append("- Barre latérale : %d variante(s) après neutralisation de l'élément actif" % len(side))
for h, fs in side.items():
    report.append("  - `%s` : %s" % (h, ", ".join(fs)))
report.append("- Barre supérieure : %d variante(s) après neutralisation du nom, du rôle et du texte de recherche" % len(top))
for h, fs in top.items():
    report.append("  - `%s` : %s" % (h, ", ".join(fs)))
report.append("")

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("rapport écrit :", OUT)
print("\n".join(report))
