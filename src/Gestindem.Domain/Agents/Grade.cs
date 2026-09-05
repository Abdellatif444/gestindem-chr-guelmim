namespace Gestindem.Domain.Agents;

/// <summary>
/// Grade d'un agent (médecin spécialiste, infirmier…). Détermine les taux de garde, d'astreinte
/// et de permanence (M4). Objet-valeur : deux grades de même code sont le même grade.
/// </summary>
public sealed record Grade(string Code, string Libelle)
{
    public bool Equals(Grade? other) => other is not null && Code == other.Code;

    public override int GetHashCode() => Code.GetHashCode();
}
