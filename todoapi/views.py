from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Todo
from .serializers import TodosSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET'])
def ListTodo(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10 
    todos = Todo.objects.all()
    result = paginator.paginate_queryset(todos, request)
    serializer = TodosSerializer(result, many=True)
    data = {
        'error': False,
        'message': "success get data",
        'data': serializer.data,
        'limit': paginator.page_size,
        'total': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        
    }
    return Response(data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def DetailTodo(request, pk):
    try:
        todos = Todo.objects.get(id=pk)
    except ObjectDoesNotExist:
        data = {
            'error': True,
            'message': "data not found",
            'data': {}
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    serializer = TodosSerializer(todos, many=False)
    data = {
        'error': False,
        'message': "success get data",
        'data': serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def CreateTodo (request):
    serializer = TodosSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            'error': False,
            'message': "success create data",
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            'error': True,
            'message': "failed create data",
            'data': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def UpdateTodo (request, pk):
    try:
        todos = Todo.objects.get(id=pk)
    except ObjectDoesNotExist:
        data = {
            'error': True,
            'message': "data not found",
            'data': {}
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    serializer = TodosSerializer(instance=todos, data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            'error': False,
            'message': "success update data",
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {
            'error': True,
            'message': "failed update data",
            'data': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def DeleteTodo (request, pk):
    try:
        todos = Todo.objects.get(id=pk)
    except ObjectDoesNotExist:
        data = {
            'error': True,
            'message': "data not found"
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    todos.delete()
    data = {
        'error': False,
        'message': "success delete data",
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ToggleCompletedStatus(request, pk):
    try:
        todos = Todo.objects.get(id=pk)
    except ObjectDoesNotExist:
        data = {
            'error': True,
            'message': "data not found",
            'data': {}
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    todos.completed = not todos.completed
    todos.save()
    serializer = TodosSerializer(instance=todos)
    data = {
        'error': False,
        'message': "success toggle status",
        'data': serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)