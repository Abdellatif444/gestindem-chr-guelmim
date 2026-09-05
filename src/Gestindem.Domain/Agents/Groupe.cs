namespace Gestindem.Domain.Agents;

/// <summary>
/// Groupe (catégorie) d'un agent : A, B, C… Détermine l'indemnité journalière et le plafond
/// de déplacement (M3, M8). Objet-valeur identifié par son code.
/// </summary>
public sealed record Groupe(string Code);
