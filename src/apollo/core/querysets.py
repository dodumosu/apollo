from djorm_expressions.base import SqlExpression, OR, AND
from djorm_hstore.models import HStoreQueryset


class SearchableLocationQuerySet(HStoreQueryset):
    def is_within(self, location):
        return self.filter(location__pk__in=[loc['id'] for loc in location.nx_descendants(include_self=True)])


class SubmissionQuerySet(SearchableLocationQuerySet):
    def is_complete(self, group):
        fields = list(group.fields.values_list('tag', flat=True))
        expr = OR(
                SqlExpression("data", "?&", fields),
                SqlExpression("master__data", "?&", fields))
        return self.where(expr) if fields else self

    def is_missing(self, group):
        fields = list(group.fields.values_list('tag', flat=True))
        expr = AND(
                ~SqlExpression("data", "?|", fields),
                ~SqlExpression("master__data", "?|", fields))
        return self.where(expr) if fields else self.none()

    def is_partial(self, group):
        fields = list(group.fields.values_list('tag', flat=True))
        # checks that either data is partial or master__data is partial
        # but none of either data or master__data is complete
        expr = AND(
                OR(
                    AND(SqlExpression("data", "?|", fields), ~SqlExpression("data", "?&", fields)),
                    AND(SqlExpression("master__data", "?|", fields), ~SqlExpression("master__data", "?&", fields))),
                AND(~SqlExpression("data", "?&", fields), ~SqlExpression("master__data", "?&", fields)))
        return self.where(expr) if fields else self

    def data(self, tags):
        _select = dict([(tag, '"core_submission"."data"->%s' % ("'%s'" % (tag,))) for tag in tags])
        return self.extra(select=_select)
