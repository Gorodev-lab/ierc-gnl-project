"""
Unit Tests — Spatial Validator Engine
=====================================
Pruebas para validación espacial, no-deformación geométrica y vacíos (Moreno-Báez 2012).
"""

import pytest
from shapely.geometry import Point, Polygon
from src.engine.spatial_validator import SpatialValidator, SpatialValidationConfig


class TestSpatialValidationConfig:
    """Pruebas para configuración de validación espacial."""

    def test_config_defaults(self):
        """Verifica valores por defecto de SpatialValidationConfig."""
        config = SpatialValidationConfig()
        assert config.gulf_bbox['min_lat'] == 22.5
        assert config.gulf_bbox['max_lat'] == 32.0
        assert config.gulf_bbox['min_lon'] == -115.0
        assert config.gulf_bbox['max_lon'] == -108.0
        assert config.utm_zone == 12
        assert config.historical_data_years == 5

    def test_config_custom_bbox(self):
        """Permite bbox personalizado."""
        config = SpatialValidationConfig(gulf_bbox={
            'min_lat': 20.0, 'max_lat': 35.0,
            'min_lon': -120.0, 'max_lon': -105.0
        })
        assert config.gulf_bbox['min_lat'] == 20.0
        assert config.gulf_bbox['max_lat'] == 35.0


class TestUIDValidation:
    """Pruebas para validación de UID espacio-temporal."""

    def test_valid_uid(self):
        """UID válido con 7 componentes."""
        result = SpatialValidator.validate_uid_espaciotemporal(
            "PUNTA_CHUECA-ARTESANAL-JAIBAMAX-TRAMPA-ZONA1-OCT_MAR-RUTA1"
        )
        assert result['valid'] is True
        assert result['components']['comunidad'] == "PUNTA_CHUECA"
        assert result['components']['actor'] == "ARTESANAL"
        assert result['components']['pesqueria'] == "JAIBAMAX"
        assert result['components']['arte'] == "TRAMPA"
        assert result['components']['zona'] == "ZONA1"
        assert result['components']['temporada'] == "OCT_MAR"
        assert result['components']['ruta'] == "RUTA1"

    def test_valid_uid_extra_components(self):
        """UID válido con más de 7 componentes (ruta con guiones)."""
        result = SpatialValidator.validate_uid_espaciotemporal(
            "COM-ACT-PES-ART-ZON-TEM-RUTA1-RUTA2"
        )
        assert result['valid'] is True
        assert result['components']['ruta'] == "RUTA1-RUTA2"

    def test_invalid_uid_too_few_components(self):
        """UID inválido con menos de 7 componentes."""
        result = SpatialValidator.validate_uid_espaciotemporal("A-B-C-D-E-F")
        assert result['valid'] is False
        assert '7 componentes' in result['error'] or 'componentes' in result['error']


class TestBoundingBoxValidation:
    """Pruebas para validación de Bounding Box del Golfo de California."""

    @pytest.fixture
    def validator(self):
        """Instancia de SpatialValidator sin DB engine (métodos estáticos/no-DB)."""
        config = SpatialValidationConfig()
        # No necesitamos DB engine para estas pruebas
        validator = SpatialValidator.__new__(SpatialValidator)
        validator.config = config
        from pyproj import CRS, Transformer
        validator.epsg4326 = CRS.from_epsg(4326)
        validator.epsg32612 = CRS.from_epsg(32612)
        validator.transformer_wgs84_to_utm = Transformer.from_crs(
            validator.epsg4326, validator.epsg32612, always_xy=True
        )
        validator.transformer_utm_to_wgs84 = Transformer.from_crs(
            validator.epsg32612, validator.epsg4326, always_xy=True
        )
        return validator

    def test_point_inside_bbox(self, validator):
        """Puerto Libertad dentro del bbox."""
        point = Point(-112.6835, 29.9107)
        assert validator.validate_bounding_box(point) is True

    def test_point_outside_bbox_south(self, validator):
        """Punto al sur del Golfo (fuera)."""
        point = Point(-112.0, 20.0)
        assert validator.validate_bounding_box(point) is False

    def test_point_outside_bbox_north(self, validator):
        """Punto al norte del Golfo (fuera)."""
        point = Point(-112.0, 35.0)
        assert validator.validate_bounding_box(point) is False

    def test_point_outside_bbox_west(self, validator):
        """Punto al oeste del Golfo (fuera)."""
        point = Point(-120.0, 29.0)
        assert validator.validate_bounding_box(point) is False

    def test_point_outside_bbox_east(self, validator):
        """Punto al este del Golfo (fuera)."""
        point = Point(-100.0, 29.0)
        assert validator.validate_bounding_box(point) is False

    def test_polygon_inside_bbox(self, validator):
        """Polígono completamente dentro del bbox."""
        poly = Polygon([
            (-112.7, 29.9), (-112.6, 29.9),
            (-112.6, 30.0), (-112.7, 30.0)
        ])
        assert validator.validate_bounding_box(poly) is True

    def test_polygon_partially_outside_bbox(self, validator):
        """Polígono que sale del bbox."""
        poly = Polygon([
            (-116.0, 29.0), (-114.0, 29.0),
            (-114.0, 31.0), (-116.0, 31.0)
        ])
        assert validator.validate_bounding_box(poly) is False


class TestNoDeformationGeometry:
    """Pruebas para no-deformación geométrica (EPSG:4326 → UTM 12N → EPSG:4326)."""

    @pytest.fixture
    def validator(self):
        """Instancia configurada para reproyección."""
        config = SpatialValidationConfig()
        validator = SpatialValidator.__new__(SpatialValidator)
        validator.config = config
        from pyproj import CRS, Transformer
        validator.epsg4326 = CRS.from_epsg(4326)
        validator.epsg32612 = CRS.from_epsg(32612)
        validator.transformer_wgs84_to_utm = Transformer.from_crs(
            validator.epsg4326, validator.epsg32612, always_xy=True
        )
        validator.transformer_utm_to_wgs84 = Transformer.from_crs(
            validator.epsg32612, validator.epsg4326, always_xy=True
        )
        return validator

    def test_point_reproject_returns_wkt(self, validator):
        """Punto reproyectado retorna WKT válido."""
        point = Point(-112.6835, 29.9107)
        wkt = validator.reproject_geometry_no_deformation(point)
        assert wkt is not None
        assert wkt.startswith("POINT")
        assert "-112" in wkt  # Longitud aproximada
        assert "29" in wkt    # Latitud aproximada

    def test_polygon_reproject_returns_wkt(self, validator):
        """Polígono reproyectado retorna WKT válido."""
        poly = Polygon([
            (-112.7, 29.9), (-112.6, 29.9),
            (-112.6, 30.0), (-112.7, 30.0), (-112.7, 29.9)
        ])
        wkt = validator.reproject_geometry_no_deformation(poly)
        assert wkt is not None
        assert wkt.startswith("POLYGON")

    def test_point_reproject_preserves_location_approximately(self, validator):
        """Reproyección mantiene ubicación aproximada (no deformación significativa)."""
        point = Point(-112.6835, 29.9107)
        wkt = validator.reproject_geometry_no_deformation(point)
        # Extraer coordenadas del WKT
        import re
        match = re.search(r'POINT \(([-\d.]+) ([-\d.]+)\)', wkt)
        assert match
        lon, lat = float(match.group(1)), float(match.group(2))
        # Diferencia < 0.01 grados (~1km) - buffer de 500m en UTM
        assert abs(lon - (-112.6835)) < 0.01
        assert abs(lat - 29.9107) < 0.01


class TestClipToGulfBBox:
    """Pruebas para recorte al Bounding Box del Golfo."""

    @pytest.fixture
    def validator(self):
        config = SpatialValidationConfig()
        validator = SpatialValidator.__new__(SpatialValidator)
        validator.config = config
        from pyproj import CRS, Transformer
        validator.epsg4326 = CRS.from_epsg(4326)
        validator.epsg32612 = CRS.from_epsg(32612)
        validator.transformer_wgs84_to_utm = Transformer.from_crs(
            validator.epsg4326, validator.epsg32612, always_xy=True
        )
        validator.transformer_utm_to_wgs84 = Transformer.from_crs(
            validator.epsg32612, validator.epsg4326, always_xy=True
        )
        return validator

    def test_point_inside_clipped_unchanged(self, validator):
        """Punto dentro del bbox no cambia al recortar."""
        point = Point(-112.0, 29.0)
        result = validator._clip_to_gulf_bbox(point)
        assert result is not None
        assert result.x == point.x
        assert result.y == point.y

    def test_point_outside_clipped_returns_none(self, validator):
        """Punto fuera del bbox retorna None al recortar."""
        point = Point(-120.0, 20.0)
        result = validator._clip_to_gulf_bbox(point)
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])