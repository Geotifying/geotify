import json
import os
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import rc
from rich import inspect

rc("font", family="AppleGothic")
plt.rcParams["axes.unicode_minus"] = False


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

    def calculate_polygon_center(self, coordinates):
        if len(coordinates) == 1:
            polygon = coordinates[0]
        else:
            polygon = np.concatenate(coordinates)
        total_x = 0
        total_y = 0
        num_points = 0
        for ring in polygon:
            for point in ring:
                x, y = point
                total_x += x
                total_y += y
                num_points += 1
        center_x = total_x / num_points
        center_y = total_y / num_points
        return (center_x, center_y)

    def visualize_barchart(self, region_names, value_column):
        sgg_data = self.load_geojson(
            Path(__file__)
            .parent.with_name("asset")
            .joinpath("skorea_municipalities_geo_simple.json")
        )
        seoul_map = sgg_data[sgg_data["CTPRVN_CD"] == "11"]
        selected_data = self.population_data[
            self.population_data["동별(2)"].isin(region_names)
        ]

        fig, ax = plt.subplots(figsize=(10, 10))
        selected_data = seoul_map.merge(
            selected_data, how="left", right_on="동별(2)", left_on="name"
        )
        selected_data.plot(
            column=value_column,
            cmap="YlGnBu",
            ax=ax,
            legend=True,
            edgecolor="black",
            missing_kwds={
                "color": "white",
                "edgecolor": "red",
                # "hatch": "///",
                "label": "Missing values",
            },
        )

        for region_name in region_names:
            region_data = selected_data[selected_data["동별(2)"] == region_name]
            coordinates = region_data["geometry"].iloc[0].centroid
            population_density = region_data[value_column].values[0]

            color = plt.cm.YlGnBu(population_density / selected_data[value_column].max())

            ax.add_patch(
                patches.Rectangle(
                    (coordinates.x, coordinates.y),  # (x, y)
                    0.01,
                    population_density / 25315 / 10,  # width, height
                    edgecolor="black",
                    facecolor=color,
                    fill=True,
                )
            )

        plt.title(
            f"Population Density Heatmap - Regions: {', '.join(region_names)}, Value Column: {value_column}"
        )
        plt.show()


if __name__ == "__main__":
    ASSETS_PATH = Path(__file__).parent.with_name("asset")
    map_data_path = ASSETS_PATH.joinpath("skorea_municipalities_geo_simple.json")
    population_density_data = ASSETS_PATH.joinpath("인구밀도_20240309190931.csv")
    density_visualizer = HeatmapVisualizer(map_data_path, population_density_data)

    # 인구밀도 시각화
    region_names = ["강북구", "강남구", "서초구"]
    value_column = "인구밀도 (명/㎢)"

    # density_visualizer.visualize_heatmap(region_names, value_column)

    density_visualizer.visualize_barchart(region_names, value_column)

    geotify_map = GeotifyMapVisualizer()
    # geotify_map.visualize_map()
