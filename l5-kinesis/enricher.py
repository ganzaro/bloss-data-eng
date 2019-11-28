import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from shapely.ops import nearest_points
import numpy as np

from scipy.spatial import cKDTree
from shapely.geometry import Point


points = gpd.read_file('hotosm_gha_points_of_interest_points_shp/hotosm_gha_points_of_interest_points.shp')

def ckdnearest(gdA, gdB, k=2):
    """Quickly find the k nearest points close to another
    
    :param gdA: geopandas dataframe A
    :param gdB: geopandas dataframe B
    :param k: number of nearest neighbours to find
    
    :returns: joined geopandas dataframe with distance computed 
    in the last column
    """
    
    nA = np.array(list(zip(gdA.geometry.x, gdA.geometry.y)))
    nB = np.array(list(zip(gdB.geometry.x, gdB.geometry.y)))
    
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=k)
    
    gdf = pd.concat(
        [gdA, gdB.loc[idx, gdB.columns != 'geometry'].reset_index(), pd.Series(dist, name='dist')], 
        axis=1
    )

    return gdf


def join_to_poi(df):
    
    # convert the df into a geopandas df
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.lon, df.lat)
    )
    
    # drop all null coordinates else burn!
    gdf = gdf[~gdf.lat.isna()]
    
    return ckdnearest(gdf, points)


def compute_metrics(gdf):
    pass