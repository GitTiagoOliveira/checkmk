#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import json
import time
from collections.abc import Mapping, MutableMapping
from typing import Any

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    get_value_store,
    register,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)
from cmk.base.plugins.agent_based.utils import netapp_ontap_models as models
from cmk.base.plugins.agent_based.utils.df import (
    FILESYSTEM_DEFAULT_LEVELS,
    MAGIC_FACTOR_DEFAULT_PARAMS,
    TREND_DEFAULT_PARAMS,
)
from cmk.base.plugins.agent_based.utils.netapp_api import check_netapp_luns

Section = Mapping[str, models.LunModel]

# <<<netapp_ontap_luns:sep(0)>>>
# {
#     "enabled": true,
#     "location": {"volume": {"name": "Converged_DS01"}},
#     "name": "/vol/Converged_DS01/lun1",
#     "space": {"size": 536870912000, "used": 34260107264},
#     "status": {"read_only": false},
#     "svm": {"name": "FlexPodXCS_SAN_Frank"},
# }
# {
#     "enabled": true,
#     "location": {"volume": {"name": "karch4"}},
#     "name": "/vol/karch4/testlun4",
#     "space": {"size": 20971520, "used": 0},
#     "status": {"read_only": false},
#     "svm": {"name": "mcc_darz_a_svm01_CIFS"},
# }


def parse_netapp_ontap_luns(string_table: StringTable) -> Section:
    return {
        lun.item_name(): lun
        for line in string_table
        if (lun := models.LunModel(**json.loads(line[0])))
    }


register.agent_section(
    name="netapp_ontap_luns",
    parse_function=parse_netapp_ontap_luns,
)


def discover_netapp_ontap_luns(section: Section) -> DiscoveryResult:
    yield from (Service(item=lun) for lun in section)


def check_netapp_ontap_luns(
    item: str,
    params: Mapping[str, Any],
    section: Section,
) -> CheckResult:
    yield from _check_netapp_ontap_luns(item, params, section, get_value_store(), time.time())


def _check_netapp_ontap_luns(
    item: str,
    params: Mapping[str, Any],
    section: Section,
    value_store: MutableMapping[str, Any],
    now: float,
) -> CheckResult:
    if (lun := section.get(item)) is None:
        return

    yield Result(state=State.OK, summary=f"Volume: {lun.volume_name}")
    yield Result(state=State.OK, summary=f"Vserver: {lun.svm_name}")

    yield from check_netapp_luns(
        item=item,
        volume_name=lun.volume_name,
        server_name=lun.svm_name,
        online=lun.enabled,
        read_only=lun.read_only,
        size_total_bytes=lun.space_size,
        size_total=lun.size(),
        size_available=lun.free_space(),
        now=now,
        value_store=value_store,
        params=params,
    )


register.check_plugin(
    name="netapp_ontap_luns",
    service_name="LUN %s",
    discovery_function=discover_netapp_ontap_luns,
    check_function=check_netapp_ontap_luns,
    check_ruleset_name="netapp_luns",
    check_default_parameters={
        **FILESYSTEM_DEFAULT_LEVELS,
        **MAGIC_FACTOR_DEFAULT_PARAMS,
        **TREND_DEFAULT_PARAMS,
        "read_only": False,
    },
)
