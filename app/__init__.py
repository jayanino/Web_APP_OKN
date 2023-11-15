from flask import Flask

app = Flask(__name__)
#change to development when deploying
#app.config.from_object("config.DevelopmentConfig")
app.config.from_object("config.ProductionConfig")

from app import views




