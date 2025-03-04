from flask import (
    Flask, request, render_template, redirect, url_for, session
)
import webview
from dotenv import load_dotenv
import threading
import os
import json
from bot import bot_move
from playsound import playsound
from time import sleep

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

x = 'X'
o = 'O'


def play_sound():
    playsound("sounds/click.mp3")


def winning_combinations(values):
    you_gonna_win = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
 
    for combo in you_gonna_win:
        try:
            if values[combo[0]] == values[combo[1]] == values[combo[2]] and values[combo[0]] != ';3':
                return values[combo[0]]
        except:
            return 'shit'

default_buttons = [';3'] * 9


@app.route('/')
def index():                           
    return render_template('login.html')


@app.post('/')
def index_click():
    args = request.form.get('login')
    user = request.form.get('name', None)
    if args == 'login':
        with open('users_score.json', 'r') as file:
            data = json.load(file)
        data.append({'player': user, 'time': 1})
        with open('users_score.json', 'w') as file:
            json.dump(data, file, indent=4)
        return redirect(url_for('game'))
    elif args == 'check_users':
        with open('users_score.json') as file:
            data = json.load(file)
            print(data)
        return render_template('users.html', users=data)


@app.get('/game')
def game():
    if 'buttons' not in session:
        session['buttons'] = default_buttons.copy()    
    return render_template('game.html', buttons=session['buttons'])

@app.post('/game')
def get_clicked_number():
    threading.Thread(target=play_sound, daemon=True).start()
    button_value = request.form.get('button')
    if button_value is None:    
        return redirect(url_for('game'))
    
    get_button_number = int(button_value)
    if session['buttons'][get_button_number] == ';3':
        session['buttons'][get_button_number] = x
        session.modified = True
        session['buttons'] = bot_move(session['buttons'], o, x)
        session.modified = True
    win = winning_combinations(session['buttons'])

    if win == 'shit':
        session.pop('buttons', None)
        return redirect(url_for('game'))
    elif win:
        session['winner'] = win
        return render_template('winner.html', winner=win)
    return redirect(url_for('game'))


@app.post('/reset')
def reset_values():
    threading.Thread(target=play_sound, daemon=True).start()
    session['buttons'] = default_buttons.copy()
    session['winner'] = None
    return redirect(url_for('game'))


def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    webview.create_window("Lovedr6s", "http://127.0.0.1:5000", width=350, height=450, resizable=False)
    webview.start()

