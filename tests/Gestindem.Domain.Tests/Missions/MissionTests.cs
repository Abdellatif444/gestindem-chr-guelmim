using AwesomeAssertions;
using Gestindem.Domain.Agents;
using Gestindem.Domain.Erreurs;
using Gestindem.Domain.Missions;

namespace Gestindem.Domain.Tests.Missions;

public class MissionTests
{
    private static readonly Agent Saidi = new("M-04527", "Dr K. Saidi", new Grade("MED_SPE", "Médecin spécialiste"), new Groupe("A"));

    [Fact(DisplayName = "Distance nulle ou négative → MISSION_DISTANCE_INVALIDE")]
    public void Distance_invalide_refusee()
    {
        var construction = () => new Mission(Saidi, new DateOnly(2026, 8, 25), new DateOnly(2026, 8, 26), 0, EtatMission.EnCours);

        construction.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.MissionDistanceInvalide);
    }

    [Theory(DisplayName = "Durée en jours, bornes incluses")]
    [InlineData(25, 25, 1)]
    [InlineData(25, 26, 2)]
    [InlineData(11, 14, 4)]
    public void Duree_bornes_incluses(int depart, int retour, int attendu)
    {
        var mission = new Mission(Saidi, new DateOnly(2026, 8, depart), new DateOnly(2026, 8, retour), 100, EtatMission.Cloturee);

        mission.DureeJours.Should().Be(attendu);
    }
}
