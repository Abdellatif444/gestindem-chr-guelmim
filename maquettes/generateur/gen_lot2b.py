# -*- coding: utf-8 -*-
"""Fournée 2 du Lot 2 : Calcul, États & rapports, Statistiques, Administration,
+ mini-lot « saisie & états » (formulaires, confirmations, succès, vides, erreur d'import).
Réutilise le gabarit et les composants de gen_lot2.py (DRY)."""
import io, os, re
from gen_lot2 import (OUT, NB, SERIF, SHELL, nav_html, page_header, btn_primary,
                      btn_secondary, sel, badge, IMPORT_ICON, render, PERSONNEL, MISSIONS)

LOT1 = os.path.join(os.path.dirname(OUT), "lot1")

# ---------------------------------------------------------------- composants
def card(inner, extra="", grow=True):
    return '<div style="%sbackground: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px; min-width: 0;%s">%s</div>' % (
        "flex-grow: 1; " if grow else "", extra, inner)

def card_title(text, right=""):
    return '<div style="display: flex; align-items: center; justify-content: space-between;"><span style="font-size: 14.5px; font-weight: 600; color: #182420;">%s</span>%s</div>' % (text, right)

def thead(cols, grid):
    cells = "".join('<span>%s</span>' % c for c in cols)
    return '<div style="display: grid; grid-template-columns: %s; gap: 8px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #5C6B64; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;">%s</div>' % (grid, cells)

def trow(cells, grid, selected=False, last=False):
    style = "background: #EDF4F1; box-shadow: inset 0 0 0 1.5px #10554A; border-radius: 8px;" if selected else ("" if last else "border-bottom: 1px solid #EDF1EE;")
    return '<div style="display: grid; grid-template-columns: %s; gap: 8px; padding: 10px; font-size: 13px; align-items: center; %s">%s</div>' % (grid, style, "".join(cells))

def kv(label, value, strong=True):
    return '<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 7px 0; border-bottom: 1px solid #EDF1EE;"><span style="font-size: 12.5px; color: #61706A;">%s</span><span style="font-size: 13px; font-weight: %s; color: #182420; text-align: right;">%s</span></div>' % (label, "600" if strong else "400", value)

def field(label, value, placeholder=False, help_text="", grow=True):
    color = "#5C6B64" if placeholder else "#182420"
    h = '<span style="font-size: 12px; color: #5C6B64;">%s</span>' % help_text if help_text else ""
    return ('<div style="display: flex; flex-direction: column; gap: 6px;%s"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">%s</label>'
            '<div style="height: 42px; border: 1px solid #C9D3CD; border-radius: 8px; background: #FFFFFF; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; box-sizing: border-box;"><span style="font-size: 13px; color: %s;">%s</span>'
            '<svg width="11" height="11" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 4.5 L6 7.5 L9 4.5" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></div>%s</div>') % (
        " flex-grow: 1;" if grow else "", label, color, value, h)

def field_text(label, value, placeholder=False, help_text="", grow=True):
    color = "#5C6B64" if placeholder else "#182420"
    h = '<span style="font-size: 12px; color: #5C6B64;">%s</span>' % help_text if help_text else ""
    return ('<div style="display: flex; flex-direction: column; gap: 6px;%s"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">%s</label>'
            '<div style="height: 42px; border: 1px solid #C9D3CD; border-radius: 8px; background: #FFFFFF; display: flex; align-items: center; padding: 0 12px; box-sizing: border-box;"><span style="font-size: 13px; color: %s;">%s</span></div>%s</div>') % (
        " flex-grow: 1;" if grow else "", label, color, value, h)

def segmented(options, active):
    out = []
    for o in options:
        if o == active:
            out.append('<span style="flex: 1 1 0; text-align: center; padding: 9px 0; background: #10554A; color: #FFFFFF; border-radius: 7px; font-size: 13px; font-weight: 600;">%s</span>' % o)
        else:
            out.append('<span style="flex: 1 1 0; text-align: center; padding: 9px 0; color: #3A4741; font-size: 13px; font-weight: 500;">%s</span>' % o)
    return '<div style="display: flex; gap: 4px; padding: 4px; background: #E7EDE9; border-radius: 9px;">%s</div>' % "".join(out)

def chips(options, active):
    out = []
    for o in options:
        if o == active:
            out.append('<span style="padding: 7px 14px; background: #10554A; color: #FFFFFF; border-radius: 20px; font-size: 12.5px; font-weight: 600;">%s</span>' % o)
        else:
            out.append('<span style="padding: 7px 14px; background: #FFFFFF; color: #3A4741; border: 1px solid #DBE3DE; border-radius: 20px; font-size: 12.5px; font-weight: 500;">%s</span>' % o)
    return '<div style="display: flex; gap: 8px; flex-wrap: wrap;">%s</div>' % "".join(out)

def alert(kind, html, action=""):
    styles = {"ok": ("#E4F2E9", "#C5E3CF", "#17663F"), "warn": ("#FBEEDC", "#F1D9B4", "#7A5210"),
              "err": ("#FADEDC", "#EFC4C0", "#7A1A1A"), "info": ("#EDF4F1", "#DCEBE6", "#3A5C52")}
    bg, bd, fg = styles[kind]
    icons = {
        "ok": '<circle cx="9" cy="9" r="7" stroke="%s" stroke-width="1.5"></circle><path d="M6 9.2 L8.2 11.4 L12.2 7" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>',
        "warn": '<path d="M9 2 L17 15.5 H1 Z" stroke="%s" stroke-width="1.5" stroke-linejoin="round"></path><path d="M9 7 V11 M9 13 V13.2" stroke="%s" stroke-width="1.6" stroke-linecap="round"></path>',
        "err": '<path d="M9 2 L17 15.5 H1 Z" stroke="%s" stroke-width="1.5" stroke-linejoin="round"></path><path d="M9 7 V11 M9 13 V13.2" stroke="%s" stroke-width="1.6" stroke-linecap="round"></path>',
        "info": '<circle cx="9" cy="9" r="7" stroke="%s" stroke-width="1.5"></circle><path d="M9 8 V12.5 M9 5.5 V5.7" stroke="%s" stroke-width="1.6" stroke-linecap="round"></path>',
    }
    icon = '<svg width="17" height="17" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">%s</svg>' % (icons[kind] % (fg, fg))
    act = '<a href="#" style="font-size: 13px; font-weight: 600; color: %s; flex-shrink: 0;">%s</a>' % (fg, action) if action else ""
    return '<div style="display: flex; align-items: center; justify-content: space-between; gap: 14px; background: %s; border: 1px solid %s; border-radius: 8px; padding: 10px 14px;"><div style="display: flex; align-items: center; gap: 10px;">%s<span style="font-size: 13px; color: %s; line-height: 1.45;">%s</span></div>%s</div>' % (bg, bd, icon, fg, html, act)

CHEV_L = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.5 3 L4.5 6 L7.5 9" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
CHEV_R = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.5 3 L7.5 6 L4.5 9" stroke="#61706A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
def pager(label):
    return ('<div style="display: flex; align-items: center; gap: 6px;">'
            '<span style="width: 30px; height: 30px; border: 1px solid #DBE3DE; border-radius: 7px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;">%s</span>'
            '<span style="font-size: 12.5px; font-weight: 600; color: #182420; padding: 0 4px;">%s</span>'
            '<span style="width: 30px; height: 30px; border: 1px solid #DBE3DE; border-radius: 7px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;">%s</span></div>') % (CHEV_L, label, CHEV_R)

def footer(left, right):
    return '<div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid #E9EEEA;"><span style="font-size: 12px; color: #5C6B64;">%s</span>%s</div>' % (left, right)

def hbar(label, value_text, pct, color):
    return ('<div style="display: flex; flex-direction: column; gap: 6px;"><div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #3A4741; font-weight: 500;">%s</span><span style="color: #182420; font-weight: 600;">%s</span></div>'
            '<div style="height: 10px; background: #E7EDE9; border-radius: 5px;"><div style="width: %d%%; height: 10px; background: %s; border-radius: 5px;"></div></div></div>') % (label, value_text, pct, color)

def btn_danger_outline(label):
    return '<button style="height: 38px; padding: 0 16px; background: #FFFFFF; border: 1px solid #E0B4B0; border-radius: 8px; font-size: 13px; font-weight: 600; color: #A61B1B; font-family: \'IBM Plex Sans\', \'Segoe UI\', sans-serif; cursor: pointer;">%s</button>' % label

def btn_disabled(label):
    return '<button style="height: 38px; padding: 0 16px; background: #E7EDE9; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #5C6B64; font-family: \'IBM Plex Sans\', \'Segoe UI\', sans-serif;">%s</button>' % label

# ============================== CALCUL DES INDEMNITÉS (M6) ==============================
calc_rows = [
    ("Dr Y. Benali", "Médecin spécialiste", "6 × 600", "2 × 400", "—", "4" + NB + "400", badge("À recalculer", "warn"), True),
    ("Dr K. Saidi", "Médecin spécialiste", "5 × 600", "1 × 400", "—", "3" + NB + "400", badge("Lot 0142", "ok"), False),
    ("Dr M. El Idrissi", "Médecin généraliste", "4 × 500", "1 × 330", "—", "2" + NB + "330", badge("Lot 0142", "ok"), False),
    ("Dr S. Ouazzani", "Médecin généraliste", "3 × 500", "—", "1 × 300", "1" + NB + "800", badge("Calculé", "neutral"), False),
    ("Inf. R. Amrani", "Infirmier polyvalent", "—", "—", "5 × 180", "900", badge("Calculé", "neutral"), False),
    ("Inf. L. Mansouri", "Infirmier anesthésiste", "2 × 300", "3 × 200", "—", "1" + NB + "200", badge("À recalculer", "warn"), False),
    ("Tech. H. Drissi", "Technicien radiologie", "1 × 250", "2 × 170", "—", "590", badge("Calculé", "neutral"), False),
]
CALC_GRID = "130px 140px 75px 80px 75px 70px 1fr"
calc_table = thead(["Agent", "Grade", "Garde", "Astreinte", "Perm.", "Total DH", "Statut"], CALC_GRID)
for i, (nom, grade, g, a, p, tot, st, selected) in enumerate(calc_rows):
    calc_table += trow([
        '<span style="font-weight: 600;">%s</span>' % nom, '<span style="color: #3A4741;">%s</span>' % grade,
        '<span style="color: #3A4741;">%s</span>' % g, '<span style="color: #3A4741;">%s</span>' % a, '<span style="color: #3A4741;">%s</span>' % p,
        '<span style="font-weight: 700;">%s</span>' % tot, '<span>%s</span>' % st], CALC_GRID, selected, i == len(calc_rows) - 1)

CALCUL = page_header(
    "Calcul des indemnités",
    "Gardes, astreintes et permanences — barème en vigueur à la date de chaque planning, recalcul si un planning ou un barème change",
    btn_secondary("Exporter (Excel)") + btn_primary("Lancer le calcul — Août 2026", plus=False)) + """

      """ + alert("warn", "<strong>Dernier calcul :</strong> 31/08/2026 à 18:02 par H. Bouzid — 312 gardes · 148 astreintes · 96 permanences · barème v3. <strong>2 agents à recalculer</strong> : leur planning a été modifié depuis.", "Recalculer les 2 agents") + """

      <div style="display: flex; align-items: center; gap: 10px;">""" + sel("Service", "Tous") + sel("Type", "Tous") + sel("Statut", "Tous") + """
        <span style="margin-left: auto; font-size: 12.5px; color: #5C6B64;">248 agents · total calculé <strong style="color: #182420;">155""" + NB + """400""" + NB + """DH</strong></span>
      </div>

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="width: 740px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; flex-shrink: 0;">
          """ + card_title("Montants par agent — Août 2026") + """
          <div style="display: flex; flex-direction: column;">""" + calc_table + """</div>
          """ + footer("7 agents affichés sur 248", pager("Page 1 sur 36")) + """
        </div>

        <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 13px; min-width: 0;">
          <div style="display: flex; align-items: flex-start; justify-content: space-between;">
            <div style="display: flex; flex-direction: column; gap: 3px;">
              <span style="font-size: 16px; font-weight: 700;">Dr Y. Benali — Août 2026</span>
              <span style="font-size: 12.5px; color: #61706A;">Médecin spécialiste · Urgences · M-04512</span>
            </div>""" + badge("À recalculer", "warn") + """
          </div>
          <div style="display: flex; flex-direction: column; gap: 0;">
            <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #5C6B64; text-transform: uppercase; padding-bottom: 6px;">Détail du calcul</span>
            """ + kv("Gardes × 6 <span style=\"color: #5C6B64; font-weight: 400;\">(01, 09, 12, 22, 29, 30/08)</span> · 600" + NB + "DH", "3" + NB + "600" + NB + "DH") + kv("Astreintes × 2 <span style=\"color: #5C6B64; font-weight: 400;\">(08, 15/08)</span> · 400" + NB + "DH", "800" + NB + "DH") + kv("Permanences × 0", "—", False) + kv("Barème appliqué", "v3 — effet 01/07/2026", False) + """
            <div style="display: flex; justify-content: space-between; align-items: baseline; padding: 9px 0;"><span style="font-size: 13px; font-weight: 700;">Total calculé le 31/08</span><span style="font-size: 20px; font-weight: 700;">4""" + NB + """400""" + NB + """DH</span></div>
          </div>
          """ + alert("warn", "Planning modifié le 02/09 : la garde du <strong>12/08</strong> a été supprimée (doublon). Nouveau total prévisionnel : <strong>3" + NB + "800" + NB + "DH</strong>.") + """
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #5C6B64; text-transform: uppercase;">Historique</span>
            <div style="display: flex; gap: 10px;"><span style="width: 7px; height: 7px; border-radius: 4px; background: #17663F; margin-top: 4px; flex-shrink: 0;"></span><span style="font-size: 12.5px; color: #3A4741;">Calculé par <strong>H. Bouzid</strong> — 31/08/2026 à 18:02 · barème v3</span></div>
            <div style="display: flex; gap: 10px;"><span style="width: 7px; height: 7px; border-radius: 4px; background: #D97706; margin-top: 4px; flex-shrink: 0;"></span><span style="font-size: 12.5px; color: #92400E;">Planning modifié par <strong>A. Tazi</strong> — 02/09/2026 à 09:40 · recalcul requis</span></div>
          </div>
          <div style="margin-top: auto; display: flex; gap: 10px;">""" + btn_secondary("Voir le planning") + """<div style="flex-grow: 1;">""" + btn_primary("Recalculer cet agent", plus=False).replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center;') + """</div></div>
        </div>
      </div>"""

# ============================== ÉTATS & RAPPORTS (M10) ==============================
etat_rows = [
    ("Récapitulatif mensuel des indemnités", "CHR de Guelmim", "Août 2026", "H. Bouzid", "31/08 18:10", "PDF"),
    ("État par service — Urgences", "CHR de Guelmim", "Août 2026", "N. El Fassi", "31/08 17:22", "Excel"),
    ("Déplacements — missions clôturées", "CHR de Guelmim", "Juillet 2026", "A. Tazi", "04/08 10:05", "CSV"),
    ("Récapitulatif trimestriel", "Direction régionale", "T2 2026 (avr.–juin)", "H. Bouzid", "07/07 09:31", "PDF"),
    ("État par agent — Dr Y. Benali", "CHR de Guelmim", "Janv.–Juin 2026", "N. El Fassi", "02/07 14:48", "PDF"),
    ("Récapitulatif annuel", "CHR de Guelmim", "Année 2025", "H. Bouzid", "12/01 11:15", "Excel"),
]
ETAT_GRID = "1fr 120px 90px 90px 55px 120px"
DL_ICON = '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 2 V10 M8 10 L5 7 M8 10 L11 7 M2.5 13.5 H13.5" stroke="#10554A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
etat_table = thead(["Rapport", "Période", "Généré par", "Le", "Format", ""], ETAT_GRID)
for i, (nom, struct, per, who, when, fmt) in enumerate(etat_rows):
    etat_table += trow([
        '<span style="display: flex; flex-direction: column;"><span style="font-weight: 600;">%s</span><span style="font-size: 12px; color: #5C6B64;">%s</span></span>' % (nom, struct), '<span style="color: #3A4741;">%s</span>' % per,
        '<span style="color: #3A4741;">%s</span>' % who, '<span style="color: #3A4741;">%s</span>' % when, '<span>%s</span>' % badge(fmt, "neutral"),
        '<span style="display: flex; gap: 10px; justify-content: flex-end; align-items: center;"><a href="#" style="font-size: 12.5px; font-weight: 600; display: flex; align-items: center; gap: 4px;">%sTélécharger</a><span style="width: 28px; height: 28px; border: 1px solid #DBE3DE; border-radius: 7px; display: flex; align-items: center; justify-content: center;" title="Régénérer"><svg width="13" height="13" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 8 A5 5 0 1 1 11.5 4.5 M11.5 2 V4.8 H8.7" stroke="#10554A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></span></span>' % DL_ICON],
        ETAT_GRID, False, i == len(etat_rows) - 1)

ETATS = page_header(
    "États &amp; rapports",
    "Rapports mensuels, trimestriels et annuels — exports Excel, PDF et CSV — archive des rapports générés",
    "") + """

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="width: 360px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 14px; flex-shrink: 0;">
          """ + card_title("Générer un état") + """
          """ + field("Type d'état", "Récapitulatif mensuel des indemnités", grow=False) + """
          <div style="display: flex; gap: 10px;">""" + field("Période", "Août 2026", grow=True) + field("Structure", "CHR de Guelmim", grow=True) + """</div>
          """ + field("Détail par", "Service", help_text="Choisir : service, agent ou type d'indemnité", grow=False) + """
          <div style="display: flex; flex-direction: column; gap: 6px;"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">Format</label>""" + chips(["PDF", "Excel", "CSV"], "PDF") + """</div>
          <div style="display: flex; flex-direction: column; gap: 6px; padding: 12px 14px; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px;">
            <span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #5C6B64; text-transform: uppercase;">Aperçu du contenu</span>
            <span style="font-size: 12.5px; color: #3A4741; line-height: 1.5;">9 services · 248 agents · 4 types d'indemnité · total 184""" + NB + """250""" + NB + """DH · lots validés et prêts pour paiement uniquement</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">""" + btn_primary("Générer le rapport (PDF)", plus=False).replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center; height: 42px;') + """
            <span style="font-size: 12px; color: #5C6B64; text-align: center;">Le rapport est archivé automatiquement et horodaté.</span>
          </div>
        </div>

        <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; min-width: 0;">
          """ + card_title("Archive des rapports générés", '<div style="display: flex; gap: 8px;">' + sel("Type", "Tous") + sel("Exercice", "2026") + '</div>') + """
          <div style="display: flex; flex-direction: column;">""" + etat_table + """</div>
          """ + footer("6 rapports affichés sur 41 · conservés 10 ans", pager("Page 1 sur 7")) + """
        </div>
      </div>"""

# ============================== STATISTIQUES (M11) ==============================
def line_chart():
    xs = [60, 130, 200, 270, 340, 410, 480, 550]
    y26 = [128, 122, 118, 96, 128, 80, 77, 54]
    y25 = [143, 135, 126, 124, 139, 105, 94, 82]
    months = ["Janv.", "Févr.", "Mars", "Avril", "Mai", "Juin", "Juil.", "Août"]
    pts26 = " ".join("%d,%d" % (x, y) for x, y in zip(xs, y26))
    pts25 = " ".join("%d,%d" % (x, y) for x, y in zip(xs, y25))
    grid = "".join('<line x1="42" y1="%s" x2="570" y2="%s"></line>' % (y, y) for y in ("20.5", "62.5", "105.5", "147.5", "190.5"))
    ylab = "".join('<text x="36" y="%d">%s</text>' % (y, t) for y, t in ((24, "200k"), (66, "180k"), (109, "160k"), (151, "140k"), (194, "120k")))
    xlab = "".join('<text x="%d" y="212">%s</text>' % (x, m) for x, m in zip(xs, months))
    return ('<svg width="700" height="224" viewBox="0 0 700 224" xmlns="http://www.w3.org/2000/svg">'
            '<g stroke="#E9EEEA" stroke-width="1">%s</g>'
            '<g font-family="IBM Plex Sans, Segoe UI, sans-serif" font-size="11.5" fill="#5C6B64" text-anchor="end">%s</g>'
            '<polyline points="%s" fill="none" stroke="#AEB9B2" stroke-width="2" stroke-dasharray="5 4" stroke-linejoin="round"></polyline>'
            '<polyline points="%s" fill="none" stroke="#10554A" stroke-width="2.2" stroke-linejoin="round"></polyline>'
            '<circle cx="550" cy="54" r="4" fill="#10554A"></circle><circle cx="550" cy="82" r="3.5" fill="#AEB9B2"></circle>'
            '<g font-family="IBM Plex Sans, Segoe UI, sans-serif" font-size="12" font-weight="600"><text x="562" y="58" fill="#10554A">2026 · 184 k</text><text x="562" y="86" fill="#5C6B64">2025 · 171 k</text></g>'
            '<g font-family="IBM Plex Sans, Segoe UI, sans-serif" font-size="11.5" fill="#61706A" text-anchor="middle">%s</g></svg>') % (grid, ylab, pts25, pts26, xlab)

STATS = page_header(
    "Statistiques",
    "Suivi des dépenses, répartition des indemnités, comparaisons entre structures et entre périodes",
    sel("Période", "Janv.–Août 2026") + sel("Comparer avec", "Même période 2025") + btn_secondary("Exporter (PDF)")) + """

      <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px;">
        <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 14px 18px; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 12.5px; font-weight: 500; color: #61706A;">Dépenses cumulées — janv.–août 2026</span><span style="font-size: 24px; font-weight: 700; line-height: 1;">1""" + NB + """297""" + NB + """000 <span style="font-size: 13px; font-weight: 600; color: #61706A;">DH</span></span><span style="font-size: 12px; color: #61706A;">+5,5""" + NB + """% vs janv.–août 2025 (1""" + NB + """229""" + NB + """000""" + NB + """DH)</span></div>
        <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 14px 18px; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 12.5px; font-weight: 500; color: #61706A;">Coût moyen d'une garde</span><span style="font-size: 24px; font-weight: 700; line-height: 1;">528 <span style="font-size: 13px; font-weight: 600; color: #61706A;">DH</span></span><span style="font-size: 12px; color: #61706A;">2""" + NB + """312 gardes sur la période</span></div>
        <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 14px 18px; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 12.5px; font-weight: 500; color: #61706A;">Part des déplacements</span><span style="font-size: 24px; font-weight: 700; line-height: 1;">15,7""" + NB + """%</span><span style="font-size: 12px; color: #61706A;">203""" + NB + """900""" + NB + """DH · 96 missions</span></div>
      </div>

      <div style="display: flex; gap: 16px;">
        <div style="width: 740px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 8px; flex-shrink: 0;">
          """ + card_title("Dépenses mensuelles — 2026 comparé à 2025", '<div style="display: flex; gap: 14px;"><span style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #61706A;"><span style="width: 14px; height: 3px; background: #10554A; border-radius: 2px;"></span>2026</span><span style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #61706A;"><span style="width: 14px; height: 0; border-top: 2px dashed #AEB9B2;"></span>2025</span></div>') + line_chart() + """
        </div>
        <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 14px; min-width: 0;">
          """ + card_title("Comparaison entre structures — Août 2026") + """
          <div style="display: flex; flex-direction: column; gap: 12px;">
            """ + hbar("CHR de Guelmim", "184" + NB + "250" + NB + "DH", 100, "#10554A") + hbar("Délégation de Tan-Tan", "96" + NB + "400" + NB + "DH", 52, "#10554A") + hbar("Délégation de Sidi Ifni", "72" + NB + "900" + NB + "DH", 40, "#10554A") + hbar("CS urbain Guelmim-Centre", "41" + NB + "300" + NB + "DH", 22, "#10554A") + hbar("Délégation d'Assa-Zag", "38" + NB + "100" + NB + "DH", 21, "#10554A") + """
          </div>
          <span style="margin-top: auto; font-size: 12px; color: #5C6B64;">Total région : 432""" + NB + """950""" + NB + """DH · <a href="#">Détail par structure</a></span>
        </div>
      </div>

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="width: 740px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px; flex-shrink: 0;">
          """ + card_title("Répartition par type d'indemnité — cumul 2026") + """
          <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 28px;">
            """ + hbar("Garde", "649" + NB + "500" + NB + "DH · 50,1" + NB + "%", 100, "#0A8467") + hbar("Astreinte", "240" + NB + "000" + NB + "DH · 18,5" + NB + "%", 37, "#D97706") + hbar("Permanence", "203" + NB + "600" + NB + "DH · 15,7" + NB + "%", 31, "#2563EB") + hbar("Déplacement", "203" + NB + "900" + NB + "DH · 15,7" + NB + "%", 31, "#C2255C") + """
          </div>
        </div>
        <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px; min-width: 0;">
          """ + card_title("Services les plus coûteux — Août 2026") + """
          <div style="display: flex; flex-direction: column; gap: 10px;">
            """ + hbar("Urgences", "61" + NB + "200" + NB + "DH", 100, "#10554A") + hbar("Réanimation", "38" + NB + "900" + NB + "DH", 64, "#10554A") + hbar("Chirurgie", "27" + NB + "400" + NB + "DH", 45, "#10554A") + hbar("Maternité", "22" + NB + "800" + NB + "DH", 37, "#10554A") + """
          </div>
        </div>
      </div>"""

# ============================== ADMINISTRATION (M1 / M12) ==============================
user_rows = [
    ("NE", "N. El Fassi", "n.elfassi", "Validateur", "CHR de Guelmim", "Validation · Plannings · États", "02/09 08:41", badge("Actif", "ok"), True),
    ("AT", "A. Tazi", "a.tazi", "Agent de saisie", "CHR — Urgences", "Plannings · Missions", "02/09 09:40", badge("Actif", "ok"), False),
    ("SM", "S. Mansouri", "s.mansouri", "Validateur", "CHR de Guelmim", "Validation · Plannings", "01/09 16:12", badge("Actif", "ok"), False),
    ("HB", "H. Bouzid", "h.bouzid", "Administrateur", "Toutes", "Tous les modules", "02/09 09:55", badge("Actif", "ok"), False),
    ("MR", "M. Raji", "m.raji", "Consultation", "Direction régionale", "États · Statistiques", "28/08 11:03", badge("Actif", "ok"), False),
    ("KA", "K. Ait Lahcen", "k.aitlahcen", "Agent de saisie", "Délégation de Tan-Tan", "Plannings", "14/06 08:20", badge("Désactivé", "neutral"), False),
]
USER_GRID = "150px 105px 135px 1fr 85px 75px"
user_table = thead(["Utilisateur", "Profil", "Structure", "Modules autorisés", "Dernière conn.", "Statut"], USER_GRID)
for i, (ini, nom, login, role, struct, mods, last, st, selected) in enumerate(user_rows):
    user_table += trow([
        '<span style="display: flex; align-items: center; gap: 8px;"><span style="width: 28px; height: 28px; border-radius: 14px; background: #DCEBE6; color: #10554A; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">%s</span><span style="display: flex; flex-direction: column;"><span style="font-weight: 600;">%s</span><span style="font-size: 12px; color: #5C6B64;">%s</span></span></span>' % (ini, nom, login),
        '<span style="color: #3A4741;">%s</span>' % role, '<span style="color: #3A4741;">%s</span>' % struct, '<span style="color: #3A4741;">%s</span>' % mods,
        '<span style="color: #3A4741;">%s</span>' % last, '<span>%s</span>' % st], USER_GRID, selected, i == len(user_rows) - 1)

audit_rows = [
    ("09:40", "A. Tazi", "a supprimé la garde du 12/08 (Dr Y. Benali) — motif : doublon", "Planning"),
    ("09:12", "N. El Fassi", "a validé le lot LOT-2026-0145 — 11" + NB + "900" + NB + "DH", "Validation"),
    ("08:41", "N. El Fassi", "connexion réussie", "Session"),
    ("02:00", "Système", "sauvegarde automatique — 412" + NB + "Mo, chiffrée", "Sauvegarde"),
    ("hier 16:40", "H. Bouzid", "a créé la version 3 du barème « Garde — Médecins »", "Barèmes"),
]
audit_list = "".join('<div style="display: flex; gap: 10px; align-items: flex-start; padding: 7px 0; border-bottom: 1px solid #EDF1EE;"><span style="font-size: 12px; color: #5C6B64; width: 68px; flex-shrink: 0;">%s</span><span style="font-size: 12.5px; color: #3A4741; line-height: 1.4; flex-grow: 1;"><strong>%s</strong> %s</span>%s</div>' % (t, who, what, badge(mod, "neutral")) for t, who, what, mod in audit_rows)

ADMIN = page_header(
    "Administration",
    "Utilisateurs et droits par module et par structure, journal d'audit, sauvegardes et sécurité",
    btn_secondary("Ouvrir le journal complet") + btn_primary("Nouvel utilisateur")) + """

      <div style="display: flex; gap: 16px; flex-grow: 1; min-height: 0;">
        <div style="width: 780px; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; flex-shrink: 0;">
          """ + card_title("Utilisateurs et droits d'accès", '<div style="display: flex; gap: 8px;">' + sel("Profil", "Tous") + sel("Structure", "Toutes") + '</div>') + """
          <div style="display: flex; flex-direction: column;">""" + user_table + """</div>
          """ + alert("info", "Quatre profils : <strong>administrateur</strong>, <strong>agent de saisie</strong>, <strong>validateur</strong>, <strong>consultation</strong>. Le <strong>validateur</strong> assure la vérification (étape 2) puis la validation (étape 3). Les droits se règlent par module et par structure sur la fiche de chaque utilisateur.") + """
          """ + footer("6 utilisateurs affichés sur 23 · déconnexion automatique après 15 min d'inactivité", pager("Page 1 sur 4")) + """
        </div>

        <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 16px; min-width: 0;">
          <div style="background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px;">
            """ + card_title("Sauvegardes", badge("Quotidienne · 02:00", "ok")) + """
            """ + kv("Dernière sauvegarde", "02/09/2026 à 02:00 · 412" + NB + "Mo") + kv("Chiffrement", "AES-256 · clé gérée par la DSI") + kv("Dernière restauration testée", "25/08/2026 — réussie en 4 min") + kv("Points de restauration", "30 jours glissants · 30 points") + """
            <div style="display: flex; gap: 10px; padding-top: 4px;">""" + btn_secondary("Restaurer…") + btn_primary("Sauvegarder maintenant", plus=False) + """</div>
          </div>
          <div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 16px 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px; min-height: 0;">
            """ + card_title("Journal d'audit — aujourd'hui", '<a href="#" style="font-size: 12.5px; font-weight: 600;">Tout le journal</a>') + """
            <div style="display: flex; flex-direction: column;">""" + audit_list + """</div>
            <span style="margin-top: auto; font-size: 12px; color: #5C6B64;">Chaque action est horodatée, attribuée et conservée 5 ans. Le journal n'est pas modifiable.</span>
          </div>
        </div>
      </div>"""

# ============================== MINI-LOT « SAISIE & ÉTATS » ==============================
def with_overlay(html, overlay):
    """Rend la racine positionnée et insère un calque par-dessus l'écran."""
    html = html.replace('<div style="width: 1440px; height: 900px; display: flex; background: #ECF1EE; overflow: hidden;">',
                        '<div style="width: 1440px; height: 900px; display: flex; background: #ECF1EE; overflow: hidden; position: relative;">', 1)
    idx = html.rindex("</div>\n</x-dc>")
    return html[:idx] + overlay + "\n" + html[idx:]

BACKDROP = '<div style="position: absolute; top: 0; left: 0; width: 1440px; height: 900px; background: rgba(11,46,41,0.38);"></div>'
CLOSE = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4 L12 12 M12 4 L4 12" stroke="#61706A" stroke-width="1.6" stroke-linecap="round"></path></svg>'

def drawer(title, sub, body, footer_html, width=460):
    return BACKDROP + ('<div style="position: absolute; top: 0; right: 0; width: %dpx; height: 900px; background: #FFFFFF; box-shadow: -8px 0 32px rgba(11,46,41,0.18); display: flex; flex-direction: column; box-sizing: border-box;">'
        '<div style="display: flex; align-items: flex-start; justify-content: space-between; padding: 22px 24px 14px; border-bottom: 1px solid #E9EEEA;"><div style="display: flex; flex-direction: column; gap: 3px;"><span style="font-family: %s; font-size: 20px; font-weight: 700;">%s</span><span style="font-size: 12.5px; color: #61706A;">%s</span></div>%s</div>'
        '<div style="flex-grow: 1; padding: 18px 24px; display: flex; flex-direction: column; gap: 14px; overflow: hidden;">%s</div>'
        '<div style="padding: 14px 24px 20px; border-top: 1px solid #E9EEEA; display: flex; flex-direction: column; gap: 10px;">%s</div></div>') % (width, SERIF, title, sub, CLOSE, body, footer_html)

def modal(title, body, footer_html, width=560, top=250):
    left = (1440 - width) // 2
    return BACKDROP + ('<div style="position: absolute; top: %dpx; left: %dpx; width: %dpx; background: #FFFFFF; border-radius: 12px; box-shadow: 0 24px 64px rgba(11,46,41,0.28); display: flex; flex-direction: column; box-sizing: border-box; overflow: hidden;">'
        '<div style="padding: 22px 26px 6px;"><span style="font-family: %s; font-size: 20px; font-weight: 700;">%s</span></div>'
        '<div style="padding: 10px 26px 18px; display: flex; flex-direction: column; gap: 12px;">%s</div>'
        '<div style="padding: 14px 26px 20px; background: #F6F9F7; border-top: 1px solid #E9EEEA; display: flex; justify-content: flex-end; gap: 10px;">%s</div></div>') % (top, left, width, SERIF, title, body, footer_html)

def toast(kind, html, action=""):
    styles = {"ok": ("#0F3B33", "#FFFFFF", "#7CD4B4"), "err": ("#7A1A1A", "#FFFFFF", "#FFC9C4")}
    bg, fg, ac = styles[kind]
    icon = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;"><circle cx="9" cy="9" r="7" stroke="%s" stroke-width="1.6"></circle><path d="M6 9.2 L8.2 11.4 L12.2 7" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg>' % (ac, ac)) if kind == "ok" else ''
    act = '<a href="#" style="font-size: 13px; font-weight: 700; color: %s; margin-left: 8px; white-space: nowrap;">%s</a>' % (ac, action) if action else ""
    return '<div style="position: absolute; top: 74px; left: 520px; width: 640px; background: %s; color: %s; border-radius: 10px; padding: 12px 16px; box-shadow: 0 12px 32px rgba(11,46,41,0.3); display: flex; align-items: center; gap: 12px; box-sizing: border-box;">%s<span style="font-size: 13px; line-height: 1.45; flex-grow: 1;">%s</span>%s%s</div>' % (bg, fg, icon, html, act, '<span style="opacity: 0.7; margin-left: 6px;">%s</span>' % CLOSE.replace("#61706A", "#FFFFFF"))

def read_lot1(name):
    with io.open(os.path.join(LOT1, name), encoding="utf-8") as f:
        return f.read()

def write_out(name, html):
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("ok", name, len(html))

# --- Planning : formulaire de saisie avec doublon détecté en direct
planning = read_lot1("Planning.dc.html")
saisie_body = (
    '<div style="display: flex; flex-direction: column; gap: 6px;"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">Type</label>' + segmented(["Garde", "Astreinte", "Permanence"], "Garde") + '</div>'
    + field("Agent", "Dr Y. Benali — M-04512 · Urgences", help_text="Tapez un nom ou un matricule", grow=False)
    + '<div style="display: flex; gap: 10px;">' + field_text("Date", "Mercredi 12/08/2026", grow=True) + field("Service", "Urgences", grow=True) + '</div>'
    + '<div style="display: flex; flex-direction: column; gap: 6px;"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">Durée</label>' + chips(["Nuit · 12 h", "24 h", "Week-end · 48 h", "Autre…"], "24 h") + '</div>'
    + alert("err", "<strong>Doublon :</strong> Dr Y. Benali a déjà une garde le 12/08/2026 (saisie par A. Tazi le 26/08). Choisissez une autre date ou un autre agent.", "Voir la saisie existante")
    + field_text("Commentaire (facultatif)", "ex. remplacement du Dr Saidi", placeholder=True, grow=False)
)
saisie_footer = ('<div style="display: flex; align-items: center; gap: 10px; font-size: 12.5px; color: #3A4741;"><span style="width: 18px; height: 18px; border-radius: 4px; border: 1.5px solid #10554A; background: #10554A; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.5 6.2 L5 8.6 L9.5 3.8" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>Saisie en série : après enregistrement, passer au jour suivant pour le même agent</div>'
    '<div style="display: flex; gap: 10px;"><div style="flex-grow: 1;">' + btn_secondary("Annuler").replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center;') + '</div><div style="flex-grow: 2;">' + btn_disabled("Enregistrer la garde").replace('padding: 0 16px;', 'padding: 0 16px; width: 100%;') + '</div></div>'
    '<span style="font-size: 12px; color: #5C6B64; text-align: center;">Enregistrer est désactivé tant que le doublon n\'est pas résolu.</span>')
write_out("PlanningSaisie.dc.html", with_overlay(planning, drawer("Nouvelle saisie", "Planning — Urgences · Août 2026 · 3 saisies dans cette série", saisie_body, saisie_footer)))

# --- Planning : succès + saisie en série
planning_ok = planning.replace(
    '<span style="font-size: 12px; font-weight: 600; color: #61706A;">13</span>',
    '<span style="font-size: 12px; font-weight: 600; color: #61706A;">13</span>\n            <span style="display: flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 600; color: #3A4741; background: #ECF1EE; border-radius: 4px; padding: 2px 6px; box-shadow: 0 0 0 1.5px #0A8467;"><span style="width: 7px; height: 7px; border-radius: 2px; background: #0A8467; flex-shrink: 0;"></span>G · Dr Benali</span>', 1)
planning_ok = planning_ok.replace('<div style="border-right: 1px solid #EDF1EE; padding: 6px 8px;"><span style="font-size: 12px; font-weight: 600; color: #61706A;">13</span>',
                                  '<div style="border-right: 1px solid #EDF1EE; padding: 6px 8px; display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 12px; font-weight: 600; color: #61706A;">13</span>', 1)
assert planning_ok != planning, "cellule du 13 introuvable"
serie_body = (
    alert("ok", "<strong>Garde du 13/08 enregistrée</strong> — Dr Y. Benali, 24 h, Urgences. Journalisée à 09:52.", "Annuler")
    + '<div style="display: flex; flex-direction: column; gap: 6px;"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">Type</label>' + segmented(["Garde", "Astreinte", "Permanence"], "Garde") + '</div>'
    + field("Agent", "Dr Y. Benali — M-04512 · Urgences", help_text="Conservé pour la série", grow=False)
    + '<div style="display: flex; gap: 10px;">' + field_text("Date", "Vendredi 14/08/2026", help_text="Jour suivant, modifiable", grow=True) + field("Service", "Urgences", grow=True) + '</div>'
    + '<div style="display: flex; flex-direction: column; gap: 6px;"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">Durée</label>' + chips(["Nuit · 12 h", "24 h", "Week-end · 48 h", "Autre…"], "24 h") + '</div>'
    + field_text("Commentaire (facultatif)", "ex. remplacement du Dr Saidi", placeholder=True, grow=False)
)
serie_footer = ('<div style="display: flex; align-items: center; gap: 10px; font-size: 12.5px; color: #3A4741;"><span style="width: 18px; height: 18px; border-radius: 4px; border: 1.5px solid #10554A; background: #10554A; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.5 6.2 L5 8.6 L9.5 3.8" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>Saisie en série : le formulaire reste ouvert au jour suivant pour le même agent</div>'
    '<div style="display: flex; gap: 10px;"><div style="flex-grow: 1;">' + btn_secondary("Terminer la série").replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center;') + '</div><div style="flex-grow: 2;">' + btn_primary("Enregistrer la garde", plus=False).replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center;') + '</div></div>'
    '<span style="font-size: 12px; color: #5C6B64; text-align: center;">4 saisies dans cette série · Échap ou « Terminer la série » ferme le formulaire.</span>')
write_out("PlanningEnregistre.dc.html", with_overlay(planning_ok, drawer("Nouvelle saisie", "Planning — Urgences · Août 2026 · saisie en série", serie_body, serie_footer)))

# --- Missions : formulaire d'ordre de mission avec calcul prévisionnel en direct
missions_html = render("Missions.dc.html", "Missions", MISSIONS, "Rechercher un OM, un agent…", "AT", "A. Tazi", "Agent de saisie")
om_body = (
    field("Agent", "Dr K. Saidi — M-04527 · Réanimation · Groupe A", grow=False)
    + '<div style="display: flex; gap: 10px;">' + field_text("Départ", "25/08/2026", grow=True) + field_text("Retour", "26/08/2026", grow=True) + '</div>'
    + '<div style="display: flex; gap: 10px;">' + field_text("Destination", "Agadir", grow=True) + field_text("Distance (aller)", "452 km", help_text="Calculée depuis Guelmim — modifiable", grow=True) + '</div>'
    + field_text("Motif", "Réunion régionale de coordination", grow=False)
    + '<div style="display: flex; flex-direction: column; gap: 4px; padding: 12px 14px; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px;">'
      '<span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #5C6B64; text-transform: uppercase; padding-bottom: 4px;">Indemnité prévisionnelle — mise à jour à chaque champ</span>'
      + kv("Durée × indemnité journalière (Groupe A)", "2 × 400" + NB + "DH") + kv("Coefficient de distance (> 150 km)", "× 1,5") +
      '<div style="display: flex; justify-content: space-between; align-items: baseline; padding-top: 8px;"><span style="font-size: 13px; font-weight: 700;">Total (plafond 2' + NB + '000' + NB + 'DH respecté)</span><span style="font-size: 18px; font-weight: 700;">1' + NB + '200' + NB + 'DH</span></div></div>'
)
om_footer = ('<div style="display: flex; gap: 10px;"><div style="flex-grow: 1;">' + btn_secondary("Annuler").replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center;') + '</div><div style="flex-grow: 2;">' + btn_primary("Créer l'ordre de mission", plus=False).replace('padding: 0 16px;', 'padding: 0 16px; width: 100%; justify-content: center;') + '</div></div>'
    '<span style="font-size: 12px; color: #5C6B64; text-align: center;">L\'ordre est créé « En cours » ; le montant définitif est calculé à la clôture, avec le barème en vigueur à la date du départ.</span>')
write_out("MissionSaisie.dc.html", with_overlay(missions_html, drawer("Nouvel ordre de mission", "Missions & déplacements — CHR de Guelmim", om_body, om_footer)))

# --- Validation : confirmation avant validation
validation = read_lot1("Validation.dc.html")
confirm_body = (
    '<span style="font-size: 13.5px; color: #3A4741; line-height: 1.5;">Vous êtes sur le point de valider le lot <strong>LOT-2026-0142</strong> — Gardes, Urgences, août 2026.</span>'
    '<div style="display: flex; flex-direction: column; padding: 4px 14px; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px;">' + kv("Agents concernés", "12") + kv("Montant total", "18" + NB + "450" + NB + "DH") + kv("Vérifié par", "S. Mansouri — 28/08/2026") + '</div>'
    + alert("info", "Après validation, le lot passe <strong>« Prêt pour paiement »</strong> et n\'est plus modifiable. Cette action est journalisée à votre nom.")
)
confirm_footer = btn_secondary("Annuler") + btn_primary("Confirmer la validation", plus=False)
write_out("ValidationConfirm.dc.html", with_overlay(validation, modal("Valider le lot LOT-2026-0142 ?", confirm_body, confirm_footer)))

# --- Validation : succès (lot retiré, suivant sélectionné, compteurs à jour)
def sans_0142(base):
    """Lot 0142 retiré de la liste, lot 0140 sélectionné, compteur « à traiter » à 11."""
    v = base
    v, n = re.subn(r'\s*<div style="display: grid; grid-template-columns: 130px 110px 105px 60px 95px 70px; gap: 10px; padding: 10px; font-size: 13px; align-items: center; background: #EDF4F1; box-shadow: inset 0 0 0 1\.5px #10554A; border-radius: 8px;">\s*<span style="font-weight: 700; color: #10554A;">LOT-2026-0142</span>.*?3' + NB + r'j</span></span>\s*</div>', "", v, count=1, flags=re.S)
    assert n == 1, "ligne 0142 introuvable"
    v = v.replace('<div style="display: grid; grid-template-columns: 130px 110px 105px 60px 95px 70px; gap: 10px; padding: 10px; font-size: 13px; align-items: center; border-bottom: 1px solid #EDF1EE;">\n              <span style="font-weight: 600; color: #10554A;">LOT-2026-0140</span>',
                  '<div style="display: grid; grid-template-columns: 130px 110px 105px 60px 95px 70px; gap: 10px; padding: 10px; font-size: 13px; align-items: center; background: #EDF4F1; box-shadow: inset 0 0 0 1.5px #10554A; border-radius: 8px;">\n              <span style="font-weight: 700; color: #10554A;">LOT-2026-0140</span>', 1)
    v = v.replace("6 lots affichés sur 12", "5 lots affichés sur 11").replace("En attente (12)", "En attente (11)")
    v = v.replace('<span style="font-size: 19px; font-weight: 700; color: #10554A;">12 lots</span>', '<span style="font-size: 19px; font-weight: 700; color: #10554A;">11 lots</span>')
    v = v.replace('<span style="font-size: 12px; color: #3A5C52;">98' + NB + '640' + NB + 'DH</span>', '<span style="font-size: 12px; color: #3A5C52;">80' + NB + '190' + NB + 'DH</span>')
    v = v.replace('>12</span>\n      </div>', '>11</span>\n      </div>', 1)  # badge sidebar
    v = (v.replace("LOT-2026-0142</span>", "LOT-2026-0140</span>", 1)
          .replace("Gardes — Urgences · Août 2026 · 12 agents", "Gardes — Chirurgie · Août 2026 · 9 agents")
          .replace('<span style="font-size: 24px; font-weight: 700; color: #182420;">18' + NB + '450</span>', '<span style="font-size: 24px; font-weight: 700; color: #182420;">14' + NB + '780</span>')
          .replace("Dr Y. Benali — 6 gardes", "Dr R. Chakir — 5 gardes").replace("3" + NB + "600" + NB + "DH</span>", "3" + NB + "000" + NB + "DH</span>", 1)
          .replace("Dr K. Saidi — 5 gardes", "Dr N. Lamrani — 5 gardes").replace("Dr M. El Idrissi — 4 gardes", "Dr F. Zahidi — 4 gardes")
          .replace("Voir les 12 lignes du lot", "Voir les 9 lignes du lot")
          .replace("26/08/2026 à 09:14", "27/08/2026 à 10:05").replace("28/08/2026 à 11:02", "30/08/2026 à 15:30").replace("depuis 3 jours", "depuis 2 jours"))
    return v

v_ok = sans_0142(validation)
v_ok = v_ok.replace('<span style="font-size: 19px; font-weight: 700; color: #182420;">23 lots</span>', '<span style="font-size: 19px; font-weight: 700; color: #182420;">24 lots</span>')
v_ok = v_ok.replace('<span style="font-size: 12px; color: #5C6B64;">96' + NB + '830' + NB + 'DH</span>', '<span style="font-size: 12px; color: #5C6B64;">115' + NB + '280' + NB + 'DH</span>')
v_ok = v_ok.replace("Prêts pour paiement (23)", "Prêts pour paiement (24)")
write_out("ValidationSucces.dc.html", with_overlay(v_ok, toast("ok", "<strong>Lot LOT-2026-0142 validé</strong> — 18" + NB + "450" + NB + "DH · prêt pour paiement · journalisé le 02/09/2026 à 09:12 (N. El Fassi).", "Annuler (5 min)")))

# --- Validation : rejet (W-05) — le lot repart en saisie avec le motif
v_rej = sans_0142(validation)
v_rej = v_rej.replace('<span style="font-size: 19px; font-weight: 700; color: #182420;">8 lots</span>', '<span style="font-size: 19px; font-weight: 700; color: #182420;">9 lots</span>')
v_rej = v_rej.replace('<span style="font-size: 12px; color: #5C6B64;">21' + NB + '340' + NB + 'DH</span>', '<span style="font-size: 12px; color: #5C6B64;">39' + NB + '790' + NB + 'DH</span>')
v_rej = v_rej.replace("Rejetés (2)", "Rejetés (3)")
write_out("ValidationRejete.dc.html", with_overlay(v_rej, toast("ok", "<strong>Lot LOT-2026-0142 renvoyé à la saisie</strong> — motif transmis à A. Tazi (notification) · 18" + NB + "450" + NB + "DH retirés de l'attente · journalisé le 02/09/2026 à 09:14.", "Annuler (5 min)")))


# --- Validation : état vide
v_empty = validation
v_empty, n = re.subn(r'<div style="display: flex; flex-direction: column;">\s*<div style="display: grid; grid-template-columns: 130px 110px 105px 60px 95px 70px;.*?(?=<div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center; padding-top: 8px;)',
    '<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; padding: 40px 0;">'
    '<svg width="72" height="72" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="6.5" y="6.5" width="11" height="11" stroke="#B98A2F" stroke-width="1.4"></rect><rect x="6.5" y="6.5" width="11" height="11" stroke="#B98A2F" stroke-width="1.4" transform="rotate(45 12 12)"></rect><path d="M9.5 12.2 L11.3 14 L14.8 10.3" stroke="#10554A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
    '<span style="font-size: 16px; font-weight: 600; color: #182420;">Aucun lot en attente de validation</span>'
    '<span style="font-size: 13px; color: #61706A; text-align: center; max-width: 380px; line-height: 1.5;">Tout est à jour pour août 2026. Les prochains lots apparaîtront ici dès qu\'ils auront été vérifiés.</span>'
    '<div style="display: flex; gap: 10px; padding-top: 6px;">' + btn_secondary("Voir les lots prêts pour paiement (24)") + btn_secondary("Voir les lots en vérification (5)") + '</div></div>\n            ',
    v_empty, count=1, flags=re.S)
assert n == 1, "tableau des lots introuvable"
v_empty = v_empty.replace('<span style="font-size: 19px; font-weight: 700; color: #10554A;">12 lots</span>', '<span style="font-size: 19px; font-weight: 700; color: #10554A;">0 lot</span>')
v_empty = v_empty.replace('<span style="font-size: 12px; color: #3A5C52;">98' + NB + '640' + NB + 'DH</span>', '<span style="font-size: 12px; color: #3A5C52;">0' + NB + 'DH</span>')
v_empty = v_empty.replace('<span style="font-size: 19px; font-weight: 700; color: #182420;">23 lots</span>', '<span style="font-size: 19px; font-weight: 700; color: #182420;">24 lots</span>')
v_empty = v_empty.replace("6 lots affichés sur 12", "0 lot en attente").replace("En attente (12)", "En attente (0)").replace("Prêts pour paiement (23)", "Prêts pour paiement (24)")
v_empty, n = re.subn(r'\s*<span style="min-width: 18px; height: 18px; border-radius: 9px; background: #B98A2F;[^>]*>12</span>', "", v_empty, count=1)
# panneau de droite : vide aussi
v_empty, n2 = re.subn(r'(<div style="flex-grow: 1; background: #FFFFFF; border: 1px solid #DBE3DE; border-radius: 10px; padding: 18px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 14px;">).*?(?=\n      </div>\n\n    </div>)',
    r'\1<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;"><span style="font-size: 13px; color: #61706A; text-align: center; max-width: 260px; line-height: 1.5;">Aucun lot à afficher pour ce filtre.</span></div>\n        </div>',
    v_empty, count=1, flags=re.S)
assert n2 == 1, "panneau détail introuvable"
v_empty = re.sub(r'<a [^>]*>Afficher tout</a>', "", v_empty, count=1)
write_out("ValidationVide.dc.html", v_empty)

# --- Personnel : résultat d'import Excel avec erreurs
personnel_html = render("Personnel.dc.html", "Personnel", PERSONNEL, "Matricule ou nom…", "HB", "H. Bouzid", "Administrateur")
IMP_GRID = "60px 1fr 1fr"
imp_rows = [
    ("7", "M-04512 · Dr Y. Benali", "Matricule déjà présent — la ligne sera ignorée (fiche existante conservée)"),
    ("11", "M-04788 · Inf. S. Bakkali", "Grade « Infirmier chef » inconnu — choisir un grade du barème"),
    ("14", "M-04791 · Tech. A. Ouhadda", "Groupe vide — obligatoire pour calculer les indemnités"),
]
imp_table = thead(["Ligne", "Agent", "Problème et correction"], IMP_GRID) + "".join(
    trow(['<span style="font-weight: 600;">%s</span>' % l, '<span style="color: #3A4741;">%s</span>' % a, '<span style="color: #A61B1B;">%s</span>' % p], IMP_GRID, False, i == 2)
    for i, (l, a, p) in enumerate(imp_rows))
import_body = (
    '<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px;">'
    '<div style="padding: 10px 12px; background: #F6F9F7; border-radius: 8px; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: #5C6B64;">Lignes lues</span><span style="font-size: 20px; font-weight: 700;">15</span></div>'
    '<div style="padding: 10px 12px; background: #E4F2E9; border-radius: 8px; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: #17663F;">Prêtes à importer</span><span style="font-size: 20px; font-weight: 700; color: #17663F;">12</span></div>'
    '<div style="padding: 10px 12px; background: #FADEDC; border-radius: 8px; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: #A61B1B;">En erreur</span><span style="font-size: 20px; font-weight: 700; color: #A61B1B;">3</span></div></div>'
    '<div style="display: flex; flex-direction: column;">' + imp_table + '</div>'
    '<span style="font-size: 12.5px; color: #3A4741; line-height: 1.5;">Aucune donnée n\'a encore été enregistrée. Vous pouvez importer les 12 lignes valides maintenant et corriger les 3 autres dans le fichier, ou tout corriger avant d\'importer.</span>'
)
import_footer = btn_secondary("Télécharger le rapport d'erreurs", DL_ICON) + btn_secondary("Annuler") + btn_primary("Importer les 12 lignes valides", plus=False)
write_out("PersonnelImportErreur.dc.html", with_overlay(personnel_html, modal("Import Excel — personnel_aout_2026.xlsx", import_body, import_footer, width=720)))

# --- Missions : ordre créé (W-01)
write_out("MissionCree.dc.html", with_overlay(missions_html, toast("ok", "<strong>Ordre de mission OM-2026-088 créé</strong> — Dr K. Saidi · Agadir · 25–26/08 · En cours · 1" + NB + "200" + NB + "DH prévisionnels. Journalisé le 20/08/2026 à 14:31 (A. Tazi).", "Modifier")))

# --- Missions : mission clôturée et envoyée au calcul (W-01)
m_clot = missions_html.replace(badge("En cours", "neutral"), badge("Clôturée", "ok"))
m_clot = m_clot.replace("En cours (5)", "En cours (4)").replace("Clôturées (6)", "Clôturées (7)")
m_clot, n = re.subn(r'(<div[^>]*>)\s*<button[^>]*>Modifier</button>\s*<button[^>]*>Clôturer et envoyer au calcul</button>\s*</div>',
    lambda m: m.group(1) + '<div style="flex-grow: 1;">' + alert("ok", "<strong>Clôturée le 27/08/2026 à 08:45</strong> par A. Tazi — 1" + NB + "200" + NB + "DH envoyés au calcul d'août (barème v3).", "Voir dans Calcul") + '</div></div>', m_clot, count=1, flags=re.S)
assert n == 1, "boutons Missions introuvables"
write_out("MissionCloturee.dc.html", with_overlay(m_clot, toast("ok", "<strong>Mission OM-2026-088 clôturée</strong> — 1" + NB + "200" + NB + "DH envoyés au calcul d'août 2026. Journalisé le 27/08/2026 à 08:45 (A. Tazi).", "Voir dans Calcul")))

# --- Validation : lignes du lot (W-02)
LIGNES_GRID = "1fr 150px 130px 70px 90px 80px"
lignes = [
    ("Dr Y. Benali", "Médecin spécialiste", "6 · 01, 09, 12, 22, 29, 30/08", "600", "3" + NB + "600"),
    ("Dr K. Saidi", "Médecin spécialiste", "5 · 02, 08, 15, 21, 29/08", "600", "3" + NB + "000"),
    ("Dr M. El Idrissi", "Médecin généraliste", "4 · 08, 16, 23, 30/08", "500", "2" + NB + "000"),
    ("Dr S. Ouazzani", "Médecin généraliste", "3 · 05, 16, 26/08", "500", "1" + NB + "500"),
    ("Dr A. Boulahya", "Médecin spécialiste", "3 · 03, 17, 24/08", "600", "1" + NB + "800"),
    ("Dr H. Sbai", "Médecin spécialiste", "3 · 06, 13, 27/08", "600", "1" + NB + "800"),
    ("Dr W. Kettani", "Médecin généraliste", "3 · 07, 19, 28/08", "500", "1" + NB + "500"),
    ("Inf. L. Mansouri", "Infirmier anesthésiste", "3 · 04, 18, 25/08", "300", "900"),
    ("Inf. S. Bakkali", "Infirmier polyvalent", "3 · 10, 20, 31/08", "300", "900"),
    ("Inf. R. Amrani", "Infirmier polyvalent", "2 · 11, 14/08", "300", "600"),
    ("Inf. H. Ouhadda", "Infirmier polyvalent", "2 · 01, 15/08", "300", "600"),
    ("Tech. H. Drissi", "Technicien radiologie", "1 · 22/08", "250", "250"),
]
lignes_table = thead(["Agent", "Grade", "Gardes · dates", "Taux", "Montant", ""], LIGNES_GRID) + "".join(
    trow(['<span style="font-weight: 600;">%s</span>' % a, '<span style="color: #3A4741;">%s</span>' % g, '<span style="color: #3A4741;">%s</span>' % d,
          '<span style="color: #3A4741;">%s' % t + NB + 'DH</span>', '<span style="font-weight: 700;">%s' % m + NB + 'DH</span>',
          '<a href="#" style="font-size: 12.5px; font-weight: 600; text-align: right;">Planning</a>'], LIGNES_GRID, False, i == len(lignes) - 1)
    for i, (a, g, d, t, m) in enumerate(lignes))
lignes_body = (
    '<span style="font-size: 13px; color: #61706A;">12 agents · 38 gardes · barème v3 (effet 01/07/2026) · issues des plannings d\'août validés par S. Mansouri le 28/08.</span>'
    '<div style="display: flex; flex-direction: column;">' + lignes_table + '</div>'
    '<div style="display: flex; justify-content: space-between; align-items: baseline; padding: 8px 10px; background: #F6F9F7; border-radius: 8px;"><span style="font-size: 13px; font-weight: 700;">Total du lot</span><span style="font-size: 18px; font-weight: 700;">18' + NB + '450' + NB + 'DH</span></div>'
)
lignes_footer = btn_secondary("Fermer") + btn_secondary("Exporter (Excel)") + btn_primary("Valider le lot", plus=False)
write_out("ValidationLignes.dc.html", with_overlay(validation, modal("Lignes du lot LOT-2026-0142 — Gardes, Urgences, août 2026", lignes_body, lignes_footer, width=880, top=48)))

# ============================== rendu des 4 écrans ==============================
render("Calcul.dc.html", "Calcul", CALCUL, "Rechercher un agent…", "HB", "H. Bouzid", "Administrateur")
render("Etats.dc.html", "États &amp; rapports", ETATS, "Rechercher un rapport…", "NE", "N. El Fassi", "Validateur")
render("Statistiques.dc.html", "Statistiques", STATS, "Rechercher…", "MR", "M. Raji", "Consultation")
admin_html = render("Administration.dc.html", "Administration", ADMIN, "Rechercher un utilisateur…", "HB", "H. Bouzid", "Administrateur")

# ============================== 5 PLANCHES DES AUDITS A / F ==============================
main_html = read_lot1("Main.dc.html")

def check(on):
    if on:
        return '<span style="width: 18px; height: 18px; border-radius: 4px; border: 1.5px solid #10554A; background: #10554A; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.5 6.2 L5 8.6 L9.5 3.8" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>'
    return '<span style="width: 18px; height: 18px; border-radius: 4px; border: 1.5px solid #C9D3CD; background: #FFFFFF; display: flex; flex-shrink: 0;"></span>'

def btn_danger(label):
    return '<button style="height: 38px; padding: 0 16px; background: #A61B1B; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: #FFFFFF; font-family: \'IBM Plex Sans\', \'Segoe UI\', sans-serif; cursor: pointer;">%s</button>' % label

def radio(label, sub, on):
    dot = ('<span style="width: 18px; height: 18px; border-radius: 9px; border: 5px solid #10554A; background: #FFFFFF; box-sizing: border-box; flex-shrink: 0;"></span>' if on
           else '<span style="width: 18px; height: 18px; border-radius: 9px; border: 1.5px solid #C9D3CD; background: #FFFFFF; box-sizing: border-box; flex-shrink: 0;"></span>')
    bg = ' background: #EDF4F1; border-color: #10554A;' if on else ''
    return ('<div style="display: flex; align-items: center; gap: 12px; padding: 10px 12px; border: 1px solid #DBE3DE; border-radius: 8px;%s">%s'
            '<div style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 13px; font-weight: 600;">%s</span><span style="font-size: 12px; color: #5C6B64;">%s</span></div></div>') % (bg, dot, label, sub)

# --- 1. Changement de mot de passe (M1) — modale depuis le menu utilisateur
def rule(ok, text):
    ic = ('<svg width="14" height="14" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="9" r="7" stroke="#17663F" stroke-width="1.5"></circle><path d="M6 9.2 L8.2 11.4 L12.2 7" stroke="#17663F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path></svg>' if ok
          else '<svg width="14" height="14" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="9" r="7" stroke="#AEB9B2" stroke-width="1.5"></circle></svg>')
    return '<span style="display: flex; align-items: center; gap: 7px; font-size: 12.5px; color: %s;">%s%s</span>' % ("#17663F" if ok else "#5C6B64", ic, text)
mdp_body = (
    field_text("Mot de passe actuel", "••••••••••••", grow=False)
    + '<div style="display: flex; gap: 10px;">' + field_text("Nouveau mot de passe", "••••••••••••••", grow=True) + field_text("Confirmer le nouveau mot de passe", "••••••••••••••", grow=True) + '</div>'
    + '<div style="display: flex; flex-direction: column; gap: 6px; padding: 10px 12px; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px;">'
      '<div style="display: flex; align-items: center; justify-content: space-between;"><span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #5C6B64; text-transform: uppercase;">Robustesse</span><span style="font-size: 12.5px; font-weight: 600; color: #17663F;">Forte</span></div>'
      '<div style="height: 6px; background: #E7EDE9; border-radius: 3px;"><div style="width: 85%; height: 6px; background: #17663F; border-radius: 3px;"></div></div>'
      '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px 16px; padding-top: 4px;">'
      + rule(True, "12 caractères minimum") + rule(True, "Une majuscule et une minuscule") + rule(True, "Un chiffre") + rule(False, "Différent des 5 derniers mots de passe — vérifié à l'enregistrement") + '</div></div>'
    + alert("info", "Vos autres sessions seront déconnectées. Ce changement est journalisé et vous recevrez une notification.")
)
mdp_footer = btn_secondary("Annuler") + btn_primary("Enregistrer le nouveau mot de passe", plus=False)
write_out("MotDePasse.dc.html", with_overlay(main_html, modal("Changer mon mot de passe", mdp_body, mdp_footer, width=600, top=150)))

# --- 2. Mission plafonnée (M8) — OM-2026-083, Groupe C, 4 j, 642 km : 1 500 DH calculés → 1 200 DH plafonnés
mp = missions_html
mp, n = re.subn(r'(<div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center;) background: #EDF4F1; box-shadow: inset 0 0 0 1\.5px #10554A; border-radius: 8px;">(\s*<span style="font-weight: )700(; color: #10554A;">OM-2026-088</span>)',
                r'\g<1> border-bottom: 1px solid #EDF1EE;">\g<2>600\g<3>', mp, count=1)
assert n == 1, "ligne 088"
mp, n = re.subn(r'(<div style="display: grid; grid-template-columns: 100px 135px 110px 70px 55px 70px 100px; gap: 8px; padding: 10px; font-size: 13px; align-items: center;)">(\s*<span style="font-weight: )600(; color: #10554A;">OM-2026-083</span>)',
                r'\g<1> background: #EDF4F1; box-shadow: inset 0 0 0 1.5px #10554A; border-radius: 8px;">\g<2>700\g<3>', mp, count=1)
assert n == 1, "ligne 083"
mp = (mp.replace('<span style="font-size: 16px; font-weight: 700; color: #182420;">OM-2026-088</span>', '<span style="font-size: 16px; font-weight: 700; color: #182420;">OM-2026-083</span>')
        .replace("Dr K. Saidi · Groupe A · Réanimation", "Inf. L. Mansouri · Groupe C · Réanimation")
        .replace("Guelmim → Agadir", "Guelmim → Rabat").replace("Réunion régionale de coordination", "Formation nationale — anesthésie")
        .replace("25–26/08/2026 (2" + NB + "jours)", "11–14/08/2026 (4" + NB + "jours)").replace("452" + NB + "km (aller)", "642" + NB + "km (aller)")
        .replace("Durée × indemnité journalière (Groupe A)</span><span>2 × 400", "Durée × indemnité journalière (Groupe C)</span><span>4 × 250")
        .replace("Créé par <strong>A. Tazi</strong> — 20/08/2026 à 14:31", "Créé par <strong>A. Tazi</strong> — 05/08/2026 à 10:12")
        .replace("Départ confirmé — 25/08/2026 à 08:02", "Clôturée le 15/08/2026 à 09:30 — envoyée au calcul d'août"))
mp = mp.replace("Groupe C · Réanimation</span>\n            </div>\n            " + badge("En cours", "neutral"), "Groupe C · Réanimation</span>\n            </div>\n            " + badge("Clôturée", "ok"), 1)
assert badge("Clôturée", "ok") in mp.split("Groupe C · Réanimation")[1][:400], "badge en-tête"
mp, n = re.subn(r'(<div style="display: flex; justify-content: space-between;[^"]*"><span[^>]*>)Total \(plafond 2' + NB + '000' + NB + r'DH respecté\)</span><span[^>]*>1' + NB + '200' + NB + 'DH</span></div>',
    lambda m: ('<div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #3A4741;">Sous-total</span><span>1' + NB + '500' + NB + 'DH</span></div>'
               '<div style="display: flex; justify-content: space-between; font-size: 12.5px;"><span style="color: #92400E;">Plafond Groupe C par mission (1' + NB + '200' + NB + 'DH)</span><span style="color: #92400E;">−' + NB + '300' + NB + 'DH</span></div>'
               + m.group(1) + 'Total (plafond appliqué)</span><span style="font-size: 18px; font-weight: 700;">1' + NB + '200' + NB + 'DH</span></div>'), mp, count=1)
assert n == 1, "ligne total"
mp, n = re.subn(r'(<div[^>]*>)\s*<button[^>]*>Modifier</button>\s*<button[^>]*>Clôturer et envoyer au calcul</button>\s*</div>',
    lambda m: m.group(1) + '<div style="flex-grow: 1;">' + alert("warn", "<strong>Plafond appliqué :</strong> 4 jours × 250" + NB + "DH × 1,5 = 1" + NB + "500" + NB + "DH, ramenés au plafond du groupe C (1" + NB + "200" + NB + "DH par mission, barème v3).", "Voir le barème") + '</div></div>', mp, count=1, flags=re.S)
assert n == 1, "boutons"
write_out("MissionPlafonnee.dc.html", mp)

# --- 3. Centre de notifications (M9) — tiroir depuis la cloche
def notif(unread, cat, text, when, action):
    dot = '<span style="width: 8px; height: 8px; border-radius: 4px; background: #B3261E; flex-shrink: 0; margin-top: 6px;"></span>' if unread else '<span style="width: 8px; height: 8px; flex-shrink: 0;"></span>'
    act = '<a href="#" style="font-size: 12.5px; font-weight: 600; white-space: nowrap;">%s</a>' % action if action else ''
    return ('<div style="display: flex; gap: 10px; padding: 10px 0; border-bottom: 1px solid #EDF1EE;%s">%s<div style="display: flex; flex-direction: column; gap: 4px; flex-grow: 1; min-width: 0;">'
            '<div style="display: flex; align-items: center; gap: 8px;">%s<span style="font-size: 12px; color: #5C6B64;">%s</span></div>'
            '<span style="font-size: 13px; color: #182420; line-height: 1.45;%s">%s</span></div>%s</div>') % (
        " background: #F6F9F7; margin: 0 -24px; padding-left: 24px; padding-right: 24px;" if unread else "", dot, badge(cat, "neutral"), when, " font-weight: 600;" if unread else "", text, act)
notif_body = (
    '<div style="display: flex; align-items: center; justify-content: space-between;">' + chips(["Toutes (6)", "Non lues (3)"], "Toutes (6)") + '<a href="#" style="font-size: 12.5px; font-weight: 600;">Tout marquer comme lu</a></div>'
    '<div style="display: flex; flex-direction: column;">'
    + notif(True, "Validation", "Lot LOT-2026-0136 en attente depuis 5 jours — Radiologie, déplacements, 4" + NB + "980" + NB + "DH", "il y a 2 h", "Traiter")
    + notif(True, "Calcul", "2 agents à recalculer — planning d'août modifié par A. Tazi (garde du 12/08 supprimée)", "09:40", "Voir")
    + notif(True, "Personnel", "Import Excel terminé — 12 agents ajoutés, 3 lignes en erreur", "08:55", "Rapport")
    + notif(False, "Validation", "Vous avez validé le lot LOT-2026-0145 — 11" + NB + "900" + NB + "DH · annulation possible jusqu'à 09:17", "09:12", "")
    + notif(False, "Barèmes", "Version 3 du barème « Garde — Médecins » en vigueur depuis le 01/07/2026", "hier", "")
    + notif(False, "Système", "Sauvegarde automatique effectuée — 412" + NB + "Mo, chiffrée", "02:00", "")
    + '</div>'
)
notif_footer = ('<div style="display: flex; align-items: center; justify-content: space-between;"><a href="#" style="font-size: 12.5px; font-weight: 600;">Préférences de notification</a><span style="font-size: 12px; color: #5C6B64;">Dans l\'application · e-mail : à confirmer</span></div>')
write_out("Notifications.dc.html", with_overlay(main_html, drawer("Notifications", "3 non lues · délais de validation, recalculs, imports, sauvegardes", notif_body, notif_footer, width=470)))

# --- 4. Confirmation de restauration (M12) — action destructive, double confirmation
rest_body = (
    '<span style="font-size: 13px; font-weight: 600; color: #3A4741;">Point de restauration</span>'
    '<div style="display: flex; flex-direction: column; gap: 8px;">' + radio("02/09/2026 à 02:00", "412" + NB + "Mo · la plus récente", False) + radio("01/09/2026 à 02:00", "409" + NB + "Mo · restauration testée le 25/08", True) + radio("31/08/2026 à 02:00", "407" + NB + "Mo · avant le calcul d'août", False) + '</div>'
    + alert("err", "<strong>Irréversible sans la sauvegarde de sécurité.</strong> La base reviendra à l'état du 01/09 à 02:00. Seront perdus : <strong>14 saisies, 2 validations et 1 import</strong> effectués depuis. Les 3 utilisateurs connectés seront déconnectés.")
    + '<div style="display: flex; flex-direction: column; padding: 4px 14px; background: #F6F9F7; border: 1px solid #E9EEEA; border-radius: 8px;">' + kv("Sauvegarde de sécurité avant restauration", "Automatique — conservée 30 jours") + kv("Durée estimée", "≈ 4 minutes · application indisponible") + kv("Journal d'audit", "Conservé, action tracée à votre nom") + '</div>'
    + '<div style="display: flex; align-items: center; gap: 10px; font-size: 12.5px; color: #3A4741;">' + check(True) + 'J\'ai prévenu la DSI et les utilisateurs connectés</div>'
    + field_text("Tapez RESTAURER pour confirmer", "RESTAU", grow=False)
)
rest_footer = btn_secondary("Annuler") + btn_danger("Restaurer la base — 01/09 02:00")
write_out("RestaurationConfirm.dc.html", with_overlay(admin_html, modal("Restaurer une sauvegarde", rest_body, rest_footer, width=640, top=90)))

# --- 5. Fiche utilisateur : droits par module × structure (M1)
STRUCTS = ["CHR de Guelmim", "CS Guelmim-Centre", "CS Bouizakarne", "Dél. Tan-Tan"]
MODULES = [("Plannings", [1, 0, 0, 0]), ("Calcul", [0, 0, 0, 0]), ("Missions", [0, 0, 0, 0]), ("Validation", [1, 0, 0, 0]), ("États & rapports", [1, 0, 0, 0]),
           ("Statistiques", [0, 0, 0, 0]), ("Personnel", [0, 0, 0, 0]), ("Structures", [0, 0, 0, 0]), ("Barèmes", [0, 0, 0, 0]), ("Administration", [0, 0, 0, 0])]
GRID_D = "150px repeat(4, minmax(0, 1fr))"
droits = ('<div style="display: grid; grid-template-columns: %s; gap: 6px; padding: 7px 10px; font-size: 12px; font-weight: 600; letter-spacing: 0.6px; color: #5C6B64; text-transform: uppercase; border-bottom: 1px solid #E9EEEA;"><span>Module</span>%s</div>' % (GRID_D, "".join('<span style="text-align: center;">%s</span>' % s for s in STRUCTS)))
for i, (mod, cells) in enumerate(MODULES):
    droits += ('<div style="display: grid; grid-template-columns: %s; gap: 6px; padding: 6px 10px; font-size: 13px; align-items: center;%s"><span style="font-weight: 600;">%s</span>%s</div>' % (
        GRID_D, "" if i == len(MODULES) - 1 else " border-bottom: 1px solid #EDF1EE;", mod, "".join('<span style="display: flex; justify-content: center;">%s</span>' % check(c) for c in cells)))
fiche_body = (
    '<div style="display: flex; gap: 10px;">' + field_text("Nom", "N. El Fassi", grow=True) + field_text("Identifiant", "n.elfassi", grow=True) + '</div>'
    '<div style="display: flex; gap: 10px;">' + field("Profil", "Validateur — vérifie et valide les lots", grow=True) + '<div style="display: flex; flex-direction: column; gap: 6px; flex-grow: 1;"><label style="font-size: 13px; font-weight: 600; color: #3A4741;">Statut</label>' + segmented(["Actif", "Désactivé"], "Actif") + '</div></div>'
    '<div style="display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #5C6B64; text-transform: uppercase;">Droits par module et par structure</span>'
    '<div style="border: 1px solid #E9EEEA; border-radius: 8px; overflow: hidden;">' + droits + '</div>'
    '<span style="font-size: 12px; color: #5C6B64;">Le profil fixe les droits par défaut ; les cases les restreignent ou les étendent structure par structure. Une structure non cochée est « hors périmètre » pour cet utilisateur.</span></div>'
    + kv("Dernière connexion", "02/09/2026 à 08:41") + kv("Mot de passe", "Modifié le 14/06/2026 · expire le 12/12/2026")
)
fiche_footer = ('<div style="display: flex; gap: 10px;">' + btn_secondary("Réinitialiser le mot de passe") + btn_danger_outline("Désactiver") + '<div style="flex-grow: 1;"></div>' + btn_primary("Enregistrer", plus=False) + '</div>')
write_out("UtilisateurFiche.dc.html", with_overlay(admin_html, drawer("N. El Fassi", "Fiche utilisateur · CHR de Guelmim · créée le 12/01/2026 par H. Bouzid", fiche_body, fiche_footer, width=640)))
