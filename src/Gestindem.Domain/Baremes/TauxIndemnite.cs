using Gestindem.Domain.Agents;

namespace Gestindem.Domain.Baremes;

/// <summary>Taux d'une indemnité de garde, d'astreinte ou de permanence pour un grade (M4), en dirhams.</summary>
public sealed record TauxIndemnite(Grade Grade, TypeIndemnite Type, decimal Montant);
