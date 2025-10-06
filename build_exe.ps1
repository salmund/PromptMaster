# Script pour créer un exécutable autonome de PromptMaster
# Utilise PyInstaller pour empaqueter l'application

Write-Host "=" -NoNewline; Write-Host ("="*59)
Write-Host "📦 Création de l'exécutable PromptMaster"
Write-Host "=" -NoNewline; Write-Host ("="*59)
Write-Host ""

# Vérifier si PyInstaller est installé
Write-Host "🔍 Vérification de PyInstaller..."
$pyinstaller = python -m pip show pyinstaller 2>$null
if (-not $pyinstaller) {
    Write-Host "⚠️  PyInstaller n'est pas installé. Installation en cours..."
    python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erreur lors de l'installation de PyInstaller"
        exit 1
    }
    Write-Host "✓ PyInstaller installé"
} else {
    Write-Host "✓ PyInstaller est déjà installé"
}

Write-Host ""
Write-Host "🏗️  Compilation de l'exécutable..."
Write-Host "   (Ceci peut prendre quelques minutes)"
Write-Host ""

# Créer l'exécutable
pyinstaller --clean `
    --onefile `
    --windowed `
    --name "PromptMaster" `
    --add-data "promptmaster.db;." `
    --hidden-import "PySide6.QtCore" `
    --hidden-import "PySide6.QtGui" `
    --hidden-import "PySide6.QtWidgets" `
    --hidden-import "pynput.keyboard" `
    --hidden-import "pynput.mouse" `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" -NoNewline; Write-Host ("="*59)
    Write-Host "✅ Exécutable créé avec succès !"
    Write-Host "=" -NoNewline; Write-Host ("="*59)
    Write-Host ""
    Write-Host "📁 Emplacement : .\dist\PromptMaster.exe"
    Write-Host ""
    Write-Host "🚀 Pour lancer l'application :"
    Write-Host "   .\dist\PromptMaster.exe"
    Write-Host ""
    Write-Host "💡 Astuce : Ajoutez un raccourci dans votre dossier de démarrage"
    Write-Host "   Win + R → shell:startup"
    Write-Host ""
    Write-Host "=" -NoNewline; Write-Host ("="*59)
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors de la création de l'exécutable"
    Write-Host "   Vérifiez les messages d'erreur ci-dessus"
    exit 1
}
