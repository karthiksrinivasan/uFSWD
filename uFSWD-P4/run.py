#!env/bin/python
from flask_script import Manager
from app import server, db_connector
from app.modules.catalog.models import *
manager = Manager(server)


@manager.command
def db_initialize():
    """Creates the db tables."""
    db_connector.create_all()
    creator_emailid = "admin@item_catalog.com"
    categories = [Category("Soccer", creator_emailid),
                  Category("Basketball", creator_emailid),
                  Category("Baseball", creator_emailid),
                  Category("Frisbee", creator_emailid),
                  Category("Snowboarding", creator_emailid),
                  Category("Rock Climbing", creator_emailid),
                  Category("Foosball", creator_emailid),
                  Category("Skating", creator_emailid),
                  Category("Hockey", creator_emailid)]
    [db_connector.session.add(cat) for cat in categories
        if not DB_Operations.checkIfCategoryExists(cat.category_name)]
    items = [Item("Stick", "Hockey Stick", "Hockey",creator_emailid),
             Item("Basketball Hoop", "Large basketball hoop", "Basketball",
                  creator_emailid),
             Item("Basketball Shorts", "Mens basketball shorts", "Basketball",
                  creator_emailid),
             Item("Baseball ball", "Adults baseball ball", "Baseball",
                  creator_emailid),
             Item("Baseball bat", "Adults baseball bat", "Baseball",
                  creator_emailid),
             Item("Baseball helmet", "Adults baseball helmet", "Baseball",
                  creator_emailid),
             Item("Baseball gloves", "Adults baseball gloves", "Baseball",
                  creator_emailid),
             Item("Soccer ball", "Football", "Soccer",
                  creator_emailid),
             Item("Goggles", "Snowboarding Goggles", "Snowboarding",
                  creator_emailid),
             Item("Snowboard", "Snowboarding board", "Snowboarding",
                  creator_emailid),
             Item("Anchor", "Anchor for rock climbing", "Rock Climbing",
                  creator_emailid),
             Item("Hook", "Hook for rock climbing", "Rock Climbing",
                  creator_emailid),
             Item("Foosball table", "1v1 Foosball table", "Foosball",
                  creator_emailid),
             Item("Rollerblades", "Rollerblades", "Skating",
                  creator_emailid),
             Item("In-line skates", "in-line skates", "Skating",
                  creator_emailid)]

    [db_connector.session.add(itm) for itm in items
        if not DB_Operations.checkIfItemExists(itm)]
    db_connector.session.commit()


if __name__ == '__main__':
    manager.run()
