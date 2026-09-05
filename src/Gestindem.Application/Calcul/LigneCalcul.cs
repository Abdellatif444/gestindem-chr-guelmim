using Gestindem.Domain.Baremes;

namespace Gestindem.Application.Calcul;

/// <summary>
/// Une ligne du calcul garde/astreinte/permanence d'un agent : un type, une version de barème,
/// une quantité, le taux appliqué et le montant. C'est l'INSTANTANÉ d'ADR-003 (D-3.3) : le taux
/// et la version sont conservés avec le montant, pour qu'il reste explicable après toute
/// revalorisation.
/// </summary>
public sealed record LigneCalcul(
    TypeIndemnite Type,
    int Quantite,
    decimal TauxApplique,
    int BaremeVersion,
    decimal Montant);
