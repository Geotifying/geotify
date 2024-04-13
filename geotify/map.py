import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Any, List

import geopandas as gpd
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
from geopandas import GeoDataFrame
from matplotlib import rc
from pandas import DataFrame
from rich.logging import RichHandler

rc("font", family="AppleGothic")
plt.rcParams["axes.unicode_minus"] = False


def catch_exception(exc_type, exc_value, exc_traceback):
    logger.exception(
        "Unexpected Exception:", exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = catch_exception

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(name)s][%(filename)s:%(funcName)s:%(lineno)d] - %(message)s",
    # handlers=[RichHandler(rich_tracebacks=True)]
)
logger.setLevel(logging.INFO)


class RegionCodeEnum(Enum):
    SEOUL = "11"
    ...


class RegionCode:
    SEOUL = "11"


class Visualizer:
    def __init__(self, geojson_file_path: Path, csv_file_path: Path) -> None:
        if not geojson_file_path.exists():
            logger.warning(f"{geojson_file_path} is not exists.")
            raise
        if not geojson_file_path.is_file():
            raise
        self.geo_data = self.load_geojson(geojson_file_path)
        self.population_data = self.load_data(csv_file_path)

    def load_geojson(self, geojson_file_path: Path) -> GeoDataFrame:
        try:
            geo_data = gpd.read_file(geojson_file_path, encoding="utf-8")
            return geo_data
        except ValueError as e:
            raise ValueError("Error loading GeoJSON file")

    def load_data(self, csv_file_path: Path, encoding="utf-8") -> DataFrame:
        try:
            csv_data = pd.read_csv(csv_file_path, encoding=encoding)
            return csv_data
        except UnicodeDecodeError:
            logger.error(f"Invalid encoding {encoding=!r}")
        except ValueError as e:
            raise ValueError("Error loading GeoJSON file")
        except Exception as e:
            logger.exception("Unexpected Exception: ", e)

    def visualize(self) -> None:
        raise NotImplementedError


class HeatmapVisualizer(Visualizer):
    def preprocess_map_data(self) -> Any:
        pass

    def visualize(self, region_names=None, color="white"):  # type: ignore
        if region_names:
            regions = self.geo_data[self.geo_data["name"].isin(region_names)]
        else:
            regions = self.geo_data

        if regions.empty:
            print(f"Regions with names {region_names} not found.")
            return

        _, ax = plt.subplots(figsize=(10, 10))
        regions.plot(ax=ax, facecolor=color, edgecolor="black")
        plt.title(f"GeotifyMap Visualization : Region Names: {region_names}")
        plt.show()


class BarChartVisualizer(Visualizer):
    def __init__(
        self,
        geojson_file_path: Path,
        csv_file_path: Path,
        region_code: RegionCodeEnum,
        region_key: str,
    ) -> None:
        self.region_code = region_code
        self.region_key = region_key
        super().__init__(geojson_file_path, csv_file_path)

    def preprocess_map_data(self) -> Any:
        pass

    def visualize(self, region_names: List[str], value_column: str) -> None:  # type: ignore
        logger.info("visualize")
        if len(region_names) > 6:
            raise ValueError("The maximum number of region_names should be 6 or lower")

        seoul_map = self.geo_data[self.geo_data["CTPRVN_CD"] == self.region_code]
        selected_data = self.population_data[
            self.population_data[self.region_key].isin(region_names)
        ]

        fig, ax = plt.subplots(figsize=(10, 10))
        selected_data = seoul_map.merge(
            selected_data, how="left", right_on=self.region_key, left_on="name"
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
                "label": "Missing values",
            },
        )

        for region_name in region_names:
            region_data = selected_data[selected_data[self.region_key] == region_name]
            coordinates = region_data["geometry"].iloc[0].centroid
            population_density = region_data[value_column].values[0]

            color = plt.cm.YlGnBu(
                population_density / selected_data[value_column].max()
            )

            ax.add_patch(
                patches.Rectangle(
                    (coordinates.x, coordinates.y),
                    0.01,
                    population_density / 25315 / 10,
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
    density_visualizer = BarChartVisualizer(
        map_data_path, population_density_data, RegionCodeEnum.SEOUL, "동별(2)"
    )

    # 인구밀도 시각화
    region_names = ["강북구", "강남구", "서초구", "용산구", "노원구", "동대문구"]
    value_column = "인구밀도 (명/㎢)"

    logger.info("hello")
    logger.error("error")

    density_visualizer.visualize(region_names, value_column)

    geotify_map = HeatmapVisualizer(map_data_path, population_density_data)
    geotify_map.visualize()
