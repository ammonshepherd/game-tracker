import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from game_tracker.database.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        player_name = request.form['player_name']
        player_bio = request.form['player_bio']
        player_image = request.form['player_image']
        password = request.form['password']
        db = get_db()
        error = None

        if not player_name:
            error = 'Player Name is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO player (player_name, player_bio, player_image, password) VALUES (?, ?, ?, ?)",
                    (player_name, player_bio, player_image,
                     generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Player {player_name} is already in use."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        player_name = request.form['player_name']
        password = request.form['password']
        db = get_db()
        error = None
        player = db.execute(
            'SELECT * FROM player WHERE player_name = ?', (player_name,)
        ).fetchone()

        if player is None:
            error = 'Incorrect Player Name.'
        elif not check_password_hash(player['password'], password):
            error = 'Incorrect Password.'

        if error is None:
            session.clear()
            session['player_id'] = player['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_player():
    player_id = session.get('player_id')

    if player_id is None:
        g.player = None
    else:
        g.player = get_db().execute(
            'SELECT * FROM player WHERE id = ?', (player_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view