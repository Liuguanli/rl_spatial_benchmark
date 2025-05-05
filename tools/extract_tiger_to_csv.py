import zipfile
import os
import tempfile
import glob
import fiona
from shapely.geometry import shape
import pandas as pd


def read_place_shapefile(shp_path: str) -> pd.DataFrame:
    """
    Read a PLACE shapefile and return attributes + centroid + bounding box
    """
    features = []
    with fiona.open(shp_path, 'r') as src:
        for feature in src:
            geom = shape(feature['geometry'])
            props = dict(feature['properties'])
            props['centroid_lon'] = geom.centroid.x
            props['centroid_lat'] = geom.centroid.y
            props['bbox_minx'], props['bbox_miny'], props['bbox_maxx'], props['bbox_maxy'] = geom.bounds
            features.append(props)
    return pd.DataFrame(features)


def read_landmark_shapefile(shp_path: str) -> pd.DataFrame:
    """
    Read shapefile and return attributes + centroid + bounding box
    """
    features = []
    with fiona.open(shp_path, 'r') as src:
        for feature in src:
            geom = shape(feature['geometry'])
            props = dict(feature['properties'])
            props['centroid_lon'] = geom.centroid.x
            props['centroid_lat'] = geom.centroid.y
            props['bbox_minx'], props['bbox_miny'], props['bbox_maxx'], props['bbox_maxy'] = geom.bounds
            features.append(props)
    return pd.DataFrame(features)

def extract_and_process_zip(zip_path: str) -> pd.DataFrame:
    """
    Unzip a ZIP file containing a shapefile and return parsed data
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmpdir)
        shp_files = glob.glob(os.path.join(tmpdir, "*.shp"))
        if not shp_files:
            return pd.DataFrame()  # Skip if no .shp
        df = read_landmark_shapefile(shp_files[0])
        df["source_file"] = os.path.basename(zip_path)
        return df

def batch_process_zip_folder(folder_path: str) -> pd.DataFrame:
    """
    Process all ZIP shapefiles in a folder and return combined results
    """
    all_dfs = []
    for zip_file in glob.glob(os.path.join(folder_path, "*.zip")):
        print(f"Processing {zip_file}")
        df = extract_and_process_zip(zip_file)
        if not df.empty:
            all_dfs.append(df)
        # break
    return pd.concat(all_dfs, ignore_index=True)


import geopandas as gpd
import fiona
import os
import pandas as pd

def extract_mbrs_from_gdb(gdb_path: str, output_csv: str):
    """
    Extract MBR (minx, miny, maxx, maxy) for all features in all layers of a .gdb
    and write to CSV.
    """
    layers = fiona.listlayers(gdb_path)
    print(f"Found {len(layers)} layers in GDB.")

    all_records = []

    for layer in layers:
        print(f"Reading layer: {layer}")
        gdf = gpd.read_file(gdb_path, layer=layer)

        if gdf.empty:
            continue

        # Extract MBR (bounding box) for each geometry
        bounds = gdf.bounds
        bounds["layer"] = layer
        all_records.append(bounds)

    # Combine and export
    if all_records:
        df_all = pd.concat(all_records, ignore_index=True)
        df_all.columns = ["minx", "miny", "maxx", "maxy", "layer"]
        df_all.to_csv(output_csv, index=True, index_label="id")
        print(f"MBRs saved to {output_csv}")
    else:
        print("No geometries found.")



if __name__ == "__main__":
    # df_all = batch_process_zip_folder("../tiger/places")
    # df_all.to_csv("../tiger/places/all_places.csv", index=True, index_label="id")

    # # Assuming all .zip files are under ./shapefiles/
    # df_all = batch_process_zip_folder("../tiger/landmarks")
    # df_all.to_csv("../tiger/landmarks/all_landmarks.csv", index=True, index_label="id")
    # https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-geodatabase-file.html
    # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_linearwater.gdb", "tiger_linearwater_mbrs.csv")
    # extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_roads.gdb", "tiger_roads_mbrs.csv")
    extract_mbrs_from_gdb("../../../../../Downloads/tlgdb_2024_a_us_block.gdb", "tiger_blocks_mbrs.csv")