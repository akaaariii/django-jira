from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Task, Category, Profile
from django.contrib.auth.models import User
from . import custompermissions

# In Django rest_framework 'view' has generics and Model-view-set
# Model-view-set provide features of CRUD('Create', 'Read', 'Update', 'Delete').


# api/create    POST     *create newuser(username + password)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # プロジェクト全体では、settings.pyで指定した'REST_FRAMEWORK'で+JWTの認証を通ったuserのみ各Viewにアクセスできるように設定したが、
    # userを新規で作成する場合は誰でもアクセスできるようにする必要がるため、それをここで設定している　　
    permission_classes = (permissions.AllowAny,)

#    /users     GET      *get user's list
class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#    /loginuser GET      *get login user's info
class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    # ログインしているuser_objectを返して欲しい時は、get_object(self)を用いる
    def get_object(self):
        # request.userとは Django においてログインしているuserという意味を表している。
        # つまり、返り値としてログインしているユーザーのオブジェクトを返す。
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


#    /profile   POST/GET/PUT *create and update profiles
# ModelViewSet provide CRUD method and partial_update(一部更新)
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # perform_create => CRUD's 'CREATE' method
    def perform_create(self, serializer):
        # user_profileに'self.request.user'="ログインしているuserの情報"が自動的に格納される。)
        serializer.save(user_profile=self.request.user)

    # 以下は'DELETE' と 'Partial Update' を行わないように制御している。
    # destroy is corresponding CRUD's 'DELETE' method
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # partial_update(一部更新) ※'PATCH'は IT用語で'修正する'の意。
    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


#    /category  POST/GET *create new category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


#    /tasks     POST/GET/PUT/DELETE *implement Task's CRUD system
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission)

    def perform_create(self, serializer):
        # ownerに'self.request.user'="オーナーの情報"が動的に格納される。
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)