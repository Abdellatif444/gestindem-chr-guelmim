namespace Gestindem.Domain.Baremes;

/// <summary>
/// Tranche de distance et son coefficient (M8). Les bornes sont INCLUSES : la tranche
/// 50–150 km couvre 50 et 150. <c>DistanceMaxKm</c> nul = « et au-delà ».
/// </summary>
public sealed class CoefficientDistance
{
    public int DistanceMinKm { get; }
    public int? DistanceMaxKm { get; }
    public decimal Coefficient { get; }

    public CoefficientDistance(int distanceMinKm, int? distanceMaxKm, decimal coefficient)
    {
        if (distanceMinKm < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(distanceMinKm), "La borne minimale ne peut pas être négative.");
        }

        if (distanceMaxKm is < 0 || distanceMaxKm < distanceMinKm)
        {
            throw new ArgumentOutOfRangeException(nameof(distanceMaxKm), "La borne maximale doit être supérieure ou égale à la borne minimale.");
        }

        if (coefficient <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(coefficient), "Le coefficient doit être positif.");
        }

        DistanceMinKm = distanceMinKm;
        DistanceMaxKm = distanceMaxKm;
        Coefficient = coefficient;
    }

    public bool Couvre(int distanceKm) =>
        distanceKm >= DistanceMinKm && (DistanceMaxKm is null || distanceKm <= DistanceMaxKm);
}
