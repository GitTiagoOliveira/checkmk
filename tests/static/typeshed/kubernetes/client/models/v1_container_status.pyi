# Stubs for kubernetes.client.models.v1_container_status (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1ContainerStatus:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    container_id: Any = ...
    image: Any = ...
    image_id: Any = ...
    last_state: Any = ...
    name: Any = ...
    ready: Any = ...
    restart_count: Any = ...
    state: Any = ...
    def __init__(self, container_id: Optional[Any] = ..., image: Optional[Any] = ..., image_id: Optional[Any] = ..., last_state: Optional[Any] = ..., name: Optional[Any] = ..., ready: Optional[Any] = ..., restart_count: Optional[Any] = ..., state: Optional[Any] = ...) -> None: ...
    @property
    def container_id(self): ...
    @container_id.setter
    def container_id(self, container_id: Any) -> None: ...
    @property
    def image(self): ...
    @image.setter
    def image(self, image: Any) -> None: ...
    @property
    def image_id(self): ...
    @image_id.setter
    def image_id(self, image_id: Any) -> None: ...
    @property
    def last_state(self): ...
    @last_state.setter
    def last_state(self, last_state: Any) -> None: ...
    @property
    def name(self): ...
    @name.setter
    def name(self, name: Any) -> None: ...
    @property
    def ready(self): ...
    @ready.setter
    def ready(self, ready: Any) -> None: ...
    @property
    def restart_count(self): ...
    @restart_count.setter
    def restart_count(self, restart_count: Any) -> None: ...
    @property
    def state(self): ...
    @state.setter
    def state(self, state: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
