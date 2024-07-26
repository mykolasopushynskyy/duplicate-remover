class PubSubBroker:
    def __init__(self):
        self._event_listeners = {}

    def subscribe(self, event, fn):
        """
        Subscribe a function to an event.

        Args:
            event (str): The name of the event.
            fn (callable): The function to call when the event is published.

        Returns:
            callable: A function to unsubscribe the function from the event.
        """
        if event in self._event_listeners:
            self._event_listeners[event].append(fn)
        else:
            self._event_listeners[event] = [fn]

        # Return a function that, when called, will unsubscribe the function.
        return lambda: self._event_listeners[event].remove(fn)

    def publish(self, event, data=None):
        """
        Publish an event to all its subscribers.

        Args:
            event (str): The name of the event.
            data (optional): The data to pass to the subscribed functions. Defaults to None.
        """
        if event not in self._event_listeners:
            return

        for func in self._event_listeners[event]:
            func(data if data is not None else self)
