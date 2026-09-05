namespace Gestindem.Domain.Erreurs;

/// <summary>
/// Codes d'erreur métier STABLES (ADR-002 : l'API renvoie des codes, jamais des libellés d'écran ;
/// le client choisit l'affichage). Un code ne change jamais de sens une fois publié.
/// </summary>
public static class CodesErreur
{
    // Barèmes
    public const string BaremeAbsentADate = "BAREME_ABSENT_A_DATE";
    public const string BaremeChevauchement = "BAREME_CHEVAUCHEMENT";
    public const string TauxAbsent = "TAUX_ABSENT";
    public const string GrilleAbsente = "GRILLE_ABSENTE";
    public const string CoefficientAbsent = "COEFFICIENT_ABSENT";

    // Agents et plannings
    public const string AgentSansGroupe = "AGENT_SANS_GROUPE";
    public const string PlanningTypeInvalide = "PLANNING_TYPE_INVALIDE";
    public const string PlanningAgentIncoherent = "PLANNING_AGENT_INCOHERENT";
    public const string PlanningDoublon = "PLANNING_DOUBLON";
    public const string PeriodeCloturee = "PERIODE_CLOTUREE";

    // Missions
    public const string MissionDatesInvalides = "MISSION_DATES_INVALIDES";
    public const string MissionDistanceInvalide = "MISSION_DISTANCE_INVALIDE";
    public const string MissionNonCloturee = "MISSION_NON_CLOTUREE";

    // Workflow de validation
    public const string LotDejaValide = "LOT_DEJA_VALIDE";
    public const string LotMotifRequis = "LOT_MOTIF_REQUIS";
    public const string LotHorsPerimetre = "LOT_HORS_PERIMETRE";
    public const string AnnulationExpiree = "ANNULATION_EXPIREE";
    public const string CalculDejaEnCours = "CALCUL_DEJA_EN_COURS";
    public const string DroitInsuffisant = "DROIT_INSUFFISANT";
}
