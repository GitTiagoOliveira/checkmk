# Stubs for kubernetes.client.models.v1_replica_set_status (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1ReplicaSetStatus:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    available_replicas: Any = ...
    conditions: Any = ...
    fully_labeled_replicas: Any = ...
    observed_generation: Any = ...
    ready_replicas: Any = ...
    replicas: Any = ...
    def __init__(self, available_replicas: Optional[Any] = ..., conditions: Optional[Any] = ..., fully_labeled_replicas: Optional[Any] = ..., observed_generation: Optional[Any] = ..., ready_replicas: Optional[Any] = ..., replicas: Optional[Any] = ...) -> None: ...
    @property
    def available_replicas(self): ...
    @available_replicas.setter
    def available_replicas(self, available_replicas: Any) -> None: ...
    @property
    def conditions(self): ...
    @conditions.setter
    def conditions(self, conditions: Any) -> None: ...
    @property
    def fully_labeled_replicas(self): ...
    @fully_labeled_replicas.setter
    def fully_labeled_replicas(self, fully_labeled_replicas: Any) -> None: ...
    @property
    def observed_generation(self): ...
    @observed_generation.setter
    def observed_generation(self, observed_generation: Any) -> None: ...
    @property
    def ready_replicas(self): ...
    @ready_replicas.setter
    def ready_replicas(self, ready_replicas: Any) -> None: ...
    @property
    def replicas(self): ...
    @replicas.setter
    def replicas(self, replicas: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
