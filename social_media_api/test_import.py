from rest_framework import generics
print("Does generics have get_object_or_404?", hasattr(generics, 'get_object_or_404'))

from django.shortcuts import get_object_or_404
print("get_object_or_404 is from django.shortcuts")
