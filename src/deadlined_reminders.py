from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from abc import ABC
from dateutil.parser import parse
from datetime import datetime

class DeadlinedMetaReminder(Iterable, metaclass=ABCMeta):
    """Abstract base class for deadlined reminders (unused)"""
    @abstractmethod
    def is_due(self):
        pass


class DeadlinedReminder(ABC, Iterable):
    """Abstract base class for deadlined reminders"""
    @abstractmethod
    def is_due(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        if cls is not DeadlinedReminder:
            return NotImplemented
        
        def attr_in_hiearchy(attr):
            return any (attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)
        
        if not all(attr_in_hiearchy(attr) for attr in ('__iter__', 'is_due')):
            return NotImplemented
        
        return True


class DateReminder(DeadlinedReminder):

    def __init__(self, text, date):
        self.date = parse(date, dayfirst=True)
        self.text = text

    def is_due(self):
        return self.date <= datetime.now()

    def __iter__(self):
        return iter([self.text, self.date.isoformat()])