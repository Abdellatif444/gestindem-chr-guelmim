using Gestindem.Domain.Erreurs;

namespace Gestindem.Domain.Agents;

/// <summary>
/// Fonctionnaire bénéficiaire des indemnités (M3). Le grade est obligatoire (il fixe les taux
/// de garde/astreinte/permanence) ; le groupe peut manquer à l'import, mais un déplacement
/// ne pourra alors pas être calculé (<see cref="CodesErreur.AgentSansGroupe"/>).
/// Entité : son identité est son MATRICULE — deux instances de même matricule sont le même agent,
/// quelle que soit la façon dont elles ont été chargées.
/// </summary>
public sealed class Agent : IEquatable<Agent>
{
    public string Matricule { get; }
    public string Nom { get; }
    public Grade Grade { get; }
    public Groupe? Groupe { get; }

    public Agent(string matricule, string nom, Grade grade, Groupe? groupe)
    {
        if (string.IsNullOrWhiteSpace(matricule))
        {
            throw new ArgumentException("Le matricule est obligatoire.", nameof(matricule));
        }

        if (string.IsNullOrWhiteSpace(nom))
        {
            throw new ArgumentException("Le nom est obligatoire.", nameof(nom));
        }

        Matricule = matricule;
        Nom = nom;
        Grade = grade;
        Groupe = groupe;
    }

    /// <summary>Le groupe de l'agent, ou l'erreur métier qui explique pourquoi on ne peut pas calculer.</summary>
    public Groupe GroupeRequis() =>
        Groupe ?? throw new ErreurMetier(
            CodesErreur.AgentSansGroupe,
            $"L'agent {Matricule} ({Nom}) n'a pas de groupe : impossible de calculer une indemnité de déplacement.");

    public bool Equals(Agent? other) => other is not null && Matricule == other.Matricule;

    public override bool Equals(object? obj) => Equals(obj as Agent);

    public override int GetHashCode() => Matricule.GetHashCode();
}
