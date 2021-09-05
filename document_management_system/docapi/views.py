from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from document_manager.models import Document
from .serializers import DocumentSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

@api_view(['GET'])
def indexView(request):
	url_list = {
		'api/':'List all urls',
		'api/docs/<pk>': 'GET,PUT,POST,OPTIONS',
	}

	return Response(url_list)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def docList(request):
# 	# breakpoint()
# 	docList  = Document.objects.filter(user=request.user)

# 	serializer = DocumentSerializer(docList, many=True)

# 	return Response(serializer.data)

class DocumentViewSet(viewsets.ModelViewSet):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	serializer_class = DocumentSerializer
	# queryset = Document.objects.all()

	def get_queryset(self, *args, **kwargs):
		return Document.objects.filter(user=self.request.user)



# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def yearList(request, year):
# 	# breakpoint()
# 	user_docs = Document.objects.filter(user=request.user)
# 	yearList  = user_docs.filter(created_at__year=year)
# 	print(yearList)
# 	serializer = DocumentSerializer(yearList, many=True)

# 	return Response(serializer.data)



# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def docDetail(request, pk):
# 	# breakpoint()
# 	user_docs = Document.objects.filter(user=request.user)
# 	yearList  = user_docs.get(id=pk)

# 	serializer = DocumentSerializer(yearList, many=False)

# 	return Response(serializer.data)



# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def docCreate(request):
# 	# breakpoint()
# 	serializer = DocumentSerializer(data=request.data)

# 	if serializer.is_valid():
# 		serializer.save()

# 	return Response(serializer.data)


# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def docUpdate(request, pk):
# 	user_docs = Document.objects.filter(user=request.user)
# 	doc = user_docs.get(id=pk)
	
# 	#instance is used to define the object we wanna update value for
# 	serializer = DocumentSerializer(data=request.data, instance=doc) 

# 	if serializer.is_valid():
# 		serializer.save()

# 	return Response(serializer.data)