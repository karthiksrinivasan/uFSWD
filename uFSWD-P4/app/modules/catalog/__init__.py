from flask import Blueprint
from app import restless_manager
from app.modules.catalog.models import Category, Item
catalog = Blueprint('catalog', __name__,
                    template_folder='templates')

# Creating JSON Endpoint for catalog and items using Flask-Restless
restless_manager.create_api(
    Category, methods=['GET'], url_prefix='/api/v1', collection_name='catalog')
restless_manager.create_api(
    Item, methods=['GET'], url_prefix='/api/v1', collection_name='items')

from app.modules.catalog import views
