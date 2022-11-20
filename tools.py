import re
from db import GasStationDB


def checkInfo(firstName, lastName, username, date, email, phone, oldUsername, oldEmail, oldPhone):
    errors = []
    toDB = GasStationDB()
    if len(firstName) == 0 or len(lastName) == 0 or len(username) == 0 or len(date) == 0 or len(email) == 0 or len(
            phone) == 0:
        errors.append("все поля должны быть заполнены")
        return errors
    if checkName(firstName) is False:
        errors.append("имени")
    if checkName(lastName) is False:
        errors.append("фамилии")
    if checkDate(date) is False:
        errors.append("даты")
    if checkEmail(email) is False:
        errors.append("email`a")
    if checkPhone(phone) is False:
        errors.append("номера телефона")
    if checkUsername(username) is False:
        errors.append("username`a")
    if oldEmail != email:
        if toDB.checkEmail(email) is False:
            errors.append("email`a(пользователь с таким email`ом уже существует)")
    if oldUsername != username:
        if toDB.checkUsername(username) is False:
            errors.append("username`a(пользователь с таким username`ом уже существует)")
    if oldPhone != phone:
        if toDB.checkPhone(phone) is False:
            errors.append("номер телефона`a(пользователь с таким номером телефона уже существует)")
    return errors


def checkPassword(pass1, pass2):
    errors = []
    if 6 > len(pass1) or len(pass1) > 31:
        errors.append("пароль должен содержать не менее 6 символов, но не более 30")
    if bool(re.search("[0-9a-z,A-Z_-]", pass1)) is False:
        errors.append("пароль должен содержать только цифры, буквы английского алфавита а также _ и -")
    if pass1 != pass2:
        errors.append("пароли не совпадают")
    return errors


def checkUsername(name):
    return bool(re.search("[0-9a-z,A-Z]", name)) and 2 < len(name) < 30


def checkPhone(phone):
    return len(phone) == 11


def checkName(name):
    return bool(re.search("[а-яА-Я]", name)) and 2 < len(name) < 30


def checkEmail(email):
    return bool(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))


def checkDate(date):
    result = re.findall("(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/([1-2][0-9]{3})", date)
    return len(result) != 0


def changeDateToOutput(date):
    return date[-2] + date[-1] + date[5:7:1] + date[0:4:1]
