using Gestindem.Domain.Agents;
using Gestindem.Domain.Erreurs;

namespace Gestindem.Domain.Missions;

/// <summary>
/// Ordre de mission (M7). Les invariants sont vérifiés à la construction : une mission
/// dont le retour précède le départ ne peut pas exister (cas golden D-06).
/// </summary>
public sealed class Mission
{
    public Agent Agent { get; }
    public DateOnly DateDepart { get; }
    public DateOnly DateRetour { get; }
    public int DistanceKm { get; }
    public EtatMission Etat { get; }

    /// <summary>Durée en jours, bornes incluses : départ et retour le même jour = 1 jour.</summary>
    public int DureeJours => DateRetour.DayNumber - DateDepart.DayNumber + 1;

    public Mission(Agent agent, DateOnly dateDepart, DateOnly dateRetour, int distanceKm, EtatMission etat)
    {
        if (dateRetour < dateDepart)
        {
            throw new ErreurMetier(
                CodesErreur.MissionDatesInvalides,
                $"La date de retour ({dateRetour:dd/MM/yyyy}) précède la date de départ ({dateDepart:dd/MM/yyyy}).");
        }

        if (distanceKm <= 0)
        {
            throw new ErreurMetier(
                CodesErreur.MissionDistanceInvalide,
                $"La distance doit être strictement positive ({distanceKm} km).");
        }

        Agent = agent;
        DateDepart = dateDepart;
        DateRetour = dateRetour;
        DistanceKm = distanceKm;
        Etat = etat;
    }
}
