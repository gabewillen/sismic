from typing import Any

__all__ = ['Event', 'InternalEvent', 'DelayedEvent', 'DelayedInternalEvent', 'MetaEvent']


class Event:
    """
    An event with a name and (optionally) some data passed as named parameters.

    The list of parameters can be obtained using *dir(event)*. Notice that
    *name* and *data* are reserved names. 

    When two events are compared, they are considered equal if their names
    and their data are equal.

    :param name: name of the event.
    :param data: additional data passed as named parameters.
    """

    __slots__ = ['name', 'data']

    def __init__(self, name: str, **additional_parameters: Any) -> None:
        self.name = name
        self.data = additional_parameters

    def __eq__(self, other):
        return (self.name == other.name and self.data == other.data) if isinstance(other, Event) else NotImplemented

    def __getattr__(self, attr):
        try:
            return self.data[attr]
        except KeyError:
            raise AttributeError('{} has no attribute {}'.format(self, attr))

    def __getstate__(self):
        # For pickle and implicitly for multiprocessing
        return self.name, self.data

    def __setstate__(self, state):
        # For pickle and implicitly for multiprocessing
        self.name, self.data = state

    def __hash__(self):
        return hash(self.name)

    def __dir__(self):
        return ['name'] + list(self.data.keys())

    def __repr__(self):
        if self.data:
            return '{}({!r}, {})'.format(self.__class__.__name__,
                                         self.name,
                                         ', '.join('{}={!r}'.format(k, v) for k, v in self.data.items()))
        else:
            return '{}({!r})'.format(self.__class__.__name__, self.name)


class InternalEvent(Event):
    """
    Subclass of Event that represents an internal event.
    """
    pass


class DelayedEvent(Event):
    """
    Event that is delayed.

    When used, *delay* is a reserved name (ie. cannot be used as event parameter).
    """
    
    __slots__ = ['name', 'delay', 'data']

    def __init__(self, name: str, delay: float, **additional_parameters: Any) -> None:
        super().__init__(name, **additional_parameters)
        self.delay = delay

    def __getstate__(self):
        # For pickle and implicitly for multiprocessing
        return self.name, self.delay, self.data

    def __setstate__(self, state):
        # For pickle and implicitly for multiprocessing
        self.name, self.delay, self.data = state

    def __dir__(self):
        return ['name', 'delay'] + list(self.data.keys())    


class DelayedInternalEvent(InternalEvent, DelayedEvent):
    """
    Internal event that is delayed.
    """
    def __init__(self, name: str, delay: float, **additional_parameters: Any) -> None:
        DelayedEvent.__init__(self, name, delay, **additional_parameters)


class MetaEvent(Event):
    """
    Subclass of Event that represents a MetaEvent, as used in property statecharts.
    """
    pass