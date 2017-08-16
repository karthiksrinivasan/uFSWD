from app.modules.index import index
from app.modules.catalog.views import index_page as catalog_indexpage
from flask import render_template, abort, redirect, request, url_for
from app import server, login_manager


@index.route('/')
def index_page():
    return catalog_indexpage()


@server.errorhandler(404)  # Not Found
@server.errorhandler(403)  # Forbidden
@server.errorhandler(500)  # Internal Server Error
def error_handler(e):
    error_code = int((str(e)).split(" ")[0])
    route = {0: {"name": "Item Catalog", "link": "/"},
             1: {"name": error_code}}

    return render_template('error.html', error=str(e), route=route), error_code


@login_manager.unauthorized_handler
def unauthorized():
    return abort(403)
