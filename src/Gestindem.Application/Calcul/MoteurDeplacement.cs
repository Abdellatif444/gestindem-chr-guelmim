using Gestindem.Domain.Missions;

namespace Gestindem.Application.Calcul;

/// <summary>
/// Moteur de calcul des indemnités de déplacement (M8) :
/// <c>brut = durée × indemnité journalière du groupe × coefficient de distance</c>,
/// puis <c>final = min(brut, plafond par mission du groupe)</c>.
/// Le barème retenu est celui en vigueur à la date de DÉPART de la mission.
/// </summary>
public sealed class MoteurDeplacement
{
    private readonly IBaremeEnVigueur _baremes;

    public MoteurDeplacement(IBaremeEnVigueur baremes)
    {
        _baremes = baremes;
    }

    public ResultatDeplacement Calculer(Mission mission)
    {
        var groupe = mission.Agent.GroupeRequis();
        var version = _baremes.PourDate(mission.DateDepart);
        var grille = version.GrillePour(groupe);
        var coefficient = version.CoefficientPour(mission.DistanceKm);

        var brut = mission.DureeJours * grille.IndemniteJournaliere * coefficient;
        var plafonne = brut > grille.PlafondParMission;

        return new ResultatDeplacement(
            Mission: mission,
            DureeJours: mission.DureeJours,
            IndemniteJournaliere: grille.IndemniteJournaliere,
            Coefficient: coefficient,
            MontantBrut: brut,
            PlafondApplique: plafonne ? grille.PlafondParMission : null,
            MontantFinal: plafonne ? grille.PlafondParMission : brut,
            BaremeVersion: version.Numero);
    }

    /// <summary>Calcule les missions clôturées ; les autres sont exclues (cas golden D-05).</summary>
    public IReadOnlyList<ResultatDeplacement> CalculerMissions(IEnumerable<Mission> missions) =>
        missions.Where(m => m.Etat == EtatMission.Cloturee).Select(Calculer).ToList();
}
