from django.db.models import Q
from typing import Sequence, Tuple
from django.http import HttpRequest
from django.db.models.query import QuerySet


def get_search_query(request: HttpRequest, param_name: str = 'q') -> str:
    """
    Extracts and normalizes the search query string from HTTP request GET parameters.
    """
    if not request or not hasattr(request, 'GET'):
        return ''
    query = request.GET.get(param_name, '')
    if isinstance(query, str):
        return query.strip()
    return ''


def filter_queryset(
    queryset: QuerySet,
    query_string: str,
    search_fields: Sequence[str],
    split_words: bool = True,
    operator: str = 'AND',
    distinct: bool = True,
) -> QuerySet:
    """
    Filters a Django QuerySet across multiple search fields using case-insensitive lookups (icontains).

    Parameters:
    - queryset: The base Django QuerySet to filter.
    - query_string: The user-entered search string.
    - search_fields: Sequence of field names/lookups (e.g., ['first_name', 'last_name', 'email', 'tag']).
    - split_words: If True, splits multi-word query strings into individual terms.
    - operator: 'AND' (all terms must match across any field) or 'OR' (any term matching any field).
    - distinct: If True, calls .distinct() on the resulting QuerySet.

    Returns:
    - Filtered QuerySet.
    """
    if not query_string or not search_fields:
        return queryset

    query_string = str(query_string).strip()
    if not query_string:
        return queryset

    if split_words:
        terms = [term for term in query_string.split() if term]
    else:
        terms = [query_string]

    if not terms:
        return queryset

    overall_query = None

    for term in terms:
        # Match term across any of the search_fields (OR logic across fields)
        term_query = None
        for field in search_fields:
            lookup = f"{field}__icontains"
            field_q = Q(**{lookup: term})
            term_query = field_q if term_query is None else (term_query | field_q)

        if overall_query is None:
            overall_query = term_query
        else:
            if operator.upper() == 'OR':
                overall_query = overall_query | term_query
            else:
                overall_query = overall_query & term_query

    if overall_query is not None:
        queryset = queryset.filter(overall_query)
        if distinct:
            queryset = queryset.distinct()

    return queryset


class ModelSearcher:
    """
    Reusable Searcher helper class for models.
    Can be configured per model/view and reused across apps.

    Usage:
        contact_searcher = ModelSearcher(['first_name', 'last_name', 'email', 'tag'])
        contacts, search_query = contact_searcher.search(request, Contact.objects.all())
    """

    def __init__(self, search_fields: Sequence[str], param_name: str = 'q', split_words: bool = True):
        self.search_fields = list(search_fields)
        self.param_name = param_name
        self.split_words = split_words

    def get_query(self, request: HttpRequest) -> str:
        return get_search_query(request, self.param_name)

    def filter(self, queryset: QuerySet, query_string: str) -> QuerySet:
        return filter_queryset(
            queryset,
            query_string,
            search_fields=self.search_fields,
            split_words=self.split_words,
        )

    def search(self, request: HttpRequest, queryset: QuerySet) -> Tuple[QuerySet, str]:
        query_string = self.get_query(request)
        filtered_qs = self.filter(queryset, query_string)
        return filtered_qs, query_string
