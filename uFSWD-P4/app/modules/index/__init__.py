from flask import Blueprint

index = Blueprint('index', __name__,
                  template_folder='templates')

from app.modules.index import views
