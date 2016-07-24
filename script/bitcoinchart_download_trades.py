import bitcoinchart.bitcoinchart as histo


base_url = 'http://api.bitcoincharts.com/v1/csv/'
filename = "anxhkHKD.csv.gz"

#histo.downloadAndDecompress(base_url+filename,uncompress=True)
print(histo.getListofFile(base_url))

for filename in histo.getListofFile(base_url):
    histo.downloadAndDecompress(base_url + filename)
