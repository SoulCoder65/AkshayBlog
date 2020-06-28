from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import login_user,current_user,logout_user,login_required
from Flask_Projects import db
from Flask_Projects.models import Post,User
from Flask_Projects.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# URL FOR NEW POST SECTION webpage =>  createpost.html

@posts.route("/post/new",methods=['POST','GET'])
@login_required
def newpost():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        
        db.session.add(post)    
        db.session.commit()
        flash('Your post has been created!', 'warning')
        return redirect(url_for('main.homepage'))
    return render_template('createpost.html', title='New Post',
                           form=form)

# URL FOR particular POST SECTION webpage =>  post.html

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id) #return not found
    return render_template('post.html',title=post.title,post=post)

# URL FOR Search post SECTION webpage =>  userpost.html or post_search.html

@posts.route("/search",methods=['POST'])
def search():
    page=request.args.get('page',1,type=int)
    post_data=request.form['blogtitle']
    post_search_title=Post.query.filter_by(title=post_data).first()
    user=User.query.filter_by(username=post_data).first()
    if post_search_title:
        return render_template('post_search.html',post=post_search_title,title=post_search_title.title)    
    elif user:
        posts=Post.query.filter_by(author=user)\
            .paginate(page=page,per_page=4)
        if posts:
            return render_template('userpost.html',posts=posts,user=user,title=f"{user.username} Posts")
        else:
            flash("No post Found",'warning')
            return redirect(url_for('main.homepage'))
    
    else:
        flash("No post Found",'warning')
        return redirect(url_for('main.homepage'))
    
# URL FOR Updating any post SECTION webpage =>  createpost.html
@posts.route("/post/<int:post_id>/update",methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403) #if user is not authorised return not access page
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("post has been Updated","warning")
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        form.content.data=post.content
        form.title.data=post.title
    return render_template('createpost.html',title='Update My Post',form=form)

#URL FOR DELETING POST 
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.homepage'))
