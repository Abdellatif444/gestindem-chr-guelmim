using Gestindem.Domain.Agents;
using Gestindem.Domain.Baremes;

namespace Gestindem.Application.Tests.Fixtures;

/// <summary>
/// Barèmes de référence des tests golden (ADR-004). Les valeurs sont celles des maquettes
/// (planche Barèmes : version 3 en vigueur depuis le 01/07/2026, version 2 archivée).
/// Ce sont des valeurs de DÉMONSTRATION : les taux réglementaires réels seront paramétrés
/// par l'administrateur (question client n°5). Une seule source de vérité : ce fichier sera
/// aussi le seed de démonstration (ADR-004, principe 2).
/// </summary>
public static class BaremesDeDemo
{
    public static readonly Grade MedecinSpecialiste = new("MED_SPE", "Médecin spécialiste");
    public static readonly Grade MedecinGeneraliste = new("MED_GEN", "Médecin généraliste");
    public static readonly Grade Infirmier = new("INF", "Infirmier");
    public static readonly Grade Technicien = new("TECH", "Technicien");

    public static readonly Groupe GroupeA = new("A");
    public static readonly Groupe GroupeB = new("B");
    public static readonly Groupe GroupeC = new("C");

    /// <summary>Version 2 — effet 01/01/2026 → 30/06/2026 (archivée). Garde spécialiste : 550 DH.</summary>
    public static BaremeVersion V2 => new(
        numero: 2,
        dateEffet: new DateOnly(2026, 1, 1),
        dateFin: new DateOnly(2026, 6, 30),
        taux:
        [
            new TauxIndemnite(MedecinSpecialiste, TypeIndemnite.Garde, 550m),
            new TauxIndemnite(MedecinSpecialiste, TypeIndemnite.Astreinte, 380m),
            new TauxIndemnite(MedecinSpecialiste, TypeIndemnite.Permanence, 330m),
            new TauxIndemnite(MedecinGeneraliste, TypeIndemnite.Garde, 460m),
            new TauxIndemnite(Infirmier, TypeIndemnite.Garde, 280m),
        ],
        grilles:
        [
            new GrilleDeplacement(GroupeA, indemniteJournaliere: 380m, plafondParMission: 1_900m),
            new GrilleDeplacement(GroupeB, indemniteJournaliere: 280m, plafondParMission: 1_400m),
            new GrilleDeplacement(GroupeC, indemniteJournaliere: 230m, plafondParMission: 1_150m),
        ],
        coefficients: CoefficientsStandard);

    /// <summary>Version 3 — effet 01/07/2026, en vigueur. Valeurs de la planche Barèmes.</summary>
    public static BaremeVersion V3 => new(
        numero: 3,
        dateEffet: new DateOnly(2026, 7, 1),
        dateFin: null,
        taux:
        [
            new TauxIndemnite(MedecinSpecialiste, TypeIndemnite.Garde, 600m),
            new TauxIndemnite(MedecinSpecialiste, TypeIndemnite.Astreinte, 400m),
            new TauxIndemnite(MedecinSpecialiste, TypeIndemnite.Permanence, 350m),
            new TauxIndemnite(MedecinGeneraliste, TypeIndemnite.Garde, 500m),
            new TauxIndemnite(MedecinGeneraliste, TypeIndemnite.Astreinte, 330m),
            new TauxIndemnite(MedecinGeneraliste, TypeIndemnite.Permanence, 300m),
            new TauxIndemnite(Infirmier, TypeIndemnite.Garde, 300m),
            new TauxIndemnite(Infirmier, TypeIndemnite.Astreinte, 200m),
            new TauxIndemnite(Infirmier, TypeIndemnite.Permanence, 180m),
            new TauxIndemnite(Technicien, TypeIndemnite.Garde, 250m),
            new TauxIndemnite(Technicien, TypeIndemnite.Astreinte, 170m),
            new TauxIndemnite(Technicien, TypeIndemnite.Permanence, 150m),
        ],
        grilles:
        [
            new GrilleDeplacement(GroupeA, indemniteJournaliere: 400m, plafondParMission: 2_000m),
            new GrilleDeplacement(GroupeB, indemniteJournaliere: 300m, plafondParMission: 1_500m),
            new GrilleDeplacement(GroupeC, indemniteJournaliere: 250m, plafondParMission: 1_200m),
        ],
        coefficients: CoefficientsStandard);

    /// <summary>
    /// Tranches de distance (bornes INCLUSES) : 0–49 km ×1,0 · 50–150 km ×1,2 · 151 km et plus ×1,5.
    /// Le cas D-03 vérifie que 150 km tombe dans la tranche ×1,2, pas ×1,5.
    /// </summary>
    private static IReadOnlyList<CoefficientDistance> CoefficientsStandard =>
    [
        new CoefficientDistance(distanceMinKm: 0, distanceMaxKm: 49, coefficient: 1.0m),
        new CoefficientDistance(distanceMinKm: 50, distanceMaxKm: 150, coefficient: 1.2m),
        new CoefficientDistance(distanceMinKm: 151, distanceMaxKm: null, coefficient: 1.5m),
    ];
}
