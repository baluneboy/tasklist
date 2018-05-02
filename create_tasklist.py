#!/usr/bin/env python

import datetime
import operator
import inflect
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
        return long(self.date.strftime('%y%m%d000'))

    def __str__(self):
        return self.title


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


class PlaceHolderTask(SimpleTask):

    def increment_task_id(self, value):
        self.task_id += value


class MonthTasks(object):

    def __init__(self, year, month):
        self.root = SimpleTask(datetime.datetime(1970, 1, 1), 'root_title', 'root', ['ignore', ], 'root')
        self.year = year
        self.month = month
        self.d1 = datetime.datetime(self.year, self.month, 1)
        self.d2 = self.d1 + relativedelta(months=1) - relativedelta(days=1)
        self._bullet_counter = 0
        self._daily_counter = 0
        self._word_engine = inflect.engine()

    def _reset_day_counter(self):
        self._bullet_counter = 0
        self._daily_counter = 0

    def add_day_subtask(self, date, title, category, tags, comments, day_parent):
        self._bullet_counter += 10
        self._daily_counter += 1
        sub = PlaceHolderTask(date, title, 'sub', ['t1', 't2'], 'nocom', parent=day_parent)
        sub.increment_task_id(self._daily_counter)
        return sub

    def _num2word(self, num):
        return self._word_engine.number_to_words(num)

    def show_dates(self):
        for ts in pd.date_range(self.d1, self.d2):
            d = ts.to_pydatetime()
            # only create tasks for weekdays
            if d.isoweekday() in range(1, 6):
                self._reset_day_counter()
                my_day = SimpleTask(d, None, 'day', ['ignore', ], 'day', parent=self.root)
                self.add_day_subtask(d, '#', 'hash', ['ignore', ], 'hash', my_day)

                # on Monday, create weekly commanding subtask
                if d.isoweekday() == 1:
                    title_str = '%d. SAMS nominal commanding.' % self._bullet_counter
                    self.add_day_subtask(d, title_str, 'cmd', ['ignore', ], 'cmd', my_day)

                # add a couple of placeholders too for each day
                for num in range(1, 3):
                    title_str = '%d. %s.' % (self._bullet_counter, self._num2word(num).title())
                    st = self.add_day_subtask(d, title_str, 'num', ['ignore', ], 'num', my_day)

        title_str = '%d. %s.' % (self._bullet_counter, 'Extra')
        self.add_day_subtask(d, title_str, 'foo', ['ignore', ], 'bah', st)

        title_str = '%d. %s.' % (self._bullet_counter, 'Dos')
        self.add_day_subtask(d, title_str, 'foo', ['ignore', ], 'bah', my_day)

        for pre, _, node in RenderTree(self.root):
            if node.is_root:
                continue
            treestr = u"%s%s" % (pre, node.title)

            if node.depth > 1:
                pstr = ''
                for i, p in enumerate(node.path[0:-1]):
                    pstr += '%s\\' % node.path[i].title
            else:
                pstr = ''

            print treestr.ljust(36), 'task id:', node.task_id,\
                'depth:', node.depth, 'height:', node.height,\
                'siblings:', len(node.siblings), 'path:', pstr


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
