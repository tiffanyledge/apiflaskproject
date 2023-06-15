from flask import Flask, render_template
import requests
from datetime import date
import random
app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get(f'https://ws-public.interpol.int/notices/v1/red?ageMax=50&ageMin=18&resultPerPage=60')
    data = response.json()
    # print(data)
    criminals = []
    #{ name: '',
    #   charges: '',
    #   pic: ''
    # }
    entity_id = []
    
    for x in range(60):
        #print(data['_embedded']['notices'][x]['forename'])
        criminal = { 
            'pic': '',
            'name': '',
            'charges': ''
        }
        criminal['name'] = data['_embedded']['notices'][x]['forename']
        #print(data['_links']['self']['href'])
        response = requests.get(data['_embedded']['notices'][x]['_links']['self']['href'])
        #print(response.json())
        criminal['charges'] = response.json()['arrest_warrants'][0]['charge']
        response1 = requests.get(data['_embedded']['notices'][x]['_links']['images']['href'])
        
        criminal['pic'] = data['_embedded']['notices'][x]['entity_id']
        criminal['id'] = response1.json()['_embedded']['notices'][x]['_links']['images']['href']
        criminal['dob'] = data['_embedded']['notices'][x]['date_of_birth']
        criminals.append(criminal)

        print(criminals)

    
        # print(data['_link']['self'])
        # print(data['arrest_warrants']['charge'][x])

    return render_template('index.html' , criminals = criminals)

def yellow_notice():
    response2 = requests.get(f'https://ws-public.interpol.int/notices/v1/yellow?ageMax=50&ageMin=18&page=1&resultPerPage=60')
    data2 = response2.json
    missing = []

    for x in range (60):
        missin = {
            'pic': '',
            'name':'',
            'missing-date': ''
        }

        missin['name'] = data2['_embedded']['notice'][x]['forename']

        missing.append(missin)

        print(missing)

@app.route('/home')
def home():
    return render_template('home_page.html')

@app.route('/')
def wanted():
    return render_template('index.html')

@app.route('/missing_ppl')
def missing():
    return render_template('second.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0')
