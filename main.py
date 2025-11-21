
from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os
import math

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DATABASE = '/nfs/demo.db'
PER_PAGE_DEFAULT = 10

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL
            );
        ''')
        db.commit()
        db.close()

# -----------------------------
# Home page
# -----------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -----------------------------
# Playlist page (CRUD on songs)
# -----------------------------
@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            song_id = request.form.get('song_id')
            if song_id:
                db = get_db()
                db.execute('DELETE FROM songs WHERE id = ?', (song_id,))
                db.commit(); db.close()
                flash('Song removed from playlist.', 'success')
            else:
                flash('Missing song ID.', 'danger')
            return redirect(url_for('playlist'))

        if action == 'update':
            song_id = request.form.get('song_id')
            title = request.form.get('title')
            artist = request.form.get('artist')
            if song_id and title and artist:
                db = get_db()
                db.execute('UPDATE songs SET title=?, artist=? WHERE id=?',
                           (title, artist, song_id))
                db.commit(); db.close()
                flash('Song updated.', 'success')
            else:
                flash('Missing fields for update.', 'danger')
            return redirect(url_for('playlist'))

        # default -> add
        title = request.form.get('title')
        artist = request.form.get('artist')
        if title and artist:
            db = get_db()
            db.execute('INSERT INTO songs (title, artist) VALUES (?, ?)',
                       (title, artist))
            db.commit(); db.close()
            flash('Song added to playlist!', 'success')
        else:
            flash('Missing song title or artist.', 'danger')
        return redirect(url_for('playlist'))

    # GET: pagination
    try:
        page = max(int(request.args.get('page', 1)), 1)
    except ValueError:
        page = 1
    try:
        per_page = max(int(request.args.get('per', PER_PAGE_DEFAULT)), 1)
    except ValueError:
        per_page = PER_PAGE_DEFAULT
    offset = (page - 1) * per_page

    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM songs').fetchone()[0]
    songs = db.execute(
        'SELECT * FROM songs ORDER BY id DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    db.close()

    pages = max(1, math.ceil(total / per_page))
    has_prev = page > 1
    has_next = page < pages
    start_page = max(1, page - 2)
    end_page = min(pages, page + 2)

    return render_template(
        'index.html',
        songs=songs,
        page=page, pages=pages, per_page=per_page,
        has_prev=has_prev, has_next=has_next, total=total,
        start_page=start_page, end_page=end_page
    )

# -----------------------------
# Suggested music page
# -----------------------------
@app.route('/suggest')
def suggest():
    suggestions = [
        "Blinding Lights – The Weeknd",
        "Flowers – Miley Cyrus",
        "Calm Down – Rema",
        "As It Was – Harry Styles",
        "Shape of You – Ed Sheeran",
    ]
    return render_template('suggest.html', suggestions=suggestions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
