from fastapi import FastAPI, UploadFile, File
import uvicorn
import fiona
import pyproj
import json

# FastAPI 객체 생성
app = FastAPI()

import geopandas as gpd
gdf = gpd.read_file("sample2.gpkg")
# gdf = gpd.read_file("Jeongeup_out_1024.gpkg")
sim_geo = gpd.GeoSeries(gdf['geometry']).simplify(tolerance=0.0001).to_json()
print('geoPackage file loaded')

@app.get("/")
def root():
    return "/docs 로 API 테스트 가능합니다."

@app.get("/geo-range/{sta_idx}/{end_idx}")
def read_geo_fiona(sta_idx: int = 0, end_idx: int = 100):
    # with fiona.open("Jeongeup_out_1024.gpkg") as layer:
    with fiona.open("sample2.gpkg") as layer:
        # cols = layer.schema['properties']
        # print(cols)
        
        # src_crs = layer.crs
        # print(src_crs)
        # target_crs = pyproj.CRS('EPSG:5186')
        # target_crs = pyproj.CRS('EPSG:4326')
        # target_crs = pyproj.CRS(req_crs)
        # transformer = pyproj.Transformer.from_crs(src_crs, target_crs)

        # folium.Polygon([(39.949610, -75.150282),(39.849610, -75.150282),(39.749610, -75.050282)]).add_to(m)
        rtn = []
        for i, f in enumerate(layer):
        #     # print(f.properties['CLS_ID'])
        
            if i >= sta_idx and i < end_idx:
                polygons = f.geometry.coordinates[0]
                tr_polygons = []
                for p in polygons:
                    lon, lat = p
                    tr_polygons.append((lat, lon))         
                #     lon, lat = transformer.transform(*p)
                #     tr_polygons.append((lon, lat))
                
                rtn.append(tr_polygons)
            # else:
            #     break
            
            if i >= end_idx:
                break
            
        print("cnt: ", len(rtn))
            
    return {'rtn':rtn}


@app.get("/geojson-range/{sta_idx}/{end_idx}")
def read_geojson_range(sta_idx: int = 0, end_idx: int = 2):
    # return json.loads(gdf[sta_idx:end_idx]['geometry'].to_json())
    return json.loads(gdf[sta_idx:end_idx].to_json())

@app.get("/geo-simlify/{tol}/{cls_id}")
def read_geo_simlify(tol: float = 0.0001, cls_id: int = 1):
    filter = (gdf['CLS_ID']==cls_id)
    return gpd.GeoSeries(gdf[filter]['geometry']).simplify(tolerance=tol).to_json()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=30001)
    # uvicorn.run(app, host="0.0.0.0", port=8000)    
#uvicorn pred_api:app --host 0.0.0.0 --port 30001 --workers 4
#gunicorn pred_api:app --workers 4 --worker-class 