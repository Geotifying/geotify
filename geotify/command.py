from pathlib import Path

from geotify.map import BarChartVisualizer, RegionCodeEnum


def main() -> None:
    ASSETS_PATH = Path(__file__).with_name("datasets")
    map_data_path = ASSETS_PATH.joinpath("skorea_municipalities_geo_simple.json")
    population_density_data = ASSETS_PATH.joinpath("강원도.csv")
    density_visualizer = BarChartVisualizer(
        map_data_path, population_density_data, RegionCodeEnum.강원특별자치도, "동별(2)"
    )

    # 인구밀도 시각화
    region_names = ["평창군"]
    value_column = "인구밀도 (명/㎢)"

    density_visualizer.visualize(region_names, value_column)

    # geotify_map = HeatmapVisualizer(map_data_path, population_density_data)
    # geotify_map.visualize(color="lightblue")
