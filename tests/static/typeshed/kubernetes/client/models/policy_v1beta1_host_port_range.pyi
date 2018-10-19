# Stubs for kubernetes.client.models.policy_v1beta1_host_port_range (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class PolicyV1beta1HostPortRange:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    max: Any = ...
    min: Any = ...
    def __init__(self, max: Optional[Any] = ..., min: Optional[Any] = ...) -> None: ...
    @property
    def max(self): ...
    @max.setter
    def max(self, max: Any) -> None: ...
    @property
    def min(self): ...
    @min.setter
    def min(self, min: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
