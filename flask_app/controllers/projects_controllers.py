from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user_model import User # CHANGE FILE NAME
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

#Test to see if 'python server.py' is running with flask installed
@app.route('/')
def index():
    return render_template('login_registration.html')


# '''
# EACH LINE FROM HERE IS SUBJECT TO CHANGE, 
# BUT THIS IS A TEMPLATE FOR WHAT YOU WANT FOR EACH CRUD STEP 
# '''
#CREATE
@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        print ("did not pass")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    update_form = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash

    }
    user_id = User.save(update_form)

    session["user_id"] = user_id

    return redirect('/success')


#READ ALL
@app.route('/login', methods=['POST'])
def login():
    user= User.get_by_email(request.form)
    # print (user.password)
    if not user:
        flash('Invalid Credentials')
        return redirect('/')
    user_is_valid = bcrypt.check_password_hash(user.password, request.form['password']) 
    print (user_is_valid)
    session["user_id"] = user.id
    return redirect('/success')



@app.route('/success')
def success():
    if "user_id" not in session:
        return redirect ('/logout')
    return render_template ('success_page.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')


@app.route('/users/<int:id>/edit/process', methods=['POST'])
def update_user(id):
    form_data = {
        **request.form,
        'id' : id
    }
    User.update(form_data)
    return redirect('/users')

#DELETE
@app.route('/users/<int:id>/destroy', methods=['POST'])
def delete(id):
    User.delete(id)
    # return render_template('/test.html')
    print('anything')
    return redirect('/users')
