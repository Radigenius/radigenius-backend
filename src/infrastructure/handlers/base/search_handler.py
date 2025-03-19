from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F
from infrastructure.handlers.base.base_filter_handler import BaseFiltersHandler


class SearchHandler(BaseFiltersHandler):
    def search(self, queryset, name, value):

        normalized_query = self.query_normalizer(value)
        search_query = SearchQuery(normalized_query)

        # Use the precomputed search_vector field and filter against it
        queryset = (
            queryset.annotate(rank=SearchRank(F("search_vector"), search_query))
            .filter(search_vector=search_query)
            .order_by("-rank")
        )

        return queryset
