from flask import Flask, redirect, request, render_template, url_for, session
import ast
from dotenv import load_dotenv
import os
from scrapper import get_playlist_details
from gpt import send_prompt

app = Flask(__name__)
load_dotenv(dotenv_path='keys.env')
app.secret_key = os.getenv('session_key')

def filter_response(song_data):
    li = ast.literal_eval(song_data)
    return_list = []
    for i in li:
        if i[2] == "NE":
            return_list.append(f"{i[0]} by {i[1]}")
        else:
            return_list.append(f"{i[0]}({i[2]}) by {i[1]}")
    return(return_list)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get("playlistUrl")
        session['url'] = url
        return(redirect(url_for('result')))
    else:
        session['url'] = ""
        return(render_template('home.html'))

@app.route('/result', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        action = request.form.get("action")
        if action == 'regenerate':
            return(redirect(url_for('result')))
        elif action == 'back':
            return(redirect(url_for('home')))
    else:
        li = get_playlist_details(url=session['url'])
        x = send_prompt(li=li)
        y = filter_response(song_data=x)
        return(render_template('result.html', list=y))


if __name__ == "__main__":
    app.run(debug=True, port=5000)