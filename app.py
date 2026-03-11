from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
  return "Merhaba, Buluttan selam!"


@app.route('about') 
def about():
  return "Hakkında Sayfası"
