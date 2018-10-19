# Stubs for kubernetes.client.models.v1_replication_controller_spec (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1ReplicationControllerSpec:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    min_ready_seconds: Any = ...
    replicas: Any = ...
    selector: Any = ...
    template: Any = ...
    def __init__(self, min_ready_seconds: Optional[Any] = ..., replicas: Optional[Any] = ..., selector: Optional[Any] = ..., template: Optional[Any] = ...) -> None: ...
    @property
    def min_ready_seconds(self): ...
    @min_ready_seconds.setter
    def min_ready_seconds(self, min_ready_seconds: Any) -> None: ...
    @property
    def replicas(self): ...
    @replicas.setter
    def replicas(self, replicas: Any) -> None: ...
    @property
    def selector(self): ...
    @selector.setter
    def selector(self, selector: Any) -> None: ...
    @property
    def template(self): ...
    @template.setter
    def template(self, template: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
