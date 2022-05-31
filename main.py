import csv
import os
import requests
import json

# Load the Component library to process the config file
from keboola.component import CommonInterface

# Rely on the KBC_DATADIR environment variable by default,
# alternatively provide a data folder path in the constructor (CommonInterface('data'))
ci = CommonInterface()
params = ci.configuration.parameters

api_url = "https://yfapi.net/v8/finance/spark?interval="+params['interval']+"&range="+params['range']+"&symbols="+params['symbol']
headers = {"X-API-KEY": params['apikey']}
response = requests.get(api_url,headers=headers)
tickers = response.json()

#for testing pusposes so we don't go over api limit
# f = open('/data/in/files/data.json')
# tickers = json.load(f)

timestamps = tickers['TSLA']['timestamp']
closes = tickers['TSLA']['close']

#print(tickers['TSLA']['timestamp'])


csvlt = '\n'
csvdel = ','
csvquo = '"'

# get input table definition by name
#in_table = ci.get_input_table_definition_by_name('source.csv')

with open(os.path.join(ci.tables_out_path, 'ticker.csv'), mode='wt', encoding='utf-8') as out_file:


    out_writer = csv.DictWriter(out_file, fieldnames=["timestamp","close"],
                                 lineterminator=csvlt, delimiter=csvdel,
                                 quotechar=csvquo)
    out_writer.writeheader()

    i = 0
    for timestamp in timestamps:
        newRow = {}
        newRow["timestamp"] = timestamp
        newRow["close"] = closes[i]
        out_writer.writerow(newRow)
        i = i + 1

#Backup down here, TODO: delete
# print("Hello world from python")
#
# csvlt = '\n'
# csvdel = ','
# csvquo = '"'
#
# # get input table definition by name
# in_table = ci.get_input_table_definition_by_name('source.csv')
#
# with open(in_table.full_path, mode='rt', encoding='utf-8') as in_file, \
#         open(os.path.join(ci.tables_out_path, 'odd.csv'), mode='wt', encoding='utf-8') as odd_file, \
#         open(os.path.join(ci.tables_out_path, 'even.csv'), mode='wt', encoding='utf-8') as even_file:
#     lazy_lines = (line.replace('\0', '') for line in in_file)
#     reader = csv.DictReader(lazy_lines, lineterminator=csvlt, delimiter=csvdel,
#                             quotechar=csvquo)
#
# even_writer = csv.DictWriter(odd_file, fieldnames=reader.fieldnames,
#                              lineterminator=csvlt, delimiter=csvdel,
#                              quotechar=csvquo)
#     even_writer.writeheader()
#
#     odd_writer = csv.DictWriter(even_file, fieldnames=reader.fieldnames,
#                                 lineterminator=csvlt, delimiter=csvdel,
#                                 quotechar=csvquo)
#     odd_writer.writeheader()
#     i = 0
#     for row in reader:
#         if i % 2 == 0:
#             even_writer.writerow(row)
#         else:
#             newRow = {}
#             for key in reader.fieldnames:
#                 newRow[key] = row[key] + ''.join([params['sound']] * params['repeat'])
#             odd_writer.writerow(newRow)
#         i = i + 1