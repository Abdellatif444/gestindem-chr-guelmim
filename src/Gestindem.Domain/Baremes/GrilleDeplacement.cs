using Gestindem.Domain.Agents;

namespace Gestindem.Domain.Baremes;

/// <summary>Grille de déplacement d'un groupe (M4) : indemnité journalière et plafond par mission, en dirhams.</summary>
public sealed class GrilleDeplacement
{
    public Groupe Groupe { get; }
    public decimal IndemniteJournaliere { get; }
    public decimal PlafondParMission { get; }

    public GrilleDeplacement(Groupe groupe, decimal indemniteJournaliere, decimal plafondParMission)
    {
        if (indemniteJournaliere <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(indemniteJournaliere), "L'indemnité journalière doit être positive.");
        }

        if (plafondParMission <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(plafondParMission), "Le plafond par mission doit être positif.");
        }

        Groupe = groupe;
        IndemniteJournaliere = indemniteJournaliere;
        PlafondParMission = plafondParMission;
    }
}
