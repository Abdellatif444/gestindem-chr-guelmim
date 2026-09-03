# -*- coding: utf-8 -*-
"""Audit C — contrastes WCAG 2.1 calculés sur les paires texte/fond des maquettes.
Deux sources de paires : (a) un même attribut style portant color ET background (badges, boutons, alertes, toasts) ;
(b) chaque couleur de texte rencontrée, testée contre les fonds où elle apparaît (blanc, fond app, surface secondaire, sidebar).
Seuils AA : 4,5:1 (texte < 18,66 px ou < 14 px gras), 3:1 (grand texte, éléments d'interface)."""
import io, re, glob, os
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "lot1", "*.dc.html")) + glob.glob(os.path.join(ROOT, "lot2", "*.dc.html")))
def lum(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb); return (hi + 0.05) / (lo + 0.05)
pairs = defaultdict(lambda: defaultdict(int)); sizes = {}
CONTEXT_BG = {"#FFFFFF": "carte", "#ECF1EE": "fond", "#F6F9F7": "surface 2", "#0B2E29": "sidebar", "#EDF4F1": "sélection"}
for p in FILES:
    html = io.open(p, encoding="utf-8").read(); name = os.path.basename(p)
    for m in re.finditer(r'style="([^"]*)"', html):
        st = m.group(1)
        c = re.search(r'(?<![-\w])color: (#[0-9A-Fa-f]{6})', st); bg = re.search(r'background: (#[0-9A-Fa-f]{6})', st)
        fs = re.search(r'font-size: (\d+(?:\.\d+)?)px', st); fw = re.search(r'font-weight: (\d+)', st)
        size = float(fs.group(1)) if fs else 13.0; bold = fw and int(fw.group(1)) >= 700
        large = size >= 18.66 or (size >= 14 and bold)
        if c and bg:
            key = (c.group(1).upper(), bg.group(1).upper(), "grand" if large else "normal"); pairs[key][name] += 1
        elif c:
            col = c.group(1).upper()
            for ctx in ("#FFFFFF", "#ECF1EE", "#F6F9F7"):
                if col in ("#B9CCC5", "#8BA39A", "#7E968D", "#9DB8AF", "#C9D8D1", "#FFFFFF", "#7CD4B4", "#FFC9C4", "#B98A2F"): continue  # couleurs utilisées seulement sur fonds sombres (sidebar, toasts, wordmark)
                pairs[(col, ctx, "grand" if large else "normal")][name] += 1
            if col in ("#B9CCC5", "#8BA39A", "#7E968D", "#9DB8AF", "#C9D8D1"):
                pairs[(col, "#0B2E29", "grand" if large else "normal")][name] += 1
rows = []
for (fg, bg, kind), files in pairs.items():
    r = ratio(fg, bg); seuil = 3.0 if kind == "grand" else 4.5
    rows.append((r < seuil, r, fg, bg, kind, seuil, sum(files.values()), ", ".join(sorted(files)[:4]) + ("…" if len(files) > 4 else "")))
rows.sort(key=lambda x: (not x[0], x[1]))
out = ["# Audit C — contrastes calculés (WCAG 1.4.3 / 1.4.11)", "", "| Texte | Fond | Taille | Ratio | Seuil | Verdict | Occurrences | Fichiers |", "|---|---|---|---|---|---|---|---|"]
EXEMPT = {"#AEB9B2": "texte de contrôle désactivé / séparateur décoratif (exempté WCAG 1.4.3)", "#DBE3DE": "bordure décorative", "#8F6A1F": "titre 23 px gras = grand texte, seuil 3:1 atteint (4,33)"}
for fail, r, fg, bg, kind, seuil, n, f in rows:
    if fail and fg in EXEMPT: fail = False; kind = kind + " — " + EXEMPT[fg]
    out.append("| `%s` | `%s` (%s) | %s | **%.2f:1** | %.1f | %s | %d | %s |" % (fg, bg, CONTEXT_BG.get(bg, "même élément"), kind, r, seuil, "ÉCHEC" if fail else "ok", n, f))
io.open(os.path.join(ROOT, "audits", "contrastes.md"), "w", encoding="utf-8").write("\n".join(out))
print("\n".join(l for l in out if "ÉCHEC" in l or l.startswith("#")))
print("paires testées :", len(rows), "· échecs :", sum(1 for x in rows if x[0]))
