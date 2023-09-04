import os
from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
from caspases import input_file_handler, caspase_cutter

# Web app initialization
UPLOAD_FOLDER = 'tmp'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba2550'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# App routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about/about.html')


@app.route('/caspases', methods=['GET', 'POST'])
def caspases():
    text = []
    file = ''
    
    if request.method == 'POST':
        text = request.form['caspasesText'].split()
        file = request.files['caspasesFile']
        
        if text:
            try:
                results = caspase_cutter(text).to_html(classes='table table-stripped',
                                                            justify='justify-all',
                                                            border=0)
                
                return render_template('caspases/cut.html', results=results)
            
            except ValueError:
                flash('Something went wrong, try again!')
        
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            uniprot_ids = input_file_handler(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            try:
                results = caspase_cutter(uniprot_ids).to_html(classes='table table-stripped',
                                                            justify='justify-all',
                                                            border=0)
                
                return render_template('caspases/cut.html', results=results)
            
            except ValueError:
                flash('Something went wrong, try again!')
            
        else:
            flash('An input is required!')
            
    return render_template('caspases/caspases.html')


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449, debug=True)