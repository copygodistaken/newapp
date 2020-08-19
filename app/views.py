from app import app
from flask import request, redirect, render_template, jsonify, make_response


@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/profile/<username>")
def profile(username):
    user = None
    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)


@app.route("/multiple/<foo>/<bar>/<baz>")
def multiple(foo, bar, baz):
    print (f"foo is {foo}")
    print (f"bar is {bar}")
    print (f"baz is {baz}")
    return f"foo is {foo}, bar is {bar}, baz is {baz}."

@app.route("/json", methods=['POST'])
def json():
    # determine if POST data was in JSON format with .is_json
    if request.is_json:
        # return an answer
        # get the JSON data from the request
        req = request.get_json()
        # write a message to send back to the user
        response = {
            "message": "JSON recieved",
            "sender": req.get("name")
        }
        # make the dict into JSON data and send it as a response
        resp = make_response(jsonify(response), 200)
        return resp

    else: # return an error if JSON isn't present
        return make_response(jsonify({"message": "POST data must be in JSON format."}), 400)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        missing = list()

        # for KEY, VALUE in list...
        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            # feedback = f"The following field(s) must be filled out: ", {' ,' .join(missing)}
            feedback = "The following field(s) must be filled out: " + ', '.join(missing)
            return render_template("public/signup.html", feedback=feedback)

        return redirect(request.url)

    return render_template("public/signup.html")

# keep for reference of how to work with data in jinja
@app.route("/jinja")
def jinja():
    # strings
    my_name = "Eric"
    # Integers
    my_age = 46
    # Lists
    langs = ["Python", "PHP", "HTML", "CSS", "SQL"]
    # Dictionaries
    friends = {
        "Jeremy": 44,
        "Preston": 44,
        "Travis": 44,
        "Charisa": 40,
        "Jody": 40,
    }
    # Tuples
    colors = ("Red", "Blue")
    # Booleans
    unemployed = True
    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return(f"Cloning into {repo}")

    my_remote = GitRemote(
        name = "Learning Flask",
        description = "Learn the Flask web framework for Python.",
        domain = "https://github.com/copygodistaken/newapp.git"
    )

    my_html = "<h5>This is some HTML</h5>"

    suspicious ="<script>alert('NEVER TRUST USER INPUT!')</script>"

    date = datetime.utcnow()

    # Functions
    def repeat(x, qty=1):
        return x * qty

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, unemployed=unemployed, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date=date, my_html=my_html,
        suspicious=suspicious
    )

# probably delete this in the future when a db is implemented.
users = {
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "Technology entrepreneur, investor, and engineer.",
        "twitter_handle": "@elonmusk"
    },
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creator of the Flask framework.",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language.",
        "twitter_handle": "@gvanrossum"
    }
}

