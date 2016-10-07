import pandas as pd
import requests
import json

QUERY = 'https://gisweb.bouldercolorado.gov/arcgis/rest/services/pds/AddressSearch/MapServer/1/query?where=ASR_ID+%3D+{}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'

df = pd.read_excel('input/ResidentialBuildingSizes20161003.xlsx', converters={'ASR_ID': str})
ids = df['ASR_ID']

zoning = {}
address = {}
lot_size = {}
neighborhood = {}
no_features = 0
for i in ids[:20]:
    print "Getting info for {}".format(i)
    r = requests.get(QUERY.format(i))
    j = json.loads(r.text)
    try:
        attributes = j['features'][0]['attributes']
        zoning[i] = attributes['ZONING']
        address[i] = attributes['ADDRESS']
        lot_size[i] = attributes['AREASQFT']
        neighborhood[i] = attributes['NEIGHBRHD']
    except:
        print "No features"
        no_features += 1
    print "Done"

print "{} with no features".format(no_features)

df['zoning'] = df['ASR_ID'].map(zoning)
df['address'] = df['ASR_ID'].map(address)
df['lot_size'] = df['ASR_ID'].map(lot_size)
df['neighborhood'] = df['ASR_ID'].map(neighborhood)

df.to_excel('output/MASTER.xlsx', index=False)
