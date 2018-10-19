# Stubs for kubernetes.client.models.v1beta2_deployment (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1beta2Deployment:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    api_version: str = ...
    kind: str = ...
    metadata: Any = ...
    spec: Any = ...
    status: Any = ...
    def __init__(self, api_version: Optional[Any] = ..., kind: Optional[Any] = ..., metadata: Optional[Any] = ..., spec: Optional[Any] = ..., status: Optional[Any] = ...) -> None: ...
    @property
    def api_version(self) -> str: ...
    @api_version.setter
    def api_version(self, api_version: str) -> None: ...
    @property
    def kind(self) -> str: ...
    @kind.setter
    def kind(self, kind: str) -> None: ...
    @property
    def metadata(self): ...
    @metadata.setter
    def metadata(self, metadata: Any) -> None: ...
    @property
    def spec(self): ...
    @spec.setter
    def spec(self, spec: Any) -> None: ...
    @property
    def status(self): ...
    @status.setter
    def status(self, status: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
