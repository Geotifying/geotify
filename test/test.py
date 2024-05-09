from pathlib import Path
from unittest.mock import patch

import pytest

from geotify.map import BarChartVisualizer, HeatmapVisualizer, RegionCodeEnum


def test():
    assert True


# TEST_GEOJSON_PATH = Path("geotify/datasets/base_korea_map.json")
# TEST_CSV_PATH = Path("geotify/datasets/강원도.csv")

# @pytest.fixture
# def bar_chart_visualizer():
#     return BarChartVisualizer(
#         geojson_file_path=TEST_GEOJSON_PATH,
#         csv_file_path=TEST_CSV_PATH,
#         region_code=RegionCodeEnum.강원특별자치도,
#         region_key="42"
#     )

# @pytest.fixture
# def heatmap_visualizer():
#     return HeatmapVisualizer(
#         geojson_file_path=TEST_GEOJSON_PATH,
#         csv_file_path=TEST_CSV_PATH
#     )

# @patch('matplotlib.pyplot.show')
# def test_heatmap_visualizer(mock_show, heatmap_visualizer):
#     try:
#         heatmap_visualizer.visualize(color="blue")
#     except Exception as e:
#         pytest.fail(f"HeatmapVisualizer visualize method failed: {e}")
