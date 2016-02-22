# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask import request
from pymongo import MongoClient
import os


# create the application object
app = Flask(__name__)

# Providing the details for mongoclient and database
client = MongoClient('localhost',27017)
db = client.anupam


# config
app.secret_key = 'my precious'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    return render_template('index.html')  # render a template
    # return "Hello, World!"  # return a string


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


#mongodb function to fetch data
@app.route('/todo')
@login_required
def todo():
   _items = db.movie.find()
   items = [item for item in _items]  
   return render_template('todo.html', items=items)


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            #flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# for highcharts
# Put the  data in xAxis category and you can change the color with the "color" option set to the color code
@app.route('/graph')
@login_required
def index(chartID = 'chart_ID', chart_type = 'area', chart_height = 900):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,"zoomType" : 'x'}
    series = [{"name": "DEFECTS FOUND", "data": [0,12,0,26,11,22,13,5,13,12,13,7,4,4,2,8,12,2,2,5,3,15],"color" : '#ff0004'}] #{"name": 'QA CYCLE', "data": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]}]
    title = {"text": 'Bugs Overview'}
    xAxis = {"name":'Cycle',"categories": ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21']}
    #yAxis = 
    
    yAxis = {"title": {"text": 'Bugs'}}
    xAxis = {"title": {"text":"Cycle number [cycle #2 was abandoned]"}}
    return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
    #return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


# Fetch the data from mongodb:

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

@app.route('/testResults')
@login_required
def test_results():
    return render_template('testResults.html')  # render a template





# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')