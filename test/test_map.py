import unittest
from unittest.mock import patch

from geotify.map import HeatmapVisualizer


class TestHeatmapVisualizer(unittest.TestCase):
    @patch("geotify.map.os.getenv", return_value=None)
    def test_load_geojson_file_path_default_path(self, mock_getenv):
        map_visualizer = HeatmapVisualizer()
        expected_path = (
            "/Users/songle/Geotify/asset/skorea_municipalities_geo_simple.json"
        )
        self.assertEqual(map_visualizer.geojson_file, expected_path)

    @patch("geotify.map.os.getenv", return_value="/custom/path/to/geojson.json")
    def test_load_geojson_file_path_custom_path(self, mock_getenv):
        map_visualizer = HeatmapVisualizer()
        expected_path = "/custom/path/to/geojson.json"
        self.assertEqual(map_visualizer.geojson_file, expected_path)

    @patch("geotify.map.gpd.read_file")
    def test_load_geojson_valid_file(self, mock_read_file):
        map_visualizer = HeatmapVisualizer()
        map_visualizer.load_geojson_file_path = lambda: "/path/to/valid.geojson"
        mock_read_file.return_value = "dummy_geo_data"
        map_visualizer.load_geojson()
        self.assertEqual(map_visualizer.geo_data, "dummy_geo_data")

    @patch(
        "geotify.map.gpd.read_file",
        side_effect=ValueError("Error loading GeoJSON file"),
    )
    def test_load_geojson_invalid_file(self, mock_read_file):
        map_visualizer = HeatmapVisualizer()
        map_visualizer.load_geojson_file_path = lambda: "/path/to/invalid.geojson"
        with self.assertRaises(ValueError):
            map_visualizer.load_geojson()

    @patch("geotify.map.plt.show")
    def test_visualize_map_with_region_name(self, mock_show):
        map_visualizer = HeatmapVisualizer()
        map_visualizer.geo_data = "dummy_geo_data"
        map_visualizer.visualize_map(region_name="TestRegion", color="blue")
        mock_show.assert_called_once()

    @patch("geotify.map.plt.show")
    def test_visualize_map_without_region_name(self, mock_show):
        map_visualizer = HeatmapVisualizer()
        map_visualizer.geo_data = "dummy_geo_data"
        map_visualizer.visualize_map()
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
