import pandas as pd


def main():
  movementFileName = "safegraph_Mar2020_vs_Feb2020_cbg.csv"
  previousMovementFileName = "safegraph_Feb2020_vs_Jan2020_cbg.csv"

  # Import movement data
  moveData = pd.read_csv(movementFileName, dtype={'cbg_N':'string'})

  # Add column for county and state FIPS to data and drop non matches
  moveData['countyFips'] = moveData.cbg_N.str.slice(0,5)

  # Do previous month for comparison
  pmoveData = pd.read_csv(previousMovementFileName, dtype={'cbg_N':'string'})

  # Add column for county and state FIPS to data and drop non matches
  pmoveData['countyFips'] = pmoveData.cbg_N.str.slice(0,5)

  joinedData = pd.merge(moveData, pmoveData, 'left', None, 'cbg_N', 'cbg_N')

  # Create joined data
  joinedData['per_movedF2M'] = joinedData['moved_out_x'] / (joinedData["residing_x"] + joinedData["moved_out_x"])
  joinedData['per_movedJ2F'] = joinedData['moved_out_y'] / (joinedData["residing_y"] + joinedData["moved_out_y"])
  joinedData['per_moved_dif'] = joinedData['per_movedF2M'] - joinedData["per_movedJ2F"]

  # Groub by fips
  joinedData = joinedData.groupby('countyFips_x', as_index=False).agg({'per_moved_dif': 'median', 'residing_x': 'sum'})
  joinedData = joinedData[joinedData["residing_x"] > 10000]

  joinedData = joinedData.sort_values(by='per_moved_dif', ascending=False)

  joinedData.to_csv('Counties/joinedCountyData.csv', index = False)


if __name__ == "__main__":
  main()


