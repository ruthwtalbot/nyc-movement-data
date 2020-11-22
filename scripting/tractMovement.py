import pandas as pd
import geopandas

stateFips = '36'
city = 'NYC'
county_list = ["071"] #["061", "085", "081", "005", "047"]
incomeFileName = "cbg_b19.csv"
movementFileName = "safegraph_Mar2020_vs_Feb2020_cbg.csv"
cityShapfilePath = "filteredCounties"
subsectionFipsFile = "subsection_fips" + city + ".csv"


def main():
	# If we've already created the income file, use it. Otherwise, create it.
	try:
	  incomeData = pd.read_csv('cleanedIncome' + city + '.csv', dtype={'census_block_group':'string'})
	except IOError:
		# Fix income data
		incomeData = pd.read_csv(incomeFileName, dtype={'census_block_group':'string'})

		# Add column for county and state FIPS to data and drop non matches
		incomeData['SFIPS'] = incomeData.census_block_group.str.slice(0,2)
		incomeData = incomeData[incomeData['SFIPS'] == stateFips]
		incomeData['CFIPS'] = incomeData.census_block_group.str.slice(2,5)
		incomeData = incomeData[incomeData['CFIPS'].isin(county_list)]
		incomeData = incomeData.loc[:, :'B19001e17']

		# Calculate percent (hardcoding these because we shouldn't ever have to change them)
		incomeData['total_under_45'] = incomeData["B19001e2"] + incomeData["B19001e3"] + incomeData["B19001e4"] + incomeData["B19001e5"] + incomeData["B19001e6"] + incomeData["B19001e7"] + incomeData["B19001e8"] + incomeData["B19001e9"]
		incomeData['per_under_45'] = incomeData['total_under_45'] / incomeData["B19001e1"]

		incomeData.to_csv('cleanedIncome' + city + '.csv', index = False)

	try:
	  moveData = pd.read_csv('cleanedMovement' + city + '.csv', dtype={'cbg_N':'string'})

	except IOError:
		# Fix movement data
		moveData = pd.read_csv(movementFileName, dtype={'cbg_N':'string'})

		# Add column for county and state FIPS to data and drop non matches
		moveData['SFIPS'] = moveData.cbg_N.str.slice(0,2)
		moveData = moveData[moveData['SFIPS'] == stateFips]

		moveData['CFIPS'] = moveData.cbg_N.str.slice(2,5)
		moveData = moveData[moveData['CFIPS'].isin(county_list)]

		# Calculate percent moved 
		moveData['per_moved'] = moveData['moved_out'] / (moveData["residing"] + moveData["moved_out"])

		moveData.to_csv('cleanedMovement' + city + '.csv', index = False)

	# Create joined data
	joinedData = pd.merge(moveData, incomeData, 'left', None, 'cbg_N', 'census_block_group')
	joinedData = joinedData[joinedData['B19001e1'] >= (joinedData['residing'] + joinedData['moved_out']) * 2]

	joinedData.to_csv('joinedData' + city + '.csv', index = False)

	# Join data with geo data
	joinedData = joinedData.rename(columns={"census_block_group": "GEOID"})
	cityGeo = geopandas.read_file(cityShapfilePath + city + '.shp', dtype={'GEOID':'string'})

	cityGeo['GEOID'] = cityGeo['GEOID'].astype('string').str.strip()
	joinedData['GEOID'] = joinedData['GEOID'].astype('string').str.strip()

	cityGeo = cityGeo.merge(joinedData, on='GEOID', how='left')
	cityGeo.to_file(city + '.geojson', driver='GeoJSON')

# Get subregion, to update, add subregion fips codes to subsection_fips.csv
def createSubRegions():
	try:
		subregionFips = pd.read_csv(subsectionFipsFile, dtype={'GEOID':'string'})
		fips_list = subregionFips.GEOID.tolist()
		subregion = cityGeo[['GEOID'].isin(fips_list)]

		subregion.to_file("subregion" + city + '.geojson', driver='GeoJSON')
		subregion.to_csv("subregion" + city + '.csv', index=False)
	except IOError:
		print ("No subregions available")

if __name__ == "__main__":
  main(sys.argv[1])

