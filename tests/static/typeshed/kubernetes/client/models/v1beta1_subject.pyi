# Stubs for kubernetes.client.models.v1beta1_subject (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1beta1Subject:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    api_group: Any = ...
    kind: str = ...
    name: Any = ...
    namespace: Any = ...
    def __init__(self, api_group: Optional[Any] = ..., kind: Optional[Any] = ..., name: Optional[Any] = ..., namespace: Optional[Any] = ...) -> None: ...
    @property
    def api_group(self): ...
    @api_group.setter
    def api_group(self, api_group: Any) -> None: ...
    @property
    def kind(self) -> str: ...
    @kind.setter
    def kind(self, kind: str) -> None: ...
    @property
    def name(self): ...
    @name.setter
    def name(self, name: Any) -> None: ...
    @property
    def namespace(self): ...
    @namespace.setter
    def namespace(self, namespace: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
