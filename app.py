from email import message
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import render_template, request, url_for, redirect, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user,login_required, current_user
from sqlalchemy.engine import url
from sqlalchemy.sql import exists
from sqlalchemy import func
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='lostandfound'

db = SQLAlchemy(app)
# db.init_app(app)

# with app.app_context():
#     db.create_all()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))

    def __repr__(self) -> str:
        return f"{self.id}-{self.email}-{self.password}-{self.username}"

class Lost(db.Model):
    type = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    # date=db.Column(db.DateTime, default= datetime.utcnow)
    img = db.Column(db.LargeBinary, nullable=False)
    # img_name = db.Column(db.String(50), nullable=False)
    # mimetype=db.Column(db.Text,nullable=False)
    location = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.type}-{self.brand}-{self.color}-{self.img}-{self.location}-{self.code}-{self.name}-{self.number}-{self.email}"

class Found(db.Model):
    type = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    # date=db.Column(db.DateTime, default= datetime.utcnow)
    img = db.Column(db.LargeBinary, nullable=False)
    # img_name = db.Column(db.String(50), nullable=False)
    # mimetype=db.Column(db.Text,nullable=False)
    location = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.type}-{self.brand}-{self.color}-{self.img}-{self.location}-{self.code}-{self.name}-{self.number}-{self.email}"


    



login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("LoginPage.html")

@app.route('/User')
def show_user():
    items=Found.query.limit(8).all()
    return render_template("UserHome.html",items=items)

@app.route('/User', methods=['POST'])
def post_user():
    def validate():
        validated = False
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        zip_code = request.form['lost_info_code']
        email = request.form['lost_info_email']
        number = request.form['lost_info_number']
        if len(zip_code) == 6 and re.fullmatch(regex,email) and len(number) == 10 :
            validated = True   
        return validated
    if request.method == 'POST' and validate():
        lost_info = request.form
        print(dict(lost_info))
        pic = request.files['lost_info_image']
        lost = Lost(type=lost_info)
        type=lost_info.get("lost_info_type")
        brand=lost_info.get("lost_info_brand") 
        color=lost_info.get("lost_info_color")
        img=pic.read()
        location=lost_info.get("lost_info_location")
        code=lost_info.get("lost_info_code")
        name=lost_info.get("lost_info_name")
        number=lost_info.get("lost_info_number") 
        email=lost_info.get("lost_info_email")
        # mimetype=pic.mimetype
        lost = Lost(type=type.capitalize(),
                    brand=brand.capitalize(),
                    color=color.capitalize(),
                    img=pic.read(),  
                    location=location.capitalize(), 
                    code=code,
                    name=name,
                    number=number, 
                    email=email)
        

        db.session.add(lost)
        db.session.commit()
        lostaka=dict(lost_info)
        return redirect(url_for('Lost_Item', type=type,brand=brand,location=location,name=name))
    else:
        
        # dblostitem =Lost.query.filter_by(type=lost_info.get("lost_info_type"), brand=lost_info.get("lost_info_brand"), color=lost_info.get("lost_info_color").first()            
        flash("Enter appropriate credentials - zipcode,phone,email")
        return redirect(url_for('show_user', _anchor="lostSection"))
@app.route('/LostItem')
def Lost_Item():
        type=request.args.get('type')
        brand=request.args.get('brand')
        location=request.args.get('location')
        lost_user_name=request.args.get('name')
        lost_item_found=False
        
        lost_item = Found.query.filter_by(type=type,brand=brand,location=location).first()

        if lost_item:
            lost_item_found=True
            found_user_name=lost_item.name
            number=lost_item.number
            color=lost_item.color
            return render_template("LostItem.html" , lost_user_name=lost_user_name, found_user_name=found_user_name,
            type=type,brand=brand,color=color,location=location,found_user_number=number,lost_item_found=lost_item_found)
        else:
            return render_template("LostItem.html",lost_item_found=lost_item_found)
        


@app.route('/login')
def login():
    return render_template("LoginPage.html")

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    else:
        login_user(user, remember=remember)
        return redirect(url_for('show_user'))

@app.route('/signup')
def signup():
    return render_template("Registration.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    print(new_user)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))
 
@app.route('/User/foundDetails', methods=['GET','POST'] )
def found_Detail():
    found_item_details = {}
    def validate():
        validated = False
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        zip_code = request.form['found_info_zip']
        email = request.form['found_info_email']
        number = request.form['found_info_number']
        if len(zip_code) == 6 and re.fullmatch(regex,email) and len(number) == 10 :
            validated = True   
        return validated
    if request.method == 'POST' and validate():
        print("form Validated")
        found_item_details["type"] = request.form['found_info_type']
        found_item_details["brand"] = request.form['found_info_brand']
        found_item_details["color"] = request.form['found_info_color']
        found_item_details["date"] = request.form['found_info_date']
        found_item_details["location"] = request.form['found_info_location']
        found_item_details["zip"] = request.form['found_info_zip']
        found_item_details["name"] = request.form['found_info_name']
        found_item_details["number"] = request.form['found_info_number']
        found_item_details["email"] = request.form['found_info_email']
        print(found_item_details["type"])
        pic = request.files['found_info_image']
        pic.save(f"static/images/{secure_filename(pic.filename)}")
        found = Found(type=found_item_details["type"].capitalize(), 
                      brand=found_item_details["brand"].capitalize(), 
                      color=found_item_details["color"].capitalize(),
                      img=pic.read(), 
                      location=found_item_details["location"].capitalize(), 
                      code=found_item_details["zip"],
                      name=found_item_details["name"], 
                      number=found_item_details["number"], 
                      email=found_item_details["email"])
        if found:
            info_register_success = True
        db.session.add(found)
        db.session.commit()
        print(secure_filename(pic.filename))
        return redirect(url_for('found_detail_feed',name=found_item_details["name"],type=found_item_details["type"], brand=found_item_details["brand"], color=found_item_details["color"],location=found_item_details["location"],pic_url=pic.filename))
    else : 
        flash("Enter appropriate credentials - zipcode,phone,email")
        return redirect(url_for('show_user', _anchor="foundSection"))
         

@app.route('/foundDetailFeedback')
def found_detail_feed():
    name=request.args.get("name")
    type=request.args.get("type")
    brand=request.args.get("brand")
    color=request.args.get("color")
    location=request.args.get("location")
    pic_name = request.args.get("pic_url")
    return render_template("foundItemFeed.html", name=name, type=type, brand=brand,color=color,location=location, pic=pic_name)


@app.route('/User/search', methods=['POST'])
def search_item():
    item_type=request.form['search_input']
    filtered_items = Found.query.filter_by(type=item_type)
    print(filtered_items)
    if filtered_items:
        return render_template("UserHome.html",items=filtered_items)
    else:
        return render_template("UserHome.html")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)