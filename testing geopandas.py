import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

fp = "World_Countries_Generalized.shp"
map_df = gpd.read_file(fp)
map_df.head()

map_df.plot()
