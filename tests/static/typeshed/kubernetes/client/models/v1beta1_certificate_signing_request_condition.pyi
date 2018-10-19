# Stubs for kubernetes.client.models.v1beta1_certificate_signing_request_condition (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1beta1CertificateSigningRequestCondition:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    last_update_time: Any = ...
    message: Any = ...
    reason: Any = ...
    type: Any = ...
    def __init__(self, last_update_time: Optional[Any] = ..., message: Optional[Any] = ..., reason: Optional[Any] = ..., type: Optional[Any] = ...) -> None: ...
    @property
    def last_update_time(self): ...
    @last_update_time.setter
    def last_update_time(self, last_update_time: Any) -> None: ...
    @property
    def message(self): ...
    @message.setter
    def message(self, message: Any) -> None: ...
    @property
    def reason(self): ...
    @reason.setter
    def reason(self, reason: Any) -> None: ...
    @property
    def type(self): ...
    @type.setter
    def type(self, type: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
