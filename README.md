# geotify

Visualization tools suitable for geographic data.

## introduction

geotify is a library that visualizes desired data on top of geographic data.

## install

Geotify depends on the following packages:
- matplotlib
- pandas
- geopandas

## Examples

```python
from pathlib import Path
from geotify.visualization import BarChartVisualizer, RegionCodeEnum

# Set the path to the datasets directory
ASSETS_PATH = Path(__file__).parent / "datasets"

# Define paths to the GeoJSON and CSV files
map_data_path = ASSETS_PATH.joinpath("base_korea_map.json")
population_density_data = ASSETS_PATH.joinpath("강원도.csv")

# Initialize the visualizer with specific regional settings
density_visualizer = BarChartVisualizer(
    map_data_path, population_density_data, RegionCodeEnum.강원특별자치도, "동별(2)"
)

# List of regions to visualize
region_names = ["평창군"]

# Column name containing the population density values
value_column = "인구밀도 (명/㎢)"

# Execute the visualization
density_visualizer.visualize(region_names, value_column)
```
<img width="801" alt="image" src="https://github.com/0gonge/Study/assets/88605949/693fb018-af21-4203-bbcf-a1d64132a9a6">




```python
geotify_map = HeatmapVisualizer(map_data_path, population_density_data)
geotify_map.visualize(color="lightblue")
```
<img width="877" alt="image" src="https://github.com/0gonge/Study/assets/88605949/025c54dd-f944-420c-bbe7-54291265149b">
