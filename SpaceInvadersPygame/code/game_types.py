from typing import List, Union

from pygame.sprite import Group, GroupSingle

Color = List[int]
Position = List[int]
Direction = List[int]

GroupUnion = Union[GroupSingle, Group]
Groups = List[GroupUnion]
