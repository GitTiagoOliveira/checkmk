# Stubs for kubernetes.client.models.v1_api_service_status (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1APIServiceStatus:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    conditions: Any = ...
    def __init__(self, conditions: Optional[Any] = ...) -> None: ...
    @property
    def conditions(self): ...
    @conditions.setter
    def conditions(self, conditions: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
