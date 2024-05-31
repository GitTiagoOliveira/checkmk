#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.base.check_api import check_levels, LegacyCheckDefinition
from cmk.base.check_legacy_includes.wmi import (
    get_levels_quadruple,
    inventory_wmi_table_instances,
    parse_wmi_table,
    wmi_calculate_raw_average,
)
from cmk.base.config import check_info

# checks for is store and is clienttype
# as I understand it, these are logically related but the performance
# counters are completely separate

# source for these defaults:
# https://blogs.technet.microsoft.com/samdrey/2015/01/26/exchange-2013-performance-counters-and-their-thresholds/


def discover_msexch_isstore(parsed):
    return inventory_wmi_table_instances(parsed)


def check_msexch_isstore(item, params, parsed):
    try:
        average = wmi_calculate_raw_average(parsed[""], item, "RPCAverageLatency", 1)
    except KeyError:
        yield 3, "item not present anymore", []
    else:
        yield check_levels(
            average,
            "average_latency",
            get_levels_quadruple(params["store_latency"]),
            infoname="Average latency",
            unit="ms",
        )


check_info["msexch_isstore"] = LegacyCheckDefinition(
    parse_function=parse_wmi_table,
    service_name="Exchange IS Store %s",
    discovery_function=discover_msexch_isstore,
    check_function=check_msexch_isstore,
    check_ruleset_name="msx_info_store",
    check_default_parameters={
        "store_latency": (40.0, 50.0),
        "clienttype_latency": (40.0, 50.0),
        "clienttype_requests": (60, 70),
    },
)
