# Stubs for kubernetes.client.models.v1_persistent_volume_claim_list (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from . import V1PersistentVolumeClaim
from typing import Any, List, Optional

class V1PersistentVolumeClaimList:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    api_version: str = ...
    items: Any = ...
    kind: str = ...
    metadata: Any = ...
    def __init__(self, api_version: Optional[Any] = ..., items: Optional[Any] = ..., kind: Optional[Any] = ..., metadata: Optional[Any] = ...) -> None: ...
    @property
    def api_version(self) -> str: ...
    @api_version.setter
    def api_version(self, api_version: str) -> None: ...
    @property
    def items(self) -> List[V1PersistentVolumeClaim]: ...
    @items.setter
    def items(self, items: List[V1PersistentVolumeClaim]) -> None: ...
    @property
    def kind(self) -> str: ...
    @kind.setter
    def kind(self, kind: str) -> None: ...
    @property
    def metadata(self): ...
    @metadata.setter
    def metadata(self, metadata: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
