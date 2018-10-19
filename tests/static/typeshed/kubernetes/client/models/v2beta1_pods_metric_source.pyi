# Stubs for kubernetes.client.models.v2beta1_pods_metric_source (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V2beta1PodsMetricSource:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    metric_name: Any = ...
    selector: Any = ...
    target_average_value: Any = ...
    def __init__(self, metric_name: Optional[Any] = ..., selector: Optional[Any] = ..., target_average_value: Optional[Any] = ...) -> None: ...
    @property
    def metric_name(self): ...
    @metric_name.setter
    def metric_name(self, metric_name: Any) -> None: ...
    @property
    def selector(self): ...
    @selector.setter
    def selector(self, selector: Any) -> None: ...
    @property
    def target_average_value(self): ...
    @target_average_value.setter
    def target_average_value(self, target_average_value: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
