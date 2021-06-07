from rest_framework import pagination
from rest_framework.response import Response

from collections import OrderedDict


def paginate(paginated_items, page, page_size=5):
    from django.core.paginator import Paginator

    """
    impelmentations for simple pagination
    returns:
        - page items
        - number of pages
        - number of items
    """
    paginator = Paginator(paginated_items, page_size)

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    return (items, paginator.num_pages, paginator.count)


class CustomPagination(pagination.PageNumberPagination):
    """
    customization of paginator response class
    """

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = request.query_params.get("page_size", self.page_size)
        return super(CustomPagination, self).paginate_queryset(
            queryset, request, view=None
        )

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("pages_number", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )
