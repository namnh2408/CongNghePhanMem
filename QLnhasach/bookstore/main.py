from bookstore import app
from flask import render_template
from bookstore.admin_module import *

@app.route("/")

def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug= True)