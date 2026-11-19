from flask import Flask, render_template, request
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY']='gs9df3nkj'

@app.route("/", methods=["GET"])
def welcome():
    name = "Paul"
    return render_template("home.html", name = name)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/shop", methods=["GET"])
def shop():
    items = ["12oz Medium Roast", "24oz French Roast", "96oz Whole Beans"]
    return render_template("shop.html", items = items)

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.data["uname"]
            password = form.data["pword"]
            confirm = form.data["confirm"]
            message = f"Successfully registered {username}"
        else:
            message = "Registration failed"
            
    return render_template("registration.html", message=message, form=form)

# def register():
#     message = ""
#     errors = []
#     if request.method == "POST":
#         username = request.form["uname"]
#         password = request.form["pword"]
#         confirm = request.form["confirm"]

#         if len(username) < 4:
#             errors.append("Username must be more than 3 characters!")
#         if not password:
#             errors.append("Password can't be blank")
#         if password and (not confirm or password != confirm):
#              errors.append("Passwords don't match!!")

#         if errors:
#             message = "Registration failed! See Errors Below"
#         else:
#             message = f"Sucessfully registered {username}!"

#     return render_template("register.html", message = message, errors = errors)