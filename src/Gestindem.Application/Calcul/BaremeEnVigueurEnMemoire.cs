using Gestindem.Domain.Baremes;
using Gestindem.Domain.Erreurs;

namespace Gestindem.Application.Calcul;

/// <summary>
/// Implémentation en mémoire de <see cref="IBaremeEnVigueur"/> : une liste de versions,
/// sélection de celle qui couvre la date. Sert aux tests golden et au jeu de démonstration.
/// L'implémentation de production (Infrastructure) fera la même sélection en base.
/// </summary>
public sealed class BaremeEnVigueurEnMemoire : IBaremeEnVigueur
{
    private readonly IReadOnlyList<BaremeVersion> _versions;

    public BaremeEnVigueurEnMemoire(IEnumerable<BaremeVersion> versions)
    {
        _versions = versions.ToList();
    }

    public BaremeVersion PourDate(DateOnly date)
    {
        var candidates = _versions.Where(v => v.EstEnVigueurLe(date)).ToList();

        return candidates.Count switch
        {
            1 => candidates[0],
            0 => throw new ErreurMetier(
                CodesErreur.BaremeAbsentADate,
                $"Aucune version de barème n'est en vigueur au {date:dd/MM/yyyy}."),
            _ => throw new ErreurMetier(
                CodesErreur.BaremeChevauchement,
                $"Plusieurs versions de barème couvrent le {date:dd/MM/yyyy} : {string.Join(", ", candidates.Select(c => "v" + c.Numero))}."),
        };
    }
}
