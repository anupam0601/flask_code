# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps

# create the application object
app = Flask(__name__)

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
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# for highcharts
@app.route('/graph')
@login_required
def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,"zoomType" : 'x'}
    series = [{"name": 'CPU', "data": [6.3,8.8,6.9,6,7,8,8,9]}, {"name": 'MEM', "data": [7.8,10.5,9.36,7,8,8,9,10]}]
    title = {"text": 'Performance Stats'}
    xAxis = {"categories": ['2015-07-29 16:25:03','2015-07-29 16:25:10','2015-07-29 16:25:10','2015-07-29 16:25:10','2015-07-29 16:25:10','2015-07-29 16:25:10','2015-07-29 16:25:10','2015-07-29 16:25:10']}
    yAxis = {"title": {"text": 'CPU and MEM'}}
    return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
    #return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)




@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True,host ='0.0.0.0')