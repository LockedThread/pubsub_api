from flask import Flask, render_template, request, redirect, jsonify, abort
from flask.json import jsonify
import requests
import psycopg2
import json
import connect_db
app = Flask(__name__, static_url_path='/static')
@app.route("/onsale/", methods = ["POST", "GET"])
def onsale_data():
    connection = connect_db.connect()   
    cur = connection.cursor()

    query = "SELECT * FROM {table}"
    cur.execute(query.format(table = connect_db.get_table()))
    sub_name = []
    last_on_sale = []
    on_sale = []
    price = []
    image = []
    records = cur.fetchall()
    for i in range(len(records)):
        sub_name.append(records[i][0])
        last_on_sale.append(records[i][1])
        on_sale.append(records[i][2])
        price.append(records[i][3])
        image.append(records[i][4])
    print(sub_name)
    data = {}
    print(last_on_sale)

    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    for i in range(len(records)):
        data["All_subs".lower()].append({
            "name": sub_name[i],
            "on_sale": on_sale[i],
            "image": image[i],
            "last_on_sale": last_on_sale[i],
            "price": price[i]
            }) 
        
    return jsonify(data["All_subs".lower()])
@app.route("/allsubs/", methods =["POST", "GET"])
def all_names():

    connection = connect_db.connect()   
    cur = connection.cursor()

    query = "SELECT pubsub_name FROM {table} ORDER BY on_sale"
    cur.execute(query.format(table = connect_db.get_table()))
    
    records = cur.fetchall()

    data = {}

    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    for sub in records:
        data["All_subs".lower()].append({"name": sub[0]}) 
        
    return jsonify(data["All_subs".lower()])

@app.route("/subs/", methods =["POST", "GET"])    
def sub():
    if request.method == "GET":
            sub_name = request.args.get("name")
            if(sub_name == ""):
                sub = random_sub()
                return sub
            else:
                sub = sub_runner(sub_name)
                return sub

def random_sub():
    try:
        connection = connect_db.connect()
        cur = connection.cursor()
        # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
        command = "SELECT * FROM {table} ORDER BY random()"
        query = cur.execute(command.format(table = connect_db.get_table()))
        
        # Fetches us all the rows so we can grab data from each
        records = cur.fetchall()
        for row in records:
            subname = row[0]
            last_on_sale = row[1]
            on_sale = row[2]
            price = row[3]
            image = row[4]
                        
        # Creates a dictionary
        data = {}

        # Creates a primary catagory
        data[subname.lower()] = []

        # Create a default JSON structure
        data[subname.lower()].append(
        {
            "sub_name": subname.lower(),
            "last_sale": last_on_sale,
            "status": on_sale,
            "price": price,
            "image": image
        })
                    
                    
        sub_info = json.dumps(data[subname.lower()], indent = 2)
        return sub_info
    except:
        return abort(404)

def sub_runner(subname):
    try:
        connection = connect_db.connect()
        cur = connection.cursor()
        # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
        try:
            command = "SELECT * FROM {table} WHERE pubsub_name = '{name}' ORDER BY dates DESC LIMIT 1"
            query = cur.execute(command.format(table = connect_db.get_table(), name = subname))
        except:
            return "Unfortunately, we do not have deal data available on " + subname.replace("-", " ") + " sub at this time.\nOur current offers is the boar-head-jerk-turkey-and-gouda sub"
        
        # Fetches us all the rows so we can grab data from each
        records = cur.fetchall()
        for row in records:
            last_on_sale = row[1]
            on_sale = row[2]
            price = row[3]
            image = row[4]
                        
        # Creates a dictionary
        data = {}

        # Creates a primary catagory
        data[subname.lower()] = []

        # Create a default JSON structure
        data[subname.lower()].append(
        {
            "sub_name": subname.lower(),
            "last_sale": last_on_sale,
            "status": on_sale,
            "price": price,
            "image": image
        })
                        
        sub_info = json.dumps(data[subname.lower()], indent = 2)
        return sub_info
    except:
        return abort(404)
                
               
@app.route("/", methods =["POST", "GET"])
def index():
        return render_template("index.html")
        
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)