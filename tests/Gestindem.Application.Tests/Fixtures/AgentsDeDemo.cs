using Gestindem.Domain.Agents;

namespace Gestindem.Application.Tests.Fixtures;

/// <summary>Agents des maquettes (Personnel, Missions). Données fictives de démonstration.</summary>
public static class AgentsDeDemo
{
    /// <summary>Dr Y. Benali — Médecin spécialiste, Groupe A, Urgences (M-04512).</summary>
    public static Agent Benali => new("M-04512", "Dr Y. Benali", BaremesDeDemo.MedecinSpecialiste, BaremesDeDemo.GroupeA);

    /// <summary>Dr K. Saidi — Médecin spécialiste, Groupe A, Réanimation (M-04527).</summary>
    public static Agent Saidi => new("M-04527", "Dr K. Saidi", BaremesDeDemo.MedecinSpecialiste, BaremesDeDemo.GroupeA);

    /// <summary>Inf. L. Mansouri — Infirmier anesthésiste, Groupe C (M-04640).</summary>
    public static Agent Mansouri => new("M-04640", "Inf. L. Mansouri", BaremesDeDemo.Infirmier, BaremesDeDemo.GroupeC);

    /// <summary>Tech. H. Drissi — Technicien radiologie, Groupe C (M-04702).</summary>
    public static Agent Drissi => new("M-04702", "Tech. H. Drissi", BaremesDeDemo.Technicien, BaremesDeDemo.GroupeC);

    /// <summary>Agent sans groupe : cas d'erreur G-05 (un groupe est obligatoire pour un déplacement).</summary>
    public static Agent SansGroupe => new("M-09999", "Agent Sans Groupe", BaremesDeDemo.Infirmier, groupe: null);
}
