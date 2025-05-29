# vue_setup.ps1
param(
    [string]$projectDir = "../../../src/frontend",
    [bool]$useConfigFiles = $true,
    [bool]$useRouter = $false,
    [bool]$useVuex = $false,
    [string]$eslintConfig = "standard", # Choose "standard", "airbnb", or "prettier"
    [bool]$lintOnSave = $true
)

Write-Host "Initializing Vue.js project in $projectDir with custom options..."

# Ensure Node.js is installed
if (-not (Get-Command "node" -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js is not installed. Please install Node.js before running this script."
    exit 1
}

# Create the project directory if it doesn't exist
if (-not (Test-Path $projectDir)) {
    New-Item -ItemType Directory -Path $projectDir -Force
}

# Navigate to the project directory
Set-Location $projectDir

# Construct Vue preset options
$jsonPreset = @{
    useConfigFiles = $useConfigFiles
    plugins = @{
        "@vue/cli-plugin-babel" = @{}
        "@vue/cli-plugin-eslint" = @{
            config = $eslintConfig
            lintOn = @("save")
        }
    }
}

if ($useRouter) {
    $jsonPreset.plugins."@vue/cli-plugin-router" = @{}
}

if ($useVuex) {
    $jsonPreset.plugins."@vue/cli-plugin-vuex" = @{}
}

# Convert PowerShell object to JSON string and escape double quotes
$preset = ($jsonPreset | ConvertTo-Json -Depth 10 -Compress).Replace('"', '\"')

# Initialize Vue.js project with inline preset
Write-Host "Running Vue CLI with inline preset..."
vue create . --inlinePreset "$preset" --no-git --bare --skipGetStarted

Write-Host "Vue.js project initialized successfully!"


