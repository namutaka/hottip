"""hottip_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from graphene_django.views import GraphQLView
from hottip.views import PrivateGraphQLView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', PrivateGraphQLView.as_view(graphiql=True)),

    # デバッグ用認証不要Graphql
    path('internal/graphql', GraphQLView.as_view(graphiql=True)),

    # login,logoutのURLは別で指定されるためそれを避けるパス定義にする
    # static リソースは別
    re_path(r'^(?!admin|static).*$', TemplateView.as_view(template_name="hottip/index.html")) 
]
