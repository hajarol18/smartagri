{
    "name": "Smart Agri Decision",
    "version": "1.0",
    "depends": ["base", "stock", "product", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/exploitation_views.xml",
        "views/intrants_views.xml",
        "views/intervention_views.xml",
        "views/scenario_views.xml",
        "views/scenario_climatique_views.xml",
        "views/meteo_views.xml",
        "views/actions.xml",
        "views/main_menu.xml",
        "data/demo_data.xml"
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
