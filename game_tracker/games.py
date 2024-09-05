from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from game_tracker.auth import login_required
from game_tracker.db import get_db

bp = Blueprint('games', __name__)

@bp.route('/')
def index():
    db = get_db()
    games = db.execute(
        'SELECT * FROM game ORDER BY game_name ASC'
        # 'SELECT * FROM game JOIN game_played ON game.id = game_played.game_id'
        # ' ORDER BY game_played.date_played DESC'
    ).fetchall()
    return render_template('games/index.html', games=games)