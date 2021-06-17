#
# Flask web app to run scrapy spider from web interface
#

# packages
from flask import Flask
from flask import render_template
from flask import request
import json
import subprocess

# create app instance
app = Flask(__name__)

# base route
   
# run scraper route
@app.route('/run', methods=['GET'])
def run():
    # extract user input parameters
    
    # settings content

    

  
   
 
    process = subprocess.Popen('python3 scraper.py', shell=True)
    process.wait()
    
    # output content
    output = ''
    
    # load scraper output
    with open('wellness.jsonl', 'r') as f:
        for line in f.read():
            output += line
    
    # parse content
    output = [json.loads(item + '\n}') for item in output.split('}\n')[0:-1]]
    
    return {'data': output}

# main driver
if __name__ == '__main__':
    # run app
    app.run(debug=True, threaded=True)