from flask import Flask, json, Response, jsonify
import json
from flask import request
import pymongo
import business.data as dataHandler
import  random

def getMenu(mongo):
    allMenu = dataHandler.getAllMenu(mongo)
    if allMenu is not None:
        newMenu = {
            'id':1,
            'breakfast':"",
            "lunch":"",
            "dinner":""
        }

        menu ={
            'breakfast':"",
            "lunch":"",
            "dinner":""
        }
        if allMenu['breakfast'] is None:
            menu['breakfast'] = ""
        else:
            menu['breakfast'] =allMenu['breakfast']

        if allMenu['lunch'] is None:
            menu['lunch'] = ""
        else:
            menu['lunch'] = allMenu['lunch']

        if allMenu['dinner'] is None:
            menu['dinner'] = ""
        else:
            menu['dinner'] = allMenu['dinner']

        lastWeekMenu = getLastWeekMenu(mongo)

        if lastWeekMenu is False:
            thisWeekBreakfast = createMenuFirstTime(allMenu['breakfast'],'breakfast')
            thisWeekLunch = createMenuFirstTime(allMenu['lunch'],'lunch')
            thisWeekDinner = createMenuFirstTime(allMenu['dinner'],'dinner')
            newMenu['breakfast'] = thisWeekBreakfast
            newMenu['lunch'] = thisWeekLunch
            newMenu['dinner'] = thisWeekDinner
            message = newMenu
            dataHandler.addLastWeekMenuInDb(mongo,newMenu)
            return Response(json.dumps(newMenu, default=str),status=200,mimetype='application/json')
        else:
            thisWeekBreakfast = createMenuForThisWeek(lastWeekMenu['breakfast'], allMenu['breakfast'], 'breakfast')
            thisWeekLunch = createMenuForThisWeek(lastWeekMenu['lunch'], allMenu['lunch'], 'lunch')
            thisWeekDinner = createMenuForThisWeek(lastWeekMenu['dinner'], allMenu['dinner'],'dinner')
            newMenu['breakfast']=thisWeekBreakfast
            newMenu['lunch'] = thisWeekLunch
            newMenu['dinner'] = thisWeekDinner
        dataHandler.updateLastWeekMenuInDb(mongo,newMenu,1)
        return Response(json.dumps(newMenu,default=str ),status=200,mimetype='application/json')
    else:
        return onError("Menu is not added. Please upload the full menu first")

def getLastWeekMenu(mongo):
    allMenu = dataHandler.getlastWeekMenu(mongo)
    if allMenu is None:
        return False
    else:
        return allMenu


def addMenu(mongo, request):
    data = request.get_json()
    addData = {
        'id': 1,
        'breakfast': "",
        'lunch': "",
        'dinner': ""
    }
    addData['breakfast'] = data['breakfast']
    addData['lunch'] = data['lunch']
    addData['dinner'] = data['dinner']
    result = dataHandler.addMenuInDb(mongo,addData)
    if result:
        return jsonify("Added "),201
    else:
        return jsonify("Faild"), 402

def updateMenu(mongo,request):
    data = request.get_json()
    addData = {
        'id':1,
        'breakfast':"",
        'lunch': "",
        'dinner': ""
    }
    addData['breakfast']= data['breakfast']
    addData['lunch'] = data['lunch']
    addData['dinner'] = data['dinner']
    result = dataHandler.updateMenuInDb(mongo,addData,1)
    if result:
        return jsonify("Updated "),204
    else:
        return jsonify("Faild"), 402


def createMenuForThisWeek(lastweek,allMenu, menuType):
    if menuType != 'dinner':
        newMenu = []
        i = 0
        flag = False
        if menuType == 'lunch':
            itemsNotInLastWeek = list(set(allMenu)-set(lastweek))
            while(i< 2):
                item = random.choice(itemsNotInLastWeek)
                if newMenu.__contains__(item):
                    continue
                else:
                    newMenu.append(item)
                    i = i + 1

        if menuType == 'breakfast':
            while (i < 7):
                itemsNotInLastWeek = list(set(allMenu) - set(lastweek))
                item = (random.choice(itemsNotInLastWeek))
                if str(item).lower() == 'dosa' or str(item).lower()=='idili' and flag == True:
                    continue
                if str(item).lower() == 'dosa' or str(item).lower() == 'idili' and flag == False:
                    if newMenu.__contains__(item):
                        continue
                    else:
                        newMenu.append(item)
                        flag == True
                        i=i+1
                else:
                    if newMenu.__contains__(item):
                        continue
                    else:
                        newMenu.append(item)
                        i = i + 1
    else:
        newMenu = {}
        salad = lastweek["Salad"]
        mains = lastweek['Main']
        saladAllMenu = allMenu['Salad']
        mainAllMenu = allMenu['Mains']
        itemsNotInLastWeekSalad = list(set(saladAllMenu) - set(salad))
        itemsNotInLastWeekMains = list(set(mainAllMenu) - set(mains))
        newMenu['Main'] = random.choice(itemsNotInLastWeekMains)
        newMenu['Salad'] = random.choice(itemsNotInLastWeekSalad)

    return newMenu

def createMenuFirstTime(allmenu,menuType):

    if menuType != 'dinner':
        newMenu = []
        i = 0
        flag = False
        if menuType == 'lunch':
            while i<2:
                item = (random.choice(allmenu))
                if newMenu.__contains__(item):
                    continue
                else:
                    newMenu.append(item)
                    i=i+1
        if menuType == 'breakfast':
            while (i < 7):
                item =(random.choice(allmenu))
                if str(item).lower() == 'dosa' or str(item).lower() =='idili':
                    if flag == True:
                        continue
                if str(item).lower() == 'dosa' or str(item).lower() =='idili':
                    if flag == False:
                        newMenu.append(item)
                        flag ==True
                else:
                    newMenu.append(item)
                i=i+1
        return newMenu
    else:
        newMenu= {}
        salad = allmenu["Salad"]
        mains = allmenu['Mains']
        newMenu['Main'] =  random.choice(salad)
        newMenu['Salad'] = random.choice(mains)
    return newMenu


def onError(error = None):
    message = {
        'errorcode':'101',
        'error_message':error
    } 
    responseMessage = jsonify(message)
    responseMessage.status_code = 403
    return responseMessage  




