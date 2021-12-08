from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

from . import views
from .views import PrivateGraphQLView

urlpatterns = [
    path("", views.home, name='home'),
    # path("login/", views.login_user, name='login_user'),
    # path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^graphql', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path("privategraphql", PrivateGraphQLView.as_view(graphiql=True)),
]
