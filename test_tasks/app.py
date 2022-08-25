from flask import Flask, jsonify, request, Response
import json
from parser_local import ROOT_OF_DATABASE
from os import path

app = Flask(__name__)
#Turn off ASCII to use Гб in memory_size
app.config['JSON_AS_ASCII'] = False

@app.route('/smartphones', methods=['GET'])
def hello_world():
    #Checking if DB is exists
    if path.isfile(ROOT_OF_DATABASE):
        
        db = json.load(open(ROOT_OF_DATABASE, encoding='utf-8'))
        price = request.args.get('price')
        
        if price != None:
        
            #Filtering db to get exact match of price
            try:
                exact_matched_products = list(filter(lambda k: k['price']==int(price), db))
                return exact_matched_products
            except ValueError:
                #Catching error when trying to pass price with characters
                return Response("You have to pass price in INT format", status=400)
                
        else:
            return Response("You have to pass price argument", status=400)
    else:
        return Response("Couldn't find database of smartphones. Before attempting current endpoint create the smartphones.json database", status=404)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")