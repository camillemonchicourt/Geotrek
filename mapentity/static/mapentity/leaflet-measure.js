L.Polyline.Measure = L.Draw.Polyline.extend({
    addHooks: function() {
        L.Draw.Polyline.prototype.addHooks.call(this);
        if (this._map) {
            this._markerGroup = new L.LayerGroup();
            this._map.addLayer(this._markerGroup);

            this._markers = [];
            this._map.on('click', this._onClick, this);
            this._startShape();
        }
    },

    removeHooks: function () {
        L.Draw.Polyline.prototype.removeHooks.call(this);

        this._clearHideErrorTimeout();

        //!\ Still useful when control is disabled before any drawing (refactor needed?)
        this._map.off('mousemove', this._onMouseMove);
        this._clearGuides();
        this._container.style.cursor = '';

        this._removeShape();

        this._map.removeLayer(this._markerGroup);
        delete this._markerGroup;
        delete this._markers;

        this._map.off('click', this._onClick);
    },

    _startShape: function() {
        this._drawing = true;
        this._poly = new L.Polyline([], this.options.shapeOptions);

        this._container.style.cursor = 'crosshair';

        this._updateTooltip();
        this._map.on('mousemove', this._onMouseMove, this);
    },

    _finishShape: function () {
        this._drawing = false;

        this._cleanUpShape();
        this._clearGuides();

        this._updateTooltip();

        this._map.off('mousemove', this._onMouseMove, this);
        this._container.style.cursor = '';
    },

    _removeShape: function() {
        if (!this._poly)
            return;
        this._map.removeLayer(this._poly);
        delete this._poly;
        this._markers.splice(0);
        this._markerGroup.clearLayers();
    },

    _onClick: function(e) {
        if (!this._drawing) {
            this._removeShape();
            this._startShape();
            return;
        }

        L.Draw.Polyline.prototype._onClick.call(this, e);
    },

    _getTooltipText: function() {
        var labelText = L.Draw.Polyline.prototype._getTooltipText.call(this);
        if (!this._drawing) {
            labelText.text = '';
        }
        return labelText;
    }
});

L.Control.Measurement = L.Control.extend({

    static: {
        TITLE: 'Measure distances'
    },
    options: {
        position: 'topleft',
        handler: {}
    },

    initialize: function(options) {
        L.Util.extend(this.options, options);
    },

    toggle: function() {
        if (this.handler.enabled()) {
            this.handler.disable.call(this.handler);
            L.DomUtil.removeClass(this._container, 'enabled');
        } else {
            this.handler.enable.call(this.handler);
            L.DomUtil.addClass(this._container, 'enabled');
        }
    },

    onAdd: function(map) {
        var className = 'leaflet-control-draw';

        this._container = L.DomUtil.create('div', 'leaflet-bar');

        this.handler = new L.Polyline.Measure(map, this.options.handler);

        var link = L.DomUtil.create('a', className+'-measure', this._container);
        link.href = '#';
        link.title = L.Control.Measurement.TITLE;

        L.DomEvent
            .addListener(link, 'click', L.DomEvent.stopPropagation)
            .addListener(link, 'click', L.DomEvent.preventDefault)
            .addListener(link, 'click', this.toggle, this);

        return this._container;
    }
});