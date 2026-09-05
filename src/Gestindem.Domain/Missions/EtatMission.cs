namespace Gestindem.Domain.Missions;

/// <summary>Cycle de vie d'un ordre de mission (M7). Seule une mission clôturée entre dans un calcul.</summary>
public enum EtatMission
{
    EnCours,
    ACloturer,
    Cloturee,
    Annulee,
}
