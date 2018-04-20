#!/usr/bin/env python

import anytree
import datetime
import operator
# from btree import BPlusTree
# import pandas as pd
from anytree import NodeMixin, RenderTree


class MyBaseTask(object):

    def __init__(self):
        pass


class MyTask(MyBaseTask, NodeMixin):  # adds Node feature

    def __init__(self, name, position, title, task_id, parent_task_id, pth, created_by, category, tags, comments, parent=None):
        super(MyTask, self).__init__()
        self.name = name
        self.position = position
        self.title = title
        self.task_id = task_id
        self.parent_task_id = parent_task_id
        self.pth = pth
        self.created_by = created_by
        self.category = category
        self.tags = tags
        self.comments = comments
        self.parent = parent


root = MyTask('root', 0, 'root', 0, None, '', 'robot', '', [], 'no comment')
my1 = MyTask('my1', 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=root)
my2 = MyTask('my2', 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=root)
rootb = MyTask("sub0B", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=my1)
roota = MyTask("sub0A", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=my1)
s1 = MyTask("sub1", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=root)
s1a = MyTask("sub1A", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=s1)
s1b = MyTask("sub1B", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=s1)
s1c = MyTask("sub1C", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=s1)
s1ca = MyTask("sub1Ca", 0, 'root', 0, None, '', 'robot', '', [], 'no comment', parent=s1c)

for pre, _, node in RenderTree(root):
    treestr = u"%s%s" % (pre, node.name)
    print treestr.ljust(8), 'position:', node.position, 'pth:', node.pth

raise SystemExit

class Spam(object):

    def __init__(self, description, value):
        self._description = None
        self._value = None
        self.description = description
        self.value = value

    description = property(operator.attrgetter('_description'))

    @description.setter
    def description(self, d):
        if not isinstance(d, str):
            raise Exception('description must be a string')
        if len(d) == 0:
            raise Exception("description cannot be empty")
        self._description = d

    value = property(operator.attrgetter('_value'))

    @value.setter
    def value(self, v):
        if not isinstance(v, int):
            raise Exception('value must be an integer')
        if not (v > 0):
            raise Exception('value must be greater than zero')
        self._value = v


class Position(object):

    def __init__(self, data, parent, siblings):
        self._parent = None
        self._siblings = None
        self.description = description
        self.value = value

    description = property(operator.attrgetter('_description'))

    @description.setter
    def description(self, d):
        if not isinstance(d, str):
            raise Exception('description must be a string')
        if len(d) == 0:
            raise Exception("description cannot be empty")
        self._description = d

    value = property(operator.attrgetter('_value'))

    @value.setter
    def value(self, v):
        if not isinstance(v, int):
            raise Exception('value must be an integer')
        if not (v > 0):
            raise Exception('value must be greater than zero')
        self._value = v

    def __str__(self):
        return 'p = %d (%d siblings)' % (self.parent, len(self.siblings))


udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

print udo

print joe


for pre, fill, node in RenderTree(udo):
    print "%s%s" % (pre, node.name)

print dan.children

# s = Spam('i', 1)
# print s.description, s.value
#
# p = Position(parent=1, siblings=None)
# print p

raise SystemExit

class DayTask(object):

    def __init__(self, dtm, position):
        self.dtm = dtm
        self.position = position
        self.title = self._get_title()
        self.task_id = self._get_task_id()
        self.parent_task_id = 0
        self.path = None
        self.priority = 5
        self.risk = 0
        self.pct_complete = 0
        self.creation_date = datetime.datetime.now()
        self.created_by = 'robot'
        self.modified_date = self.creation_date
        self.start_date = dtm
        self.completed_date = None
        self.cost = 0
        self.subtask_completion = None
        self.comment = None

    def _get_task_id(self):
        return int(self.dtm.strftime('%y%m%d000'))

    def __str__(self):
        s = self.dtm.strftime('%Y-%m-%d %a')
        return s


d1 = '2018-05-01'
d2 = '2018-06-01'
for ts in pd.date_range(d1, d2):
    d = DayTask(ts.to_pydatetime())
    # only create tasks for weekdays
    if d.dtm.isoweekday() in range(1, 6):
        print d, d.task_id, '#',
        # on Monday, create weekly commanding task
        if d.dtm.isoweekday() == 1:
            print 'SAMS weekly commanding',
        for i in ['one', 'two', 'three']:
            print i,
        print
