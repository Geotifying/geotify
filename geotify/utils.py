import os
from pathlib import Path


def load_geojson_file_path():
    geojson_file_path = os.getenv("GEOTIFY_GEOJSON_FILE")

    if geojson_file_path is not None:
        return geojson_file_path
    else:
        current_dir = Path(__file__).parent
        default_geojson_path = current_dir / "datasets" / "base_korea_map.json"
        return str(default_geojson_path)
