#!/usr/bin/env python

import datetime
import operator
import pandas as pd
from anytree import NodeMixin, RenderTree
from dateutil.relativedelta import relativedelta


class DateTitle(object):
    """topmost, simple task (date stuff) object"""

    def __init__(self, date):
        self.date = date
        self.title = self._get_title()
        self.task_id = self._get_task_id()

    def _get_title(self):
        return self.date.strftime('%Y-%m-%d %a')

    def _get_task_id(self):
        return self.date.strftime('%y%m%d000')

    def __str__(self):
        return self.title


# class SubTitle(DateTitle):
#     """generic subtitle for a child just under a DateTitle"""
#
#     def __init__(self, date):
#         self.date = date
#         self.title = self._get_title()
#         self.task_id = self._get_task_id()


class DateTask(object):
    """with dtm like datetime.datetime(2018, 5, 1), get task id like 180501000"""

    def __init__(self, date, title):
        self.date = date
        self.date_title = DateTitle(date)
        if title is None:
            title = self.date_title.title
        self.title = title
        self.task_id = self.date_title.task_id
        self.tpath = self.date.strftime('%Y-%m-%d %a\\')


class SimpleTask(DateTask, NodeMixin):  # NodeMixin adds Node feature

    def __init__(self, date, title, category, tags, comments, parent=None):
        super(SimpleTask, self).__init__(date=date, title=title)
        self.category = category
        self.tags = tags
        self.comments = comments
        self.parent = parent
        if parent is None:
            self.parent_task_id = None
            self.position = 0
        else:
            self.parent_task_id = parent.task_id
            #self.position = 10 * (len(self.siblings) + len(self.ancestors))
            self.position = self.depth


class MonthTasks(object):

    def __init__(self, year, month):
        self.root = SimpleTask(datetime.datetime(1970, 1, 1), 'root_title', 'root', ['ignore', ], 'root')
        self.year = year
        self.month = month
        self.d1 = datetime.datetime(self.year, self.month, 1)
        self.d2 = self.d1 + relativedelta(months=1)

    def show_dates(self):
        for ts in pd.date_range(self.d1, self.d2):
            d = ts.to_pydatetime()
            # only create tasks for weekdays
            if d.isoweekday() in range(1, 6):
                day_one = SimpleTask(d, None, 'day', ['ignore', ], 'day', parent=self.root)

                print d.strftime('%Y-%m-%d %a'),
                # on Monday, create weekly commanding task
                if d.isoweekday() == 1:
                    print 'SAMS weekly commanding',
                for i in ['one', 'two', 'three']:
                    print i,
                print


class Position(object):

    def __init__(self, data, parent, siblings):
        self._parent = None
        self._siblings = None
        self.data = data
        self.parent = parent

    data = property(operator.attrgetter('_description'))

    @data.setter
    def description(self, d):
        if not isinstance(d, str):
            raise Exception('data must be a string')
        if len(d) == 0:
            raise Exception("data cannot be empty")
        self._data = d

    parent = property(operator.attrgetter('_value'))

    @parent.setter
    def value(self, v):
        if not isinstance(v, int):
            raise Exception('parent must be an integer')
        if not (v > 0):
            raise Exception('parent must be greater than zero')
        self._parent = v

    def __str__(self):
        return 'p = %d (%d siblings)' % (self.parent, len(self.siblings))


# d1 = '2018-05-01'
# d2 = '2018-06-01'
# for ts in pd.date_range(d1, d2):
#     d = DayTask(ts.to_pydatetime())
#     # only create tasks for weekdays
#     if d.dtm.isoweekday() in range(1, 6):
#         print d, d.task_id, '#',
#         # on Monday, create weekly commanding task
#         if d.dtm.isoweekday() == 1:
#             print 'SAMS weekly commanding',
#         for i in ['one', 'two', 'three']:
#             print i,
#         print



mt = MonthTasks(2018, 5)
mt.show_dates()
raise SystemExit


def main():
    dtm0 = datetime.datetime(1970, 1, 1)
    root = SimpleTask(dtm0, 'root_title', 'root', ['ignore', ], 'root')
    print 'len', len(root.children)

    dtm = datetime.datetime(2018, 5, 1)
    d1 = SimpleTask(dtm, None, 'day', ['ignore', ], 'day', parent=root)
    hash = SimpleTask(dtm, '#', 'hash', ['ignore', ], 'hash', parent=d1)
    one = SimpleTask(dtm, '10. one', 'cat', ['t1', 't2'], 'nope', parent=d1)
    two = SimpleTask(dtm, '20. two', 'cat', ['t1', 't2'], 'nope', parent=d1)
    print 'len', len(root.children)

    dtm += datetime.timedelta(days=1)
    d2 = SimpleTask(dtm, None, 'day', ['ignore', ], 'day', parent=root)
    hash = SimpleTask(dtm, 'hash_title', 'hash', ['ignore', ], 'hash', parent=d2)
    one = SimpleTask(dtm, 'one_title', 'cat', ['t1', 't2'], 'nope', parent=d2)
    two = SimpleTask(dtm, 'two_title', 'cat', ['t1', 't2'], 'nope', parent=d2)
    wtf = SimpleTask(dtm, 'wtf_title', 'cat', ['t1', 't2'], 'nope', parent=two)
    print 'len', len(root.children)

    for pre, _, node in RenderTree(root):
        if node.is_root:
            continue
        treestr = u"%s%s" % (pre, node.title)
        print treestr.ljust(8), 'task id:', node.task_id, 'pos:', node.position,\
            'depth:', node.depth, 'height:', node.height


if __name__ == '__main__':
    main()
