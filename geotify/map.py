import os
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt


# 시각화 함수 설정
class GeotifyMapVisualizer:
    def __init__(self):
        self.geojson_file = self.load_geojson_file_path()
        self.geo_data = self.load_geojson()

    def load_geojson_file_path(self):
        # GEOTIFY_GEOJSON_FILE 환경 변수가 설정되어 있는지 확인. -> 사용자 입력 받을 수 있게
        DEFAULT_JSON_PATH = (
            Path(__file__).parent.parent
            / "asset"
            / "skorea_municipalities_geo_simple.json"
        )
        geojson_file_path = os.getenv("GEOTIFY_GEOJSON_FILE", DEFAULT_JSON_PATH)
        return geojson_file_path

    def load_geojson(self):
        if not self.geojson_file.exists():
            raise FileExistsError
        if not self.geojson_file.is_file():
            raise FileNotFoundError
        try:
            geo_data = gpd.read_file(self.geojson_file, encoding="utf-8")
            return geo_data
        except ValueError as e:
            raise ValueError(f"Error loading GeoJSON file: {e}")

    # 전체 지도 시각화 시, 기본 지도 배경 설정 값 흰색으로 지정
    def visualize_map(self, region_name=None, color="white"):
        if region_name:
            region = self.geo_data[self.geo_data["name_eng"] == region_name]
        else:
            region = self.geo_data

        if region.empty:
            print(f"Region with name '{region_name}' not found.")
            raise

        _, ax = plt.subplots(figsize=(10, 10))
        region.plot(ax=ax, facecolor=color, edgecolor="black")
        plt.title(f"GeoMap Visualization - Region Name: {region_name}")
        plt.show()


# 예시 사용법
if __name__ == "__main__":
    map_visualizer = GeotifyMapVisualizer()

    # 시각화를 원하는 지역 이름과 색상을 입력하여 visualize_map 함수 호출
    map_visualizer.visualize_map(region_name="Gwangyang-si", color="blue")
    map_visualizer.visualize_map() #이건 아무것도 입력 해 주지 않았을 경우