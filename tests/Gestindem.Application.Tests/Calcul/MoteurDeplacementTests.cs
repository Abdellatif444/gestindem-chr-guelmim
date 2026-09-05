using AwesomeAssertions;
using Gestindem.Application.Calcul;
using Gestindem.Application.Tests.Fixtures;
using Gestindem.Domain.Agents;
using Gestindem.Domain.Erreurs;
using Gestindem.Domain.Missions;

namespace Gestindem.Application.Tests.Calcul;

/// <summary>
/// Cas golden G-05 et D-01 à D-06 (ADR-004) : moteur de calcul des indemnités de déplacement.
/// Formule M8 : durée × indemnité journalière du groupe × coefficient de distance,
/// plafonnée par mission (ADR-003). Le barème retenu est celui en vigueur à la date de DÉPART.
/// </summary>
public class MoteurDeplacementTests
{
    private static MoteurDeplacement Moteur() =>
        new(new BaremeEnVigueurEnMemoire([BaremesDeDemo.V2, BaremesDeDemo.V3]));

    private static Mission Mission(Agent agent, int jourDepart, int jourRetour, int distanceKm, EtatMission etat = EtatMission.Cloturee) =>
        new(agent, new DateOnly(2026, 8, jourDepart), new DateOnly(2026, 8, jourRetour), distanceKm, etat);

    [Fact(DisplayName = "D-01 · 2 j, 452 km, Groupe A : 2 × 400 × 1,5 = 1 200 DH, non plafonné")]
    public void D01_Deplacement_standard()
    {
        var mission = Mission(AgentsDeDemo.Saidi, jourDepart: 25, jourRetour: 26, distanceKm: 452);

        var r = Moteur().Calculer(mission);

        r.Should().BeEquivalentTo(new
        {
            DureeJours = 2,
            IndemniteJournaliere = 400m,
            Coefficient = 1.5m,
            MontantBrut = 1_200m,
            PlafondApplique = (decimal?)null,
            MontantFinal = 1_200m,
            BaremeVersion = 3,
        });
    }

    [Fact(DisplayName = "D-02 · 4 j, 642 km, Groupe C : brut 1 500 → plafonné à 1 200 DH (planche MissionPlafonnee)")]
    public void D02_Deplacement_plafonne()
    {
        var mission = Mission(AgentsDeDemo.Mansouri, jourDepart: 11, jourRetour: 14, distanceKm: 642);

        var r = Moteur().Calculer(mission);

        r.MontantBrut.Should().Be(1_500m, "4 × 250 × 1,5");
        r.PlafondApplique.Should().Be(1_200m, "plafond du Groupe C par mission");
        r.MontantFinal.Should().Be(1_200m);
    }

    [Theory(DisplayName = "D-03 · Bornes de tranche : 150 km → × 1,2 (pas × 1,5) ; 151 km → × 1,5 ; 49 km → × 1,0 ; 50 km → × 1,2")]
    [InlineData(150, 1.2)]
    [InlineData(151, 1.5)]
    [InlineData(49, 1.0)]
    [InlineData(50, 1.2)]
    public void D03_Bornes_des_tranches_de_distance(int distanceKm, decimal coefficientAttendu)
    {
        var mission = Mission(AgentsDeDemo.Saidi, jourDepart: 25, jourRetour: 25, distanceKm: distanceKm);

        Moteur().Calculer(mission).Coefficient.Should().Be(coefficientAttendu);
    }

    [Fact(DisplayName = "D-04 · 1 j, 42 km, Groupe C : 1 × 250 × 1,0 = 250 DH")]
    public void D04_Courte_distance()
    {
        var mission = Mission(AgentsDeDemo.Drissi, jourDepart: 19, jourRetour: 19, distanceKm: 42);

        var r = Moteur().Calculer(mission);

        r.DureeJours.Should().Be(1, "départ et retour le même jour = 1 jour");
        r.MontantFinal.Should().Be(250m);
    }

    [Fact(DisplayName = "D-05 · Une mission non clôturée est exclue du calcul")]
    public void D05_Mission_non_cloturee_exclue()
    {
        var cloturee = Mission(AgentsDeDemo.Saidi, 25, 26, 452, EtatMission.Cloturee);
        var enCours = Mission(AgentsDeDemo.Saidi, 28, 29, 300, EtatMission.EnCours);

        var resultats = Moteur().CalculerMissions([cloturee, enCours]);

        resultats.Should().ContainSingle().Which.Mission.Should().BeSameAs(cloturee);
    }

    [Fact(DisplayName = "D-06 · Retour avant départ → erreur MISSION_DATES_INVALIDES (invariant du domaine)")]
    public void D06_Dates_invalides()
    {
        var creation = () => Mission(AgentsDeDemo.Saidi, jourDepart: 26, jourRetour: 25, distanceKm: 100);

        creation.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.MissionDatesInvalides);
    }

    [Fact(DisplayName = "G-05 · Agent sans groupe → erreur AGENT_SANS_GROUPE")]
    public void G05_Agent_sans_groupe()
    {
        var mission = Mission(AgentsDeDemo.SansGroupe, 25, 26, 452);

        var calcul = () => Moteur().Calculer(mission);

        calcul.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.AgentSansGroupe);
    }
}
