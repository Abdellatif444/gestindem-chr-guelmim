using Gestindem.Domain.Agents;
using Gestindem.Domain.Baremes;
using Gestindem.Domain.Erreurs;

namespace Gestindem.Domain.Plannings;

/// <summary>
/// Une garde, une astreinte ou une permanence saisie pour un agent à une date (M5).
/// Un planning vaut une unité d'indemnité ; l'unité de durée (nuit, demi-journée…) reste
/// une question client (AGENTS.md §11.4) et sera ajoutée quand elle sera tranchée.
/// </summary>
public sealed class Planning
{
    public Agent Agent { get; }
    public DateOnly Date { get; }
    public TypeIndemnite Type { get; }

    public Planning(Agent agent, DateOnly date, TypeIndemnite type)
    {
        if (type == TypeIndemnite.Deplacement)
        {
            throw new ErreurMetier(
                CodesErreur.PlanningTypeInvalide,
                "Un planning ne peut être qu'une garde, une astreinte ou une permanence ; un déplacement est une mission.");
        }

        Agent = agent;
        Date = date;
        Type = type;
    }
}
