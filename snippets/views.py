# _*_ coding:UTF-8 _*_
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
import django_filters
from weichat.models import *

# class SnippetList(APIView):
#   def get(self, request, format=None):
#       snippets = Snippet.objects.all()
#       serializer = SnippetSerializer(snippets, many=True)
#       return Response(serializer.data)
#   #@csrf_exempt
#   def post(self, request, format=None):
#       serializer = SnippetSerializer(data=request.data)
#       if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data, status=status.HTTP_201_CREATED)
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#   def get_object(self,pk):
#       try:
#           return Snippet.objects.get(pk=pk)
#       except Snippet.DoesNotExist:
#           raise Http404

#   def get(self,request,pk,format=None):
#       Snippet = self.get_object(pk)
#       serializer = SnippetSerializer(Snippet)
#       return Response(serializer.data)

#   def put(self,request,pk,format=None):
#       snippet = self.get_object(pk)
#       serializer = SnippetSerializer(snippet,data = request.data)
#       if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data)
#       return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#   def delete(self,request,pk,format=None):
#       snippet = self.get_object(pk)
#       snippet.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)


# class UserList(generics.ListAPIView):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer
#   permission_classes = (permissions.IsAuthenticated,)

# class UserDetail(generics.RetrieveAPIView):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer
#   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class SnippetList(generics.ListCreateAPIView):
#   queryset = Snippet.objects.all()
#   serializer_class = SnippetSerializer
#   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#   def pre_save(self,obj):
#       obj.owner = self.request.user

# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#   queryset = Snippet.objects.all()
#   serializer_class = SnippetSerializer
#   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#   def pre_save(self,obj):
#       obj.owner = self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, permissions.IsAuthenticated)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title', 'linenos', 'language', 'owner__username')

    def perform_update(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(owner=self.request.user)

        serializer.save(owner=User.objects.get(pk=1))

        # pass

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(owner=self.request.user)
        serializer.save(owner=User.objects.get(pk=1))


# class MsgViewSet(viewsets.ModelViewSet):
#   queryset = Messges.objects.all()
#   serializer_class = MessagesSerializer
