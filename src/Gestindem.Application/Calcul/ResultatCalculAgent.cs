using Gestindem.Domain.Agents;

namespace Gestindem.Application.Calcul;

/// <summary>Résultat du calcul garde/astreinte/permanence d'un agent sur une période.</summary>
public sealed record ResultatCalculAgent(Agent Agent, IReadOnlyList<LigneCalcul> Lignes)
{
    public decimal MontantTotal => Lignes.Sum(l => l.Montant);
}
