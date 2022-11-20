import re
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == "__main__":
    # user = "Client6"
    # name = "Сергей"
    # email = "email8@gmail.com"
    # print(bool(re.search("[а-яА-Я]", name)))
    # print(bool(re.search("[0-9a-z,A-Z]", user)))
    # re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)
    # print(bool(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)))
    # print(str(date.today().day) + " " + str(date.today().month) + " " + str(date.today().year))
    # print(float("3423.353"))
    # print(int("00000000000"))
    psw = generate_password_hash("123456")
    print(psw)