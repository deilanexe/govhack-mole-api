#!flask/bin/python
from flask import Flask, request, jsonify
import json, sys
from support import constants as c

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/region/getRegion', methods=["GET"])
def find_region_details():
    region = c.regions[request.args.get('query')]
    print region
    try:
        with open ('data/{}'.format(region, 'r')) as region_file:
            for line in region_file:
                response = json.loads(line)
            return jsonify (response)
    except:
        return jsonify({'error': 'region not found'})

@app.route('/region/getServices', methods=["GET"])
def find_region_services():
    region = c.regions[request.args.get('query')]
    print region
    try:
        with open ('data/{}'.format(region, 'r')) as region_file:
            for line in region_file:
                response = json.loads(line)
            services = response['Services']
            return jsonify (services)
    except:
        return jsonify({'error': 'region not found'})

@app.route('/region/getHospitals', methods=["GET"])
def find_region_hospitals():
    region = c.regions[request.args.get('query')]
    print region
    try:
        with open ('data/{}'.format(region, 'r')) as region_file:
            for line in region_file:
                response = json.loads(line)
                services = {
                    'nearest_emergency_hospital': response['Hospital']['Nearest public hospital with emergency department'],
                    'nearest_maternity_hospital': response['Hospital']['Nearest public hospital with maternity services'],
                    'nearest_public_hospital': response['Hospital']['Nearest Public Hospital']
                }
            return jsonify (services)
    except:
        return jsonify({'error': 'region not found'})

@app.route('/language/getRegionsWithLanguage', methods=["GET"])
def find_regions_with_lang():
    return jsonify ({'error': 'endpoint not implemented'})

@app.route('/language/getLanguagesInRegion', methods=['GET'])
def find_languages_in_region():
    region = c.regions[request.args.get('query')]
    print region
    try:
        with open ('data/{}'.format(region, 'r')) as region_file:
            for line in region_file:
                content = json.loads(line)
                diversity = content['Diversity']
                components = []
                for prefix in c.ordinals:
                    components.append({
                        'language': diversity['{} language spoken'.format(prefix)],
                        'speakers': diversity['{} language spoken, persons'.format(prefix)],
                        'perc': diversity['{} language spoken, %'.format(prefix)]
                        })
                response = {
                    'Top languages spoken in region': [
                        components
                    ]
                }
            return jsonify (response)
    except:
        print sys.exc_info()
        return jsonify({'error': 'region not found'})

if __name__ == '__main__':
    app.run(debug=True)
