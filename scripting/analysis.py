import pandas as pd
import numpy as np
import geopandas
from scipy import stats

joinedData = pd.read_csv('cityDataNYC.csv', dtype={'GEOID':'string'})
# subregion = geopandas.read_file('subregionNYC.geojson')
# joinedData = joinedData[joinedData['B19013e1'] < 100000]
print(len(joinedData))
print("overall data corr:\n", joinedData[['med_inc', 'per_moved_dif']].corr(method ='pearson'))

# subregion = subregion[['per_under_45', 'per_moved']]
# print("subregion corr:\n",  subregion.corr(method ='pearson'))


# joinedData = joinedData[(np.abs(stats.zscore(joinedData)) < 3).all(axis=1)]

# print("overall data corr:\n", joinedData[['per_under_45', 'per_moved']].corr(method ='pearson'))

