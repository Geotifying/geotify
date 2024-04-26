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


# sys.excepthook = catch_exception

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(name)s][%(filename)s:%(funcName)s:%(lineno)d] - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger.setLevel(logging.INFO)
MAX_SHOW_REGION = 10
DEFAULT_FIGURE_SIZE = (10, 10)
DEFAULT_BAR_WIDTH = 0.01
DEFAULT_BAR_CHART_SCALE = 10


class RegionCodeEnum(Enum):
    서울특별시 = "11"
    광주광역시 = "29"
    세종특별자치시 = "36"
    울산광역시 = "31"
    부산광역시 = "26"
    대구광역시 = "27"
    인천광역시 = "28"
    전북특별자치도 = "45"
    충청남도 = "44"
    강원특별자치도 = "42"
    경기도 = "41"
    경상북도 = "47"
    경상남도 = "48"
    전라남도 = "46"
    대전광역시 = "30"
    충청북도 = "43"
    제주특별자치도 = "50"


class Visualizer:
    def __init__(self, geojson_file_path: Path, csv_file_path: Path) -> None:
        if not geojson_file_path.exists():
            logger.warning(f"{geojson_file_path} is not exists.")
            raise
        if not geojson_file_path.is_file():
            logger.error(f"[geojson_file_path] is not a valid file.")
            raise ValueError(f"Provided path{geojson_file_path} is not a file.")

        self.geo_data = self.load_geojson(geojson_file_path)
        self.population_data = self.load_data(csv_file_path)

    def load_geojson(
        self, geojson_file_path: Path, encoding: str = "utf-8"
    ) -> GeoDataFrame:
        try:
            geo_data = gpd.read_file(geojson_file_path, encoding=encoding)
            return geo_data
        except ValueError as e:
            logger.error(
                f"Error loading GeoJSON file {geojson_file_path} with encoding {encoding} : {e}"
            )
            raise ValueError(
                f"Error loading GeoJson file with encoding {encoding}:{e}"
            ) from e

    def load_data(self, csv_file_path: Path, encoding="utf-8") -> DataFrame:
        try:
            csv_data = pd.read_csv(csv_file_path, encoding=encoding)
            return csv_data
        except UnicodeDecodeError:
            logger.error(f"Invalid encoding {encoding=!r}")
        except ValueError as e:
            logger.error(
                f"Error loading CSV file {csv_file_path} with encoding{encoding}:{e}"
            )
            raise ValueError("Error loading CSV file") from e
        except Exception as e:
            logger.exception(
                "Unexpected Exception while loading CSV file: ", exc_info=e
            )

    def visualize(self) -> None:
        logger.error(
            "The visualize method has not been implemented. "
            "using the geo_data and population_data attributes"
            "example : density_visualizer.visualize(region_names, value_column)"
        )
        raise NotImplementedError("The 'visualize' method has not been implemented. ")


class HeatmapVisualizer(Visualizer):
    def preprocess_map_data(self) -> Any:
        pass

    def visualize(self, region_names=None, color="white"):  # type: ignore
        if region_names:
            regions = self.geo_data[self.geo_data["name"].isin(region_names)]
        else:
            regions = self.geo_data

        if regions.empty:
            logger.error(f"Regions with names {region_names} not found")
            return

        _, ax = plt.subplots(figsize=DEFAULT_FIGURE_SIZE)
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
        self.region_code = region_code.value
        self.region_key = region_key
        super().__init__(geojson_file_path, csv_file_path)

    def preprocess_map_data(self) -> Any:
        pass

    def visualize(  # type: ignore
        self,
        region_names: List[str],
        value_column: str,
        cmap: str = "YlGnBu",
        missing_color: str = "white",
        missing_edgecolor: str = "red",
    ) -> None:
        logger.info(
            f"Starting visualization with region names: {region_names}, value column: {value_column}"
        )

        if len(region_names) > MAX_SHOW_REGION:
            logger.warning(
                f"Visualizing more than 10 elements can be difficult to see."
            )

        map = self.geo_data[self.geo_data["CTPRVN_CD"] == self.region_code]
        selected_data = self.population_data[
            self.population_data[self.region_key].isin(region_names)
        ]

        selected_data = selected_data.dropna(subset=[value_column])
        _, ax = plt.subplots(figsize=DEFAULT_FIGURE_SIZE)

        selected_data = map.merge(
            selected_data, how="left", right_on=self.region_key, left_on="name"
        )
        selected_data.plot(
            column=value_column,
            cmap=cmap,
            ax=ax,
            legend=True,
            edgecolor="black",
            missing_kwds={
                "color": missing_color,
                "edgecolor": missing_edgecolor,
                "label": "Missing values",
            },
        )

        max_population_density = selected_data[value_column].max()

        for region_name in region_names:
            region_data = selected_data[selected_data[self.region_key] == region_name]
            coordinates = region_data["geometry"].iloc[0].centroid
            population_density = region_data[value_column].values[0]

            scaled_population_density = population_density / max_population_density

            color = plt.cm.YlGnBu(scaled_population_density)

            ax.add_patch(
                patches.Rectangle(
                    (coordinates.x, coordinates.y),
                    DEFAULT_BAR_WIDTH,
                    scaled_population_density / DEFAULT_BAR_CHART_SCALE,
                    edgecolor="black",
                    facecolor=color,
                    fill=True,
                )
            )

        plt.title(
            f"Population Density Heatmap - Regions: {', '.join(region_names)}, Value Column: {value_column}"
        )
        plt.show()

        logger.info(f"Visualization completed successfully for regions: {region_names}")


if __name__ == "__main__":
    ASSETS_PATH = Path(__file__).parent.with_name("asset")
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
