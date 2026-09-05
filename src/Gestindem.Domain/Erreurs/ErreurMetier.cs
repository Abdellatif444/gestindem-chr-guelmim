namespace Gestindem.Domain.Erreurs;

/// <summary>
/// Violation d'une règle métier. Porte un <see cref="Code"/> stable (voir <see cref="CodesErreur"/>)
/// que l'API renverra tel quel, et un message en français destiné aux journaux et au développeur —
/// jamais affiché tel quel à l'utilisateur (le client traduit le code).
/// </summary>
public sealed class ErreurMetier : Exception
{
    public string Code { get; }

    public ErreurMetier(string code, string message) : base(message)
    {
        Code = code;
    }
}
