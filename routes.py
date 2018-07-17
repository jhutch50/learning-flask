#1. import Flask class and the function render_template
from flask import Flask, render_template
#2.  create a new usable instance of the flask class 
# and save it into the variable app
app = Flask(__name__)


#3. map the url to the python function 
# index. The python function uses the Flask function render_template
# to render index.html, so now when the user types in
# / the function index will run and return thep age index.html
@app.route("/")
def index():
    return render_template("index.html")

##4. Finally, add an if statement that allows 
# app.run to run on a local server and the debug=true
# will provide any error messages along the way
if __name__ == "__main__":
    app.run(debug=True)