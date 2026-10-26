from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from authlib.integrations.flask_client import OAuth
from user import User
import database
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config["GOOGLE_CLIENT_ID"] = os.environ["GOOGLE_CLIENT_ID"]
app.config["GOOGLE_CLIENT_SECRET"] = os.environ["GOOGLE_CLIENT_SECRET"]

login_manager = LoginManager()
login_manager.init_app(app)

oauth = OAuth(app)

google = oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

@login_manager.user_loader
def load_user(user_id):
    row = database.get_user_by_id(int(user_id))

    if row is None:
        return None
    
    user = User(
        row[0],
        row[1],
        row[2],
        row[3]
    )

    return user

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/login/google")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()
    userinfo = token["userinfo"]
    google_id = userinfo["sub"]
    auth_account = database.get_auth_account("google", google_id)

    if auth_account is None:
        email = userinfo["email"]
        display_name = userinfo["name"]
        avatar_url = userinfo.get("picture")

        user_id = database.add_user(email, display_name, avatar_url)
        database.add_auth_account(user_id, "google", google_id)

    else:
        user_id = auth_account[1]

    row = database.get_user_by_id(user_id)

    user = User(
        row[0],
        row[1],
        row[2],
        row[3]
    )

    login_user(user)

    return redirect(url_for("home"))

@app.route("/")
def home():
    if current_user.is_authenticated:
        campaigns = database.get_campaigns_for_user(current_user.id)
        print("CURRENT USER:", current_user.display_name)
        print("CURRENT USER ID:", current_user.id)
        print(database.get_campaigns())

    else:
        campaigns = []

    return render_template("index.html", campaigns=campaigns)

@app.route("/campaign/<int:campaign_id>")
@login_required
def campaign_page(campaign_id):

    if not database.is_campaign_member(campaign_id, current_user.id):
        flash("You are not a member of that campaign.", "error")
        return redirect(url_for("home"))
        
    campaign = database.get_campaign(campaign_id)
    players = database.get_players(campaign_id)
    npcs = database.get_npcs(campaign_id)
    locations = database.get_locations(campaign_id)
    notes = database.get_notes(campaign_id)

    return render_template(
        "campaign.html", 
        campaign = campaign,
        players = players,
        npcs = npcs,
        locations = locations,
        notes = notes
        )

@app.route("/campaign/create", methods=["GET", "POST"])
@login_required
def create_campaign():
    if request.method == "POST":
        campaign_name = request.form["campaign_name"]
        system = request.form["system"]
        invite_code = database.generate_invite_code()
        campaign_id = database.add_campaign(
            campaign_name, 
            current_user.display_name, 
            system,
            invite_code
            )

        database.add_campaign_member(
            campaign_id, 
            current_user.id, 
            "DM"
            )

        return redirect(
            url_for("campaign_page", campaign_id=campaign_id)
        )

    return render_template("create_campaign.html")

@app.route("/campaign/join", methods=["GET", "POST"])
@login_required
def join_campaign():
    if request.method == "POST":
        invite_code = request.form["invite_code"]

        campaign = database.get_campaign_by_invite_code(invite_code)

        if campaign is None:
            flash("Invalid invite code.", "error")
            return redirect(url_for("join_campaign"))

        if not database.is_campaign_member(campaign[0], current_user.id):
            database.add_campaign_member(
                campaign[0], 
                current_user.id, 
                "PLAYER"
                )


        return redirect(
            url_for("campaign_page", campaign_id=campaign[0])
        )

    
    return render_template("join_campaign.html")
    


if __name__ == "__main__":
    from livereload import Server

    app.debug = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    server = Server(app.wsgi_app)

    server.watch("templates/*.html")
    server.watch("static/css/output.css")

    server.serve(
        host="localhost",
        port=5000,
        debug=True
    )
