# Stubs for kubernetes.client.models.v1beta1_api_service_spec (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1beta1APIServiceSpec:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    ca_bundle: Any = ...
    group: Any = ...
    group_priority_minimum: Any = ...
    insecure_skip_tls_verify: Any = ...
    service: Any = ...
    version: Any = ...
    version_priority: Any = ...
    def __init__(self, ca_bundle: Optional[Any] = ..., group: Optional[Any] = ..., group_priority_minimum: Optional[Any] = ..., insecure_skip_tls_verify: Optional[Any] = ..., service: Optional[Any] = ..., version: Optional[Any] = ..., version_priority: Optional[Any] = ...) -> None: ...
    @property
    def ca_bundle(self): ...
    @ca_bundle.setter
    def ca_bundle(self, ca_bundle: Any) -> None: ...
    @property
    def group(self): ...
    @group.setter
    def group(self, group: Any) -> None: ...
    @property
    def group_priority_minimum(self): ...
    @group_priority_minimum.setter
    def group_priority_minimum(self, group_priority_minimum: Any) -> None: ...
    @property
    def insecure_skip_tls_verify(self): ...
    @insecure_skip_tls_verify.setter
    def insecure_skip_tls_verify(self, insecure_skip_tls_verify: Any) -> None: ...
    @property
    def service(self): ...
    @service.setter
    def service(self, service: Any) -> None: ...
    @property
    def version(self): ...
    @version.setter
    def version(self, version: Any) -> None: ...
    @property
    def version_priority(self): ...
    @version_priority.setter
    def version_priority(self, version_priority: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
