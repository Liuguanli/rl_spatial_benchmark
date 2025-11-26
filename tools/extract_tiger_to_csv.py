# import zipfile
# import os
# import tempfile
# import glob
# import fiona
# from shapely.geometry import shape
# import pandas as pd


# def read_place_shapefile(shp_path: str) -> pd.DataFrame:
#     """
#     Read a PLACE shapefile and return attributes + centroid + bounding box
#     """
#     features = []
#     with fiona.open(shp_path, 'r') as src:
#         for feature in src:
#             geom = shape(feature['geometry'])
#             props = dict(feature['properties'])
#             props['centroid_lon'] = geom.centroid.x
#             props['centroid_lat'] = geom.centroid.y
#             props['bbox_minx'], props['bbox_miny'], props['bbox_maxx'], props['bbox_maxy'] = geom.bounds
#             features.append(props)
#     return pd.DataFrame(features)


# def read_landmark_shapefile(shp_path: str) -> pd.DataFrame:
#     """
#     Read shapefile and return attributes + centroid + bounding box
#     """
#     features = []
#     with fiona.open(shp_path, 'r') as src:
#         for feature in src:
#             geom = shape(feature['geometry'])
#             props = dict(feature['properties'])
#             props['centroid_lon'] = geom.centroid.x
#             props['centroid_lat'] = geom.centroid.y
#             props['bbox_minx'], props['bbox_miny'], props['bbox_maxx'], props['bbox_maxy'] = geom.bounds
#             features.append(props)
#     return pd.DataFrame(features)

# def extract_and_process_zip(zip_path: str) -> pd.DataFrame:
#     """
#     Unzip a ZIP file containing a shapefile and return parsed data
#     """
#     with tempfile.TemporaryDirectory() as tmpdir:
#         with zipfile.ZipFile(zip_path, 'r') as z:
#             z.extractall(tmpdir)
#         shp_files = glob.glob(os.path.join(tmpdir, "*.shp"))
#         if not shp_files:
#             return pd.DataFrame()  # Skip if no .shp
#         df = read_landmark_shapefile(shp_files[0])
#         df["source_file"] = os.path.basename(zip_path)
#         return df

# def batch_process_zip_folder(folder_path: str) -> pd.DataFrame:
#     """
#     Process all ZIP shapefiles in a folder and return combined results
#     """
#     all_dfs = []
#     for zip_file in glob.glob(os.path.join(folder_path, "*.zip")):
#         print(f"Processing {zip_file}")
#         df = extract_and_process_zip(zip_file)
#         if not df.empty:
#             all_dfs.append(df)
#         # break
#     return pd.concat(all_dfs, ignore_index=True)


# import geopandas as gpd
# import fiona
# import os
# import pandas as pd

# def extract_mbrs_from_gdb(gdb_path: str, output_csv: str):
#     """
#     Extract MBR (minx, miny, maxx, maxy) for all features in all layers of a .gdb
#     and write to CSV.
#     """
#     layers = fiona.listlayers(gdb_path)
#     print(f"Found {len(layers)} layers in GDB.")

#     all_records = []

#     for layer in layers:
#         print(f"Reading layer: {layer}")
#         gdf = gpd.read_file(gdb_path, layer=layer)

#         if gdf.empty:
#             continue

#         # Extract MBR (bounding box) for each geometry
#         bounds = gdf.bounds
#         bounds["layer"] = layer
#         all_records.append(bounds)

#     # Combine and export
#     if all_records:
#         df_all = pd.concat(all_records, ignore_index=True)
#         df_all.columns = ["minx", "miny", "maxx", "maxy", "layer"]
#         df_all.to_csv(output_csv, index=True, index_label="id")
#         print(f"MBRs saved to {output_csv}")
#     else:
#         print("No geometries found.")



# if __name__ == "__main__":
#     # df_all = batch_process_zip_folder("../tiger/places")
#     # df_all.to_csv("../tiger/places/all_places.csv", index=True, index_label="id")

#     # # Assuming all .zip files are under ./shapefiles/
#     # df_all = batch_process_zip_folder("../tiger/landmarks")
#     # df_all.to_csv("../tiger/landmarks/all_landmarks.csv", index=True, index_label="id")
#     # https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-geodatabase-file.html
#     # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_linearwater.gdb", "tiger_linearwater_mbrs.csv")
#     # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_roads.gdb", "tiger_roads_mbrs.csv")
#     extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_block.gdb", "tiger_blocks_mbrs.csv")
# export_geoms_simple.py
# -*- coding: utf-8 -*-
# extract_tiger_to_csv.py
# -*- coding: utf-8 -*-
# extract_tiger_to_csv.py
# -*- coding: utf-8 -*-

import os
import csv
import json
import pandas as pd  # kept for compatibility, though streaming doesn't rely on DataFrames
import geopandas as gpd
# import fiona
from shapely.geometry import shape, mapping
from shapely.errors import GEOSException
from shapely.ops import transform as shp_transform
from shapely.validation import make_valid  # optional; not used by default
from pyproj import Transformer


# -----------------------------
# Utilities: enrich GeoDataFrame (kept for small layers or reuse)
# -----------------------------
# def _add_geometry_columns(
#     gdf: gpd.GeoDataFrame,
#     add_geojson: bool = False,
#     calc_area_length: bool = True,
#     area_crs: str | None = "EPSG:6933"  # Global meter-based projection; prefer local UTM if available
# ) -> gpd.GeoDataFrame:
#     """
#     Enrich a GeoDataFrame with:
#       - geom_type
#       - geometry_wkt
#       - (optional) geometry_geojson (compact JSON string)
#       - centroid_lon, centroid_lat (computed in EPSG:4326)
#       - bbox_minx, bbox_miny, bbox_maxx, bbox_maxy (in EPSG:4326)
#       - (optional) area_m2, length_m (computed in a projected CRS)
#     """
#     if "geometry" not in gdf or gdf.geometry.isna().all():
#         raise ValueError("No valid geometry column found in the GeoDataFrame.")

#     gdf = gdf.copy()

#     # WGS84 view for centroid/bbox
#     if gdf.crs and gdf.crs.to_string() != "EPSG:4326":
#         gdf_wgs84 = gdf.to_crs("EPSG:4326")
#     else:
#         gdf_wgs84 = gdf

#     # Basic per-geometry attributes
#     gdf["geom_type"] = gdf.geometry.geom_type
#     gdf["geometry_wkt"] = gdf.geometry.apply(lambda g: None if g is None else g.wkt)

#     if add_geojson:
#         gdf["geometry_geojson"] = gdf.geometry.apply(
#             lambda g: None if g is None else json.dumps(mapping(g), ensure_ascii=False)
#         )

#     # Centroid and bounding box in WGS84
#     gdf["centroid_lon"] = gdf_wgs84.geometry.centroid.x
#     gdf["centroid_lat"] = gdf_wgs84.geometry.centroid.y
#     bounds = gdf_wgs84.geometry.bounds  # DataFrame with minx, miny, maxx, maxy
#     gdf["bbox_minx"] = bounds["minx"]
#     gdf["bbox_miny"] = bounds["miny"]
#     gdf["bbox_maxx"] = bounds["maxx"]
#     gdf["bbox_maxy"] = bounds["maxy"]

#     # Area and length in meters (requires projected CRS)
#     if calc_area_length:
#         try:
#             gdf_metric = gdf
#             if area_crs:
#                 if gdf.crs:
#                     if gdf.crs.to_string() != area_crs:
#                         gdf_metric = gdf.to_crs(area_crs)
#                 else:
#                     gdf_metric = gdf.set_crs("EPSG:4326", allow_override=True).to_crs(area_crs)
#             gdf["area_m2"] = gdf_metric.geometry.area
#             gdf["length_m"] = gdf_metric.geometry.length
#         except GEOSException:
#             gdf["area_m2"] = None
#             gdf["length_m"] = None

#     return gdf


# -----------------------------
# GDB reader helper: skip organizePolygons via GDAL config
# -----------------------------
# def _read_gdb_layer_skip_organize(gdb_path: str, layer: str) -> gpd.GeoDataFrame:
#     """
#     Read a FileGDB layer using Fiona while skipping the expensive organizePolygons step.
#     This uses a GDAL config option that OpenFileGDB honors (open_options won't work here).
#     NOTE: This function returns a GeoDataFrame (loads whole layer) — only use for small layers.
#     """
#     os.environ["OGR_ORGANIZE_POLYGONS"] = "SKIP"  # or "ONLY_CCW"
#     with fiona.Env(OGR_ORGANIZE_POLYGONS="SKIP"):
#         return gpd.read_file(gdb_path, layer=layer, engine="fiona")


# -----------------------------
# Streaming exporters (memory-safe)
# -----------------------------
# def extract_mbrs_from_gdb(gdb_path: str, output_csv: str):
#     """
#     Stream MBRs for every feature in every layer of a FileGDB and write to CSV.
#     Avoids loading the whole layer into memory; skips slow polygon organizing.
#     Output columns: layer, minx, miny, maxx, maxy
#     """
#     os.environ["OGR_ORGANIZE_POLYGONS"] = "SKIP"

#     layers = fiona.listlayers(gdb_path)
#     print(f"Found {len(layers)} layers in GDB.")

#     with open(output_csv, "w", newline="", encoding="utf-8") as f:
#         w = csv.writer(f)
#         w.writerow(["layer", "minx", "miny", "maxx", "maxy"])  # header

#         for layer in layers:
#             print(f"Reading layer: {layer}")
#             with fiona.Env(OGR_ORGANIZE_POLYGONS="SKIP"):
#                 with fiona.open(gdb_path, layer=layer) as src:
#                     for feat in src:
#                         if not feat or not feat.get("bbox"):
#                             continue
#                         minx, miny, maxx, maxy = feat["bbox"]
#                         w.writerow([layer, minx, miny, maxx, maxy])

#     print(f"MBRs saved to {output_csv}")


# def extract_geoms_from_gdb(
#     gdb_path: str,
#     output_csv: str,
#     add_geojson: bool = False,
#     calc_area_length: bool = True,
#     area_crs: str | None = "EPSG:6933",
#     explode_multi: bool = False  # kept for API compatibility; streaming doesn't need it
# ):
#     """
#     Stream attributes + geometry info (WKT/centroid/bbox/[area/length]) to CSV.
#     - No GeoDataFrame concatenation; avoids OOM on huge GDB layers.
#     - Skips expensive organizePolygons via GDAL config.
#     - Geometry is serialized per-feature; memory is bounded.
#     Output columns:
#       layer, <all original properties...>,
#       geom_type, geometry_wkt, [geometry_geojson],
#       centroid_lon, centroid_lat,
#       bbox_minx, bbox_miny, bbox_maxx, bbox_maxy,
#       [area_m2, length_m]
#     """
#     os.environ["OGR_ORGANIZE_POLYGONS"] = "SKIP"

#     layers = fiona.listlayers(gdb_path)
#     print(f"Found {len(layers)} layers in GDB.")

#     header_written = False

#     with open(output_csv, "w", newline="", encoding="utf-8") as f_csv:
#         writer = csv.writer(f_csv)

#         for layer in layers:
#             print(f"Reading layer: {layer}")
#             with fiona.Env(OGR_ORGANIZE_POLYGONS="SKIP"):
#                 with fiona.open(gdb_path, layer=layer) as src:
#                     # Determine attribute fields from schema
#                     attr_fields = list(src.schema.get("properties", {}).keys())

#                     # Prepare CRS transformers (to WGS84 for centroid/bbox; to area_crs for area/length)
#                     to_wgs84 = None
#                     to_area = None
#                     src_crs = src.crs or src.crs_wkt
#                     try:
#                         if src_crs:
#                             to_wgs84 = Transformer.from_crs(src_crs, "EPSG:4326", always_xy=True).transform
#                             if calc_area_length and area_crs:
#                                 to_area = Transformer.from_crs(src_crs, area_crs, always_xy=True).transform
#                     except Exception:
#                         to_wgs84 = None
#                         to_area = None

#                     # Write header once (first non-empty layer)
#                     if not header_written:
#                         header = ["layer"] + attr_fields + [
#                             "geom_type", "geometry_wkt"
#                         ]
#                         if add_geojson:
#                             header.append("geometry_geojson")
#                         header += [
#                             "centroid_lon", "centroid_lat",
#                             "bbox_minx", "bbox_miny", "bbox_maxx", "bbox_maxy"
#                         ]
#                         if calc_area_length:
#                             header += ["area_m2", "length_m"]
#                         writer.writerow(header)
#                         header_written = True

#                     # Stream features
#                     for feat in src:
#                         if not feat or not feat.get("geometry"):
#                             continue

#                         props = feat.get("properties", {}) or {}

#                         # Build Shapely geometry for this feature only
#                         try:
#                             g = shape(feat["geometry"])
#                         except Exception:
#                             continue

#                         # If you need to ensure validity (costly), uncomment:
#                         # try:
#                         #     g = make_valid(g)
#                         # except Exception:
#                         #     pass

#                         gtype = g.geom_type

#                         # Centroid & bbox in WGS84
#                         try:
#                             g_wgs = shp_transform(to_wgs84, g) if to_wgs84 else g
#                             cx, cy = g_wgs.centroid.x, g_wgs.centroid.y
#                             minx, miny, maxx, maxy = g_wgs.bounds
#                         except Exception:
#                             cx = cy = minx = miny = maxx = maxy = None

#                         # Area/length in projected CRS (optional)
#                         area_m2 = length_m = None
#                         if calc_area_length and to_area:
#                             try:
#                                 g_proj = shp_transform(to_area, g)
#                                 area_m2 = g_proj.area
#                                 length_m = g_proj.length
#                             except GEOSException:
#                                 pass
#                             except Exception:
#                                 pass

#                         # Geometry serialization
#                         try:
#                             wkt = g.wkt
#                         except Exception:
#                             wkt = None

#                         row = [layer] + [props.get(k) for k in attr_fields] + [gtype, wkt]
#                         if add_geojson:
#                             try:
#                                 row.append(json.dumps(feat["geometry"], ensure_ascii=False))
#                             except Exception:
#                                 row.append(None)
#                         row += [cx, cy, minx, miny, maxx, maxy]
#                         if calc_area_length:
#                             row += [area_m2, length_m]

#                         writer.writerow(row)

#     print(f"Geometries saved to {output_csv}")


def clean_up(in_csv, out_csv):

    df = pd.read_csv(in_csv, header=None)
    df = df.iloc[:, 1:-1]  
    df.to_csv(out_csv, index=False, header=False)



# -----------------------------
# Main (keep your original calls)
# -----------------------------
if __name__ == "__main__":
    # 1) Full geometry export (WKT + centroid + bbox + area/length)
    #    Tip: switch output to .csv.gz if files are huge
    # extract_geoms_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_block.gdb",
    #                        "tiger_blocks_with_geom.csv",
    #                        add_geojson=False,
    #                        calc_area_length=True,
    #                        area_crs="EPSG:6933",
    #                        explode_multi=False)

    # extract_geoms_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_roads.gdb",
    #                        "tiger_roads_with_geom.csv",
    #                        add_geojson=False,
    #                        calc_area_length=True,
    #                        area_crs="EPSG:6933",
    #                        explode_multi=False)

    # extract_geoms_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_linearwater.gdb",
    #                        "tiger_linearwater_with_geom.csv",
    #                        add_geojson=False,
    #                        calc_area_length=True,
    #                        area_crs="EPSG:6933",
    #                        explode_multi=False)

    # 2) If you only need MBRs (super light):
    # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_block.gdb",
    #                       "tiger_blocks_mbrs.csv")
    # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_roads.gdb",
    #                       "tiger_roads_mbrs.csv")
    # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_linearwater.gdb",
    #                       "tiger_linearwater_mbrs.csv")

    # clean_up("./data/real/dataset/tiger_blocks_8180866.csv", "./data/real/dataset/tiger_blocks_8180866_clean.csv")
    # clean_up("./data/real/dataset/tiger_linearwater_5668549.csv", "./data/real/dataset/tiger_linearwater_5668549_clean.csv")
    # clean_up("./data/real/dataset/tiger_roads_17813006.csv", "./data/real/dataset/tiger_roads_17813006_clean.csv")

    locate_dirty_line("./data/real/dataset/tiger_blocks_8180866.csv")
