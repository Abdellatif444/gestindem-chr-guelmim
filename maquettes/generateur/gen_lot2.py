# -*- coding: utf-8 -*-
"""Génère les 4 premiers écrans du Lot 2 (Personnel, Structures, Baremes, Missions)
à partir d'un gabarit commun (sidebar + topbar identiques au Lot 1 validé)."""
import io, os

OUT = r"C:\Users\alibo\Desktop\lire\coding_Always\charges_idemnites\maquettes\lot2"
os.makedirs(OUT, exist_ok=True)

NB = "\u00A0"
SERIF = "'IBM Plex Serif', Georgia, serif"

KHATAM8 = ('<svg width="8" height="8" viewBox="0 0 24 24" fill="none" style="margin-right: 6px; vertical-align: -1px;" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="6.5" y="6.5" width="11" height="11" stroke="#B98A2F" stroke-width="2.2"></rect>'
    '<rect x="6.5" y="6.5" width="11" height="11" stroke="#B98A2F" stroke-width="2.2" transform="rotate(45 12 12)"></rect></svg>')

ICONS = {
    "dash": '<rect x="2" y="2" width="6" height="6" rx="1" stroke="{c}" stroke-width="1.5"></rect><rect x="10" y="2" width="6" height="6" rx="1" stroke="{c}" stroke-width="1.5"></rect><rect x="2" y="10" width="6" height="6" rx="1" stroke="{c}" stroke-width="1.5"></rect><rect x="10" y="10" width="6" height="6" rx="1" stroke="{c}" stroke-width="1.5"></rect>',
    "cal": '<rect x="2" y="3" width="14" height="13" rx="1.5" stroke="{c}" stroke-width="1.5"></rect><path d="M2 7 H16 M6 1.5 V4.5 M12 1.5 V4.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"></path>',
    "clock": '<circle cx="9" cy="9" r="7" stroke="{c}" stroke-width="1.5"></circle><path d="M9 5.5 V9 L11.5 11" stroke="{c}" stroke-width="1.5" stroke-linecap="round"></path>',
    "box": '<path d="M9 2 L15 5.5 V12.5 L9 16 L3 12.5 V5.5 Z" stroke="{c}" stroke-width="1.5" stroke-linejoin="round"></path><path d="M9 9 L15 5.5 M9 9 V16 M9 9 L3 5.5" stroke="{c}" stroke-width="1.2"></path>',
    "check": '<circle cx="9" cy="9" r="7" stroke="{c}" stroke-width="1.5"></circle><path d="M6 9.2 L8.2 11.4 L12.2 7" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>',
    "file": '<path d="M4 2 H11 L15 6 V16 H4 Z" stroke="{c}" stroke-width="1.5" stroke-linejoin="round"></path><path d="M7 9 H12 M7 12 H12" stroke="{c}" stroke-width="1.4" stroke-linecap="round"></path>',
    "bars": '<path d="M3 15 V9 M9 15 V4 M15 15 V7" stroke="{c}" stroke-width="1.8" stroke-linecap="round"></path>',
    "users": '<circle cx="6.5" cy="6" r="2.8" stroke="{c}" stroke-width="1.5"></circle><circle cx="12.5" cy="7" r="2.2" stroke="{c}" stroke-width="1.5"></circle><path d="M2 15 C2 12 4 10.5 6.5 10.5 C9 10.5 11 12 11 15 M12.5 11 C14.8 11 16 12.5 16 14.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"></path>',
    "building": '<path d="M3 16 V5 L9 2 L15 5 V16 M3 16 H15 M7 16 V12 H11 V16" stroke="{c}" stroke-width="1.5" stroke-linejoin="round"></path>',
    "sliders": '<path d="M3 5 H15 M3 9 H15 M3 13 H15" stroke="{c}" stroke-width="1.5" stroke-linecap="round"></path><circle cx="6.5" cy="5" r="1.6" fill="#0B2E29" stroke="{c}" stroke-width="1.4"></circle><circle cx="11.5" cy="9" r="1.6" fill="#0B2E29" stroke="{c}" stroke-width="1.4"></circle><circle cx="8" cy="13" r="1.6" fill="#0B2E29" stroke="{c}" stroke-width="1.4"></circle>',
    "shield": '<path d="M9 1.5 L15 4 V8.5 C15 12 12.6 14.8 9 16.5 C5.4 14.8 3 12 3 8.5 V4 Z" stroke="{c}" stroke-width="1.5" stroke-linejoin="round"></path>',
}

NAV = [
    ("group", "OPÉRATIONS"),
    ("dash", "Tableau de bord", None),
    ("cal", "Plannings", None),
    ("clock", "Indemnités", None),
    ("box", "Missions", None),
    ("check", "Validation", "12"),
    ("group", "RESTITUTION"),
    ("file", "États &amp; rapports", None),
    ("bars", "Statistiques", None),
    ("group", "RÉFÉRENTIELS"),
    ("users", "Personnel", None),
    ("building", "Structures", None),
    ("sliders", "Barèmes", None),
    ("group", "SYSTÈME"),
    ("shield", "Administration", None),
]

def nav_html(active_label):
    out, first_group = [], True
    for item in NAV:
        if item[0] == "group":
            pad = "8px 10px 4px" if first_group else "14px 10px 4px"
            first_group = False
            out.append('      <div style="font-size: 11px; font-weight: 600; letter-spacing: 1.5px; color: #8BA39A; padding: %s;">%s%s</div>' % (pad, KHATAM8, item[1]))
            continue
        icon_key, label, badge = item
        active = (label == active_label)
        color = "#FFFFFF" if active else "#B9CCC5"
        icon = ICONS[icon_key].replace("{c}", color)
        span = '<span style="font-size: 13.5px;%s color: %s;">%s</span>' % (" font-weight: 600;" if active else "", color, label)
        bg = " background: rgba(255,255,255,0.11);" if active else ""
        if badge:
            out.append('''      <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; border-radius: 7px;%s">
        <div style="display: flex; align-items: center; gap: 10px;">
          <svg width="17" height="17" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">%s</svg>
          %s
        </div>
        <span style="min-width: 18px; height: 18px; border-radius: 9px; background: #B98A2F; color: #0B2E29; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; padding: 0 5px; box-sizing: border-box;">%s</span>
      </div>''' % (bg, icon, span, badge))
        else:
            out.append('''      <div style="display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 7px;%s">
        <svg width="17" height="17" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">%s</svg>
        %s
      </div>''' % (bg, icon, span))
    return "\n".join(out)

SHELL = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@600;700&display=swap" rel="stylesheet">
  <style>
    body {{ margin: 0; font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif; color: #182420; font-variant-numeric: tabular-nums; }}
    a {{ color: #10554A; text-decoration: none; }}
    a:hover {{ color: #0B2E29; text-decoration: underline; }}
  </style>
</helmet>
<div style="width: 1440px; height: 900px; display: flex; background: #ECF1EE; overflow: hidden;">

  <!-- ===== Barre latérale ===== -->
  <div style="width: 236px; height: 900px; background: #0B2E29; display: flex; flex-direction: column; box-sizing: border-box; padding: 20px 14px; flex-shrink: 0;">
    <div style="display: flex; align-items: center; gap: 11px; padding: 4px 8px 18px 8px;">
      <svg width="34" height="34" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg" fill="none">
        <rect x="16" y="16" width="40" height="40" stroke="#B98A2F" stroke-width="3"></rect>
        <rect x="16" y="16" width="40" height="40" stroke="#B98A2F" stroke-width="3" transform="rotate(45 36 36)"></rect>
        <path d="M36 28 V44 M28 36 H44" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"></path>
      </svg>
      <div style="display: flex; flex-direction: column; gap: 1px;">
        <span style="font-family: {serif}; font-size: 15.5px; font-weight: 700; letter-spacing: 0.8px; color: #FFFFFF;">GESTIN<span style="color: #B98A2F;">DEM</span></span>
        <span style="font-size: 11px; color: #7E968D;">CHR Guelmim</span>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; gap: 2px; flex-grow: 1;">
{nav}
    </div>

    <div style="padding: 10px 10px 0; border-top: 1px solid rgba(255,255,255,0.09); font-size: 11.5px; color: #8BA39A;">v1.0 · Dernière sauvegarde 02:00</div>
  </div>

  <!-- ===== Zone principale ===== -->
  <div style="flex-grow: 1; display: flex; flex-direction: column; min-width: 0;">

    <!-- Barre supérieure -->
    <div style="height: 60px; background: #FFFFFF; border-bottom: 1px solid #DBE3DE; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; box-sizing: border-box; flex-shrink: 0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 8px; border: 1px solid #DBE3DE; border-radius: 8px; padding: 7px 12px; background: #F6F9F7;">
          <svg width="15" height="15" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 16 V5 L9 2 L15 5 V16 M3 16 H15" stroke="#61706A" stroke-width="1.5" stroke-linejoin="round"></path></svg>
          <span style="font-size: 13px; font-weight: 500; color: #182420;">CHR de Guelmim</span>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 4.5 L6 7.5 L9 4.5" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; border: 1px solid #DBE3DE; border-radius: 8px; padding: 7px 12px; background: #F6F9F7;">
          <svg width="15" height="15" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="3" width="14" height="13" rx="1.5" stroke="#61706A" stroke-width="1.5"></rect><path d="M2 7 H16 M6 1.5 V4.5 M12 1.5 V4.5" stroke="#61706A" stroke-width="1.5" stroke-linecap="round"></path></svg>
          <span style="font-size: 13px; font-weight: 500; color: #182420;">Août 2026</span>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 4.5 L6 7.5 L9 4.5" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </div>
      </div>
      <div style="display: flex; align-items: center; gap: 16px;">
        <div style="display: flex; align-items: center; gap: 8px; border: 1px solid #DBE3DE; border-radius: 8px; padding: 7px 12px; width: 240px; box-sizing: border-box;">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="7" cy="7" r="4.5" stroke="#66746D" stroke-width="1.5"></circle><path d="M10.5 10.5 L14 14" stroke="#66746D" stroke-width="1.5" stroke-linecap="round"></path></svg>
          <span style="font-size: 13px; color: #66746D;">{search}</span>
        </div>
        <div style="position: relative;">
          <svg width="19" height="19" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 2.5 C7 2.5 5.2 4.8 5.2 7.5 V10.5 L3.5 13.5 H16.5 L14.8 10.5 V7.5 C14.8 4.8 13 2.5 10 2.5 Z" stroke="#61706A" stroke-width="1.5" stroke-linejoin="round"></path><path d="M8.5 16 C8.8 16.9 9.3 17.3 10 17.3 C10.7 17.3 11.2 16.9 11.5 16" stroke="#61706A" stroke-width="1.5" stroke-linecap="round"></path></svg>
          <span style="position: absolute; top: -7px; right: -9px; min-width: 17px; height: 17px; padding: 0 4px; border-radius: 9px; background: #B3261E; color: #FFFFFF; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; border: 1.5px solid #FFFFFF; box-sizing: border-box;">3</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; padding-left: 16px; border-left: 1px solid #DBE3DE;">
          <div style="width: 34px; height: 34px; border-radius: 17px; background: #DCEBE6; color: #10554A; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{initials}</div>
          <div style="display: flex; flex-direction: column; gap: 1px;">
            <span style="font-size: 13px; font-weight: 600; color: #182420;">{user}</span>
            <span style="font-size: 12px; color: #61706A;">{role}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenu -->
    <div style="flex-grow: 1; padding: 18px 24px; display: flex; flex-direction: column; gap: 14px; box-sizing: border-box; overflow: hidden;">
{content}
    </div>
  </div>
</div>
</x-dc>
</body>
</html>
"""

def page_header(title, sub, buttons=""):
    return '''      <div style="display: flex; align-items: flex-end; justify-content: space-between;">
        <div style="display: flex; flex-direction: column; gap: 3px;">
          <div style="font-family: %s; font-size: 23px; font-weight: 700; color: #182420;">%s</div>
          <div style="font-size: 13px; color: #61706A;">%s</div>
        </div>
        <div style="display: flex; gap: 10px;">%s</div>
      </div>''' % (SERIF, title, sub, buttons)

def btn_primary(label, plus=True):
    icon = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 3 V13 M3 8 H13" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"></path></svg>' if plus else ''
    return '<button style="height: 38px; padding: 0 16px; background: #10554A; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #FFFFFF; font-family: \'IBM Plex Sans\', \'Segoe UI\', sans-serif; display: flex; align-items: center; gap: 8px; cursor: pointer;">%s%s</button>' % (icon, label)

def btn_secondary(label, icon=""):
    return '<button style="height: 38px; padding: 0 16px; background: #FFFFFF; border: 1px solid #C9D3CD; border-radius: 8px; font-size: 13px; font-weight: 600; color: #182420; font-family: \'IBM Plex Sans\', \'Segoe UI\', sans-serif; display: flex; align-items: center; gap: 8px; cursor: pointer;">%s%s</button>' % (icon, label)

def sel(label, value):
    return ('<div style="display: flex; align-items: center; gap: 7px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 8px; padding: 8px 12px;">'
        '<span style="font-size: 12px; color: #66746D;">%s</span>'
        '<span style="font-size: 13px; font-weight: 500; color: #182420;">%s</span>'
        '<svg width="11" height="11" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 4.5 L6 7.5 L9 4.5" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></div>') % (label, value)

def badge(text, kind):
    styles = {
        "ok": ("#E4F2E9", "#17663F"), "warn": ("#FBEEDC", "#92400E"),
        "err": ("#FADEDC", "#A61B1B"), "neutral": ("#E8EDEA", "#5B6660"),
        "info": ("#E3EBFC", "#1D4ED8"),
    }
    bg, fg = styles[kind]
    return '<span style="background: %s; color: %s; font-size: 12px; font-weight: 600; padding: 3px 9px; border-radius: 20px;">%s</span>' % (bg, fg, text)

IMPORT_ICON = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 10 V2 M8 2 L5 5 M8 2 L11 5 M2.5 13.5 H13.5" stroke="#182420" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>'

# ============================== PERSONNEL ==============================
personnel_rows = [
    ("M-04512", "Dr Y. Benali", "Médecin spécialiste", "A", "Urgences", True),
    ("M-04527", "Dr K. Saidi", "Médecin spécialiste", "A", "Réanimation", False),
    ("M-04533", "Dr M. El Idrissi", "Médecin généraliste", "B", "Chirurgie", False),
    ("M-04561", "Dr S. Ouazzani", "Médecin généraliste", "B", "Pédiatrie", False),
    ("M-04618", "Inf. R. Amrani", "Infirmier polyvalent", "C", "Urgences", False),
    ("M-04640", "Inf. L. Mansouri", "Infirmier anesthésiste", "C", "Réanimation", False),
    ("M-04702", "Tech. H. Drissi", "Technicien radiologie", "C", "Radiologie", False),
]

rows_html = []
for mat, nom, grade, grp, svc, selected in personnel_rows[:7]:
    style_extra = " background: #EDF4F1; box-shadow: inset 0 0 0 1.5px #10554A; border-radius: 8px;" if selected else " border-bottom: 1px solid #EDF1EE;"
    rows_html.append('''            <div style="display: grid; grid-template-columns: 80px 160px 160px 65px 110px 70px; gap: 8px; padding: 10px; font-size: 13px; align-items: center;%s">
              <span style="color: #61706A;">%s</span><span style="font-weight: 600; color: #182420;">%s</span><span style="color: #3A4741;">%s</span><span style="color: #3A4741;">Groupe %s</span><span style="color: #3A4741;">%s</span>
              <span>%s</span>
            </div>''' % (style_extra, mat, nom, grade, grp, svc, badge("Actif", "ok")))

PERSONNEL = page_header(
    "Personnel",
    "Référentiel des agents bénéficiaires — 248 agents actifs · classés par groupes déterminant les taux",
    btn_secondary("Importer depuis Excel", IMPORT_ICON) + btn_primary("Nouvel agent")) + """

      <div style="display: flex; align-items: center; gap: 10px;">
        """ + sel("Grade", "Tous") + sel("Groupe", "Tous") + sel("Service", "Tous") + """
        <span style="font-size: 12.5px; color: #66746D; margin-left: auto;">248 agents · filtre : aucun</span>
      </div>

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 8px;">
          <div style="display: grid; grid-template-columns: 80px 160px 160px 65px 110px 70px; gap: 8px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #66746D; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;">
            <span>Matricule</span><span>Nom</span><span>Grade</span><span>Groupe</span><span>Affectation</span><span>Statut</span>
          </div>
          <div style="display: flex; flex-direction: column;">
""" + "\n".join(rows_html) + """
          </div>
          <div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid #E9EEEA;">
            <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #61706A;">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 8 L6.5 11.5 L13 4.5" stroke="#17663F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path></svg>
              Dernier import Excel : 28/08/2026 — 12 agents ajoutés, 0 erreur
            </div>
            <div style="display: flex; align-items: center; gap: 12px;"><span style="font-size: 12px; color: #66746D;">7 agents affichés sur 248</span><div style="display: flex; align-items: center; gap: 6px;"><span style="width: 30px; height: 30px; border: 1px solid #DBE3DE; border-radius: 7px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.5 3 L4.5 6 L7.5 9" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span style="font-size: 12.5px; font-weight: 600; color: #182420; padding: 0 4px;">Page 1 sur 36</span><span style="width: 30px; height: 30px; border: 1px solid #DBE3DE; border-radius: 7px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.5 3 L7.5 6 L4.5 9" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></span></div></div>
          </div>
        </div>

        <div style="width: 400px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 14px; flex-shrink: 0;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 44px; height: 44px; border-radius: 22px; background: #DCEBE6; color: #10554A; font-size: 15px; font-weight: 700; display: flex; align-items: center; justify-content: center;">YB</div>
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <span style="font-size: 16px; font-weight: 700; color: #182420;">Dr Y. Benali</span>
              <span style="font-size: 12px; color: #61706A;">M-04512 · Urgences</span>
            </div>
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 6px 0; border-bottom: 1px solid #EDF1EE;"><span style="color: #61706A;">Grade</span><span style="font-weight: 600;">Médecin spécialiste</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 6px 0; border-bottom: 1px solid #EDF1EE;"><span style="color: #61706A;">Groupe (taux)</span><span style="font-weight: 600;">Groupe A</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 6px 0; border-bottom: 1px solid #EDF1EE;"><span style="color: #61706A;">Structure</span><span style="font-weight: 600;">CHR de Guelmim</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 6px 0;"><span style="color: #61706A;">Depuis le</span><span style="font-weight: 600;">14/03/2022</span></div>
          </div>
          <div style="background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px;">
            <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #66746D; text-transform: uppercase;">Août 2026</span>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #3A4741;">6 gardes · 2 astreintes</span><span style="font-weight: 700;">4""" + NB + """400""" + NB + """DH</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #3A4741;">1 mission (Sidi Ifni)</span><span style="font-weight: 700;">400""" + NB + """DH</span></div>
          </div>
          <div style="margin-top: auto; display: flex; gap: 10px;">
            """ + btn_secondary("Historique") + """
            <button style="flex-grow: 1; height: 38px; background: #10554A; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #FFFFFF; font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif; cursor: pointer;">Modifier la fiche</button>
          </div>
        </div>
      </div>"""

# ============================== STRUCTURES ==============================
LOCK = '<svg width="11" height="11" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 4px; vertical-align: -1px;"><rect x="3" y="7" width="10" height="7" rx="1.5" stroke="#66746D" stroke-width="1.4"></rect><path d="M5.5 7 V5 A2.5 2.5 0 0 1 10.5 5 V7" stroke="#66746D" stroke-width="1.4"></path></svg>'

def tree_item(indent, icon, label, count, selected=False, muted=False):
    color = "#10554A" if selected else ("#66746D" if muted else "#182420")
    weight = "700" if selected else "500"
    bg = ' background: #EDF4F1; box-shadow: inset 0 0 0 1.5px #10554A; border-radius: 7px;' if selected else ''
    return ('<div style="display: flex; align-items: center; gap: 8px; padding: 8px 10px 8px %dpx;%s">'
        '%s<span style="font-size: 13px; font-weight: %s; color: %s;">%s</span>'
        '<span style="font-size: 12px; color: #66746D; margin-left: auto;">%s</span></div>') % (10 + indent * 18, bg, icon, weight, color, label, (LOCK + 'hors périmètre · ' + count) if muted else count)

def ticon(c):
    return '<svg width="15" height="15" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 16 V5 L9 2 L15 5 V16 M3 16 H15" stroke="%s" stroke-width="1.5" stroke-linejoin="round"></path></svg>' % c

STRUCTURES = page_header(
    "Structures",
    "Référentiel organisationnel — hôpitaux, centres de santé, délégations et services",
    btn_primary("Nouvelle structure")) + """

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="width: 430px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 14px; box-sizing: border-box; display: flex; flex-direction: column; gap: 2px; flex-shrink: 0;">
          <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #66746D; text-transform: uppercase; padding: 0 10px 8px;">Hiérarchie régionale</span>
""" + "\n".join([
    tree_item(0, ticon("#61706A"), "Direction Régionale Guelmim-Oued Noun", "4 provinces"),
    tree_item(1, ticon("#61706A"), "Délégation de Guelmim", "12 structures"),
    tree_item(2, ticon("#10554A"), "CHR de Guelmim", "9 services", selected=True),
    tree_item(3, '<span style="width: 6px; height: 6px; border-radius: 3px; background: #66746D;"></span>', "Urgences", "57 agents"),
    tree_item(3, '<span style="width: 6px; height: 6px; border-radius: 3px; background: #66746D;"></span>', "Réanimation", "31 agents"),
    tree_item(3, '<span style="width: 6px; height: 6px; border-radius: 3px; background: #66746D;"></span>', "Chirurgie · Maternité · Pédiatrie…", "7 autres"),
    tree_item(2, ticon("#61706A"), "CS urbain Guelmim-Centre", "23 agents"),
    tree_item(2, ticon("#61706A"), "CS rural Bouizakarne", "11 agents"),
    tree_item(1, ticon("#66746D"), "Délégation de Tan-Tan", "8 structures", muted=True),
    tree_item(1, ticon("#66746D"), "Délégation de Sidi Ifni", "7 structures", muted=True),
    tree_item(1, ticon("#66746D"), "Délégation d'Assa-Zag", "5 structures", muted=True),
]) + """
        </div>

        <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 14px; min-width: 0;">
          <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; align-items: flex-start; justify-content: space-between;">
              <div style="display: flex; flex-direction: column; gap: 3px;">
                <span style="font-size: 16px; font-weight: 700; color: #182420;">CHR de Guelmim</span>
                <span style="font-size: 12.5px; color: #61706A;">Code CHR-GLM-01 · Hôpital régional · Province de Guelmim</span>
              </div>
              """ + btn_secondary("Modifier") + """
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px;">
              <div style="background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px;">
                <span style="font-size: 12px; color: #61706A;">Agents rattachés</span><span style="font-size: 20px; font-weight: 700;">248</span>
              </div>
              <div style="background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px;">
                <span style="font-size: 12px; color: #61706A;">Utilisateurs</span><span style="font-size: 20px; font-weight: 700;">9</span>
              </div>
              <div style="background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px;">
                <span style="font-size: 12px; color: #61706A;">Services</span><span style="font-size: 20px; font-weight: 700;">9</span>
              </div>
            </div>
          </div>

          <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; display: flex; flex-direction: column; gap: 10px; flex-grow: 1;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <span style="font-size: 14.5px; font-weight: 600; color: #182420;">Exercices et périodes</span>
              """ + btn_secondary("Ouvrir une période") + """
            </div>
            <div style="display: grid; grid-template-columns: 130px 1fr 190px 130px; gap: 10px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #66746D; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;">
              <span>Exercice</span><span>Période</span><span>Saisies</span><span>État</span>
            </div>
            <div style="display: grid; grid-template-columns: 130px 1fr 190px 130px; gap: 10px; padding: 9px 10px; font-size: 13px; align-items: center; background: #EDF4F1; border-radius: 8px;">
              <span style="font-weight: 600;">2026</span><span>Août 2026</span><span>312 plannings · 14 missions</span><span>""" + badge("Ouverte", "ok") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 130px 1fr 190px 130px; gap: 10px; padding: 9px 10px; font-size: 13px; align-items: center; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600;">2026</span><span>Juillet 2026</span><span>298 plannings · 11 missions</span><span>""" + badge("Clôturée", "ok") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 130px 1fr 190px 130px; gap: 10px; padding: 9px 10px; font-size: 13px; align-items: center;">
              <span style="font-weight: 600;">2026</span><span>Trimestre 2 (avr.–juin)</span><span>867 plannings · 29 missions</span><span>""" + badge("Clôturée", "ok") + """</span>
            </div>
            <div style="margin-top: auto; display: flex; align-items: flex-start; gap: 9px; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 11px 13px;">
              <svg width="15" height="15" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: 1px; flex-shrink: 0;"><circle cx="8" cy="8" r="6.5" stroke="#10554A" stroke-width="1.4"></circle><path d="M8 7.5 V11 M8 5 V5.2" stroke="#10554A" stroke-width="1.6" stroke-linecap="round"></path></svg>
              <span style="font-size: 12px; color: #3A5C52; line-height: 1.5;">Les formulaires et paramètres de saisie sont adaptables par structure (champs visibles, services, types d'indemnité activés) — <a href="#">ouvrir Administration</a>.</span>
            </div>
          </div>
        </div>
      </div>"""

# ============================== BAREMES ==============================
BAREMES = page_header(
    "Barèmes &amp; règles de calcul",
    "Taux paramétrables sans modification du code — historisés par date d'entrée en vigueur",
    btn_secondary("Exporter (Excel)") + btn_primary("Nouvelle version")) + """


      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 14px; min-width: 0;">
          <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; display: flex; flex-direction: column; gap: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <span style="font-size: 14.5px; font-weight: 600; color: #182420;">Taux par grade et par type — version 3</span>
              """ + badge("En vigueur depuis le 01/07/2026", "ok") + """
            </div>
            <div style="display: grid; grid-template-columns: 1fr 110px 110px 120px; gap: 10px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #66746D; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;">
              <span>Grade</span><span>Garde</span><span>Astreinte</span><span>Permanence</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 110px 110px 120px; gap: 10px; padding: 9px 10px; font-size: 13px; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600;">Médecin spécialiste</span><span>600""" + NB + """DH</span><span>400""" + NB + """DH</span><span>350""" + NB + """DH</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 110px 110px 120px; gap: 10px; padding: 9px 10px; font-size: 13px; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600;">Médecin généraliste</span><span>500""" + NB + """DH</span><span>330""" + NB + """DH</span><span>300""" + NB + """DH</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 110px 110px 120px; gap: 10px; padding: 9px 10px; font-size: 13px; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600;">Infirmier</span><span>300""" + NB + """DH</span><span>200""" + NB + """DH</span><span>180""" + NB + """DH</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 110px 110px 120px; gap: 10px; padding: 9px 10px; font-size: 13px;">
              <span style="font-weight: 600;">Technicien</span><span>250""" + NB + """DH</span><span>170""" + NB + """DH</span><span>150""" + NB + """DH</span>
            </div>
          </div>

          <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; display: flex; flex-direction: column; gap: 10px; flex-grow: 1;">
            <span style="font-size: 14.5px; font-weight: 600; color: #182420;">Grille de déplacement par groupe</span>
            <div style="display: grid; grid-template-columns: 1fr 170px 160px; gap: 10px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #66746D; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;">
              <span>Groupe</span><span>Indemnité journalière</span><span>Plafond / mission</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 170px 160px; gap: 10px; padding: 8px 10px; font-size: 13px; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600;">Groupe A</span><span>400""" + NB + """DH""" + NB + """/""" + NB + """jour</span><span>2""" + NB + """000""" + NB + """DH</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 170px 160px; gap: 10px; padding: 8px 10px; font-size: 13px; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600;">Groupe B</span><span>300""" + NB + """DH""" + NB + """/""" + NB + """jour</span><span>1""" + NB + """500""" + NB + """DH</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 170px 160px; gap: 10px; padding: 8px 10px; font-size: 13px;">
              <span style="font-weight: 600;">Groupe C</span><span>250""" + NB + """DH""" + NB + """/""" + NB + """jour</span><span>1""" + NB + """200""" + NB + """DH</span>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 4px;">
              <div style="flex-grow: 1; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 10px 13px; display: flex; flex-direction: column; gap: 6px;">
                <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #66746D; text-transform: uppercase;">Coefficients de distance (paramétrables)</span>
                <div style="display: flex; gap: 18px; font-size: 12.5px; color: #3A4741;">
                  <span>&lt;""" + NB + """50""" + NB + """km : <strong>×""" + NB + """1,0</strong></span>
                  <span>50–150""" + NB + """km : <strong>×""" + NB + """1,2</strong></span>
                  <span>&gt;""" + NB + """150""" + NB + """km : <strong>×""" + NB + """1,5</strong></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div style="width: 400px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px; flex-shrink: 0;">
          <span style="font-size: 14.5px; font-weight: 600; color: #182420;">Historique des versions</span>
          <div style="display: flex; flex-direction: column; gap: 0;">
            <div style="display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid #EDF1EE;">
              <span style="width: 8px; height: 8px; border-radius: 4px; background: #17663F; margin-top: 5px; flex-shrink: 0;"></span>
              <div style="display: flex; flex-direction: column; gap: 3px;">
                <span style="font-size: 13px; font-weight: 600;">Version 3 — en vigueur</span>
                <span style="font-size: 12px; color: #61706A;">Effet 01/07/2026 · créée par H. Bouzid le 24/06/2026</span>
                <span style="font-size: 12px; color: #61706A;">Revalorisation garde spécialistes : 550 → 600""" + NB + """DH</span>
              </div>
            </div>
            <div style="display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid #EDF1EE;">
              <span style="width: 8px; height: 8px; border-radius: 4px; background: #AEB9B2; margin-top: 5px; flex-shrink: 0;"></span>
              <div style="display: flex; flex-direction: column; gap: 3px;">
                <span style="font-size: 13px; font-weight: 600; color: #61706A;">Version 2 — archivée</span>
                <span style="font-size: 12px; color: #66746D;">Effet 01/01/2026 → 30/06/2026</span>
              </div>
            </div>
            <div style="display: flex; gap: 12px; padding: 10px 0;">
              <span style="width: 8px; height: 8px; border-radius: 4px; background: #AEB9B2; margin-top: 5px; flex-shrink: 0;"></span>
              <div style="display: flex; flex-direction: column; gap: 3px;">
                <span style="font-size: 13px; font-weight: 600; color: #61706A;">Version 1 — archivée</span>
                <span style="font-size: 12px; color: #66746D;">Effet 01/06/2025 → 31/12/2025</span>
              </div>
            </div>
          </div>
          <div style="margin-top: auto; display: flex; align-items: flex-start; gap: 9px; background: #FBEEDC; border: 1px solid #F2DDBB; border-radius: 8px; padding: 11px 13px;">
            <svg width="15" height="15" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: 1px; flex-shrink: 0;"><path d="M9 2 L17 15.5 H1 Z" stroke="#92400E" stroke-width="1.5" stroke-linejoin="round"></path><path d="M9 7 V11 M9 13 V13.2" stroke="#92400E" stroke-width="1.6" stroke-linecap="round"></path></svg>
            <span style="font-size: 12px; color: #7A5210; line-height: 1.5;">Le calcul applique toujours le barème en vigueur à la date du planning ou de la mission — jamais le barème courant.</span>
          </div>
        </div>
      </div>"""

# ============================== MISSIONS ==============================
MISSIONS = page_header(
    "Missions &amp; déplacements",
    "Ordres de mission et historique complet des déplacements",
    btn_secondary("Exporter (Excel)") + btn_primary("Nouvel ordre de mission")) + """

      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="padding: 7px 14px; background: #10554A; color: #FFFFFF; border-radius: 20px; font-size: 12.5px; font-weight: 600;">Toutes (14)</span>
        <span style="padding: 7px 14px; background: #FFFFFF; color: #61706A; border: 1px solid #DBE3DE; border-radius: 20px; font-size: 12.5px;">En cours (5)</span>
        <span style="padding: 7px 14px; background: #FFFFFF; color: #61706A; border: 1px solid #DBE3DE; border-radius: 20px; font-size: 12.5px;">À valider (3)</span>
        <span style="padding: 7px 14px; background: #FFFFFF; color: #61706A; border: 1px solid #DBE3DE; border-radius: 20px; font-size: 12.5px;">Clôturées (6)</span>
      </div>

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 8px;">
          <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #66746D; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;">
            <span>N° OM</span><span>Agent</span><span>Destination</span><span>Départ</span><span>Durée</span><span>Distance</span><span>État</span>
          </div>
          <div style="display: flex; flex-direction: column;">
            <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center; background: #EDF4F1; box-shadow: inset 0 0 0 1.5px #10554A; border-radius: 8px;">
              <span style="font-weight: 700; color: #10554A;">OM-2026-088</span><span style="font-weight: 600;">Dr K. Saidi</span><span>Agadir</span><span>25/08</span><span>2""" + NB + """j</span><span>452""" + NB + """km</span><span>""" + badge("En cours", "neutral") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600; color: #10554A;">OM-2026-087</span><span style="font-weight: 600;">Inf. R. Amrani</span><span>Tan-Tan</span><span>24/08</span><span>1""" + NB + """j</span><span>125""" + NB + """km</span><span>""" + badge("À valider", "warn") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600; color: #10554A;">OM-2026-086</span><span style="font-weight: 600;">Dr Y. Benali</span><span>Sidi Ifni</span><span>21/08</span><span>1""" + NB + """j</span><span>68""" + NB + """km</span><span>""" + badge("Clôturée", "ok") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600; color: #10554A;">OM-2026-085</span><span style="font-weight: 600;">Tech. H. Drissi</span><span>Bouizakarne</span><span>19/08</span><span>1""" + NB + """j</span><span>42""" + NB + """km</span><span>""" + badge("Clôturée", "ok") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center; border-bottom: 1px solid #EDF1EE;">
              <span style="font-weight: 600; color: #10554A;">OM-2026-084</span><span style="font-weight: 600;">Dr S. Ouazzani</span><span>Laâyoune</span><span>17/08</span><span>3""" + NB + """j</span><span>298""" + NB + """km</span><span>""" + badge("À valider", "warn") + """</span>
            </div>
            <div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center;">
              <span style="font-weight: 600; color: #10554A;">OM-2026-083</span><span style="font-weight: 600;">Inf. L. Mansouri</span><span>Rabat</span><span>11/08</span><span>4""" + NB + """j</span><span>642""" + NB + """km</span><span>""" + badge("Clôturée", "ok") + """</span>
            </div>
          </div>
          <div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid #E9EEEA;">
            <span style="font-size: 12px; color: #66746D;">6 missions affichées sur 14 — Août 2026</span>
            <div style="display: flex; align-items: center; gap: 16px;"><a href="#" style="font-size: 12.5px; font-weight: 600;">Historique complet des déplacements</a><div style="display: flex; align-items: center; gap: 6px;"><span style="width: 30px; height: 30px; border: 1px solid #DBE3DE; border-radius: 7px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.5 3 L4.5 6 L7.5 9" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span style="font-size: 12.5px; font-weight: 600; color: #182420; padding: 0 4px;">Page 1 sur 3</span><span style="width: 30px; height: 30px; border: 1px solid #DBE3DE; border-radius: 7px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.5 3 L7.5 6 L4.5 9" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></span></div></div>
          </div>
        </div>

        <div style="width: 400px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 13px; flex-shrink: 0;">
          <div style="display: flex; align-items: flex-start; justify-content: space-between;">
            <div style="display: flex; flex-direction: column; gap: 3px;">
              <span style="font-size: 16px; font-weight: 700; color: #182420;">OM-2026-088</span>
              <span style="font-size: 12.5px; color: #61706A;">Dr K. Saidi · Groupe A · Réanimation</span>
            </div>
            """ + badge("En cours", "neutral") + """
          </div>

          <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 5px 0; border-bottom: 1px solid #EDF1EE;"><span style="color: #61706A;">Trajet</span><span style="font-weight: 600;">Guelmim → Agadir</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 5px 0; border-bottom: 1px solid #EDF1EE;"><span style="color: #61706A;">Motif</span><span style="font-weight: 600;">Réunion régionale de coordination</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 5px 0; border-bottom: 1px solid #EDF1EE;"><span style="color: #61706A;">Dates</span><span style="font-weight: 600;">25–26/08/2026 (2""" + NB + """jours)</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; padding: 5px 0;"><span style="color: #61706A;">Distance</span><span style="font-weight: 600;">452""" + NB + """km (aller)</span></div>
          </div>

          <div style="background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 7px;">
            <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #66746D; text-transform: uppercase;">Indemnité prévisionnelle — détail du calcul</span>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #3A4741;">Durée × indemnité journalière (Groupe A)</span><span>2 × 400""" + NB + """DH</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #3A4741;">Coefficient de distance (&gt;""" + NB + """150""" + NB + """km)</span><span>×""" + NB + """1,5</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; border-top: 1px solid #E9EEEA; padding-top: 7px;"><span>Total (plafond 2""" + NB + """000""" + NB + """DH respecté)</span><span>1""" + NB + """200""" + NB + """DH</span></div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 8px;">
            <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #66746D; text-transform: uppercase;">Historique</span>
            <div style="display: flex; gap: 10px;"><span style="width: 7px; height: 7px; border-radius: 4px; background: #17663F; margin-top: 4px; flex-shrink: 0;"></span><span style="font-size: 12.5px; color: #3A4741;">Créé par <strong>A. Tazi</strong> — 20/08/2026 à 14:31</span></div>
            <div style="display: flex; gap: 10px;"><span style="width: 7px; height: 7px; border-radius: 4px; background: #17663F; margin-top: 4px; flex-shrink: 0;"></span><span style="font-size: 12.5px; color: #3A4741;">Départ confirmé — 25/08/2026 à 08:02</span></div>
          </div>

          <div style="margin-top: auto; display: flex; gap: 10px;">
            """ + btn_secondary("Modifier") + """
            <button style="flex-grow: 1; height: 40px; background: #10554A; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #FFFFFF; font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif; cursor: pointer;">Clôturer et envoyer au calcul</button>
          </div>
        </div>
      </div>"""

SCREENS = [
    ("Personnel.dc.html", "Personnel", PERSONNEL, "Matricule ou nom…", "HB", "H. Bouzid", "Administrateur"),
    ("Structures.dc.html", "Structures", STRUCTURES, "Rechercher une structure…", "HB", "H. Bouzid", "Administrateur"),
    ("Baremes.dc.html", "Barèmes", BAREMES, "Rechercher un barème…", "HB", "H. Bouzid", "Administrateur"),
    ("Missions.dc.html", "Missions", MISSIONS, "Rechercher un OM, un agent…", "AT", "A. Tazi", "Agent de saisie"),
]

for fname, active, content, search, initials, user, role in SCREENS:
    html = SHELL.format(serif=SERIF, nav=nav_html(active), content=content,
                        search=search, initials=initials, user=user, role=role)
    with io.open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("ok", fname, len(html))
