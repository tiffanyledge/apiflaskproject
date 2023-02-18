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
        response1 = requests.get(data['_embedded']['notices'][x]['_links']['thumbnail']['href'])
        
        criminal['pic'] = data['_embedded']['notices'][x]['entity_id']
        criminal['id'] = data['_embedded']['notices'][x]['_links']['thumbnail']['href']
        criminal['dob'] = data['_embedded']['notices'][x]['date_of_birth']
        criminals.append(criminal)

        print(criminals)

    
        # print(data['_link']['self'])
        # print(data['arrest_warrants']['charge'][x])

    return render_template('index.html' , criminals = criminals)

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0')
