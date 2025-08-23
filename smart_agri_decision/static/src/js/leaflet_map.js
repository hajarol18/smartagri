odoo.define('smart_agri_decision.leaflet_map', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    var LeafletMapWidget = AbstractField.extend({
        template: 'LeafletMapWidget',
        supportedTypes: ['char', 'text'],
        
        init: function () {
            this._super.apply(this, arguments);
            this.map = null;
            this.drawingLayer = null;
            this.drawnItems = new L.FeatureGroup();
            this.currentPolygon = null;
            this.isDrawing = false;
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._initMap();
                self._initDrawingTools();
                self._loadExistingParcelles();
            });
        },

        _initMap: function () {
            var self = this;
            
            // Initialiser la carte Leaflet
            this.map = L.map(this.el.querySelector('.leaflet-map'), {
                center: [46.2276, 2.2137], // Centre de la France
                zoom: 6,
                zoomControl: true,
                attributionControl: true
            });

            // Ajouter la couche de tuiles OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(this.map);

            // Ajouter la couche de dessin
            this.map.addLayer(this.drawnItems);

            // Événements de la carte
            this.map.on('click', function (e) {
                if (self.isDrawing) {
                    self._addPointToPolygon(e.latlng);
                }
            });
        },

        _initDrawingTools: function () {
            var self = this;
            
            // Boutons de contrôle
            var drawControl = L.control({position: 'topright'});
            
            drawControl.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'leaflet-draw-control');
                div.innerHTML = `
                    <div class="leaflet-draw-buttons">
                        <button class="btn btn-primary btn-sm" id="start-drawing" title="Commencer le dessin">
                            <i class="fa fa-pencil"></i> Dessiner
                        </button>
                        <button class="btn btn-success btn-sm" id="finish-drawing" title="Terminer le dessin" style="display:none;">
                            <i class="fa fa-check"></i> Terminer
                        </button>
                        <button class="btn btn-warning btn-sm" id="clear-drawing" title="Effacer le dessin">
                            <i class="fa fa-trash"></i> Effacer
                        </button>
                        <button class="btn btn-info btn-sm" id="measure-area" title="Mesurer l'aire">
                            <i class="fa fa-calculator"></i> Mesurer
                        </button>
                    </div>
                `;
                
                // Événements des boutons
                div.querySelector('#start-drawing').addEventListener('click', function() {
                    self._startDrawing();
                });
                
                div.querySelector('#finish-drawing').addEventListener('click', function() {
                    self._finishDrawing();
                });
                
                div.querySelector('#clear-drawing').addEventListener('click', function() {
                    self._clearDrawing();
                });
                
                div.querySelector('#measure-area').addEventListener('click', function() {
                    self._measureArea();
                });
                
                return div;
            };
            
            drawControl.addTo(this.map);
        },

        _startDrawing: function () {
            this.isDrawing = true;
            this.currentPolygon = [];
            this.drawingLayer = L.layerGroup().addTo(this.map);
            
            // Changer l'apparence du curseur
            this.map.getContainer().style.cursor = 'crosshair';
            
            // Afficher/masquer les boutons
            this.el.querySelector('#start-drawing').style.display = 'none';
            this.el.querySelector('#finish-drawing').style.display = 'inline-block';
            
            // Message d'aide
            this._showMessage('Cliquez sur la carte pour ajouter des points à votre parcelle. Cliquez sur "Terminer" quand vous avez fini.', 'info');
        },

        _addPointToPolygon: function (latlng) {
            if (!this.isDrawing) return;
            
            this.currentPolygon.push(latlng);
            
            // Ajouter un marqueur pour le point
            var marker = L.marker(latlng, {
                icon: L.divIcon({
                    className: 'polygon-point',
                    html: '<div style="background-color: #ff4444; width: 10px; height: 10px; border-radius: 50%; border: 2px solid white;"></div>',
                    iconSize: [10, 10]
                })
            }).addTo(this.drawingLayer);
            
            // Ajouter une ligne entre les points
            if (this.currentPolygon.length > 1) {
                var line = L.polyline([this.currentPolygon[this.currentPolygon.length - 2], latlng], {
                    color: '#ff4444',
                    weight: 3,
                    opacity: 0.8
                }).addTo(this.drawingLayer);
            }
            
            // Afficher les coordonnées
            this._showMessage(`Point ajouté: ${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`, 'success');
        },

        _finishDrawing: function () {
            if (!this.isDrawing || this.currentPolygon.length < 3) {
                this._showMessage('Une parcelle doit avoir au moins 3 points.', 'warning');
                return;
            }
            
            this.isDrawing = false;
            this.map.getContainer().style.cursor = '';
            
            // Créer le polygone final
            var polygon = L.polygon(this.currentPolygon, {
                color: '#3388ff',
                weight: 2,
                opacity: 0.8,
                fillColor: '#3388ff',
                fillOpacity: 0.2
            }).addTo(this.drawnItems);
            
            // Ajouter un popup avec les informations
            var area = this._calculateArea(this.currentPolygon);
            var coordinates = this.currentPolygon.map(function(point) {
                return `${point.lat.toFixed(6)}, ${point.lng.toFixed(6)}`;
            }).join(';');
            
            polygon.bindPopup(`
                <div class="parcelle-info">
                    <h4>Nouvelle Parcelle</h4>
                    <p><strong>Surface:</strong> ${area.toFixed(2)} hectares</p>
                    <p><strong>Points:</strong> ${this.currentPolygon.length}</p>
                    <p><strong>Coordonnées:</strong></p>
                    <textarea readonly style="width: 100%; height: 60px;">${coordinates}</textarea>
                    <br><br>
                    <button class="btn btn-success btn-sm" onclick="this._saveParcelle('${coordinates}', ${area})">
                        <i class="fa fa-save"></i> Sauvegarder
                    </button>
                </div>
            `);
            
            // Nettoyer la couche de dessin
            this.drawingLayer.clearLayers();
            this.currentPolygon = null;
            
            // Afficher/masquer les boutons
            this.el.querySelector('#start-drawing').style.display = 'inline-block';
            this.el.querySelector('#finish-drawing').style.display = 'none';
            
            this._showMessage('Parcelle créée avec succès !', 'success');
        },

        _clearDrawing: function () {
            this.isDrawing = false;
            this.currentPolygon = null;
            this.map.getContainer().style.cursor = '';
            
            if (this.drawingLayer) {
                this.drawingLayer.clearLayers();
            }
            
            // Afficher/masquer les boutons
            this.el.querySelector('#start-drawing').style.display = 'inline-block';
            this.el.querySelector('#finish-drawing').style.display = 'none';
            
            this._showMessage('Dessin effacé.', 'info');
        },

        _measureArea: function () {
            if (this.currentPolygon && this.currentPolygon.length >= 3) {
                var area = this._calculateArea(this.currentPolygon);
                this._showMessage(`Surface de la parcelle en cours: ${area.toFixed(2)} hectares`, 'info');
            } else {
                this._showMessage('Dessinez d\'abord une parcelle pour mesurer sa surface.', 'warning');
            }
        },

        _calculateArea: function (points) {
            // Calcul de l'aire d'un polygone (formule de Gauss)
            var area = 0;
            for (var i = 0; i < points.length; i++) {
                var j = (i + 1) % points.length;
                area += points[i].lng * points[j].lat;
                area -= points[j].lng * points[i].lat;
            }
            area = Math.abs(area) / 2;
            
            // Convertir en hectares (approximatif)
            return area * 111.32 * 111.32 * Math.cos(points[0].lat * Math.PI / 180) / 10000;
        },

        _loadExistingParcelles: function () {
            var self = this;
            
            // Charger les parcelles existantes depuis le modèle
            this.trigger_up('field_changed', {
                dataPointID: this.dataPointID,
                changes: {parcelles_geometrie: 'load'}
            });
        },

        _saveParcelle: function (coordinates, area) {
            // Sauvegarder la parcelle dans Odoo
            var self = this;
            
            this.trigger_up('field_changed', {
                dataPointID: this.dataPointID,
                changes: {
                    parcelles_geometrie: coordinates,
                    surface_calculee: area
                }
            });
            
            this._showMessage('Parcelle sauvegardée dans Odoo !', 'success');
        },

        _showMessage: function (message, type) {
            // Créer un message temporaire
            var messageDiv = document.createElement('div');
            messageDiv.className = `alert alert-${type} alert-dismissible fade show`;
            messageDiv.style.position = 'absolute';
            messageDiv.style.top = '10px';
            messageDiv.style.left = '50%';
            messageDiv.style.transform = 'translateX(-50%)';
            messageDiv.style.zIndex = '1000';
            messageDiv.style.minWidth = '300px';
            
            messageDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            this.el.appendChild(messageDiv);
            
            // Supprimer le message après 5 secondes
            setTimeout(function() {
                if (messageDiv.parentNode) {
                    messageDiv.parentNode.removeChild(messageDiv);
                }
            }, 5000);
        },

        destroy: function () {
            if (this.map) {
                this.map.remove();
            }
            this._super.apply(this, arguments);
        }
    });

    fieldRegistry.add('leaflet_map', LeafletMapWidget);
    return LeafletMapWidget;
});
