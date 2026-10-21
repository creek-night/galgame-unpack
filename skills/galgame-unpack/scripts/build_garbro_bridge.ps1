param(
    [Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Garbro,
    [Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Output
)
$ErrorActionPreference = 'Stop'
function Get-TaskSha256([string]$Path) {
    $taskStream = [System.IO.File]::OpenRead($Path)
    $taskHasher = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([System.BitConverter]::ToString($taskHasher.ComputeHash($taskStream))).Replace('-', '').ToLowerInvariant()
    } finally {
        $taskHasher.Dispose()
        $taskStream.Dispose()
    }
}
$taskCompiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$taskWpf = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\WPF'
foreach ($taskRequired in @($taskCompiler, (Join-Path $Garbro 'GameRes.dll'), (Join-Path $Garbro 'ArcFormats.dll'), (Join-Path $Garbro 'GameData\Formats.dat'))) {
    if (-not (Test-Path -LiteralPath $taskRequired -PathType Leaf)) { throw "Missing prerequisite: $taskRequired" }
}
New-Item -ItemType Directory -Path $Output -Force | Out-Null
$taskExe = Join-Path $Output 'garbro_bridge.exe'
if (Test-Path -LiteralPath $taskExe) { throw "Output already exists: $taskExe; choose another build directory." }
& $taskCompiler /nologo /target:exe /platform:x64 /optimize+ "/out:$taskExe" "/r:$Garbro\GameRes.dll" "/r:$Garbro\ArcFormats.dll" /r:System.Core.dll /r:System.Xaml.dll /r:System.Web.Extensions.dll "/r:$taskWpf\PresentationCore.dll" "/r:$taskWpf\WindowsBase.dll" (Join-Path $PSScriptRoot 'garbro_bridge.cs')
if ($LASTEXITCODE -ne 0) { throw 'Bridge compilation failed' }
Get-TaskSha256 $taskExe

$taskRecord = @{
    schema_version = 1
    binary = 'garbro_bridge.exe'
    binary_sha256 = (Get-TaskSha256 $taskExe)
    source_sha256 = (Get-TaskSha256 (Join-Path $PSScriptRoot 'garbro_bridge.cs'))
    libraries = @{}
}
foreach ($taskName in @('GameRes.dll','ArcFormats.dll','GameData\Formats.dat')) {
    $taskPath = Join-Path $Garbro $taskName
    $taskRecord.libraries[$taskName] = @{
        path = $taskPath
        sha256 = (Get-TaskSha256 $taskPath)
    }
}
$taskRecord | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Output 'tool.json') -Encoding UTF8
