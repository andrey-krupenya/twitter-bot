from django.db.models import Aggregate, CharField


class GroupConcat(Aggregate):
    # GROUP_CONCAT(DISTINCT field_name SEPARATOR ', ')
    function = 'GROUP_CONCAT'
    template = "%(function)s(%(distinct)s %(expressions)s %(separator)s)"

    def __init__(self, expression, distinct=False, separator=', ', **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT' if distinct else '',
            separator="SEPARATOR '%s'" % separator,
            output_field=CharField(),
            **extra
        )
