import logging

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from .models import User, File
from .serializer import UserSerializer, RestrictedUserSerializer, FileSerializer


logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)
    
    def get_serializer_class(self):
        if not self.request.user.is_staff:
            return RestrictedUserSerializer
        return super().get_serializer_class()
    
    def get_object(self):
        if not self.request.user.is_staff:
            return User.objects.get(pk=self.request.user.pk)
        return super().get_object()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_message = f"User '{serializer.instance.username}' was successfully created."
            logger.info(response_message)
        except Exception as e:
            response_message = f"User '{serializer.instance.username}' was not created. Error: {e}."
            logger.error(response_message)
            return Response({'response': response_message}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        return Response({'response': response_message}, status=status.HTTP_201_CREATED, content_type='application/json')

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            password = request.data.get('password', None)
            
            if password:
                serializer = self.get_serializer(instance, data=request.data, partial=partial)

                if serializer.is_valid():
                    instance.set_password(password)
                    instance.save()
                    logger.info(f"Password for user '{instance.username}' was changed successfully.")
                    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_message = f"User '{instance.username}' was successfully updated."
            logger.info(response_message)
        except Exception as e:
            response_message = f"User '{instance.username}' was not updated. Error: {e}."
            logger.error(response_message)
            return Response({'response': response_message}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        return Response({'response': response_message}, status=status.HTTP_200_OK, content_type='application/json')

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(
                f"Function 'perform_update' failed. User '{serializer.instance.username}' was not updated. Error: {e}.")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response_message = f"User '{instance.username}' was successfully deleted."
            logger.info(response_message)
        except Exception as e:
            response_message = f"User '{instance.username}' was not deleted. Error: {e}."
            logger.error(response_message)
        return Response({'response': response_message}, status=status.HTTP_204_NO_CONTENT, content_type='application/json')



class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return File.objects.none()
        if user.is_staff:
            return File.objects.all()
        return File.objects.filter(by_user=user.id)


    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_message = f"File with id='{instance.id}' was successfully updated by user '{instance.by_user}'."
            logger.info(response_message)
        except Exception as e:
            response_message = f"File was not updated. Error: {e}."
            logger.error(response_message)
            return Response({'response': response_message},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='application/json')
        return Response({'response': response_message},
                            status=status.HTTP_200_OK,
                            content_type='application/json')

    def perform_update(self, serializer):
        new_filename = self.request.data.get("name", None)
        if new_filename:
            serializer.instance.new_filename = new_filename
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        
        for k, v in kwargs.items():
            for id in v.split(','):
                try:
                    obj = get_object_or_404(File, pk=int(id))
                    logger.info(
                        f"File '{obj.filename}' delete was initialized by user '{obj.by_user}'.")
                    self.perform_destroy(obj)
                    response_message = f"File '{obj.filename}' was successfully deleted by user '{obj.by_user}'."
                    logger.warning(response_message)

                except Exception as e:
                    response_message = f"File {obj.filename} was not deleted. Error: {e}."
                    logger.error(response_message)
                    return Response({'response': response_message},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    content_type='application/json')

        return Response({'response': response_message},
                        status=status.HTTP_204_NO_CONTENT,
                        content_type='application/json')