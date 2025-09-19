from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Lỗ hổng: Hardcoded secret key

# Tạo database
def init_db():
    conn = sqlite3.connect('vuln.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
    # Thêm bảng comments cho chức năng bình luận
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (id INTEGER PRIMARY KEY, username TEXT, comment TEXT)''')
    # Thêm một số dữ liệu mẫu
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    c.execute("INSERT OR IGNORE INTO posts VALUES (1, 'Welcome', 'Hello World!')")
    conn.commit()
    conn.close()

init_db()

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerable Web App</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8f9fa; }
        .container { max-width: 900px; margin-top: 40px; }
        .card { margin-bottom: 20px; }
        .comment { border-bottom: 1px solid #eee; margin-bottom: 10px; padding-bottom: 5px; }
        .footer { margin-top: 40px; color: #888; text-align: center; }
        .navbar-brand { font-weight: bold; }
        .xss { color: #d63384; }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">Vulnerable WebApp</a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        {% if session.logged_in %}
        <li class="nav-item">
          <span class="nav-link">👤 {{ session.username }}</span>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/logout">Logout</a>
        </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
<div class="container">
    <h1 class="my-4">Welcome to <span class="text-primary">Vulnerable Web App</span></h1>
    {% if not session.logged_in %}
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title mb-3">Login</h3>
            <form action="/login" method="post">
              <div class="mb-3">
                <input type="text" class="form-control" name="username" placeholder="Username">
              </div>
              <div class="mb-3">
                <input type="password" class="form-control" name="password" placeholder="Password">
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    {% else %}
    <div class="row">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h4 class="card-title">Add New Post</h4>
            <form action="/add_post" method="post">
              <div class="mb-2">
                <input type="text" class="form-control" name="title" placeholder="Title">
              </div>
              <div class="mb-2">
                <textarea class="form-control" name="content" placeholder="Content"></textarea>
              </div>
              <button type="submit" class="btn btn-success">Add Post</button>
            </form>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h4 class="card-title">Search Posts</h4>
            <form action="/search" method="get">
              <div class="input-group mb-2">
                <input type="text" class="form-control" name="q" placeholder="Search...">
                <button class="btn btn-outline-secondary" type="submit">Search</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-md-8">
        <h3>Posts</h3>
        {% for post in posts %}
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ post.title }}</h5>
            <p class="card-text">{{ post.content }}</p>
          </div>
        </div>
        {% endfor %}
      </div>
      <div class="col-md-4">
        <h3>Comments <span class="xss">(Stored XSS)</span></h3>
        <form action="/comment" method="post" class="mb-3">
          <div class="input-group">
            <input type="text" class="form-control" name="comment" placeholder="Your comment here...">
            <button class="btn btn-warning" type="submit">Add Comment</button>
          </div>
        </form>
        <div class="list-group">
        {% for c in comments %}
          <div class="list-group-item">
            <b>{{ c.username }}</b>: <span class="xss">{{ c.comment|safe }}</span>
          </div>
        {% endfor %}
        </div>
      </div>
    </div>
    {% endif %}
    {% if error %}
    <div class="alert alert-danger mt-3">{{ error }}</div>
    {% endif %}
    {% if success %}
    <div class="alert alert-success mt-3">{{ success }}</div>
    {% endif %}
</div>
<footer class="footer">
    <hr>
    <p>© 2024 Vulnerable Web App | Demo for AI Security Testing</p>
</footer>
<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    posts = []
    comments = []
    if session.get('logged_in'):
        conn = sqlite3.connect('vuln.db')
        c = conn.cursor()
        c.execute("SELECT * FROM posts")
        posts = [{'title': row[1], 'content': row[2]} for row in c.fetchall()]
        c.execute("SELECT username, comment FROM comments ORDER BY id DESC")
        comments = [{'username': row[0], 'comment': row[1]} for row in c.fetchall()]
        conn.close()
    return render_template_string(HTML_TEMPLATE, posts=posts, comments=comments)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Lỗ hổng SQL Injection
    conn = sqlite3.connect('vuln.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()
    
    if user:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, error='Invalid credentials', posts=[], comments=[])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Lỗ hổng XSS: Phản chiếu trực tiếp input
    return render_template_string(HTML_TEMPLATE, 
                                posts=[{'title': 'Search Results', 'content': f'You searched for: {query}'}],
                                comments=[])

@app.route('/add_post', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    
    # Lỗ hổng SQL Injection
    conn = sqlite3.connect('vuln.db')
    c = conn.cursor()
    query = f"INSERT INTO posts (title, content) VALUES ('{title}', '{content}')"
    c.execute(query)
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Thêm route bình luận (stored XSS)
@app.route('/comment', methods=['POST'])
def comment():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    comment = request.form.get('comment', '')
    username = session.get('username', 'guest')
    # Lưu bình luận không lọc XSS
    conn = sqlite3.connect('vuln.db')
    c = conn.cursor()
    query = f"INSERT INTO comments (username, comment) VALUES ('{username}', '{comment}')"
    c.execute(query)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 