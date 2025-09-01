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
from books.views import BookCreateView, BookListView, BookPreviewView, BookGengesFilterView, BookDeleteView, BookShowByTitleView, BookRedactView
from user.views import UserCreateView, UserCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/BookCreate/', BookCreateView.as_view()),
    path('api/v1/BookListView/', BookListView.as_view()),
    path('api/v1/BookPreviewView/', BookPreviewView.as_view()),
    path('api/v1/BookGengesFilterView/', BookGengesFilterView.as_view()),
    path('api/v1/BookDelete/', BookDeleteView.as_view()),
    path('api/v1/BookShowByTitle/', BookShowByTitleView.as_view()),
    path('api/v1/BookRedact/', BookRedactView.as_view()),

    path('api/v1/UserCreate/', UserCreateView.as_view()),
    path('api/v1/UserCheck/', UserCheckView.as_view())
]
