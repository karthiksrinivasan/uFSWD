from app.modules.catalog import catalog
from flask import render_template, abort, redirect, request, url_for
from app import server
from app.modules.catalog.models import *
from app.modules.catalog.forms import *
from flask_login import login_required, current_user


@catalog.route('/')
def index_page():
    """
    index_page: Returns home page for the website with
        list of categories and recent items
    """
    route = {0: {"name": "Item Catalog", "link": "/"}}
    listOfCategories = DB_Operations.getListOfCategory()
    listOfRecentItems = DB_Operations.getRecentItems()
    return render_template("catalog.html",
                           route=route,
                           categories=listOfCategories,
                           items=listOfRecentItems)


@catalog.route('/category/add', methods=["POST", "GET"])
@login_required
def add_category():
    """
    add_category: Handles POST and GET call for adding a new category
        GET: Return a page with a form
        POST: Processes the form data and redirects user to appropriate page
    """
    route = route = {0: {"name": "Item Catalog", "link": "/"},
                     1: {"name": "Add Category"}}
    form = CatalogForm(request.form)
    if request.method == 'POST' and form.validate():
        DB_Operations.addCategory(form.name.data, current_user.email)
        return redirect(url_for('catalog.index_page'))
    return render_template("form.html",
                           form_header="Add New Category",
                           form=form,
                           confirm_button='Add',
                           route=route)


@catalog.route('/category/<string:cat_name>/edit', methods=["POST", "GET"])
@login_required
def edit_category(cat_name):
    """
    edit_category: Handles POST and GET call for editing a category
        GET: Return a page with a form with data loaded
        POST: Processes the form data and redirects user to appropriate page
    """
    route = route = {0: {"name": "Item Catalog", "link": "/"},
                     1: {"name": cat_name, "link": url_for('catalog.category',
                                                           cat_name=cat_name)},
                     2: {"name": "Edit"}}
    category = DB_Operations.getCategory(cat_name)
    if category.created_by != current_user.email:
        return render_template('error.html',
                               error=str("unauthorized"),
                               route=route), 403
    form = CatalogForm(request.form)
    if request.method == 'GET':
        form.name.data = cat_name
    if request.method == 'POST' and form.validate():
        DB_Operations.editCategory(cat_name, form.name.data)
        return redirect(url_for('catalog.index_page'))
    return render_template("form.html",
                           form_header="Edit Category",
                           form=form,
                           confirm_button='Update',
                           route=route)


@catalog.route('/category/<string:cat_name>/delete', methods=["POST", "GET"])
@login_required
def delete_category(cat_name):
    """
    delete_category: Handles POST and GET call for deleting a category
        GET: Return a page with a form with data and confirmation button
        POST: Processes the form data and redirects user to appropriate page
    """
    route = route = {0: {"name": "Item Catalog", "link": "/"},
                     1: {"name": cat_name, "link": url_for('catalog.category',
                                                           cat_name=cat_name)},
                     2: {"name": "Delete"}}
    category = DB_Operations.getCategory(cat_name)
    if category.created_by != current_user.email:
        return render_template('error.html',
                               error=str("unauthorized"),
                               route=route), 403
    form = CatalogForm(request.form)
    if request.method == 'GET':
        form.name.data = cat_name
        form.name.description = u'static'
    if request.method == 'POST':
        DB_Operations.deleteCategory(form.name.data)
        return redirect(url_for('catalog.index_page'))
    else:
        print (form.name.data)
    return render_template("form.html",
                           form_header="Delete Category",
                           form=form,
                           confirm_button='Delete',
                           route=route)


@catalog.route('/item/<string:cat_name>/add', methods=["POST", "GET"])
@login_required
def add_item(cat_name):
    """
    add_item: Handles POST and GET call for adding a new item
        GET: Return a page with a form
        POST: Processes the form data and redirects user to appropriate page
    """
    route = route = {0: {"name": "Item Catalog", "link": "/"},
                     1: {"name": cat_name, "link": url_for('catalog.category',
                                                           cat_name=cat_name)},
                     2: {"name": "Add Item"}}
    form = ItemForm(request.form)

    listOfCategories = DB_Operations.getListOfCategory()
    val = [(val, val) for val in listOfCategories]
    form.category.choices = val
    form.category.data = cat_name
    if request.method == 'POST' and form.validate():
        DB_Operations.addItem(form.name.data, form.description.data,
                              form.category.data, current_user.email)
        return redirect(url_for('catalog.category', cat_name=cat_name))

    return render_template("form.html",
                           form_header="Add New Item",
                           form=form,
                           confirm_button='Add',
                           route=route)


@catalog.route('/item/<string:item_id>/edit', methods=["POST", "GET"])
@login_required
def edit_item(item_id):
    """
    edit_item: Handles POST and GET call for editing a item
        GET: Return a page with a form with data initialized
        POST: Processes the form data and redirects user to appropriate page
    """
    item = DB_Operations.getItem(item_id)
    route = {0: {"name": "Item Catalog", "link": "/"},
             1: {"name": item.category.category_name, "link":
                 url_for('catalog.category',
                         cat_name=item.category.category_name)},
             2: {"name": item.item_name, "link":
                 url_for('catalog.item', item_id=item_id)},
             3: {"name": "Edit"}}
    if item.created_by != current_user.email:
        return render_template('error.html',
                               error=str("unauthorized"),
                               route=route), 403
    form = ItemForm(request.form)
    listOfCategories = DB_Operations.getListOfCategory()
    val = [(val, val) for val in listOfCategories]
    form.category.choices = val
    if request.method == 'GET':
        form.name.data = item.item_name
        form.description.data = item.item_desc
        form.category.data = item.category.category_name
    if request.method == 'POST' and form.validate():
        DB_Operations.editItem(item_id, form.name.data, form.description.data,
                               form.category.data)
        return redirect(url_for('catalog.item', item_id=item_id))
    return render_template("form.html",
                           form_header="Edit Item",
                           form=form,
                           confirm_button='Update',
                           route=route)


@catalog.route('/item/<string:item_id>/delete', methods=["POST", "GET"])
@login_required
def delete_item(item_id):
    """
    delete_item: Handles POST and GET call for deleting a item
        GET: Return a page with a form with data and confirmation
        POST: Processes the form data and redirects user to appropriate page
    """
    item = DB_Operations.getItem(item_id)
    route = {0: {"name": "Item Catalog", "link": "/"},
             1: {"name": item.category.category_name, "link":
                 url_for('catalog.category',
                         cat_name=item.category.category_name)},
             2: {"name": item.item_name, "link":
                 url_for('catalog.item', item_id=item_id)},
             3: {"name": "Delete"}}
    if item.created_by != current_user.email:
        return render_template('error.html',
                               error=str("unauthorized"),
                               route=route), 403
    form = ItemForm(request.form)
    listOfCategories = DB_Operations.getListOfCategory()
    val = [(val, val) for val in listOfCategories]
    form.category.choices = val
    if request.method == 'GET':
        form.name.data = item.item_name
        form.description.data = item.item_desc
        form.category.data = item.category.category_name
        form.name.description = u'static'
        form.description.description = u'static'
        form.category.description = u'static'
    if request.method == 'POST':
        DB_Operations.deleteItem(item_id)
        return redirect(url_for('catalog.category',
                                cat_name=item.category.category_name))

    return render_template("form.html",
                           form_header="Delete Item",
                           form=form,
                           confirm_button='Delete',
                           route=route)


@catalog.route('/category/<string:cat_name>')
def category(cat_name):
    """
    category: Handles GET to serve list of items within a category
    """
    route = {0: {"name": "Item Catalog", "link": "/"},
             1: {"name": cat_name, "link": ""}}
    listOfCategories = DB_Operations.getListOfCategory()
    listOfRecentItems = DB_Operations.getItemsByCategory(cat_name)
    return render_template("catalog.html",
                           route=route,
                           category_name=cat_name,
                           categories=listOfCategories,
                           items=listOfRecentItems)


@catalog.route('/item/<string:item_id>')
def item(item_id):
    """
    category: Handles GET to serve item information
    """
    item = DB_Operations.getItem(item_id)
    route = {0: {"name": "Item Catalog", "link": "/"},
             1: {"name": item.category.category_name, "link":
                 url_for('catalog.category',
                         cat_name=item.category.category_name)},
             2: {"name": item.item_name, "link": "/"}}
    return render_template("item.html",
                           route=route, item=item)
