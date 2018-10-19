# Stubs for kubernetes.client.models.v1_resource_quota_status (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1ResourceQuotaStatus:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    hard: Any = ...
    used: Any = ...
    def __init__(self, hard: Optional[Any] = ..., used: Optional[Any] = ...) -> None: ...
    @property
    def hard(self): ...
    @hard.setter
    def hard(self, hard: Any) -> None: ...
    @property
    def used(self): ...
    @used.setter
    def used(self, used: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
