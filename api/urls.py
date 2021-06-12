from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, CategoryViewSet, CreateUserView, ListUserView, LoginUserView, ProfileViewSet

# Here is Routing(紐付け) 'View' and 'Url'
# REST API Endpoint
# api/create    POST                 *create newuser(username + password)
#    /users     GET                  *get user's list
#    /loginuser GET                  *get login user's info
#    /category  POST/GET             *create new category
#    /profile   POST/GET/PUT         *create and update profiles
#    /tasks     POST/GET/PUT/DELETE  *implement Task's CRUD system


# ModelViewSet を継承したViewは'router' part で管理
router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('tasks', TaskViewSet)
router.register('profile', ProfileViewSet)

# generics系は 'Urlpatterns'に追記する決まりになっている
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('users/', ListUserView.as_view(), name='users'),
    path('loginuser/', LoginUserView.as_view(), name='loginuser'),
    path('', include(router.urls))
]