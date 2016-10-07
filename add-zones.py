import pandas as pd
import requests
import json

QUERY = 'https://gisweb.bouldercolorado.gov/arcgis/rest/services/pds/AddressSearch/MapServer/1/query?where=ASR_ID+%3D+{}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'


class ZoningInfo:
  def __init__(self):
    self.df = pd.read_excel('input/ResidentialBuildingSizes20161003.xlsx', converters={'ASR_ID': str})
    self.ids = self.df['ASR_ID']
    self.zoning = {}
    self.address = {}
    self.lot_size = {}
    self.neighborhood = {}

  def update(self):
    no_features = 0

    for i in self.ids[:20]:
        print "Getting info for {}".format(i)
        r = requests.get(QUERY.format(i))
        j = json.loads(r.text)
        try:
            attributes = j['features'][0]['attributes']
            self.zoning[i] = attributes['ZONING']
            self.address[i] = attributes['ADDRESS']
            self.lot_size[i] = attributes['AREASQFT']
            self.neighborhood[i] = attributes['NEIGHBRHD']
        except IndexError:
            print "No features for {}".format(i)
            no_features += 1
        print "Done!\n"

  def write(self):
    self.df['zoning'] =       self.df['ASR_ID'].map(self.zoning)
    self.df['address'] =      self.df['ASR_ID'].map(self.address)
    self.df['lot_size'] =     self.df['ASR_ID'].map(self.lot_size)
    self.df['neighborhood'] = self.df['ASR_ID'].map(self.neighborhood)

    self.df.to_excel('output/with_zones.xlsx', index=False)

zoning_info = ZoningInfo()
zoning_info.update()
zoning_info.write()
