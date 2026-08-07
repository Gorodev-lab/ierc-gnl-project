'use client'

import React, { useEffect, useRef, useState } from 'react'
import { useMap } from 'react-leaflet'

interface HeatmapProps {
  latLngs: [number, number, number][]
  options?: {
    radius?: number
    blur?: number
    maxZoom?: number
    gradient?: Record<number, string>
    minOpacity?: number
    max?: number
  }
}

// Variable a nivel de módulo para evitar re-definir la clase en cada render
let HeatLayerClass: any = null

export default function Heatmap({ latLngs, options }: HeatmapProps) {
  const map = useMap()
  const heatLayerRef = useRef<any>(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const initHeat = async () => {
      if (typeof window === 'undefined') return
      // Leaflet se carga asíncronamente en RiskMap, esperar a que esté disponible
      let L = (window as any).L
      while (!L) {
        await new Promise(r => setTimeout(r, 100))
        L = (window as any).L
      }
      if (!HeatLayerClass) {
        try {
          // simpleheat logic
          const simpleheat = function(canvas: HTMLCanvasElement): any {
            // @ts-ignore
            if (!(this instanceof simpleheat)) return new simpleheat(canvas);
            // @ts-ignore
            this._canvas = canvas = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;
            // @ts-ignore
            this._ctx = canvas.getContext('2d');
            // @ts-ignore
            this._width = canvas.width;
            // @ts-ignore
            this._height = canvas.height;
            // @ts-ignore
            this._max = 1;
            // @ts-ignore
            this.clear();
          };
          simpleheat.prototype = {
            defaultRadius: 25,
            defaultGradient: { 0.4: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1.0: 'red' },
            data: function (data: any) { this._data = data; return this; },
            max: function (max: any) { this._max = max; return this; },
            add: function (point: any) { this._data.push(point); return this; },
            clear: function () { this._data = []; return this; },
            radius: function (r: number, blur: number) {
              blur = blur || 15;
              var circle = this._circle = document.createElement('canvas'),
                  ctx = circle.getContext('2d')!,
                  r2 = this._r = r + blur;
              circle.width = circle.height = r2 * 2;
              ctx.shadowOffsetX = ctx.shadowOffsetY = 200;
              ctx.shadowBlur = blur;
              ctx.shadowColor = 'black';
              ctx.beginPath();
              ctx.arc(r2 - 200, r2 - 200, r, 0, Math.PI * 2, true);
              ctx.closePath();
              ctx.fill();
              return this;
            },
            gradient: function (grad: any) {
              var canvas = document.createElement('canvas'),
                  ctx = canvas.getContext('2d')!,
                  gradient = ctx.createLinearGradient(0, 0, 0, 256);
              canvas.width = 1;
              canvas.height = 256;
              for (var i in grad) { gradient.addColorStop(+i, grad[i]); }
              ctx.fillStyle = gradient;
              ctx.fillRect(0, 0, 1, 256);
              this._grad = ctx.getImageData(0, 0, 1, 256).data;
              return this;
            },
            draw: function (minOpacity: number) {
              if (!this._circle) this.radius(this.defaultRadius);
              if (!this._grad) this.gradient(this.defaultGradient);
              var ctx = this._ctx;
              ctx.clearRect(0, 0, this._width, this._height);
              for (var i = 0, len = this._data.length, p; i < len; i++) {
                  p = this._data[i];
                  ctx.globalAlpha = Math.max(p[2] / this._max, minOpacity || 0.05);
                  ctx.drawImage(this._circle, p[0] - this._r, p[1] - this._r);
              }
              var imgData = ctx.getImageData(0, 0, this._width, this._height);
              this._colorize(imgData.data, this._grad);
              ctx.putImageData(imgData, 0, 0);
              return this;
            },
            _colorize: function (pixels: any, gradient: any) {
              for (var i = 3, len = pixels.length, j; i < len; i += 4) {
                  j = pixels[i] * 4;
                  if (j) {
                      pixels[i - 3] = gradient[j];
                      pixels[i - 2] = gradient[j + 1];
                      pixels[i - 1] = gradient[j + 2];
                  }
              }
            }
          };

          // Definir la clase localmente extendiendo la clase base de Leaflet L.Layer o L.Class
          const BaseLayer = L.Layer ? L.Layer : L.Class;
          HeatLayerClass = BaseLayer.extend({
            initialize: function (latlngs: any, options: any) {
              this._latlngs = latlngs;
              L.setOptions(this, options);
            },
            setLatLngs: function (latlngs: any) {
              this._latlngs = latlngs;
              return this.redraw();
            },
            addLatLng: function (latlng: any) {
              this._latlngs.push(latlng);
              return this.redraw();
            },
            setOptions: function (options: any) {
              L.setOptions(this, options);
              if (this._heat) { this._updateOptions(); }
              return this.redraw();
            },
            redraw: function () {
              if (this._heat && !this._frame && !this._map._animating) {
                this._frame = L.Util.requestAnimFrame(this._redraw, this);
              }
              return this;
            },
            onAdd: function (map: any) {
              this._map = map;
              if (!this._canvas) { this._initCanvas(); }
              map.getPanes().overlayPane.appendChild(this._canvas);
              map.on('moveend', this._reset, this);
              if (map.options.zoomAnimation && L.Browser.any3d) {
                map.on('zoomanim', this._animateZoom, this);
              }
              this._reset();
            },
            onRemove: function (map: any) {
              map.getPanes().overlayPane.removeChild(this._canvas);
              map.off('moveend', this._reset, this);
              if (map.options.zoomAnimation) {
                map.off('zoomanim', this._animateZoom, this);
              }
            },
            addTo: function (map: any) {
              map.addLayer(this);
              return this;
            },
            _initCanvas: function () {
              var canvas = this._canvas = L.DomUtil.create('canvas', 'leaflet-heatmap-layer leaflet-layer');
              var originProp = L.DomUtil.testProp(['transformOrigin', 'WebkitTransformOrigin', 'msTransformOrigin']);
              canvas.style[originProp] = '50% 50%';
              var size = this._map.getSize();
              canvas.width = size.x;
              canvas.height = size.y;
              var animated = this._map.options.zoomAnimation && L.Browser.any3d;
              L.DomUtil.addClass(canvas, 'leaflet-zoom-' + (animated ? 'animated' : 'hide'));
              // @ts-ignore
              this._heat = simpleheat(canvas);
              this._updateOptions();
            },
            _updateOptions: function () {
              this._heat.radius(this.options.radius || this._heat.defaultRadius, this.options.blur);
              if (this.options.gradient) { this._heat.gradient(this.options.gradient); }
              if (this.options.max) { this._heat.max(this.options.max); }
            },
            _reset: function () {
              var topLeft = this._map.containerPointToLayerPoint([0, 0]);
              L.DomUtil.setPosition(this._canvas, topLeft);
              var size = this._map.getSize();
              if (this._heat._width !== size.x) {
                this._canvas.width = this._heat._width = size.x;
              }
              if (this._heat._height !== size.y) {
                this._canvas.height = this._heat._height = size.y;
              }
              this._redraw();
            },
            _redraw: function () {
              if (!this._map) return;
              var r = this._heat._r,
                  size = this._map.getSize(),
                  bounds = new L.Bounds(L.point([-r, -r]), size.add([r, r])),
                  max = this.options.max === undefined ? 1 : this.options.max,
                  maxZoom = this.options.maxZoom === undefined ? this._map.getMaxZoom() : this.options.maxZoom,
                  v = this._map._getMapPanePos(),
                  w = v.x % (r / 2),
                  y = v.y % (r / 2),
                  grid = [] as any,
                  data = [] as any,
                  i, len, latlng, point, altVal, scale;

              scale = 1 / Math.pow(2, Math.max(0, Math.min(maxZoom - this._map.getZoom(), 12)));

              for (i = 0, len = this._latlngs.length; i < len; i++) {
                  latlng = this._latlngs[i];
                  point = this._map.latLngToContainerPoint(latlng);
                  if (bounds.contains(point)) {
                      var x = Math.floor((point.x - w) / (r / 2)) + 2,
                          yCoord = Math.floor((point.y - y) / (r / 2)) + 2;
                      altVal = latlng[2] !== undefined ? +latlng[2] : 1;

                      var val = altVal * scale;
                      grid[yCoord] = grid[yCoord] || [];
                      var cell = grid[yCoord][x];
                      if (!cell) {
                          grid[yCoord][x] = [point.x, point.y, val];
                      } else {
                          cell[0] = (cell[0] * cell[2] + point.x * val) / (cell[2] + val);
                          cell[1] = (cell[1] * cell[2] + point.y * val) / (cell[2] + val);
                          cell[2] += val;
                      }
                  }
              }

              for (i = 0, len = grid.length; i < len; i++) {
                  if (grid[i]) {
                      for (var j = 0, len2 = grid[i].length; j < len2; j++) {
                          var cellVal = grid[i][j];
                          if (cellVal) {
                              data.push([
                                  Math.round(cellVal[0]),
                                  Math.round(cellVal[1]),
                                  Math.min(cellVal[2], max)
                              ]);
                          }
                      }
                  }
              }
              this._heat.data(data).draw(this.options.minOpacity);
              this._frame = null;
            },
            _animateZoom: function (e: any) {
              var scale = this._map.getZoomScale(e.zoom),
                  offset = this._map._getCenterOffset(e.center)._multiplyBy(-scale).subtract(this._map._getMapPanePos());
              if (L.DomUtil.setTransform) {
                L.DomUtil.setTransform(this._canvas, offset, scale);
              } else {
                this._canvas.style[L.DomUtil.TRANSFORM] = L.DomUtil.getTranslateString(offset) + ' scale(' + scale + ')';
              }
            }
          });
        } catch (e) {
          console.error('Failed to create HeatLayerClass:', e)
        }
      }

      if (HeatLayerClass) {
        setReady(true)
      }
    }
    initHeat()
  }, [])

  useEffect(() => {
    if (!ready || !latLngs?.length || !HeatLayerClass) return
    const L = (window as any).L
    if (!L) return

    try {
      // Instanciar la clase local directamente
      const layer = new HeatLayerClass(latLngs, {
        radius: options?.radius ?? 25,
        blur: options?.blur ?? 15,
        maxZoom: options?.maxZoom ?? 7,
        gradient: options?.gradient ?? { 0.2: '#4F46E5', 0.4: '#6366F1', 0.6: '#818CF8', 0.8: '#A5B4FC', 1: '#FFFFFF' },
        minOpacity: options?.minOpacity ?? 0.15,
        max: options?.max ?? 100,
        ...options,
      })

      heatLayerRef.current = layer
      layer.addTo(map)
    } catch (err) {
      console.error('Error creating heatLayer:', err)
    }

    return () => {
      if (heatLayerRef.current) {
        try {
          map.removeLayer(heatLayerRef.current)
        } catch (e) {
          // ignore removal errors during unmount
        }
      }
    }
  }, [ready, latLngs, options, map])

  // Update latLngs when they change
  useEffect(() => {
    if (heatLayerRef.current && latLngs) {
      try {
        heatLayerRef.current.setLatLngs(latLngs)
      } catch (e) {}
    }
  }, [latLngs])

  return null
}