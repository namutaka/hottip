from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    """Adds a login requirement to graphQL API access via main endpoint."""
    pass

