import pymongo
def getAllMenu(connection):
    menu = connection.db.menu
    try:
        return menu.find_one()
    except:
        return False


def getlastWeekMenu(connection):
    lastweek = connection.db.history
    try:
        return lastweek.find_one()
    except:
        return False


def addLastWeekMenuInDb(connection, model):
    menuitem = connection.db.history
    try:
        menuitem.insert(model)
    except:
        return False
    return True

def updateLastWeekMenuInDb(connection, model, id):
    myquery ={'id': id}
    menuitem = connection.db.history
    try:
        id = menuitem.update_one({'id':1}, {'$set': model})
    except():
        return False
    return True




def addMenuInDb(connection, model):
    menuitem = connection.db.menu
    try:
        id = menuitem.insert(model)
    except:
        return False
    return True

def updateMenuInDb(connection, model, id):
    myquery ={'id': id}
    menuitem = connection.db.menu
    try:
        id = menuitem.update_one({'id':1}, {'$set': model})
    except():
        return False
    return True




