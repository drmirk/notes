'''Import flask objects'''
from flask import Flask

'''defined main flask app object'''
app = Flask(__name__)

'''Import models from models'''
from models import *
'''Import forms from forms'''
from forms import *
'''Import views'''
from views import *
'''Import file manager'''
from filemanager import *

'''get config based on production or development'''
app.config.from_object('config.DevelopmentConfig')

'''initialize db object from models'''
db.init_app(app)

if __name__ == "__main__":
    app.run()
