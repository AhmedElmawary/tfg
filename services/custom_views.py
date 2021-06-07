from rest_framework import viewsets

from services.exceptions import HttpError

import json


class FilterSearch(viewsets.GenericViewSet):
    """ add filters and search functionality to a view """

    def filter(self, queryset):
        try:
            query_params = self.request.query_params

            filter_dict = {}
            current_parameter = None
            for parameter, value in query_params.items():
                current_parameter = parameter
                if parameter in self.filter_flag_fields:
                    if value == "true":
                        filter_dict[parameter] = True
                    elif value == "false":
                        filter_dict[parameter] = True
                    else:
                        raise ValueError
                if parameter in self.filter_fields:
                    filter_dict[parameter] = value

            queryset = queryset.filter(**filter_dict)
        except AttributeError as e:
            pass
        except ValueError as e:
            raise HttpError(
                {"details": ["please fix %s in query string." % parameter]}, status=400
            )
        return queryset

    def search(self, queryset):
        try:
            request = self.request
            if request.query_params.get("search", False):
                search_param_arr = request.query_params.get("search").split()
                query = []
                for search_field in self.search_fields:
                    query.append(
                        reduce(
                            operator.and_,
                            [
                                Q(**{search_field + "__icontains": search_param})
                                for search_param in search_param_arr
                            ],
                        )
                    )

                queryset = queryset.filter(reduce(operator.or_, query))
        except AttributeError as e:
            pass
        return queryset

    def get_queryset(self):
        queryset = super(FilterSearch, self).get_queryset()
        queryset = self.filter(queryset)
        queryset = self.search(queryset)
        return queryset
