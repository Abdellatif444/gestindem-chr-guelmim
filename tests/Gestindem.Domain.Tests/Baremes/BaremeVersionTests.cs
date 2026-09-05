using AwesomeAssertions;
using Gestindem.Domain.Agents;
using Gestindem.Domain.Baremes;
using Gestindem.Domain.Erreurs;

namespace Gestindem.Domain.Tests.Baremes;

/// <summary>Invariants d'une version de barème : ce qui ne peut pas être construit (revue de code, correction n°2).</summary>
public class BaremeVersionTests
{
    private static readonly Grade Specialiste = new("MED_SPE", "Médecin spécialiste");
    private static readonly Groupe A = new("A");

    private static BaremeVersion Version(
        IReadOnlyList<TauxIndemnite>? taux = null,
        IReadOnlyList<GrilleDeplacement>? grilles = null,
        IReadOnlyList<CoefficientDistance>? coefficients = null,
        DateOnly? dateFin = null) =>
        new(1, new DateOnly(2026, 1, 1), dateFin,
            taux ?? [new TauxIndemnite(Specialiste, TypeIndemnite.Garde, 600m)],
            grilles ?? [new GrilleDeplacement(A, 400m, 2_000m)],
            coefficients ?? [new CoefficientDistance(0, 150, 1.2m), new CoefficientDistance(151, null, 1.5m)]);

    [Fact(DisplayName = "Deux taux pour le même (grade, type) → construction refusée")]
    public void Taux_en_double_refuse()
    {
        var construction = () => Version(taux:
        [
            new TauxIndemnite(Specialiste, TypeIndemnite.Garde, 600m),
            new TauxIndemnite(Specialiste, TypeIndemnite.Garde, 650m),
        ]);

        construction.Should().Throw<ArgumentException>().WithParameterName("taux");
    }

    [Fact(DisplayName = "Deux grilles pour le même groupe → construction refusée")]
    public void Grille_en_double_refusee()
    {
        var construction = () => Version(grilles:
        [
            new GrilleDeplacement(A, 400m, 2_000m),
            new GrilleDeplacement(A, 420m, 2_100m),
        ]);

        construction.Should().Throw<ArgumentException>().WithParameterName("grilles");
    }

    [Fact(DisplayName = "Tranches de distance qui se chevauchent (0–150 et 100–∞) → construction refusée")]
    public void Tranches_en_chevauchement_refusees()
    {
        var construction = () => Version(coefficients:
        [
            new CoefficientDistance(0, 150, 1.2m),
            new CoefficientDistance(100, null, 1.5m),
        ]);

        construction.Should().Throw<ArgumentException>().WithParameterName("coefficients");
    }

    [Fact(DisplayName = "Date de fin avant la date d'effet → construction refusée")]
    public void Date_de_fin_avant_effet_refusee()
    {
        var construction = () => Version(dateFin: new DateOnly(2025, 12, 31));

        construction.Should().Throw<ArgumentException>().WithParameterName("dateFin");
    }

    [Fact(DisplayName = "Taux absent pour un grade → TAUX_ABSENT ; distance hors tranches → COEFFICIENT_ABSENT")]
    public void Lectures_absentes_donnent_des_erreurs_metier()
    {
        var version = Version(coefficients: [new CoefficientDistance(0, 100, 1.0m)]);
        var infirmier = new Grade("INF", "Infirmier");

        var taux = () => version.TauxPour(infirmier, TypeIndemnite.Garde);
        var coefficient = () => version.CoefficientPour(101);

        taux.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.TauxAbsent);
        coefficient.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.CoefficientAbsent);
    }

    [Theory(DisplayName = "En vigueur le : bornes incluses")]
    [InlineData(2025, 12, 31, false)]
    [InlineData(2026, 1, 1, true)]
    [InlineData(2026, 6, 30, true)]
    [InlineData(2026, 7, 1, false)]
    public void Est_en_vigueur_bornes_incluses(int annee, int mois, int jour, bool attendu)
    {
        var version = Version(dateFin: new DateOnly(2026, 6, 30));

        version.EstEnVigueurLe(new DateOnly(annee, mois, jour)).Should().Be(attendu);
    }
}
