import sys
import requests


def getBasis(token):
    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/get_data/get_training_basis",
                    headers=header)
    data = r.json()
    return data

def getForms(token):
    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/get_data/get_training_forms",
                    headers=header)
    data = r.json()
    return data

def getLevelSource(token):
    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/get_data/get_level_source",
                    headers=header)
    data = r.json()
    return data

def getLevel(token):
    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/get_data/get_level",
                    headers=header)
    data = r.json()
    return data

def getStateCategory(token):
    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/get_data/get_state_category",
                    headers=header)
    data = r.json()
    return data

def getComp(token):
    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/get_data/get_type_in_comp",
                    headers=header)
    data = r.json()
    return data


def rezNationalityFunc(tmp):
    if tmp == 'Россия':
        return 1
    elif tmp == 'СНГ, бюджет' or tmp == 'СНГ, платно' or 'СНГ, контракт':
        return 2
    else:
        return 3


def rezOldEducationFunc(tmp):
    if tmp == 'Среднее c 2014 года' or tmp =='Основное среднее' or 'Восьмилетнее образование (до 1991)':
        return 1
    elif tmp == 'Техникум' or tmp == 'Политехническое училище' or tmp == 'Среднее до 2014 года':
        return 2
    else:
        return 3

def rezLevelFunc(tmp):
    if tmp == 'СПО':
        return 4
    elif tmp == "Бакалавриат":
        return 1
    elif tmp == 'Магистратура':
        return 2
    else:
        return 3

def rezTrainingFormsFunc(tmp):
    if tmp == 'очная форма обучения':
        return 1
    elif tmp == "заочная форма обучения":
        return 2
    else:
        return 3

def rezPrivilegesFunc(tmp):
    if tmp == "На общих основаниях":
        return 2
    else:
        return 1


def getData(token):
    basis = getBasis(token)
    Forms = getForms(token)
    LevelSource = getLevelSource(token)
    Level = getLevel(token)
    Category = getStateCategory(token)
    Comp = getComp(token)

    header = {'Accept': 'application/json','Content-Type': 'application/json','X-Apikey' : token}
    r = requests.get("https://api.ciu.nstu.ru/v1.1/abitbot/data/DF93D593CA0324D2E0530718000A928D",
                    headers=header)
    data = r.json()
    rezCat = rezLevelSource = rezLevel = rezTrainingForms = rezTrBasis = rezInComp = 0

    for el in Category:
        if el['ID'] == data[0]['ID_STATE_CATEGORY']:
            rezCat = rezNationalityFunc(el['NAME'])

    for el in LevelSource:
        if el['ID'] == data[0]['IS_LEVEL_SOURCE']:
            rezLevelSource = rezOldEducationFunc(el['NAME'])

    for el in Level:
        if el['ID'] == data[0]['ID_LEVEL']:
            rezLevel = rezLevelFunc(el['NAME'])

    for el in Forms:
        if el['ID'] == data[0]['ID_TRAINING_FORMS']:
            rezTrainingForms = rezTrainingFormsFunc(el['NAME'])

    for el in basis:
        if el['ID'] == data[0]['ID_TRAINING_BASIS']:
            rezTrBasis = el['NAME']

    for el in Comp:
        if el['ID'] == data[0]['ID_TYPE_IN_COMP']:
            rezInComp = rezPrivilegesFunc(el['NAME'])

    rezult = {'nationality': rezCat, 'direction': rezTrainingForms, 'oldeducation': rezLevelSource, 'level': rezLevel,'privileges': rezInComp, 'resthelth': 2 }

    return rezult
