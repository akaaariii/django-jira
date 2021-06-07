from django.urls import path, include
from rest_framework import routers

# Here is Routing(紐付け) 'View' and 'Url'
# REST API Endpoint
# api/create    POST     *create newuser(username + password)
#    /users     GET      *get user's list
#    /loginuser GET      *get login user's info
#    /category  POST     *create new category
#    /profile   POST/PUT *create and update profiles
#    /tasks     POST/GET/PUT/DELETE *implement Task's CRUD system


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls))
]