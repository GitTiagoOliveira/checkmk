# Stubs for kubernetes.client.models.v2beta1_metric_spec (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V2beta1MetricSpec:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    external: Any = ...
    object: Any = ...
    pods: Any = ...
    resource: Any = ...
    type: Any = ...
    def __init__(self, external: Optional[Any] = ..., object: Optional[Any] = ..., pods: Optional[Any] = ..., resource: Optional[Any] = ..., type: Optional[Any] = ...) -> None: ...
    @property
    def external(self): ...
    @external.setter
    def external(self, external: Any) -> None: ...
    @property
    def object(self): ...
    @object.setter
    def object(self, object: Any) -> None: ...
    @property
    def pods(self): ...
    @pods.setter
    def pods(self, pods: Any) -> None: ...
    @property
    def resource(self): ...
    @resource.setter
    def resource(self, resource: Any) -> None: ...
    @property
    def type(self): ...
    @type.setter
    def type(self, type: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
