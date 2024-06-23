from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.http import FileResponse
import logging
from dotenv import load_dotenv
import os
from api import serializer as api_serializer
from api import models as api_models


load_dotenv()
logger = logging.getLogger(__name__)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = api_models.User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = api_serializer.RegisterSerializer
    logger.info(f'Зарегистрирован новый пользователь')


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = api_serializer.ProfileSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        profile = api_models.Profile.objects.get(user=user)
        return profile

class FileList(generics.ListAPIView):
    serializer_class = api_serializer.FileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        
        return api_models.File.objects.filter(by_user=user).order_by("-id") 
        

class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.FileSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
      
        user_id = request.data.get('by_user')
        filename = request.data.get('filename')
        file = request.data.get('file')
        user = api_models.User.objects.get(id=user_id)
        file = api_models.File.objects.create(
            by_user=user,
            filename=filename,
            file=file,
            
        )
        logger.info(f'Пользователь {user.username} загрузил файл {file.filename}')
        return Response({"message": "File has been uploaded successfully"}, status=status.HTTP_201_CREATED)
    
class FileDeleteAPIView(generics.DestroyAPIView):
    queryset = api_models.File.objects.all()
    serializer_class = api_serializer.FileSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f'Файл {instance} был удален')
        return Response(status=status.HTTP_204_NO_CONTENT)

class FileView(generics.RetrieveAPIView):
    queryset = api_models.File.objects.all()
    serializer_class = api_serializer.FileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

class FileDownloadView(generics.GenericAPIView):
    queryset = api_models.File.objects.all()

    def get(self, request, uid):
        print('uid', uid)
        file_obj = self.queryset.get(uid=uid)
        print(file_obj)
        print(file_obj.file.path)
        # response = HttpResponse(file_obj.file.path)
        file_download = open(file_obj.file.path, 'rb')
        response = FileResponse(file_download, as_attachment=True)
        response['Access-Control-Expose-Headers'] = 'Filename'
        # print(response)
        response['Content-Disposition'] = f'attachment; filename="{file_obj.filename}"'
        logger.info(f'Файл скачан {file_obj.filename}')
        return response


class FileView(generics.GenericAPIView):
    queryset = api_models.File.objects.all()

    def get(self, request, uid, *args, **kwargs):
        file_obj = self.queryset.get(uid=uid)
        file = open(file_obj.file.path, 'rb')
        response = FileResponse(file)
        return response
    


