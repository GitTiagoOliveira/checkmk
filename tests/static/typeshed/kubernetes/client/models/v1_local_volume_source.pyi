# Stubs for kubernetes.client.models.v1_local_volume_source (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1LocalVolumeSource:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    fs_type: Any = ...
    path: Any = ...
    def __init__(self, fs_type: Optional[Any] = ..., path: Optional[Any] = ...) -> None: ...
    @property
    def fs_type(self): ...
    @fs_type.setter
    def fs_type(self, fs_type: Any) -> None: ...
    @property
    def path(self): ...
    @path.setter
    def path(self, path: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
