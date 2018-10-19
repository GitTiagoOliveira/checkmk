# Stubs for kubernetes.client.models.v1_flex_persistent_volume_source (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1FlexPersistentVolumeSource:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    driver: Any = ...
    fs_type: Any = ...
    options: Any = ...
    read_only: Any = ...
    secret_ref: Any = ...
    def __init__(self, driver: Optional[Any] = ..., fs_type: Optional[Any] = ..., options: Optional[Any] = ..., read_only: Optional[Any] = ..., secret_ref: Optional[Any] = ...) -> None: ...
    @property
    def driver(self): ...
    @driver.setter
    def driver(self, driver: Any) -> None: ...
    @property
    def fs_type(self): ...
    @fs_type.setter
    def fs_type(self, fs_type: Any) -> None: ...
    @property
    def options(self): ...
    @options.setter
    def options(self, options: Any) -> None: ...
    @property
    def read_only(self): ...
    @read_only.setter
    def read_only(self, read_only: Any) -> None: ...
    @property
    def secret_ref(self): ...
    @secret_ref.setter
    def secret_ref(self, secret_ref: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
