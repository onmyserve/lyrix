from datetime import timedelta
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from django.db.models import QuerySet, Q
from django.utils import timezone
from django.http import HttpRequest


def filter_queryset_by_params(
    queryset: QuerySet,
    params: Dict[str, Any],
    exact_fields: Optional[Sequence[str]] = None,
    date_fields: Optional[Sequence[str]] = None,
) -> Tuple[QuerySet, Dict[str, Any]]:
    """
    Generic utility to filter a Django QuerySet based on request GET parameters.

    Parameters:
    - queryset: The base Django QuerySet.
    - params: Dictionary of request parameters (e.g. request.GET).
    - exact_fields: Fields to match on exact/case-insensitive values (e.g. ['tag', 'status']).
    - date_fields: Date/DateTimeField names to support date range presets (e.g. ['created_at']).

    Returns:
    - (filtered_queryset, active_filters_dict)
    """
    if not params:
        return queryset, {}

    active_filters: Dict[str, Any] = {}
    exact_fields = exact_fields or []
    date_fields = date_fields or []

    # 1. Handle exact/choice fields
    for field in exact_fields:
        val = params.get(field)
        if val and str(val).strip() and str(val).strip().lower() != 'all':
            clean_val = str(val).strip()
            queryset = queryset.filter(**{f"{field}__iexact": clean_val})
            active_filters[field] = clean_val

    # 2. Handle date range filters
    now = timezone.now()
    for date_field in date_fields:
        date_preset_param = f"{date_field}_range"
        preset = params.get(date_preset_param, params.get('date_range', '')).strip().lower()

        if preset and preset != 'all':
            if preset == 'today':
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(**{f"{date_field}__gte": start})
                active_filters[date_preset_param] = 'Today'
            elif preset == '7days':
                start = now - timedelta(days=7)
                queryset = queryset.filter(**{f"{date_field}__gte": start})
                active_filters[date_preset_param] = 'Past 7 Days'
            elif preset == '30days':
                start = now - timedelta(days=30)
                queryset = queryset.filter(**{f"{date_field}__gte": start})
                active_filters[date_preset_param] = 'Past 30 Days'
            elif preset == 'this_year':
                start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(**{f"{date_field}__gte": start})
                active_filters[date_preset_param] = 'This Year'

        # Custom date range: date_from / date_to
        date_from = params.get(f"{date_field}_from")
        date_to = params.get(f"{date_field}_to")
        if date_from:
            queryset = queryset.filter(**{f"{date_field}__gte": date_from})
            active_filters[f"{date_field}_from"] = date_from
        if date_to:
            queryset = queryset.filter(**{f"{date_field}__lte": date_to})
            active_filters[f"{date_field}_to"] = date_to

    return queryset, active_filters


class ModelFilterer:
    """
    Reusable Model Filterer helper for Django views.

    Usage:
        filterer = ModelFilterer(
            exact_fields=['tag'],
            date_fields=['created_at']
        )
        filtered_qs, active_filters = filterer.filter(request, queryset)
        available_tags = filterer.get_distinct_values(Contact.objects.all(), 'tag')
    """

    def __init__(
        self,
        exact_fields: Optional[Sequence[str]] = None,
        date_fields: Optional[Sequence[str]] = None,
    ):
        self.exact_fields = list(exact_fields or [])
        self.date_fields = list(date_fields or [])

    def filter(self, request: HttpRequest, queryset: QuerySet) -> Tuple[QuerySet, Dict[str, Any]]:
        params = request.GET.dict() if hasattr(request, 'GET') else {}
        return filter_queryset_by_params(
            queryset=queryset,
            params=params,
            exact_fields=self.exact_fields,
            date_fields=self.date_fields,
        )

    def get_distinct_values(self, queryset: QuerySet, field_name: str) -> List[str]:
        """Returns sorted list of distinct non-empty string values for a model field."""
        raw_vals = (
            queryset.values_list(field_name, flat=True)
            .distinct()
            .order_by(field_name)
        )
        return [str(v).strip() for v in raw_vals if v and str(v).strip()]
