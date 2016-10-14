# Install Notes

## Rental Info Scraping
```
pip install cython pandas xlrd lxml openpyxl
```

(If you're on OS X, and have homebrew installed, `brew install python`)

If you get an error when writing the file that says:
```
 UserWarning: The installed version of lxml is too old to be used with openpyxl
```

Then you'll have to run `pip install lxml --upgrade`

If *that* gives you an error:
```
Could not find function xmlCheckVersion in library libxml2. Is libxml2
installed?

Perhaps try: xcode-select --install
```

You'll have to run:
```
brew install libxml2
brew install libxslt
brew link libxml2 --force
brew link libxslt --force
```

Then run `pip install lxml --upgrade` again. Then you should be abl


## Importing to SQLite

From command line:
```
sqlite3 output/db.sqlite3
```


Then, inside the `sqlite3` console, type:
```
.read import-from-csv.sql
```

This *drops* existing `properties` table and imports from `output/output.csv` into
a new `properties` tables.


## Getting all ID's for city propertyies
URL:
https://maps.bouldercolorado.gov/arcgis/rest/services/pds/AddressSearch/MapServer/0/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=ASR_ID&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=html
