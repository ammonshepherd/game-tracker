from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from game_tracker.auth import login_required
from game_tracker.database.db import get_db

bp = Blueprint('games', __name__)

@bp.route('/')
def index():
    db = get_db()
    games = db.execute(
        'SELECT g.id as game_id, g.game_name, g.game_info, (SELECT MAX(game_played.date_played) FROM game_played WHERE game_id = g.id) AS last_played, (SELECT player.player_name FROM player JOIN game_played ON game_played.player_id = player.id WHERE game_played.game_id = g.id AND game_played.date_played = (SELECT MAX(game_played.date_played) FROM game_played WHERE game_id = g.id)) AS player_name FROM game g ORDER BY g.game_name'
    ).fetchall()
    return render_template('games/index.html', games=games)

@bp.route('/game/<int:id>')
def game(id):
    db = get_db()
    game = db.execute('SELECT * FROM game WHERE id = ?', (id)).fetchone()
    plays = db.execute('SELECT * FROM game_played JOIN games_players_played ON game_played.id = games_players_played.game_played_id')
    return render_template('/games/display.html', game=game)

@bp.route('/game/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('games/create.html')
