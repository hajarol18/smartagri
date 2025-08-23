#!/bin/bash

# 🌾 Script d'installation Smart Agri Decision
# Ce script installe et configure le module Smart Agri Decision sur Odoo 18

set -e  # Arrêter en cas d'erreur

echo "🌾 Installation de Smart Agri Decision..."
echo "========================================"

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"

# Vérifier que le module est présent
if [ ! -d "smart_agri_decision" ]; then
    echo "❌ Le dossier smart_agri_decision n'est pas trouvé"
    echo "   Assurez-vous d'être dans le bon répertoire"
    exit 1
fi

echo "✅ Module Smart Agri Decision trouvé"

# Arrêter les conteneurs existants s'ils tournent
echo "🔄 Arrêt des conteneurs existants..."
docker-compose down 2>/dev/null || true

# Démarrer les services
echo "🚀 Démarrage des services..."
docker-compose up -d

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente que PostgreSQL soit prêt..."
sleep 10

# Vérifier que Odoo est démarré
echo "🔍 Vérification du démarrage d'Odoo..."
for i in {1..30}; do
    if curl -s http://localhost:10018 > /dev/null; then
        echo "✅ Odoo est démarré et accessible"
        break
    fi
    echo "⏳ Attente du démarrage d'Odoo... ($i/30)"
    sleep 10
done

if ! curl -s http://localhost:10018 > /dev/null; then
    echo "❌ Odoo n'a pas pu démarrer correctement"
    echo "   Vérifiez les logs avec: docker-compose logs odoo18"
    exit 1
fi

# Mettre à jour le module
echo "🔄 Mise à jour du module Smart Agri Decision..."
docker-compose exec odoo18 odoo -d smartagri -u smart_agri_decision --stop-after-init

echo ""
echo "🎉 Installation terminée avec succès !"
echo "====================================="
echo ""
echo "🌐 Accès à Odoo : http://localhost:10018"
echo "🗄️  Accès à PgAdmin : http://localhost:5050"
echo "   - Email : admin@smartagri.com"
echo "   - Mot de passe : admin"
echo ""
echo "📚 Documentation : https://github.com/hajarol18/smartagri#readme"
echo ""
echo "🔧 Commandes utiles :"
echo "   - Voir les logs : docker-compose logs -f odoo18"
echo "   - Redémarrer : docker-compose restart odoo18"
echo "   - Arrêter : docker-compose down"
echo ""
echo "🌾 Votre module Smart Agri Decision est maintenant opérationnel !"
