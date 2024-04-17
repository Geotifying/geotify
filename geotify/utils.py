import os


def load_geojson_file_path():
    # GEOTIFY_GEOJSON_FILE 환경 변수가 설정되어 있는지 확인. -> 사용자 입력 받을 수 있게
    geojson_file_path = os.getenv("GEOTIFY_GEOJSON_FILE")

    if geojson_file_path is not None:
        return geojson_file_path
    else:
        # 환경 변수가 설정되어 있지 않다면 기본 경로를 제공.
        current_dir = os.path.dirname(__file__)
        # 나는 기본적으로 json을 제공하고 싶음.
        default_geojson_path = os.path.join(
            current_dir, "data", "skorea_municipalities_geo_simple.json"
        )
        return default_geojson_path
