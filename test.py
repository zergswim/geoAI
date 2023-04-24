# import geopandas as gpd
# data = gpd.read_file("codepo_gb.gpkg")

import fiona
import pyproj

import folium
import streamlit as st

from streamlit_folium import st_folium
import requests
import torch

# from httpx import AsyncClient
import asyncio 
# async_client = AsyncClient()

import json

# @st.cache_data
# def requestAPI(sta_idx, end_idx):
#     print("requestAPI:", sta_idx, end_idx)
#     # response = requests.get(f"http://localhost:30001/read?sta_idx={sta_idx}&end_idx={end_idx}") #, files=file, params=params)
#     response = requests.get(f"http://localhost:30001/read_geopandas?sta_idx={sta_idx}&end_idx={end_idx}") #, files=file, params=params)
#     json_obj = json.loads(response.json())
#     # print(type(json_obj), dir(json_obj))
    
#     polys = []
#     for p in json_obj['features']:
#         po = p['geometry']['coordinates'][0]
#         poly = [(lat, lon) for lon, lat in po]
#         polys.append(poly)
#     return polys

@st.cache_data
def requestAPI_simple(tol, cls_id):
    print("requestAPI_simple:", tol, cls_id)
    response = requests.get(f"http://localhost:30001/geojson-simplify/{tol}/{cls_id}") #, files=file, params=params)
    json_obj = json.loads(response.json())
    # print(type(json_obj), dir(json_obj))
    
    polys = []
    for p in json_obj['features']:
        po = p['geometry']['coordinates'][0]
        poly = [(lat, lon) for lon, lat in po]
        polys.append(poly)
    return polys

# @st.cache_data
# def requestAPI_geojson(simple):
#     print("requestAPI_geojson:", simple)
#     response = requests.get(f"http://localhost:30001/read_geojson?tol={simple}") #, files=file, params=params)
#     json_obj = json.loads(response.json())
#     return json_obj

def main():
    st.title("위성영상 재난탐지 실습")
    sim_lvl = st.radio("SIMPLIFY_LEVEL : ", (0.00001, 0.0001, 0.001, 0.01, 0.1), index=2, horizontal=True)
    zoom_lvl = st.slider("ZOOM_LEVEL : ", 1, 15, 8)
    cls_id = st.radio("CLS_ID : ", (1, 2, 3, 4, 5), horizontal=True)

    polys = requestAPI_simple(sim_lvl, cls_id)

    lat, lon = polys[0][0]

    m = folium.Map(location=[lat, lon], zoom_start=zoom_lvl)
    
    # json_obj = requestAPI_geojson(0.0001)
    # folium.GeoJson(data=json_obj).add_to(m)

    folium.Polygon(polys).add_to(m)

    # polys = requestAPI(500, 1000)
    # folium.Polygon(polys).add_to(m)

    # polys = requestAPI(1500, 2000)
    # folium.Polygon(polys).add_to(m)

    # polys = requestAPI(2000, 2500)
    # folium.Polygon(polys).add_to(m)

    # polys = requestAPI(2500, 3000)
    # folium.Polygon(polys).add_to(m)


    # folium.Marker(
    #     [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
    # ).add_to(m)

    # folium.Polygon([[39.949610, -75.150282],[39.849610, -75.150282],[39.749610, -75.050282]]).add_to(m)

    # m = drawPolygon('Jeongeup_out_1024.gpkg', m)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=1024)

main()

#streamlit run test.py --server.port 30002 --server.fileWatcherType none

# async def drawPolygon(filename, m):
# def drawPolygon(filename, m):
#     with fiona.open(filename) as layer:
#         # cols = layer.schema['properties']
#         # print(cols)
        
#         src_crs = layer.crs
#         print(src_crs)
#         # target_crs = pyproj.CRS('EPSG:5186')
#         # target_crs = pyproj.CRS('EPSG:4326')
#         target_crs = pyproj.CRS('EPSG:4004')
#         transformer = pyproj.Transformer.from_crs(src_crs, target_crs)

#         # folium.Polygon([(39.949610, -75.150282),(39.849610, -75.150282),(39.749610, -75.050282)]).add_to(m)

#         for i, f in enumerate(layer):
#         #     # print(f.properties['CLS_ID'])
#             polygons = f.geometry.coordinates[0]
#             tr_polygons = []
#             for p in polygons:
#                 lon, lat = transformer.transform(*p)
#                 tr_polygons.append((lon, lat))
            
#             # print(tr_polygons)
#             folium.Polygon(tr_polygons).add_to(m)
#             # await asyncio.sleep(1)
            
#             if i>100:
#                 break
#         #     folium.Polygon(polygon).add_to(m)
#         #     break
            
#             # for c in f.geometry.coordinates[0]:
#             #     lon, lat = transformer.transform(*c)
#                 # print(lon, lat)    
#     return m

# asyncio.run(main())
# main()

#streamlit run test.py --server.port 30002 --server.fileWatcherType none

# # No need to pass "layer='etc'" if there's only one layer

# # print(fiona.listlayers('codepo_gb.gpkg'))

# # with fiona.open('codepo_gb.gpkg', driver="GPKG") as layer:
# # with fiona.open('codepo_gb.gpkg', crs='EPSG:4326') as layer:
# with fiona.open('Jeongeup_out_1024.gpkg') as layer:

#     cols = layer.schema['properties']
#     print(cols)
    
#     src_crs = layer.crs    
#     # target_crs = pyproj.CRS('EPSG:5186')
#     target_crs = pyproj.CRS('EPSG:4326')
#     transformer = pyproj.Transformer.from_crs(src_crs, target_crs)

#     for f in layer:
#         # lon, lat = f.geometry.coordinates
#         # lon, lat = transformer.transform(*coordinates)
        
#         print(f.properties['CLS_ID'])

#         for c in f.geometry.coordinates[0]:
#             lon, lat = transformer.transform(*c)
#             print(lon, lat)

#         break
        

#         # rst = {}
#         # for c in cols:
#         #     rst[c] = f.properties[c]

#         # arr = rst['postcode'].split()
#         # if arr[0] == 'AB11':
#         #     print(lon, lat, rst)
#         # break

#         # print(feature.geometry.coordinates, feature.geometry.type)
#         # # print(dir(feature['geometry'].items))

#         # # print(feature.items)
#         # print(feature['geometry'].coordinates, feature['geometry'].type)
        
#         # f = {k: feature[k] for k in ['id', 'geometry']}
#         # print(f)
        
#         # break


# # data.plot()

# # print(data.head())

# # print(data["real"].head())