from app import app
from flask import render_template, request, url_for, redirect, abort, flash
from flask import Flask
from .models import Lost,User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user,login_required, current_user
from sqlalchemy.engine import url
from sqlalchemy.sql import exists
from sqlalchemy import func

@app.route('/')
def index():
    return render_template("Registration.html")

@app.route('/User')
def show_user():
    return render_template("UserHome.html")

@app.route('/User', methods=['POST'])
def post_user():
    if request.method == 'POST':
        lost_info = request.form
        print(dict(lost_info))
        pic = request.files['lost_info_image']
        lost = Lost(type=lost_info)
        
        # mimetype=pic.mimetype
        lost = Lost(type=lost_info.get("lost_info_type"), brand=lost_info.get("lost_info_brand"), color=lost_info.get("lost_info_color"),
                    img=pic.read(),  location=lost_info.get("lost_info_location"), code=lost_info.get("lost_info_code"),
                    name=lost_info.get("lost_info_name"), number=lost_info.get("lost_info_number"), email=lost_info.get("lost_info_email"))
        
        db.session.add(lost)
        db.session.commit()
        lostaka=dict(lost_info)
        return redirect(url_for('Lost_Item', lost_info=lostaka))
    else:
        
        # dblostitem =Lost.query.filter_by(type=lost_info.get("lost_info_type"), brand=lost_info.get("lost_info_brand"), color=lost_info.get("lost_info_color").first()            
        return render_template("UserHome.html")
        # img_name=pic.filename,
                # print(dblostitem)

    #     if 'file' not in request.fil'hkgvyhfvgjngvles:
    #       flash('No file part')
    #       return redirect(request.url)
    # file = request.files['file']
    # if file.filename == '':
    #     flash('No image selected for uploading')
    #     return redirect(request.url)
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     # print('upload_image filename: ' + filename)
    #     flash('Image successfully uploaded and displayed below')
    #     return redirect(url_for('found_Item', filename=filename))

    # else:
    #     flash('Allowed image types are - png, jpg, jpeg, gif')
    #     return redirect(request.url)
        


# @app.route('/display/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/LostItem')
def Lost_Item():
        lost_infoxd12 = request.args.get('lost_info')
    # dblostitem =Lost.query.filter_by(type=lost_info.get("lost_info_type"), brand=lost_info.get("lost_info_brand"), color=lost_info.get("lost_info_color")).first()            
    # print(dblostitem.type)
    # print(dblostitem.number)
        # dictr=json.loads(lost_infoxd12)
        # print(dictr)
    # filename=request.args("filename")
        print(lost_infoxd12)
        return render_template("LostItem.html")
        # return redirect(url_for('Lost_Item'))


@app.route('/login')
def login():
    return render_template("UserHome.html")

...
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
    login_user(user, remember=remember)
    return redirect(url_for('User'))

@app.route('/signup')
def signup():
    return render_template("LoginPage.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    print(email)
    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    # if user: # if a user is found, we want to redirect back to signup page so user can try again
    #     flash('Email address already exists')
    #     return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    print(new_user)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))
 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

