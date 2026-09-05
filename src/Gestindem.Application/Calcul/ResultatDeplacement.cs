using Gestindem.Domain.Missions;

namespace Gestindem.Application.Calcul;

/// <summary>
/// Détail du calcul d'une indemnité de déplacement (M8) — c'est le « justificatif du calcul »
/// exigé par le cahier des charges, et l'instantané d'ADR-003 : tout ce qui a servi au montant
/// est conservé avec lui. <c>PlafondApplique</c> est renseigné seulement si le plafond a joué.
/// </summary>
public sealed record ResultatDeplacement(
    Mission Mission,
    int DureeJours,
    decimal IndemniteJournaliere,
    decimal Coefficient,
    decimal MontantBrut,
    decimal? PlafondApplique,
    decimal MontantFinal,
    int BaremeVersion);
