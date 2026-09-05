using AwesomeAssertions;
using Gestindem.Domain.Agents;
using Gestindem.Domain.Baremes;
using Gestindem.Domain.Erreurs;
using Gestindem.Domain.Plannings;

namespace Gestindem.Domain.Tests.Agents;

public class AgentTests
{
    private static readonly Grade Specialiste = new("MED_SPE", "Médecin spécialiste");

    [Fact(DisplayName = "Deux instances de même matricule sont le même agent (identité d'entité — revue n°1)")]
    public void Identite_par_matricule()
    {
        var chargeDepuisLaListe = new Agent("M-04512", "Dr Y. Benali", Specialiste, new Groupe("A"));
        var chargeDepuisLePlanning = new Agent("M-04512", "Dr Y. Benali", Specialiste, new Groupe("A"));

        chargeDepuisLaListe.Should().Be(chargeDepuisLePlanning);
        chargeDepuisLaListe.GetHashCode().Should().Be(chargeDepuisLePlanning.GetHashCode());
    }

    [Fact(DisplayName = "Matricule vide → refusé")]
    public void Matricule_vide_refuse()
    {
        var construction = () => new Agent(" ", "Dr Y. Benali", Specialiste, null);

        construction.Should().Throw<ArgumentException>().WithParameterName("matricule");
    }

    [Fact(DisplayName = "Un planning de type Déplacement est impossible → PLANNING_TYPE_INVALIDE")]
    public void Planning_de_type_deplacement_refuse()
    {
        var agent = new Agent("M-04512", "Dr Y. Benali", Specialiste, null);

        var construction = () => new Planning(agent, new DateOnly(2026, 8, 1), TypeIndemnite.Deplacement);

        construction.Should().Throw<ErreurMetier>().Which.Code.Should().Be(CodesErreur.PlanningTypeInvalide);
    }
}
