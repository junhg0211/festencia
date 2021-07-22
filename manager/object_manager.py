from typing import List

from display import Display
from object import Object


class ObjectManager(Object):
    def __init__(self):
        super().__init__(0, 0)
        self.objects: List[Object] = list()

    def add(self, object_: Object):
        self.objects.append(object_)
        return self

    def tick(self):
        for object_ in self.objects:
            object_.tick()

    def render(self, display: Display):
        for object_ in self.objects:
            object_.render(display)
