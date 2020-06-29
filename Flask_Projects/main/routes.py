from flask import render_template,request,Blueprint,flash,redirect,url_for
from Flask_Projects.models import Post,User
from Flask_Projects.models import ContactUs
from Flask_Projects import db
from Flask_Projects.users.forms import ContactUsForm
import os

main = Blueprint('main', __name__)

# URL FOR HOME SECTION

@main.route("/home")
@main.route("/")
def homepage():
	
    #APPLY PAGINATION
    page=request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_post.desc()).paginate(page=page, per_page=5)
    users=User.query.all()
    #FOR SEARCHING POST BY USERNAME OR TITLE OF BLOG
    posts_list=[]
    posts_author=[]
    user_names=[]
    for post in posts.items:
       
        posts_list.append(post.title)

    for user in users:
     	user_names.append(user.username)
    
    return render_template('blog.html',posts=posts,title="Soul Blog",posts_list=posts_list,user_names=user_names)

# URL FOR ABOUT SECTION
@main.route("/about",methods=["POST","GET"])
def about():
	form=ContactUsForm()
	if form.validate_on_submit():
		flash("Thank you for your message/feedback and have a good day.","warning")
		return redirect(url_for('main.about'))
	return render_template('about.html', title='About',form=form)