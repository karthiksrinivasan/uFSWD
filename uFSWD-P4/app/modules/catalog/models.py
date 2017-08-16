from app import db_connector as db
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_sqlalchemy import BaseQuery


class Category(db.Model):
    """
    Category: Database ORM to work categories table
    Inherits:
        Model (SQLAlchemy.Model): Model object from SQLAlchemy
    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), unique=True)
    created_by = db.Column(db.String(100))

    def __init__(self, name, created_by):
        """
        __init__: Constructor for Class Category
        Args:
            name (str): Category Name
            created_by (str): Creator's email id
        Returns:
            Category Object
        """
        self.category_name = name
        self.created_by = created_by


class Item(db.Model):
    """
    Item: Database ORM to work items table
    Inherits:
        Model (SQLAlchemy.Model): Model object from SQLAlchemy
    """
    __tablename__ = "items"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name = db.Column(db.String(50))
    created_by = db.Column(db.String(100))
    item_desc = db.Column(db.Text)
    cat_id = db.Column(db.Integer, db.ForeignKey(
        "categories.id"), nullable=False)
    category = db.relationship('Category', backref='items', uselist=False)
    __table_args__ = (db.UniqueConstraint(
        'item_name', 'cat_id', name='item_category'),)

    def __init__(self, name, desc, cat_name, created_by):
        """
        __init__: Constructor for Class Category
        Args:
            name (str): Item Name
            desc (str): Description
            cat_name (str): Category Name
            created_by (str): Creator's email id
        Returns:
            Item Object
        """
        self.item_name = name
        self.item_desc = desc
        self.created_by = created_by
        cat_id = DB_Operations.getCategoryID(cat_name)
        if cat_id == -1:
            raise Exception("Invalid category name")
        self.cat_id = cat_id


class DB_Operations():
    """
    DB_Operations: A wrapper class for DB Operations
    """
    @staticmethod
    def checkIfCategoryExists(name):
        """
        checkIfCategoryExists: Function to check if a category exists
        Args:
            name (str): Category Name
        Returns:
            True if category exists else False
        """
        result = db.session.query(Category).filter(
            Category.category_name == name).all()
        return False if len(result) == 0 else True

    @staticmethod
    def getCategoryID(name):
        """
        getCategoryID: Function to retrieve Category ID based on Category name
        Args:
            name (str): Category Name
        Returns:
            Category ID (int)
        """
        result = db.session.query(Category).filter(
            Category.category_name == name).all()
        return -1 if len(result) == 0 else result[0].id

    @staticmethod
    def getCategory(name):
        """
        getCategory: Function to retrieve Category based on Category name
        Args:
            name (str): Category Name
        Returns:
            Category Object
        """
        result = db.session.query(Category).filter(
            Category.category_name == name).all()
        return result[0]

    @staticmethod
    def getListOfCategory():
        """
        getListOfCategory: Function to retrieve list of categories
        Returns:
            List of categories (list)
        """
        result = db.session.query(Category).all()
        return [cat.category_name for cat in result]

    @staticmethod
    def addCategory(name, created_by):
        """
        addCategory: Function to add a new category
        Args:
            name (str): Category Name
            created_by (str): Creator's email id
        Returns:
            None
        """
        new_category = Category(name, created_by)
        db.session.add(new_category)
        db.session.commit()

    @staticmethod
    def editCategory(oldname, newname):
        """
        editCategory: Function to edit category
        Args:
            oldname (str): Previous Category Name
            newname (str): New Category Name
        Returns:
            None
        """
        category = db.session.query(Category).filter(
            Category.category_name == oldname).all()[0]
        category.category_name = newname
        db.session.commit()

    @staticmethod
    def deleteCategory(name):
        """
        deleteCategory: Function to delete a category
        Args:
            name (str): Category Name
        Returns:
            None
        """
        category = db.session.query(Category).filter(
            Category.category_name == name).all()[0]
        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def addItem(name, description, category, created_by):
        """
        addItem: Function to add a new item
        Args:
            name (str): Item Name
            description (str): Item description
            category (str): Item category name
            created_by (str): Creator's email id
        Returns:
            None
        """
        new_item = Item(name, description, category, created_by)
        db.session.add(new_item)
        db.session.commit()

    @staticmethod
    def editItem(id, name, description, category):
        """
        editItem: Function to edit a item
        Args:
            id (str): Item ID
            description (str): Item description
            category (str): Item category name
        Returns:
            None
        """
        item = DB_Operations.getItem(id)
        item.item_name = name
        item.item_desc = description
        item.cat_id = DB_Operations.getCategoryID(category)
        db.session.commit()

    @staticmethod
    def deleteItem(id):
        """
        deleteItem: Function to delete a item
        Args:
            id (str): Item ID
        Returns:
            None
        """
        item = DB_Operations.getItem(id)
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def getRecentItems(limit=5):
        """
        getRecentItems: Function to retrieve list of recent items
        Args:
            limit (int) : Number of recent items to retrieve
        Returns:
            list of items (list)
        """
        result = db.session.query(Item).order_by(
            Item.id.desc()).limit(limit).all()
        return result

    @staticmethod
    def getItem(item_id):
        """
        getItem: Function to retrieve item based on Item id
        Args:
            id (str): Item ID
        Returns:
            Item object
        """
        result = db.session.query(Item).filter(Item.id == item_id).all()
        return result[0]

    @staticmethod
    def getItemsByCategory(cat_name):
        """
        getItemsByCategory: Function to retrieve items based on category_name
        Args:
            cat_name (str): Category Name
        Returns:
            list of Item Object (list)
        """
        cat_id = DB_Operations.getCategoryID(cat_name)
        result = db.session.query(Item).filter(Item.cat_id == cat_id).all()
        return result

    @staticmethod
    def checkIfItemExists(item):
        """
        checkIfItemExists: Function to check if a item exists
        Args:
            item (Item): Item Object
        Returns:
            True if item exists else False
        """
        result = db.session.query(Item) \
            .filter(Item.item_name == item.item_name) \
            .filter(Item.cat_id == item.cat_id).all()
        return False if len(result) == 0 else True
