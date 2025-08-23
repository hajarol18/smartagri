{
    'name': 'Smart Agri Decision',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Hajar',
    'category': 'Agriculture',
    'description': 'Module d\'aide à la décision agricole basé sur les paiements géographiques',
    'data': [
        # 1. D'abord la sécurité de base
        'security/ir.model.access.csv',
        # 2. Ensuite les vues des modèles (dans l'ordre des dépendances)
        'views/exploitation_views.xml',
        'views/culture_views.xml',
        'views/parcelle_views.xml',
        'views/intervention_views.xml',
        'views/intrants_views.xml',
        'views/meteo_views.xml',
        'views/rcp_views.xml',
        'views/ia_views.xml',
        'views/dashboard_views.xml',
        'views/actions.xml',
        # 3. Assets pour la carte Leaflet
        'static/src/assets.xml',
        # 4. Enfin les menus (après que toutes les actions soient définies)
        'views/main_menu.xml',
        # 5. Données de démonstration en dernier
        'data/demo_data.xml',
        'data/demo_parcelles.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'smart_agri_decision/static/src/css/leaflet_map.css',
            'smart_agri_decision/static/src/js/leaflet_map.js',
            'smart_agri_decision/static/src/xml/leaflet_map.xml',
        ],
    },
    'installable': True,
    'application': True,
}
