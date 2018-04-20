#!/usr/bin/env python

import datetime
import operator
# import pandas as pd
from anytree import NodeMixin, RenderTree


class DateTask(object):
    """with dtm like datetime.datetime(2018, 5, 1), get task id like 180501000"""

    def __init__(self, date):
        self.date = date
        self.title = self.date.strftime('%Y-%m-%d %a')
        self.task_id = self.date.strftime('%y%m%d000')
        self.task_path = self.date.strftime('%Y-%m-%d %a\\')


class B(DateTask):

    def __init__(self, b, **kwargs):
        self.b = b
        super(B, self).__init__(**kwargs)


class C(DateTask):

    def __init__(self, c, **kwargs):
        self.c = c
        super(C, self).__init__(**kwargs)


class D(B, C):

    def __init__(self, date, b, c, d):
        super(D, self).__init__(date=date, b=b, c=c)
        self.d = d


class SimpleTask(DateTask, NodeMixin):  # adds Node feature

    def __init__(self, date, category, tags, parent=None):
        super(SimpleTask, self).__init__(date=date)
        self.category = category
        self.tags = tags
        self.parent = parent
        # self.name = name
        # self.position = position
        # self.title = title
        # self.task_id = task_id
        # self.parent_task_id = parent_task_id
        # self.pth = pth
        # self.created_by = created_by
        # self.comments = comments
        # self.parent = parent


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

def main():
    dtm = datetime.datetime(2018, 5, 11)
    root = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'])
    my1 = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=root)
    my2 = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=root)
    rootb = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=my1)
    roota = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=my2)
    s1 = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=root)
    s1a = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=s1)
    s1b = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=s1)
    s1c = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=s1)
    s1ca = SimpleTask(dtm, 'mycategory', ['tagOne', 'tagTwo'], parent=s1c)

    for pre, _, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.title)
        print treestr.ljust(8), 'category:', node.category, 'tags:', node.tags

if __name__ == '__main__':
    main()
