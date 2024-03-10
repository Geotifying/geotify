import os
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

class GeotifyMapVisualizer:
    def __init__(self):
        self.geojson_file = self.load_geojson_file_path()
        self.geo_data = self.load_geojson()

    def load_geojson_file_path(self):
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

    def visualize_map(self, region_names=None, color="white"):
        if region_names:
            regions = self.geo_data[self.geo_data["name"].isin(region_names)]
        else:
            regions = self.geo_data

        if regions.empty:
            print(f"Regions with names {region_names} not found.")
            raise

        _, ax = plt.subplots(figsize=(10, 10))
        regions.plot(ax=ax, facecolor=color, edgecolor="black")
        plt.title(f"GeotifyMap Visualization : Region Names: {region_names}")
        plt.show()


class HeatmapVisualizer:
    def __init__(self, geojson_file_path, csv_file_path):
        self.geo_data = self.load_geojson(geojson_file_path)
        self.population_data = self.load_data(csv_file_path)

    def load_geojson(self, geojson_file_path):
        try:
            geo_data = gpd.read_file(geojson_file_path, encoding="utf-8")
            return geo_data
        except ValueError as e:
            raise ValueError(f"Error loading GeoJSON file: {e}")

    def load_data(self, csv_file_path):
        try:
            csv_data = pd.read_csv(csv_file_path)
            return csv_data
        except FileNotFoundError:
            print(f"CSV file not found at path: {csv_file_path}")
            raise

    def visualize_heatmap(self, region_names, value_column):
        # region_names에 해당하는 행만 추출
        selected_data = self.population_data[self.population_data["동별(2)"].isin(region_names)]

        # "동별(2)" 대신 "소계" 등의 값 대신에 지역 이름으로 변경
        selected_data = selected_data.replace({"소계": "합계"})

        # 지도 위에 히트맵 추가
        fig, ax = plt.subplots(figsize=(10, 10))
        self.geo_data.plot(ax=ax, facecolor="white", edgecolor="black")
        selected_data.plot(column=value_column, cmap="YlGnBu", linewidth=0.8, ax=ax, legend=True)

        plt.title(f"Population Density Heatmap - Regions: {', '.join(region_names)}, Value Column: {value_column}")
        plt.show()

if __name__ == "__main__":
    density_visualizer = HeatmapVisualizer(
        "/Users/songle/Geotify/asset/skorea_municipalities_geo_simple.json",
        "/Users/songle/Geotify/asset/인구밀도_20240309190931.csv"
    )

    # 인구밀도 시각화
    region_names = ["강북구", "강남구", "서초구"]
    value_column = "인구밀도 (명/㎢)" 

    density_visualizer.visualize_heatmap(region_names, value_column)