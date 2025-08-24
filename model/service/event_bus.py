from collections import defaultdict
from typing import Callable, Any, Dict, List

class EventBus:
    """Simple synchronous publish/subscribe event bus.

    Usage:
        GLOBAL_EVENTS.subscribe('health_changed', handler)
        GLOBAL_EVENTS.emit('health_changed', current=10, max_hp=30)
    """
    def __init__(self):
        self._subs: Dict[str, List[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, evt: str, fn: Callable[..., Any]):
        if fn not in self._subs[evt]:
            self._subs[evt].append(fn)

    def unsubscribe(self, evt: str, fn: Callable[..., Any]):
        if fn in self._subs.get(evt, []):
            self._subs[evt].remove(fn)

    def emit(self, evt: str, **payload):
        for fn in list(self._subs.get(evt, [])):
            fn(**payload)

GLOBAL_EVENTS = EventBus()
