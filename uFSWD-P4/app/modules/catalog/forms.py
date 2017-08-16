from wtforms import *
from app.modules.catalog.models import *


def validate_category(form, field):
    if DB_Operations.checkIfCategoryExists(field.data):
        raise ValidationError("Category already exists.")


class CatalogForm(Form):
    """
    CatalogForm: Used to generate forms for editing/creating new Category
    Inherits:
        Form (wtforms.Form): Form object from wtforms
    """
    name = StringField('Category Name', [validators.DataRequired(
    ), validate_category], description=u"Category Name")
    field_items = ["name"]


class ItemForm(Form):
    """
    ItemForm: Used to generate forms for editing/creating new Items
    Inherits:
        Form (wtforms.Form): Form object from wtforms
    """
    name = StringField(
        'Item Name', [validators.DataRequired()], description=u"Item Name")
    description = StringField('Item Descrption', [
        validators.DataRequired()],
        description=u"Enter a product description")
    category = SelectField('Categories', choices=[])
    field_items = ["name", "description", "category"]
