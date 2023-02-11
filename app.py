from flask import Flask, render_template
import requests
from datetime import date
import random
app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get(f'https://ws-public.interpol.int/notices/v1/red?ageMax=50&ageMin=18&resultPerPage=10')
    data = response.json()
    # print(data)
    criminals = []
    #{ name: '',
    #   charges: '',
    #   pic: ''
    # }

    for x in range(10):
        #print(data['_embedded']['notices'][x]['forename'])
        criminal = { 
            'name': '',
            'charges': '',
            'pic': ''
        }
        criminal['name'] = data['_embedded']['notices'][x]['forename']
        #print(data['_links']['self']['href'])
        response = requests.get(data['_embedded']['notices'][x]['_links']['self']['href'])
        #print(response.json())
        criminal['charges'] = response.json()['arrest_warrants'][0]['charge']
        criminals.append(criminal)
        # print(criminals)

    
        # print(data['_link']['self'])
        # print(data['arrest_warrants']['charge'][x])

    return render_template('index.html' , criminals = criminals)

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0')
