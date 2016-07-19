import urllib2
import StringIO
import gzip
import pandas as pd
import re

base_filesystem = '/Users/martin/Documents/dev/mabit/histo/'
base_url = 'http://api.bitcoincharts.com/v1/csv/'
filename = "bitfinexUSD.csv "

def downloadAndDecompress(url, uncompress=False,local_path = '/Users/martin/Documents/dev/mabit/histo/'):
    print("Dowloading " + url)
    response = urllib2.urlopen(url)
    if uncompress:
        compressedFile = StringIO.StringIO(response.read())
        print("Uncompressing data")
        decompressedFile = gzip.GzipFile(fileobj=compressedFile)
        filename = local_path + url.split('/')[-1][:-3]
        content = decompressedFile.read()
    else:
        filename =local_path + url.split('/')[-1]
        content = response.read()

    with open(filename, 'w') as outfile:
        print("saving " + filename)
        outfile.write(content)

def getListofFile(url):
    response = urllib2.urlopen(url).read()
    pattern = '<a href="(.*?csv\.gz)"'
    return re.findall(pattern, response)
