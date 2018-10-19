# Stubs for kubernetes.client.models.v1_iscsi_volume_source (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1ISCSIVolumeSource:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    chap_auth_discovery: Any = ...
    chap_auth_session: Any = ...
    fs_type: Any = ...
    initiator_name: Any = ...
    iqn: Any = ...
    iscsi_interface: Any = ...
    lun: Any = ...
    portals: Any = ...
    read_only: Any = ...
    secret_ref: Any = ...
    target_portal: Any = ...
    def __init__(self, chap_auth_discovery: Optional[Any] = ..., chap_auth_session: Optional[Any] = ..., fs_type: Optional[Any] = ..., initiator_name: Optional[Any] = ..., iqn: Optional[Any] = ..., iscsi_interface: Optional[Any] = ..., lun: Optional[Any] = ..., portals: Optional[Any] = ..., read_only: Optional[Any] = ..., secret_ref: Optional[Any] = ..., target_portal: Optional[Any] = ...) -> None: ...
    @property
    def chap_auth_discovery(self): ...
    @chap_auth_discovery.setter
    def chap_auth_discovery(self, chap_auth_discovery: Any) -> None: ...
    @property
    def chap_auth_session(self): ...
    @chap_auth_session.setter
    def chap_auth_session(self, chap_auth_session: Any) -> None: ...
    @property
    def fs_type(self): ...
    @fs_type.setter
    def fs_type(self, fs_type: Any) -> None: ...
    @property
    def initiator_name(self): ...
    @initiator_name.setter
    def initiator_name(self, initiator_name: Any) -> None: ...
    @property
    def iqn(self): ...
    @iqn.setter
    def iqn(self, iqn: Any) -> None: ...
    @property
    def iscsi_interface(self): ...
    @iscsi_interface.setter
    def iscsi_interface(self, iscsi_interface: Any) -> None: ...
    @property
    def lun(self): ...
    @lun.setter
    def lun(self, lun: Any) -> None: ...
    @property
    def portals(self): ...
    @portals.setter
    def portals(self, portals: Any) -> None: ...
    @property
    def read_only(self): ...
    @read_only.setter
    def read_only(self, read_only: Any) -> None: ...
    @property
    def secret_ref(self): ...
    @secret_ref.setter
    def secret_ref(self, secret_ref: Any) -> None: ...
    @property
    def target_portal(self): ...
    @target_portal.setter
    def target_portal(self, target_portal: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
