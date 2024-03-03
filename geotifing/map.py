import geopandas as gpd
import matplotlib.pyplot as plt
from .utils import import_optional_dependency
import os

# 시각화 함수 설정
class GeotifyMapVisualizer:
    def __init__(self):
        self.geojson_file = self.load_geojson_file_path()
        self.geo_data = self.load_geojson()

    def load_geojson_file_path(self):
        # GEOTIFY_GEOJSON_FILE 환경 변수가 설정되어 있는지 확인. -> 사용자 입력 받을 수 있게 
        geojson_file_path = os.getenv('GEOTIFY_GEOJSON_FILE')
        
        if geojson_file_path is not None:
            return geojson_file_path
        else:
            # 환경 변수가 설정되어 있지 않다면 기본 경로를 제공. 이거 경로가.. 맞나? 
            return "/Users/songle/Geotify/asset/skorea_municipalities_geo_simple.json"

    def load_geojson(self):
        try:
            geo_data = gpd.read_file(self.geojson_file, encoding='utf-8')
            return geo_data
        except Exception as e:
            raise ValueError(f"Error loading GeoJSON file: {e}")

    # 전체 지도 시각화 시, 기본 지도 배경 설정 값 흰색으로 지정
    def visualize_map(self, region_name=None, color='white'):

        # 입력값이 없을 때는 전체 지도 출력
        if region_name is not None:
            selected_region = self.geo_data[self.geo_data['name'] == region_name]

            # 사용자 입력을 받았을 경우, custom
            if not selected_region.empty:
                fig, ax = plt.subplots(figsize=(10, 10))
                selected_region.plot(ax=ax, facecolor=color, edgecolor='black')
                plt.title(f"GeoMap Visualization - Region Name: {region_name}")
                plt.show()
            else:
                print(f"Region with name '{region_name}' not found.")
        else:
            fig, ax = plt.subplots(figsize=(10, 10))
            self.geo_data.plot(ax=ax, facecolor=color, edgecolor='black')  # 전체 지도 그림
            plt.title("GeoMap Visualization - Entire Map")
            plt.show()

# 예시 사용법
if __name__ == "__main__":
    map_visualizer = GeotifyMapVisualizer()

    # 시각화를 원하는 지역 이름과 색상을 입력하여 visualize_map 함수 호출
    map_visualizer.visualize_map(region_name='남원시', color='blue')
    map_visualizer.visualize_map()
