"""
URL configuration for librarysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books.views import BookCRUDView, BookSearchPreviewView, BooksImportView, ExportBooksExcelView
from user.views import UserCreateView, UserCheckView, UserEmailSendView, UserPasswordChangeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),                                                #Admin

    #Books
    path('api/v1/BookCRUDView/', BookCRUDView.as_view()),                           #POST | DELETE | PUT | GET
    path('api/v1/BookPreviewView/', BookSearchPreviewView.as_view()),               #GET
    path('api/v1/BooksImportView/', BooksImportView.as_view()),                     #POST
    path('api/v1/ExportBooksExcelView/', ExportBooksExcelView.as_view()),           #GET
    
    #User
    path('api/v1/UserCreate/', UserCreateView.as_view()),                           #POST
    path('api/v1/UserCheck/', UserCheckView.as_view()),                             #GET
    path('api/v1/UserEmailSendView/', UserEmailSendView.as_view()),                 #POST
    path('api/v1/UserPasswordChangeView/', UserPasswordChangeView.as_view()),       #PUT
    
    #SimpleJWT
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #POST
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh') #POST
]
