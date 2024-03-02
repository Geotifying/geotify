import geopandas as gpd
import matplotlib.pyplot as plt

geojson_path = "/Users/songle/Geotify/asset/TL_SCCO_CTPRVN.json"

gdf_korea = gpd.read_file(geojson_path)


# 경기도 정보만 추출하여 새로운 GeoDataFrame 생성
gdf_seoul = gdf_korea[gdf_korea['CTP_ENG_NM'] == 'Seoul']

# 경기도 GeoDataFrame을 플로팅
gdf_seoul.plot()

# 시각화
plt.show()
