import urllib3                                  #! This file was created specifically only to test the API after making changes.
import json                                         #* Parts of this file can be used in the frontend later.
from http import HTTPStatus                             #I know about the standard tests.py files in DRF, but I find it more convenient to write it this way
from colorama import init, Fore, Style
import random
import string

http = urllib3.PoolManager()
init(autoreset=True)
Cstatus = []
url = "http://127.0.0.1:8000/"
BookName = ''.join(random.choices(string.ascii_letters, k=20))



def PrintStatus():
    for name, status in Cstatus:
        if status == "OK":
            status_colored = Fore.GREEN + status
        elif status == "SKIP":
            status_colored = Fore.YELLOW + status
        else:
            status_colored = Fore.RED + status
        print(f"{name:40} | {status_colored}")


def divider():
    print("-------------------------------------------------------------------------------------")



def CreateAdmin():
    HeadersAdmin = {
        "Content-Type": "application/json"
    }

    data_admin = {
        "username": "AdminTest",
        "email": "admintest@gmail.com",
        "password": "admintest",
        "is_admin": True
    }

    JsonAdmin = json.dumps(data_admin).encode("utf-8")

    response = http.request("POST", url + "api/v1/UserCreate/", body=JsonAdmin, headers=HeadersAdmin)

    if 200 <= response.status < 300:
        Cstatus.append(("Create user", "OK"))
    else:
        Cstatus.append(("Create user", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def UserCheck(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "username": "AdminTest"
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("GET", url + "api/v1/UserCheck/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("User check", "OK"))
    else:
        Cstatus.append(("User check", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def GetAccessToken():
    body = {
        "username": "AdminTest",
        "password": "admintest"
    }

    bodyjs = json.dumps(body).encode("utf-8")

    headers = {
        "Content-Type": "application/json"
    }

    response = http.request("POST", url + "api/v1/token/", body=bodyjs, headers=headers)
    
    if 200 <= response.status < 300:
        Cstatus.append(("Get access and refresh token", "OK"))
    else:
        Cstatus.append(("Get access and refresh token", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()

    data = json.loads(response.data)

    access = data["access"]
    refresh = data["refresh"]

    return access, refresh


def GetRefreshToken(refresh):
    body = {
        "refresh": refresh
    }

    bodyjs = json.dumps(body).encode("utf-8")

    headers = {
        "Content-Type": "application/json"
    }

    response = http.request("POST", url + "api/v1/token/refresh/", body=bodyjs, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Get refresh token", "OK"))
    else:
        Cstatus.append(("Get refresh token", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def GetBooksInfoShort(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    response = http.request("GET", url + "api/v1/BookPreviewView/", headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Get short book info", "OK"))
    else:
        Cstatus.append(("Get short book info", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def GetBooksInfoFull(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    response = http.request("GET", url + "api/v1/BookListView/", headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Get full book info", "OK"))
    else:
        Cstatus.append(("Get full book info", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def ExportExcel(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    response = http.request("GET", url + "api/v1/ExportBooksExcelView/", headers=headers)
    if 200 <= response.status < 300:
        Cstatus.append(("Export", "OK"))
    else:
        Cstatus.append(("Export", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()



    headers2 = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "title": "a"
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("GET", url + "api/v1/ExportBooksExcelView/", body=Json, headers=headers2)

    if 200 <= response.status < 300:
        Cstatus.append(("Export (param)", "OK"))
    else:
        Cstatus.append(("Export (param)", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def BookCreate(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "title": BookName,
        "img": "https://github.com",
        "reviews": "3",
        "content": "abc",
        "price": "12.00",
        "availability": "10",
        "reviews_count": "40",
        "genre": "15",
        "writed_at": "2010-10-15",
        "author": "Ben"
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("POST", url + "api/v1/BookCreate/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Create book", "OK"))
    else:
        Cstatus.append(("Create book", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def ImportBook(Access):
    print("Importing need ≈ 15-20 minutes")
    acception = input("Do you want to import books?(Y/N): ")
    divider()

    if acception == "Y" or acception == "y":
        headers = {
            "Authorization": f"Bearer {Access}",
            "Content-Type": "application/json"
        }

        response = http.request("POST", url + "api/v1/BooksImportView/", headers=headers)

        if 200 <= response.status < 300:
            Cstatus.append(("Import book", "OK"))
        else:
            Cstatus.append(("Import book", "ERROR"))
            print(f"{response.status} {HTTPStatus(response.status).phrase}")
            print(response.data.decode("utf-8"))
            divider()
    else:
        Cstatus.append(("Import book", "SKIP"))


def DeleteBook(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "title": BookName
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("DELETE", url + "api/v1/BookDelete/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Delete book", "OK"))
    else:
        Cstatus.append(("Delete book", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def BookRedact(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "title": BookName,
        "img": "https://github.com",
        "reviews": "3",
        "content": "abc" + "cdb",
        "price": "12.00",
        "availability": "10",
        "reviews_count": "40",
        "genre": "15",
        "writed_at": "2010-10-15",
        "author": "Ben"
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("PUT", url + "api/v1/BookRedact/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Redact book", "OK"))
    else:
        Cstatus.append(("Redact book", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def FilterGenreBook(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "genre": "15"
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("GET", url + "api/v1/BookGengesFilterView/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Filter books by genre", "OK"))
    else:
        Cstatus.append(("Filter books by genre", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def GetBookInfo(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "title": BookName,
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("PUT", url + "api/v1/BookRedact/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Get book info", "OK"))
    else:
        Cstatus.append(("Get book info", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()


def SendEmail(Access):
    print("You will need to delete the AdminTest account before starting again.")
    acception = input("Run the test Send email?(Y/N): ")
    divider()

    if acception == "Y" or acception == "y":
        headers = {
            "Authorization": f"Bearer {Access}",
            "Content-Type": "application/json"
        }

        data = {
            "username": "AdminTest",
            "email": "admintest@gmail.com"
        }

        Json = json.dumps(data).encode("utf-8")

        response = http.request("POST", url + "api/v1/UserEmailSendView/", body=Json, headers=headers)

        if 200 <= response.status < 300:
            Cstatus.append(("Send email", "OK"))
        else:
            Cstatus.append(("Send email", "ERROR"))
            print(f"{response.status} {HTTPStatus(response.status).phrase}")
            print(response.data.decode("utf-8"))
            divider()
    else:
        Cstatus.append(("Send email", "SKIP"))


def ChangePassword(Access):
    headers = {
        "Authorization": f"Bearer {Access}",
        "Content-Type": "application/json"
    }

    data = {
        "username": "AdminTest",
        "password": "admintest"
    }

    Json = json.dumps(data).encode("utf-8")

    response = http.request("PUT", url + "api/v1/UserPasswordChangeView/", body=Json, headers=headers)

    if 200 <= response.status < 300:
        Cstatus.append(("Change password", "OK"))
    else:
        Cstatus.append(("Change password", "ERROR"))
        print(f"{response.status} {HTTPStatus(response.status).phrase}")
        print(response.data.decode("utf-8"))
        divider()



CreateAdmin()
AccessToken, RefreshToken = GetAccessToken()
UserCheck(AccessToken)
GetRefreshToken(RefreshToken)
ImportBook(AccessToken)
BookCreate(AccessToken)
GetBooksInfoShort(AccessToken)
GetBooksInfoFull(AccessToken)
FilterGenreBook(AccessToken)
GetBookInfo(AccessToken)
BookRedact(AccessToken)
ExportExcel(AccessToken)
DeleteBook(AccessToken)
ChangePassword(AccessToken)
SendEmail(AccessToken)

PrintStatus()
