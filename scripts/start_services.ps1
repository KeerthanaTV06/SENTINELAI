# Start Docker Compose services for SENTINEL-AI (Windows PowerShell)

param(
    [switch]$Detach
)

$cmd = "docker-compose up --build"
if ($Detach) { $cmd = "$cmd -d" }
Write-Output "Running: $cmd"
Invoke-Expression $cmd
