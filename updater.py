import pandas as pd
import requests
import json
from datetime import datetime

QUERY = 'https://gisweb.bouldercolorado.gov/arcgis/rest/services/pds/{}/MapServer/1/query?where=ASR_ID+IN+({})&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'

file_name = 'ResidentialBuildingSizes20161003.xlsx'

def chunks(l, n):
  n = max(1, n)
  return (l[i:i+n] for i in xrange(0, len(l), n))

class ZoningInfo:
  def __init__(self):
    self.start_time = datetime.now()
    self.df = pd.read_excel(file_name, converters={'ASR_ID': str})
    self.ids = self.df['ASR_ID']
    self.zoning = {}
    self.address = {}
    self.lot_size = {}
    self.neighborhood = {}
    self.rental_license_number = {}

  def update(self):
    error_ids = []
    number_of_ids = len(self.ids)

    # To test out part of data set, do something like:
    #     for index, asr_id in enumerate(self.ids[:20]):
    # And this to process all the data (it will take a long time)
    #     for index, asr_id in enumerate(self.ids[:20]):

    chunk_size = 199

    chunkz = chunks(self.ids, chunk_size)

    for chunk_number, chunk in enumerate(chunkz):
      r = requests.get(QUERY.format("AddressSearch", ",".join(chunk)))
      for record_number, record in enumerate(json.loads(r.text)['features']):
        try:
          attributes = record['attributes']
          asr_id = attributes['ASR_ID']
          self.zoning[asr_id] =       attributes['ZONING']
          self.address[asr_id] =      attributes['ADDRESS']
          self.lot_size[asr_id] =     attributes['AREASQFT']
          self.neighborhood[asr_id] = attributes['NEIGHBRHD']
        except (KeyError, IndexError):
          error_ids.append(asr_id)
        else:
          print "{:.6f}% {:10} {:30} {:10} {}".format(
            ((chunk_size * chunk_number) + record_number) / float(number_of_ids),
            asr_id,
            self.address[asr_id],
            self.zoning[asr_id],
            "RENTAL" if asr_id in self.rental_license_number else ""
          )

      r = requests.get(QUERY.format("RentalInquiry", ",".join(chunk)))
      for record_number, record in enumerate(json.loads(r.text)['features']):
        try:
          attributes = record['attribues']
          self.rental_license_number[asr_id] = attributes['PROP_NO']
        except (KeyError, IndexError):
          None
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
