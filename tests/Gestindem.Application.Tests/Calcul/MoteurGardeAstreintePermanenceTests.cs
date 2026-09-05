using AwesomeAssertions;
using Gestindem.Application.Calcul;
using Gestindem.Application.Tests.Fixtures;
using Gestindem.Domain.Agents;
using Gestindem.Domain.Baremes;
using Gestindem.Domain.Erreurs;
using Gestindem.Domain.Plannings;

namespace Gestindem.Application.Tests.Calcul;

/// <summary>
/// Cas golden G-01 à G-04 (ADR-004) : moteur de calcul des indemnités de garde, d'astreinte
/// et de permanence. Règle M6 du cahier des charges : « application du barème en vigueur
/// à la date concernée » — chaque planning est valorisé au taux de la version en vigueur
/// À SA DATE, jamais au barème courant.
///
/// Pourquoi les montants sont en <c>decimal</c> : un <c>double</c> représente 0,1 + 0,2 comme
/// 0,30000000000000004 ; <c>decimal</c> est exact en base 10 — obligatoire pour de l'argent.
/// </summary>
public class MoteurGardeAstreintePermanenceTests
{
    // Le moteur reçoit ses barèmes par injection (interface IBaremeEnVigueur) :
    // les tests lui donnent une source en mémoire, l'API lui donnera la base de données.
    private static MoteurGardeAstreintePermanence Moteur() =>
        new(new BaremeEnVigueurEnMemoire([BaremesDeDemo.V2, BaremesDeDemo.V3]));

    private static Planning Garde(Agent agent, int jour, int mois = 8) =>
        new(agent, new DateOnly(2026, mois, jour), TypeIndemnite.Garde);

    private static Planning Astreinte(Agent agent, int jour, int mois = 8) =>
        new(agent, new DateOnly(2026, mois, jour), TypeIndemnite.Astreinte);

    [Fact(DisplayName = "G-01 · 6 gardes de spécialiste en août (barème v3) = 3 600 DH")]
    public void G01_Six_gardes_specialiste_v3()
    {
        var benali = AgentsDeDemo.Benali;
        var plannings = new[] { 1, 9, 12, 22, 29, 30 }.Select(j => Garde(benali, j)).ToList();

        var resultat = Moteur().CalculerAgent(benali, plannings);

        resultat.MontantTotal.Should().Be(3_600m);
        resultat.Lignes.Should().ContainSingle()
            .Which.Should().BeEquivalentTo(new
            {
                Type = TypeIndemnite.Garde,
                Quantite = 6,
                TauxApplique = 600m,
                BaremeVersion = 3,
                Montant = 3_600m,
            });
    }

    [Fact(DisplayName = "G-02 · 6 gardes + 2 astreintes de spécialiste = 4 400 DH (une ligne par type)")]
    public void G02_Gardes_et_astreintes_donnent_deux_lignes()
    {
        var benali = AgentsDeDemo.Benali;
        var plannings = new[] { 1, 9, 12, 22, 29, 30 }.Select(j => Garde(benali, j))
            .Concat([Astreinte(benali, 8), Astreinte(benali, 15)])
            .ToList();

        var resultat = Moteur().CalculerAgent(benali, plannings);

        resultat.MontantTotal.Should().Be(4_400m);
        resultat.Lignes.Should().HaveCount(2);
        resultat.Lignes.Single(l => l.Type == TypeIndemnite.Garde).Montant.Should().Be(3_600m);
        resultat.Lignes.Single(l => l.Type == TypeIndemnite.Astreinte).Montant.Should().Be(800m);
    }

    [Fact(DisplayName = "G-03 · Mois à cheval sur deux versions : 2 gardes au 28/06 (v2 : 550) + 4 au 05/07 (v3 : 600) = 3 500 DH, deux instantanés")]
    public void G03_Bareme_en_vigueur_a_la_date_de_chaque_planning()
    {
        var benali = AgentsDeDemo.Benali;
        var plannings = new List<Planning>
        {
            Garde(benali, 27, mois: 6), Garde(benali, 28, mois: 6),                           // v2 : 550 DH
            Garde(benali, 5, mois: 7), Garde(benali, 12, mois: 7), Garde(benali, 19, mois: 7), Garde(benali, 26, mois: 7), // v3 : 600 DH
        };

        var resultat = Moteur().CalculerAgent(benali, plannings);

        resultat.MontantTotal.Should().Be(1_100m + 2_400m);
        resultat.Lignes.Should().HaveCount(2, "une ligne par (type, version de barème) : l'instantané est conservé (ADR-003)");
        resultat.Lignes.Single(l => l.BaremeVersion == 2).Should().BeEquivalentTo(new { Quantite = 2, TauxApplique = 550m, Montant = 1_100m });
        resultat.Lignes.Single(l => l.BaremeVersion == 3).Should().BeEquivalentTo(new { Quantite = 4, TauxApplique = 600m, Montant = 2_400m });
    }

    [Fact(DisplayName = "Revue n°1 · Des plannings portant une autre INSTANCE du même matricule sont acceptés ; un autre matricule est refusé")]
    public void Plannings_compares_par_matricule_pas_par_reference()
    {
        var benali = AgentsDeDemo.Benali;
        var memeAgentAutreInstance = AgentsDeDemo.Benali;   // nouvelle instance à chaque accès
        var saidi = AgentsDeDemo.Saidi;

        var accepte = () => Moteur().CalculerAgent(benali, [Garde(memeAgentAutreInstance, 1)]);
        var refuse = () => Moteur().CalculerAgent(benali, [Garde(saidi, 1)]);

        accepte.Should().NotThrow();
        refuse.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.PlanningAgentIncoherent);
    }

    [Fact(DisplayName = "G-04 · Aucun barème en vigueur à la date → erreur BAREME_ABSENT_A_DATE")]
    public void G04_Aucun_bareme_a_la_date()
    {
        var benali = AgentsDeDemo.Benali;
        var planningAvantToutBareme = new Planning(benali, new DateOnly(2020, 1, 1), TypeIndemnite.Garde);

        var calcul = () => Moteur().CalculerAgent(benali, [planningAvantToutBareme]);

        calcul.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.BaremeAbsentADate);
    }
}
