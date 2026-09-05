using Gestindem.Domain.Baremes;

namespace Gestindem.Application.Calcul;

/// <summary>
/// Port (au sens Clean Architecture) : « quel barème s'applique à cette date ? ».
/// Les moteurs de calcul ne dépendent que de cette interface — la base de données
/// (Infrastructure) et la mémoire (tests, démo) en sont deux implémentations interchangeables.
/// C'est la règle M6 « barème en vigueur à la date concernée » rendue injectable.
/// </summary>
public interface IBaremeEnVigueur
{
    /// <exception cref="Domain.Erreurs.ErreurMetier">
    /// <c>BAREME_ABSENT_A_DATE</c> si aucune version ne couvre la date ;
    /// <c>BAREME_CHEVAUCHEMENT</c> si plusieurs versions la couvrent (données incohérentes).
    /// </exception>
    BaremeVersion PourDate(DateOnly date);
}
