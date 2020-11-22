
mapshaper $1 \
	-filter where='"047,061,081,085,005".indexOf(COUNTYFP) > -1' \
	-o filteredCounties.shp