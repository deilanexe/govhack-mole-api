#!flask/bin/python

from os import listdir
from os.path import isfile, join
import json, sys

sys.path.append('../support/')
import constants as c

output_json_by_language_file = open ('../data/languages_by_region.json', 'w+')
output_json_by_language = {}
output_json_by_country = {}

countries_by_region = {}
for region_name, file_name in c.regions.iteritems():
    with open ('../data/{}'.format(file_name), 'r') as fsource:
        for line in fsource:
            content = json.loads(line)
            counter = 1
            for prefix in c.ordinals:
                country = content['Diversity']["{} country of birth".format(prefix)]
                regions = []
                if country in countries_by_region:
                    regions = countries_by_region[country]
                regions.append({'region': region_name, 'position': counter})
                countries_by_region[country] = regions
                # print counter
                counter += 1
            output_json_by_country['countries'] = countries_by_region
print output_json_by_country
