using Gestindem.Domain.Agents;
using Gestindem.Domain.Erreurs;
using Gestindem.Domain.Plannings;

namespace Gestindem.Application.Calcul;

/// <summary>
/// Moteur de calcul des indemnités de garde, d'astreinte et de permanence (M6).
/// Règle : chaque planning est valorisé au taux de la version de barème en vigueur À SA DATE ;
/// les plannings sont regroupés par (type, version) pour conserver un instantané par taux appliqué
/// (cas golden G-03 : un mois à cheval sur deux versions produit deux lignes).
/// </summary>
public sealed class MoteurGardeAstreintePermanence
{
    private readonly IBaremeEnVigueur _baremes;

    public MoteurGardeAstreintePermanence(IBaremeEnVigueur baremes)
    {
        _baremes = baremes;
    }

    public ResultatCalculAgent CalculerAgent(Agent agent, IReadOnlyList<Planning> plannings)
    {
        // Égalité d'entité (matricule), pas de référence : les plannings peuvent avoir été chargés séparément.
        var etranger = plannings.FirstOrDefault(p => !p.Agent.Equals(agent));
        if (etranger is not null)
        {
            throw new ErreurMetier(
                CodesErreur.PlanningAgentIncoherent,
                $"Le planning du {etranger.Date:dd/MM/yyyy} appartient à {etranger.Agent.Matricule}, pas à {agent.Matricule}.");
        }

        var lignes = plannings
            .Select(p => (p.Type, Version: _baremes.PourDate(p.Date)))
            .GroupBy(x => (x.Type, x.Version.Numero))
            .OrderBy(g => g.Key.Type).ThenBy(g => g.Key.Numero)
            .Select(g =>
            {
                var version = g.First().Version;
                var taux = version.TauxPour(agent.Grade, g.Key.Type);
                var quantite = g.Count();
                return new LigneCalcul(g.Key.Type, quantite, taux, version.Numero, quantite * taux);
            })
            .ToList();

        return new ResultatCalculAgent(agent, lignes);
    }
}
