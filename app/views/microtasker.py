import datetime as dt

from flask import (flash, redirect, render_template, request,
                   session, url_for, abort, Blueprint)
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.security import check_password_hash, generate_password_hash

from models import Board, Card, Column, User
from utils.forms import (AddColForm, CreateBoardForm, CreateCardForm,
                         EditCardForm, LoginForm, RegisterForm,
                         EditBoardForm, EditColForm, DeleteAccountForm,
                         ChangePasswordForm)
from models import db
microtasker = Blueprint('microtasker', __name__, url_prefix='/microtasker')


@microtasker.route("/theme", methods=["GET"])
def theme():
    """
    Receives a theme string and a path, saves the theme to a cookie
    and redirects back to the page from the post request is made.
    """
    session['theme'] = request.args.get('theme')
    path = request.args.get('path')
    return redirect(path)


@microtasker.route("/")
def home():
    return render_template('microtasker/index.html')


@microtasker.route("/profile/<username>")
@login_required
def profile(username):
    return render_template('microtasker/profile.html')


@microtasker.route("/profile/<username>/delete", methods=["GET", "POST"])
@login_required
def deleteaccount(username):
    form = DeleteAccountForm()
    if username != current_user.username:
        return abort(401)

    if request.method == "POST":
        if form.verification.data and form.validate_on_submit():
            for board in current_user.boards:
                db.session.delete(board)
            for col in current_user.columns:
                db.session.delete(col)
            for card in current_user.cards:
                db.session.delete(card)
            user = db.session.query(User)\
                .filter_by(username=current_user.username)\
                .first()
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('home'))
        return redirect(url_for('microtasker.deleteaccount',
                                username=current_user.username))
    return render_template('microtasker/deleteaccount.html', form=form)


@microtasker.route("/profile/<username>/change-password", 
                   methods=["GET", "POST"])
@login_required
def changepassword(username):
    form = ChangePasswordForm()
    if username != current_user.username:
        return abort(401)

    if request.method == "POST":
        if form.validate_on_submit():
            if check_password_hash(current_user.password,
                                   form.current_password.data):
                if form.new_password.data == form.confirm_password.data:
                    user = db.session.query(User)\
                        .filter_by(username=current_user.username)\
                        .first()
                    user.password = generate_password_hash(
                                                form.new_password.data,
                                                "pbkdf2:sha256", 8)
                    db.session.commit()
                    return redirect(url_for('microtasker.profile',
                                            username=current_user.username))
                flash('Password confirmation mismatch')
                return redirect(url_for('microtasker.changepassword',
                                        username=current_user.username))
            flash('You inserted the wrong current password.')
            return redirect(url_for('microtasker.changepassword',
                                    username=current_user.username))
        flash('Something went wrong.')
        return redirect(url_for('microtasker.changepassword',
                                username=current_user.username))
    return render_template('microtasker/changepassword.html', form=form)


@microtasker.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = db.session.query(User)\
            .filter_by(username=request.form["username"]).first()

        if user:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user,
                           remember=form.remember_me.data,
                           duration=dt.timedelta(days=30))
                return redirect(url_for('microtasker.home'))

            flash('Wrong password. Try again.')
            return redirect(url_for('microtasker.login'))

        flash('User does not exist.')
        return redirect(url_for('microtasker.login'))
    return render_template("microtasker/login.html", form=form)


@microtasker.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('microtasker.home'))


@microtasker.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User)\
                .filter_by(email=request.form["email"]).first()

            user_check = db.session.query(User)\
                .filter_by(username=request.form['username']).first()

            if user:
                flash("Email is already registered. Login instead.")
                return redirect(url_for('microtasker.login'))
            if user_check:
                flash("Username is taken. Use a different one.")
                return redirect(url_for('microtasker.register'))

            hashed_password = generate_password_hash(request.form["password"],
                                                     "pbkdf2:sha256", 8)

            new_user = User(
                username=request.form["username"],
                email=request.form["email"],
                password=hashed_password,
                date_created=dt.datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('microtasker.login'))

    return render_template("microtasker/register.html", form=form)


@microtasker.route("/board/<int:board_id>", methods=["GET"])
@login_required
def board(board_id):
    board_object = db.session.query(Board)\
        .filter_by(id=board_id, user_id=current_user.id)\
        .first()
    if not board_object:
        return abort(404)
    return render_template('microtasker/board.html', board=board_object)


@microtasker.route("/delete/<int:board_id>/<int:card_id>")
@login_required
def delete(card_id, board_id):
    card_data = db.session.query(Card)\
        .filter_by(id=card_id, user_id=current_user.id)\
        .first()
    if not card_data:
        return abort(404)
    db.session.delete(card_data)
    db.session.commit()
    return redirect(url_for('microtasker.board', board_id=board_id))


@microtasker.route("/card/<int:card_id>", methods=["GET", "POST"])
@login_required
def card(card_id):
    form = CreateCardForm()
    return render_template('microtasker/card.html', form=form)


@microtasker.route("/editcard/<int:card_id>", methods=["GET", "POST"])
@login_required
def editcard(card_id):
    card_data = db.session.query(Card)\
        .filter_by(id=card_id, user_id=current_user.id)\
        .first()
    if not card_data:
        return abort(404)
    form = EditCardForm(
            card_name=card_data.card_name,
            card_subtitle=card_data.card_subtitle,
            card_content=card_data.card_content,
            card_color=card_data.color)
    col_data = db.session.get(Column, card_data.column_id)
    if request.method == "POST":
        if form.validate_on_submit():
            card_data.card_name = form.card_name.data
            card_data.card_subtitle = form.card_subtitle.data
            card_data.card_content = form.card_content.data
            card_data.user = current_user
            card_data.column = col_data
            card_data.board = db.session.get(Board, col_data.board_id)
            card_data.color = form.card_color.data
            card_data.last_edited = dt.datetime.utcnow()
            db.session.commit()
            return redirect(url_for('microtasker.board', 
                                    board_id=col_data.board_id))

    return render_template('microtasker/editcard.html',
                           form=form,
                           col=col_data,
                           card=card_data)


@microtasker.route("/newcard/<int:col_id>", methods=["GET", "POST"])
@login_required
def newcard(col_id):
    form = CreateCardForm()
    col_object = db.session.query(Column)\
        .filter_by(id=col_id, user_id=current_user.id)\
        .first()
    if not col_object:
        return abort(404)
    if request.method == "POST":
        if form.validate_on_submit():
            new_card = Card(
                card_name=form.card_name.data,
                card_subtitle=form.card_subtitle.data,
                card_content=form.card_content.data,
                user=current_user,
                column=col_object,
                board=db.session.get(Board, col_object.board_id),
                color=form.card_color.data,
                date_created=dt.datetime.utcnow()
            )
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('microtasker.board',
                                    board_id=col_object.board_id))

    return render_template('microtasker/createcard.html',
                           form=form,
                           col_id=col_id,
                           col_name=col_object.column_name)


@microtasker.route("/createboard", methods=["GET", "POST"])
@login_required
def createboard():
    form = CreateBoardForm()
    if request.method == "POST":
        if form.validate_on_submit():
            board_detect = db.session.query(Board)\
                .filter_by(title=request.form['title'],
                           user_id=current_user.id)\
                .first()

            if board_detect:
                flash("A board already exists with that name. Try again")
                return redirect(url_for('microtasker.createboard'))

            new_board = Board(
                title=form.title.data,
                user=current_user,
                color=form.board_color.data,
                date_created=dt.datetime.utcnow()
            )
            db.session.add(new_board)
            db.session.commit()
            board_id = db.session.query(Board)\
                .filter_by(user_id=current_user.id, title=form.title.data)\
                .all()[-1].id

            return redirect(url_for('microtasker.addcol', board_id=board_id))

        flash("The board name can't be longer than 50 characters")
        return redirect(url_for('microtasker.createboard'))

    return render_template('microtasker/createboard.html', form=form)


@microtasker.route("/editboard/<int:board_id>", methods=["GET", "POST"])
@login_required
def editboard(board_id):
    board_data = db.session.query(Board)\
            .filter_by(id=board_id, user_id=current_user.id)\
            .first()
    if not board_data:
        return abort(404)
    form = EditBoardForm(
            title=board_data.title,
            board_color=board_data.color)
    if request.method == "POST":
        if form.validate_on_submit():
            board_data.title = form.title.data
            board_data.color = form.board_color.data
            board_data.last_edited = dt.datetime.utcnow()
            db.session.commit()
            return redirect(url_for('microtasker.board',
                                    board_id=board_data.id))

    return render_template('microtasker/editboard.html',
                           form=form,
                           board=board_data)


@microtasker.route("/deleteboard/<int:board_id>")
@login_required
def deleteboard(board_id):
    board_data = db.session.query(Board)\
        .filter_by(id=board_id, user_id=current_user.id)\
        .first()
    if not board_data:
        return abort(404)
    db.session.delete(board_data)
    db.session.commit()
    return redirect(url_for('microtasker.home'))


@microtasker.route("/editcol/<int:col_id>", methods=["GET", "POST"])
@login_required
def editcol(col_id):
    col_data = db.session.query(Column)\
            .filter_by(id=col_id, user_id=current_user.id)\
            .first()
    if not col_data:
        return abort(404)
    form = EditColForm(
            col_name=col_data.column_name,
            col_color=col_data.color)
    if request.method == "POST":
        if form.validate_on_submit():
            col_data.column_name = form.col_name.data
            col_data.color = form.col_color.data
            col_data.last_edited = dt.datetime.utcnow()
            db.session.commit()
            return redirect(url_for('microtasker.board', 
                                    board_id=col_data.board_id))

    return render_template('microtasker/editcolumn.html',
                           form=form,
                           col=col_data)


@microtasker.route("/addcol/<int:board_id>", methods=["GET", "POST"])
@login_required
def addcol(board_id):
    form = AddColForm()
    if request.method == "POST":
        if form.validate_on_submit():
            board_object = db.session.query(Board)\
                .filter_by(id=board_id, user_id=current_user.id)\
                .first()
            if not board_object:
                return abort(404)

            col_check = db.session.query(Column)\
                .filter_by(column_name=form.col_name.data,
                           board=board_object, user_id=current_user.id).first()

            if col_check:
                flash("A column with this name already exists in this board.\
                       Try again")

                return redirect(url_for('microtasker.addcol', 
                                        board_id=board_id))
            newcol = Column(
                column_name=form.col_name.data,
                user=current_user,
                board=board_object,
                color=form.col_color.data,
                date_created=dt.datetime.utcnow()
            )
            db.session.add(newcol)
            db.session.commit()
            return redirect(url_for('microtasker.addcol', board_id=board_id))

        flash("The column name can't have more than 50 characters")
        return redirect(url_for('microtasker.addcol', board_id=board_id))

    board_object = db.session.query(Board)\
        .filter_by(id=board_id, user_id=current_user.id)\
        .first()
    if not board_object:
        return abort(404)
    return render_template('microtasker/addcolumn.html',
                           board_id=board_object.id,
                           form=form,
                           cols=board_object.columns)


@microtasker.route("/deletecol/<int:col_id>")
@login_required
def deletecol(col_id):
    col_data = db.session.query(Column)\
        .filter_by(id=col_id, user_id=current_user.id)\
        .first()
    if not col_data:
        return abort(404)
    db.session.delete(col_data)
    db.session.commit()
    return redirect(url_for('microtasker.board', board_id=col_data.board_id))


@microtasker.route('/update-position', methods=["POST"])
@login_required
def update_position():
    col_id = request.form['col_id']
    card_id = request.form['card_id']
    col_data = db.session.get(Column, col_id)
    board_data = col_data.board
    card_data = db.session.get(Card, card_id)

    new_card = Card(
            card_name=card_data.card_name,
            card_subtitle=card_data.card_subtitle,
            card_content=card_data.card_content,
            user=card_data.user,
            column=col_data,
            board=board_data,
            date_created=card_data.date_created,
            color=card_data.color,
            last_edited=dt.datetime.utcnow()
        )
    db.session.add(new_card)
    db.session.delete(card_data)
    db.session.commit()
    return ('', 204)
