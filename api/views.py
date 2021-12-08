from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from graphene_django.views import GraphQLView


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


def home(request):
    return render(request, 'home.html')
