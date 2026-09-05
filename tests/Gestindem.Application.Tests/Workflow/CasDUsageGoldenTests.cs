namespace Gestindem.Application.Tests.Workflow;

/// <summary>
/// Cas golden W-01 à W-06 (ADR-004) : règles du workflow (périodes, doublons, recalcul,
/// idempotence, rejet, annulation). Ils dépendent des cas d'usage et de leurs ports
/// (dépôts, horloge) qui seront introduits à l'étape suivante. Ils sont déclarés dès
/// maintenant, marqués « ignorés » avec leur attendu, pour que la liste des 17 golden
/// reste visible dans chaque rapport de tests — un test ignoré se voit, un test absent non.
/// </summary>
public class CasDUsageGoldenTests
{
    private const string EtapeSuivante = "Étape suivante : cas d'usage et ports (ADR-003).";

    [Fact(DisplayName = "W-01 · Saisie sur une période clôturée → PERIODE_CLOTUREE", Skip = EtapeSuivante)]
    public void W01_Periode_cloturee() { }

    [Fact(DisplayName = "W-02 · Même agent, même date, même type → PLANNING_DOUBLON", Skip = EtapeSuivante)]
    public void W02_Doublon() { }

    [Fact(DisplayName = "W-03 · Recalcul : nouveau Calcul, ancien Obsolete, lignes anciennes intactes", Skip = EtapeSuivante)]
    public void W03_Recalcul_immuable() { }

    [Fact(DisplayName = "W-04 · Deux validations avec la même Idempotency-Key → une seule EtapeValidation", Skip = EtapeSuivante)]
    public void W04_Idempotence() { }

    [Fact(DisplayName = "W-05 · Rejet sans motif → LOT_MOTIF_REQUIS", Skip = EtapeSuivante)]
    public void W05_Rejet_sans_motif() { }

    [Fact(DisplayName = "W-06 · Annulation à 5 min 01 s → ANNULATION_EXPIREE", Skip = EtapeSuivante)]
    public void W06_Annulation_expiree() { }
}
