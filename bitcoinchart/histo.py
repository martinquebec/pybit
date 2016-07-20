import urllib2
import StringIO
import gzip
import pandas as pd
import re
import getpass

local_histo_archive = '/Users/' + getpass.getuser() + '/Documents/dev/mabit/histo/'
print 'Using ' + local_histo_archive + ' as local archive path'

base_url = 'http://api.bitcoincharts.com/v1/csv/'
filename = "bitfinexUSD.csv "

def downloadAndDecompress(url, uncompress=False,local_path = local_histo_archive):
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


def get_df_histo(name,local_path = '/Users/apple/Documents/dev/mabit/histo/'):
    filename = local_path + name + ".csv.gz"
    df = pd.read_csv(filename,compression='gzip',header=None,names=['date','price','qty'])
    return df