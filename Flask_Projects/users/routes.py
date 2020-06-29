from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import login_user,current_user,logout_user,login_required
from Flask_Projects import db,bcrypt
from Flask_Projects.models import Post,User
from Flask_Projects.users.forms import (RegistrationForm,
								 SigninForm,RequestResetForm,
								 UpdateAccountForm,
                                 ResetPasswordForm)
from Flask_Projects.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/registration",methods=['GET','POST'])
def registration():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Succesfully You can Login now!!!','success')
        return redirect(url_for('users.signin'))
    return render_template('registration.html',title='Register',form=form)

@users.route("/signin",methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form=SigninForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f"Wecome To Soul Blog!!","success")
            return redirect(url_for('main.homepage'))
        else:
            flash("Login Unsuccesful. Please Check email and password",'warning')
        
    return render_template('signin.html',title='Sign-in',form=form)



@users.route("/logout")
def logout():
    logout_user()
    flash("Thanks You for Visiting our Site. Have a nice day..",'warning')
    return redirect(url_for('main.homepage'))
@users.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

            current_user.img_file = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profilepic/' + current_user.img_file)
    
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)



@users.route("/user/<string:username>")
def userposts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
            .paginate(page=page,per_page=4)
    return render_template('userpost.html',posts=posts,user=user,title=f"{user.username} Posts")




@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'warning')
        return redirect(url_for('users.signin'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    user=User.verify_reset_token(token)
    
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_pass
        db.session.commit()
        flash('Password Reset Successfully! Login and Enjoy Blogs!!','warning')
        return redirect(url_for('users.signin'))
    return render_template('reset_token.html',title='Reset Password',form=form)
