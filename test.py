from flask import Flask, request, make_response, redirect, url_for
import jwt
import requests

app = Flask(__name__)
JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"

USERS = {
    "alice": {"password": "alice123"},
    "bob": {"password": "bob123"},
}

@app.route('/')
def index():
    token = request.cookies.get('auth')
    if not token:
        return redirect(url_for('login'))
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get('sub')
        return f"Hello, {username}! (insecure demo)"
    except Exception:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form method="post">
                username: <input name="username"><br>
                password: <input name="password" type="password"><br>
                <input type="submit" value="Login">
            </form>
        '''
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    user = USERS.get(username)
    if user and user['password'] == password:
        token = jwt.encode({"sub": username}, JWT_SECRET, algorithm=JWT_ALGORITHM)
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('auth', token)
        return resp
    return "Invalid credentials", 401

@app.route('/fetch-external')
def fetch_external():
    r = requests.get('https://example.com/api/data', verify=False)
    return f"external data length: {len(r.content)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
