# 🌾 Script d'installation Smart Agri Decision pour Windows
# Ce script installe et configure le module Smart Agri Decision sur Odoo 18

param(
    [switch]$Force
)

Write-Host "🌾 Installation de Smart Agri Decision..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Vérifier que Docker est installé
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker est installé : $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker n'est pas installé. Veuillez l'installer d'abord." -ForegroundColor Red
    Write-Host "   Téléchargez Docker Desktop depuis : https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Vérifier que Docker Compose est installé
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose est installé : $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord." -ForegroundColor Red
    exit 1
}

# Vérifier que le module est présent
if (-not (Test-Path "smart_agri_decision")) {
    Write-Host "❌ Le dossier smart_agri_decision n'est pas trouvé" -ForegroundColor Red
    Write-Host "   Assurez-vous d'être dans le bon répertoire" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Module Smart Agri Decision trouvé" -ForegroundColor Green

# Arrêter les conteneurs existants s'ils tournent
Write-Host "🔄 Arrêt des conteneurs existants..." -ForegroundColor Yellow
try {
    docker-compose down 2>$null
} catch {
    # Ignorer les erreurs si aucun conteneur n'est en cours
}

# Démarrer les services
Write-Host "🚀 Démarrage des services..." -ForegroundColor Yellow
docker-compose up -d

# Attendre que PostgreSQL soit prêt
Write-Host "⏳ Attente que PostgreSQL soit prêt..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Vérifier que Odoo est démarré
Write-Host "🔍 Vérification du démarrage d'Odoo..." -ForegroundColor Yellow
$odooReady = $false
for ($i = 1; $i -le 30; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:10018" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Odoo est démarré et accessible" -ForegroundColor Green
            $odooReady = $true
            break
        }
    } catch {
        # Ignorer les erreurs de connexion
    }
    
    Write-Host "⏳ Attente du démarrage d'Odoo... ($i/30)" -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

if (-not $odooReady) {
    Write-Host "❌ Odoo n'a pas pu démarrer correctement" -ForegroundColor Red
    Write-Host "   Vérifiez les logs avec: docker-compose logs odoo18" -ForegroundColor Yellow
    exit 1
}

# Mettre à jour le module
Write-Host "🔄 Mise à jour du module Smart Agri Decision..." -ForegroundColor Yellow
docker-compose exec odoo18 odoo -d smartagri -u smart_agri_decision --stop-after-init

Write-Host ""
Write-Host "🎉 Installation terminée avec succès !" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Accès à Odoo : http://localhost:10018" -ForegroundColor Cyan
Write-Host "🗄️  Accès à PgAdmin : http://localhost:5050" -ForegroundColor Cyan
Write-Host "   - Email : admin@smartagri.com" -ForegroundColor White
Write-Host "   - Mot de passe : admin" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation : https://github.com/hajarol18/smartagri#readme" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Commandes utiles :" -ForegroundColor Yellow
Write-Host "   - Voir les logs : docker-compose logs -f odoo18" -ForegroundColor White
Write-Host "   - Redémarrer : docker-compose restart odoo18" -ForegroundColor White
Write-Host "   - Arrêter : docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "🌾 Votre module Smart Agri Decision est maintenant opérationnel !" -ForegroundColor Green

# Ouvrir le navigateur automatiquement
if (-not $Force) {
    $openBrowser = Read-Host "Voulez-vous ouvrir Odoo dans votre navigateur ? (O/N)"
    if ($openBrowser -eq "O" -or $openBrowser -eq "o") {
        Start-Process "http://localhost:10018"
    }
}
