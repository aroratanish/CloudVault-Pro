import os
from flask import render_template,flash,redirect,url_for,request,abort,send_from_directory
from flashblog import app, db,bcrypt,mail
from flashblog.forms import RegistrationForm, LoginForm,UpdateForm,PostForm,RequestResetForm,ResetPasswordForm,UploadFileForm,FolderForm
from flashblog.models import User, Post, File,Folder,SharedFile
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message
import secrets

@app.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page=5)
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form  = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
       user =User.query.filter_by(email=form.email.data).first()
       if user and bcrypt.check_password_hash(user.password,form.password.data):
           login_user(user,remember=form.remember.data)
           return redirect(url_for('home'))
       else:
           flash('Login unsuccessful, check username or password again')
    return render_template("login.html",title='Login',form = form)

@app.route("/test")
def test():
    return "<h1>Test Route Working</h1>"

@app.route("/register",methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data,password =hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully')
        return redirect(url_for('login'))
    return render_template("register.html",title='Register',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static',
        filename='profile_pics/' + current_user.image_file
    )
    return render_template(
        'account.html',
        title='Account',
        image_file=image_file,
        form=form
    )

@app.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
    form  = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','Success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title = 'New Post',form  = form,legend ='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(
            url_for('post', post_id=post.id)
        )
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        'create_post.html',
        title='Update Post',
        form=form,
        legend='Update Post'
    )

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template(
        'user_posts.html',
        posts=posts,
        user=user
    )

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email.'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password.',
            'info'
        )
        return redirect(url_for('login'))
    return render_template(
        'reset_request.html',
        title='Reset Password',
        form=form
    )

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template(
        'reset_token.html',
        title='Reset Password',
        form=form
    )

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    form.folder.choices = [
    (folder.id, folder.name)
    for folder in Folder.query.filter_by(
        user_id=current_user.id
    ).all()
    ]
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = uploaded_file.filename
        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)
        save_path = os.path.join(
            app.root_path,
            'uploads',
            filename
        )
        uploaded_file.save(save_path)
        new_file = File(
        filename=filename,
        size=file_size,
        user_id=current_user.id,
        folder_id=form.folder.data
        )
        db.session.add(new_file)
        db.session.commit()
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('my_files'))
    return render_template(
        'upload.html',
        title='Upload',
        form=form
    )

@app.route("/files")
@login_required
def my_files():
    files = File.query.filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).all()
    return render_template(
        'files.html',
        title='My Files',
        files=files
    )

@app.route("/download/<int:file_id>")
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    return send_from_directory(
        os.path.join(app.root_path, 'uploads'),
        file.filename,
        as_attachment=True
    )

@app.route("/delete/<int:file_id>")
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    file.is_deleted = True
    db.session.commit()
    flash('File moved to trash!', 'success')
    return redirect(url_for('my_files'))

@app.route("/search")
@login_required
def search():
    query = request.args.get('q')
    files = File.query.filter(
        File.filename.contains(query),
        File.user_id == current_user.id
    ).all()
    return render_template(
        "search.html",
        files=files,
        query=query
    )

@app.route("/folder/new", methods=['GET', 'POST'])
@login_required
def new_folder():
    form = FolderForm()
    if form.validate_on_submit():
        folder = Folder(
            name=form.name.data,
            user_id=current_user.id
        )
        db.session.add(folder)
        db.session.commit()
        flash(
            'Folder created successfully!','success'
        )
        return redirect(
            url_for('folders')
        )
    return render_template(
        'create_folder.html',
        title='New Folder',
        form=form
    )

@app.route("/folders")
@login_required
def folders():
    folders = Folder.query.filter_by(
        user_id=current_user.id
    ).all()
    return render_template(
        'folders.html',
        folders=folders,
        title='My Folders'
    )

@app.route("/folder/<int:folder_id>")
@login_required
def view_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    if folder.user_id != current_user.id:
        abort(403)
    files = File.query.filter_by(
        folder_id=folder.id,
        is_deleted=False
    ).all()
    return render_template(
        'folder_files.html',
        folder=folder,
        files=files
    )

@app.route("/trash")
@login_required
def trash():
    files = File.query.filter_by(
        user_id=current_user.id,
        is_deleted=True
    ).all()
    return render_template(
        'trash.html',
        files=files
    )

@app.route("/restore/<int:file_id>")
@login_required
def restore_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    file.is_deleted = False
    db.session.commit()
    flash(
        'File restored successfully!',
        'success'
    )
    return redirect(
        url_for('trash')
    )

@app.route("/permanent_delete/<int:file_id>")
@login_required
def permanent_delete(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    file_path = os.path.join(
        app.root_path,
        'uploads',
        file.filename
    )
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    flash(
        'File permanently deleted!',
        'success'
    )
    return redirect(
        url_for('trash')
    )

@app.route("/share/<int:file_id>")
@login_required
def share_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    existing = SharedFile.query.filter_by(
        file_id=file.id
    ).first()
    if existing:
        token = existing.token
    else:
        token = secrets.token_urlsafe(16)
        shared = SharedFile(
            token=token,
            file_id=file.id
        )
        db.session.add(shared)
        db.session.commit()
    flash(
        f'http://127.0.0.1:5000/shared/{token}',
        'success'
    )
    return redirect(
        url_for('my_files')
    )

@app.route("/shared/<token>")
def public_download(token):
    shared = SharedFile.query.filter_by(
        token=token
    ).first_or_404()
    file = File.query.get_or_404(
        shared.file_id
    )
    return send_from_directory(
        os.path.join(
            app.root_path,
            'uploads'
        ),
        file.filename,
        as_attachment=True
    )

@app.route("/dashboard")
@login_required
def dashboard():
    total_files = File.query.filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).count()
    total_folders = Folder.query.filter_by(
        user_id=current_user.id
    ).count()
    trash_files = File.query.filter_by(
        user_id=current_user.id,
        is_deleted=True
    ).count()
    files = File.query.filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).all()
    total_storage = sum(file.size for file in files)
    recent_files = File.query.filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).order_by(
        File.upload_date.desc()
    ).limit(5)
    return render_template(
        'dashboard.html',
        total_files=total_files,
        total_folders=total_folders,
        trash_files=trash_files,
        total_storage=round(total_storage / (1024 * 1024), 2),
        recent_files=recent_files
    )

