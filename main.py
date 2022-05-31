import csv
import os

# Load the Component library to process the config file
from keboola.component import CommonInterface

# Rely on the KBC_DATADIR environment variable by default,
# alternatively provide a data folder path in the constructor (CommonInterface('data'))
ci = CommonInterface()
params = ci.configuration.parameters

print("Hello world from python")

csvlt = '\n'
csvdel = ','
csvquo = '"'

# get input table definition by name
in_table = ci.get_input_table_definition_by_name('source.csv')

with open(in_table.full_path, mode='rt', encoding='utf-8') as in_file, \
        open(os.path.join(ci.tables_out_path, 'odd.csv'), mode='wt', encoding='utf-8') as odd_file, \
        open(os.path.join(ci.tables_out_path, 'even.csv'), mode='wt', encoding='utf-8') as even_file:
    lazy_lines = (line.replace('\0', '') for line in in_file)
    reader = csv.DictReader(lazy_lines, lineterminator=csvlt, delimiter=csvdel,
                            quotechar=csvquo)

    even_writer = csv.DictWriter(odd_file, fieldnames=reader.fieldnames,
                                 lineterminator=csvlt, delimiter=csvdel,
                                 quotechar=csvquo)
    even_writer.writeheader()

    odd_writer = csv.DictWriter(even_file, fieldnames=reader.fieldnames,
                                lineterminator=csvlt, delimiter=csvdel,
                                quotechar=csvquo)
    odd_writer.writeheader()
    i = 0
    for row in reader:
        if i % 2 == 0:
            even_writer.writerow(row)
        else:
            newRow = {}
            for key in reader.fieldnames:
                newRow[key] = row[key] + ''.join([params['sound']] * params['repeat'])
            odd_writer.writerow(newRow)
        i = i + 1