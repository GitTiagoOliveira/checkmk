# Stubs for kubernetes.client.models.extensions_v1beta1_scale_spec (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class ExtensionsV1beta1ScaleSpec:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    replicas: Any = ...
    def __init__(self, replicas: Optional[Any] = ...) -> None: ...
    @property
    def replicas(self): ...
    @replicas.setter
    def replicas(self, replicas: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
