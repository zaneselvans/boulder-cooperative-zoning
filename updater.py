import pandas as pd
import requests
import json
from datetime import datetime

QUERY = 'https://gisweb.bouldercolorado.gov/arcgis/rest/services/pds/{}/MapServer/1/query?where=ASR_ID+%3D+{}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'

file_name = 'ResidentialBuildingSizes20161003.xlsx'

class ZoningInfo:
  def __init__(self):
    self.start_time = datetime.now()
    self.df = pd.read_excel("input/{}".format(file_name), converters={'ASR_ID': str})
    self.ids = self.df['ASR_ID']
    self.zoning = {}
    self.address = {}
    self.lot_size = {}
    self.neighborhood = {}
    self.rental_license_number = {}

  def update(self):
    error_ids = []

    for i in self.ids[:20]:
      try:
        r = requests.get(QUERY.format("AddressSearch", i))
        attributes = json.loads(r.text)['features'][0]['attributes']
        self.zoning[i] =       attributes['ZONING']
        self.address[i] =      attributes['ADDRESS']
        self.lot_size[i] =     attributes['AREASQFT']
        self.neighborhood[i] = attributes['NEIGHBRHD']
      except (KeyError, IndexError):
        error_ids.append(i)
      else:
        try:
          r = requests.get(QUERY.format("RentalInquiry", i))
          attributes = json.loads(r.text)['features'][0]['attributes']
          self.rental_license_number[i] = attributes['PROP_NO']
          self.rental_license_number[i] = attributes['PROP_NO']
        except (KeyError, IndexError):
          None
        print "{:10} {:30} {:10} {}".format(
          i,
          self.address[i],
          self.zoning[i],
          "RENTAL" if i in self.rental_license_number else ""
        )
    print "\nError ASR_ID's: {}\n".format(error_ids)
    print "Done getting all zones!"

  def write(self):
    out_file_name = 'output/output.xlsx'
    print "Writing them out to {}...".format(out_file_name)
    self.df['zoning'] =         self.df['ASR_ID'].map(self.zoning)
    self.df['address'] =        self.df['ASR_ID'].map(self.address)
    self.df['lot_size'] =       self.df['ASR_ID'].map(self.lot_size)
    self.df['neighborhood'] =   self.df['ASR_ID'].map(self.neighborhood)
    self.df['rental_license'] = self.df['ASR_ID'].map(self.rental_license_number)

    self.df.to_excel(out_file_name, index=False)
    print "Done writing to {}!".format(out_file_name)
    print "Started at {} and ended at {}".format(self.start_time.isoformat(), datetime.now().isoformat())


zoning_info = ZoningInfo()
zoning_info.update()
zoning_info.write()
