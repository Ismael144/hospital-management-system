# Define the path to your Django project
$projectPath = "C:\Users\swale\Desktop\hms"

# Get all migration folders within the project
$migrationFolders = Get-ChildItem -Path $projectPath -Recurse -Directory | Where-Object { $_.Name -eq "migrations" }

# Iterate over each migration folder
foreach ($folder in $migrationFolders) {
    # Get all Python files in the migration folder except __init__.py
    $migrationFiles = Get-ChildItem -Path $folder.FullName -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" }
    # Delete each migration file
    foreach ($file in $migrationFiles) {
        Remove-Item -Path $file.FullName -Force
        Write-Output "Deleted: $($file.FullName)"
    }
}

Write-Output "All migrations cleared!"
