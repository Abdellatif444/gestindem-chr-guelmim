using Gestindem.Domain.Agents;
using Gestindem.Domain.Erreurs;

namespace Gestindem.Domain.Baremes;

/// <summary>
/// Version complète et datée d'un barème (ADR-003, décision D-3.1) : elle contient TOUTES ses
/// lignes (taux par grade et type, grilles par groupe, coefficients de distance) et une plage
/// de validité <c>[DateEffet, DateFin]</c>. Une version archivée est immuable : une revalorisation
/// crée une nouvelle version.
/// </summary>
public sealed class BaremeVersion
{
    public int Numero { get; }
    public DateOnly DateEffet { get; }
    public DateOnly? DateFin { get; }
    public IReadOnlyList<TauxIndemnite> Taux { get; }
    public IReadOnlyList<GrilleDeplacement> Grilles { get; }
    public IReadOnlyList<CoefficientDistance> Coefficients { get; }

    public BaremeVersion(
        int numero,
        DateOnly dateEffet,
        DateOnly? dateFin,
        IReadOnlyList<TauxIndemnite> taux,
        IReadOnlyList<GrilleDeplacement> grilles,
        IReadOnlyList<CoefficientDistance> coefficients)
    {
        if (numero <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(numero), "Le numéro de version doit être positif.");
        }

        if (dateFin is not null && dateFin < dateEffet)
        {
            throw new ArgumentException("La date de fin ne peut pas précéder la date d'effet.", nameof(dateFin));
        }

        // Un barème incohérent doit être impossible à construire (revue de code, correction n°2) :
        // un seul taux par (grade, type), une seule grille par groupe, des tranches de distance disjointes.
        var tauxEnDouble = taux.GroupBy(t => (t.Grade, t.Type)).FirstOrDefault(g => g.Count() > 1);
        if (tauxEnDouble is not null)
        {
            throw new ArgumentException(
                $"Taux en double pour {tauxEnDouble.Key.Grade.Libelle} / {tauxEnDouble.Key.Type}.", nameof(taux));
        }

        var grilleEnDouble = grilles.GroupBy(g => g.Groupe).FirstOrDefault(g => g.Count() > 1);
        if (grilleEnDouble is not null)
        {
            throw new ArgumentException($"Grille en double pour le groupe {grilleEnDouble.Key.Code}.", nameof(grilles));
        }

        var chevauchement = coefficients
            .SelectMany((a, i) => coefficients.Skip(i + 1).Select(b => (a, b)))
            .FirstOrDefault(p => p.a.Couvre(p.b.DistanceMinKm) || p.b.Couvre(p.a.DistanceMinKm));
        if (chevauchement != default)
        {
            throw new ArgumentException(
                $"Tranches de distance en chevauchement : {chevauchement.a.DistanceMinKm}–{chevauchement.a.DistanceMaxKm?.ToString() ?? "∞"} et {chevauchement.b.DistanceMinKm}–{chevauchement.b.DistanceMaxKm?.ToString() ?? "∞"}.",
                nameof(coefficients));
        }

        Numero = numero;
        DateEffet = dateEffet;
        DateFin = dateFin;
        Taux = taux;
        Grilles = grilles;
        Coefficients = coefficients;
    }

    /// <summary>Vrai si la date tombe dans la plage de validité (bornes incluses).</summary>
    public bool EstEnVigueurLe(DateOnly date) =>
        date >= DateEffet && (DateFin is null || date <= DateFin);

    public decimal TauxPour(Grade grade, TypeIndemnite type)
    {
        var ligne = Taux.FirstOrDefault(t => t.Grade == grade && t.Type == type)
            ?? throw new ErreurMetier(
                CodesErreur.TauxAbsent,
                $"La version {Numero} du barème n'a pas de taux {type} pour le grade {grade.Libelle}.");

        return ligne.Montant;
    }

    public GrilleDeplacement GrillePour(Groupe groupe) =>
        Grilles.FirstOrDefault(g => g.Groupe == groupe)
        ?? throw new ErreurMetier(
            CodesErreur.GrilleAbsente,
            $"La version {Numero} du barème n'a pas de grille de déplacement pour le groupe {groupe.Code}.");

    public decimal CoefficientPour(int distanceKm)
    {
        var tranche = Coefficients.FirstOrDefault(c => c.Couvre(distanceKm))
            ?? throw new ErreurMetier(
                CodesErreur.CoefficientAbsent,
                $"La version {Numero} du barème n'a pas de coefficient pour {distanceKm} km.");

        return tranche.Coefficient;
    }
}
