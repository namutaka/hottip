import logging
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

LOGGER = logging.getLogger(__name__)

class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    """Adds a login requirement to graphQL API access via main endpoint."""

    @property
    def raise_exception(self):
        """非認証時にAjaxアクセスの場合は例外を発生させる
        Ajaxかどうか: headerに'X-Requested-With': 'XMLHttpRequest'があるか
        """
        return self.request.is_ajax()
