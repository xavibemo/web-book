import re
from sys import path
from flask import Flask, render_template, request, url_for, flash, redirect
from caspases import caspase_cutter

# path.append('./modules')
# from caspases import caspase_cutter


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba2550'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about/about.html')


@app.route('/caspases', methods=['GET', 'POST'])
def caspases():
    sequences = []
    if request.method == 'POST':
        sequences = request.form['caspasesText'].split()
        if not sequences:
            flash('An input is required!')
        else:
            try:
                results = caspase_cutter(sequences).to_html(classes='table table-stripped',
                                                            justify='justify-all',
                                                            border=0)
                
                return render_template('caspases/cut.html', results=results)
            
            except ValueError:
                flash('Something went wrong, try again!')
            
    return render_template('caspases/caspases.html')


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449, debug=True)