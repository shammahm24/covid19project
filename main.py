#Tanyaradzwa Matasva
#Assignment 10
#Python for Data Science
#University of Bridgeport
from contextlib import closing

import pandas as pd
import numpy as np
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
import os
import dbconnect as db

#clear up stored graphs
if os.path.exists("./static/confirmed.png"):
  os.remove("./static/confirmed.png")
else:
  print("The file does not exist")

if os.path.exists("./static/deaths.png"):
  os.remove("./static/deaths.png")
else:
  print("The file does not exist")

if os.path.exists("./static/recovered.png"):
  os.remove("./static/recovered.png")
else:
  print("The file does not exist")

desired_width=320

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',None)
pd.set_option('precision', 0)


country_general_df=pd.read_csv("covid_19_data.csv",keep_default_na=False)
#print(country_general_df.isnull().values.any())
country_general_clean_df=country_general_df.dropna()
#print(country_general_clean_df)
groupedByCountry=country_general_clean_df.groupby(["Country/Region","Confirmed","Deaths","Recovered"]).count().reset_index()
groupedByCountry.columns.values[0]='Country'
groupedByCountry.drop_duplicates(subset="Country",keep="last", inplace=True)
groupedByCountry.sort_values(by="Confirmed",ascending=False,inplace=True)

print(groupedByCountry.head(50))

groupedByCountry.head(10).plot.bar(x='Country', y='Confirmed', rot=90,color='orange')
plt.savefig("./static/confirmed.png")


plt.figure(1)
groupedByCountry.sort_values(by="Deaths",ascending=False,inplace=True)
groupedByCountry.head(10).plot.bar(x='Country', y='Deaths', rot=90,color='mediumvioletred')
plt.savefig("./static/deaths.png")

plt.figure(2)
groupedByCountry.sort_values(by="Recovered",ascending=False,inplace=True)
groupedByCountry.head(10).plot.bar(x='Country', y='Recovered', rot=90,color='limegreen')
plt.savefig("./static/recovered.png")

#plt.show()


#run query function
def runQuery(query):
    groupedByCountry.query(query,inplace=True)
    print(groupedByCountry)
    queryData = [(country, confirmed, deaths, recovered) for country, confirmed, deaths, recovered in
                     zip(groupedByCountry['Country'],
                         groupedByCountry['Confirmed'].astype(int), groupedByCountry['Deaths'].astype(int),
                         groupedByCountry['Recovered'].astype(int))]
    return queryData

groupedByCountry.sort_values(by="Confirmed",ascending=False,inplace=True)

mainTableData=[(country,confirmed,deaths,recovered) for country,confirmed,deaths,recovered in zip(groupedByCountry['Country'],
                            groupedByCountry['Confirmed'].astype(int),groupedByCountry['Deaths'].astype(int),
                            groupedByCountry['Recovered'].astype(int))]

from flask import Flask, render_template, request,redirect,url_for

loggedIn=False
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def getIndex():
    if request.method=='GET':
        print("This is an incoming get request ")
        options =db.getQueries()
        print(options)

        return render_template('dashboard.html',data=mainTableData,options=options)

    if request.method=='POST':
        query = request.form['queries']
        queryData=runQuery(query)
        options=db.getQueries()
        return render_template('dashboard.html',data=mainTableData,options=options,queryData=queryData)

@app.route('/admin',methods=['POST','GET'])
def getAdmin():
    global loggedIn

    if request.method=='GET':
        queryData =db.getQueries()
        if loggedIn:
            return render_template("admin.html",queryData=queryData)
        else:
            return render_template("login.html")

    if request.method=='POST':
        newQuery=request.form['newquery']
        db.addQuery(newQuery)
        return redirect('/admin')

@app.route('/login',methods=['POST','GET'])
def login():
    global loggedIn
    if request.method=='POST':
        uname=request.form['username']
        pword=request.form['password']
        result=db.authenticate(uname,pword)

        if result:
            loggedIn=True
            return redirect("/admin")
        else:
            return redirect("/admin")

@app.route('/newAdmin',methods=['POST','GET'])
def addAdmin():
    if request.method=='POST':
        uname=request.form['username']
        pword=request.form['password']
        db.addAdmin(uname,pword)
        return redirect("/admin")




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)