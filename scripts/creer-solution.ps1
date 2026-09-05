# creer-solution.ps1 — crée la solution GESTINDEM selon ADR-002 (couches) et ADR-004 (tests).
# À exécuter UNE FOIS depuis la racine du dépôt :  .\scripts\creer-solution.ps1
# Chaque bloc est commenté : lisez-le avant de lancer. Le script s'arrête à la première erreur.

$ErrorActionPreference = "Stop"
$fw = "net10.0"                     # .NET 10 LTS (ADR-006)

# ---------- 1. Solution ----------
# Un fichier .sln regroupe les projets ; c'est ce que `dotnet build` / `dotnet test` ouvrent.
dotnet new sln -n Gestindem

# ---------- 2. Projets de production (src/) ----------
# classlib = bibliothèque sans point d'entrée ; webapi = API ASP.NET Core ; wpf = client Windows.
dotnet new classlib -n Gestindem.Domain         -o src/Gestindem.Domain         -f $fw
dotnet new classlib -n Gestindem.Application    -o src/Gestindem.Application    -f $fw
dotnet new classlib -n Gestindem.Contracts      -o src/Gestindem.Contracts      -f $fw
dotnet new classlib -n Gestindem.Infrastructure -o src/Gestindem.Infrastructure -f $fw
dotnet new webapi   -n Gestindem.Api            -o src/Gestindem.Api            -f $fw --use-controllers
dotnet new wpf      -n Gestindem.Desktop        -o src/Gestindem.Desktop        -f $fw

# Les templates créent un fichier d'exemple Class1.cs inutile : on le supprime pour partir propre.
Get-ChildItem -Path src -Recurse -Filter Class1.cs | Remove-Item

# ---------- 3. Projets de tests (tests/) ----------
# xunit = template de tests xUnit ; il inclut déjà coverlet.collector (mesure de couverture).
foreach ($p in "Domain", "Application", "Infrastructure", "Api", "Desktop") {
    dotnet new xunit -n "Gestindem.$p.Tests" -o "tests/Gestindem.$p.Tests" -f $fw
    Get-ChildItem -Path "tests/Gestindem.$p.Tests" -Filter UnitTest1.cs | Remove-Item
}

# ---------- 4. Ajout de tous les projets à la solution ----------
Get-ChildItem -Path src, tests -Recurse -Filter *.csproj | ForEach-Object { dotnet sln add $_.FullName }

# ---------- 5. Règle de dépendance (ADR-002) : les flèches pointent vers l'intérieur ----------
# Domain ne dépend de rien. Contracts ne dépend de rien.
dotnet add src/Gestindem.Application    reference src/Gestindem.Domain
dotnet add src/Gestindem.Infrastructure reference src/Gestindem.Application
dotnet add src/Gestindem.Api            reference src/Gestindem.Application src/Gestindem.Infrastructure src/Gestindem.Contracts
dotnet add src/Gestindem.Desktop        reference src/Gestindem.Contracts      # UNIQUEMENT Contracts : aucun métier dans le client

# Chaque projet de tests ne voit que la couche qu'il teste (+ ce qu'elle expose).
dotnet add tests/Gestindem.Domain.Tests         reference src/Gestindem.Domain
dotnet add tests/Gestindem.Application.Tests    reference src/Gestindem.Application
dotnet add tests/Gestindem.Infrastructure.Tests reference src/Gestindem.Infrastructure
dotnet add tests/Gestindem.Api.Tests            reference src/Gestindem.Api
dotnet add tests/Gestindem.Desktop.Tests        reference src/Gestindem.Desktop

# ---------- 6. Paquets de test communs (ADR-004) ----------
# FluentAssertions : messages d'échec lisibles ; NSubstitute : doubles de test (mocks).
foreach ($p in "Domain", "Application", "Infrastructure", "Api", "Desktop") {
    dotnet add "tests/Gestindem.$p.Tests" package FluentAssertions
    dotnet add "tests/Gestindem.$p.Tests" package NSubstitute
}
# Tests d'intégration API : héberge l'API en mémoire pour des appels HTTP réels.
dotnet add tests/Gestindem.Api.Tests package Microsoft.AspNetCore.Mvc.Testing

# ---------- 7. Vérification ----------
dotnet build
dotnet test
Write-Host "`nSolution créée. Vérifiez : dotnet sln list" -ForegroundColor Green
