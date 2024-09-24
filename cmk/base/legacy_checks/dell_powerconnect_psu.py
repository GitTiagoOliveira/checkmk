#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Tested with Dell PowerConnect 5448 and 5424 models.
# Relevant SNMP OIDs:
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.1.67109185 = INTEGER: 67109185
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.1.67109186 = INTEGER: 67109186
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.2.67109185 = STRING: "ps1_unit1"
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.2.67109186 = STRING: "ps2_unit1"
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.3.67109185 = INTEGER: 1
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.3.67109186 = INTEGER: 5
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.4.67109185 = INTEGER: 5
# .1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1.4.67109186 = INTEGER: 4

# Status codes:
# 1 => normal,
# 2 => warning,
# 3 => critical,
# 4 => shutdown,
# 5 => notPresent,
# 6 => notFunctioning

# Supply Source Codes:
# 1 => unknown
# 2 => ac
# 3 => dc
# 4 => externalPowerSupply
# 5 => internalRedundant

# GENERAL MAPS:


from collections.abc import Sequence

from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.config import check_info

from cmk.agent_based.v2 import any_of, contains, SNMPTree, StringTable

dell_powerconnect_psu_status_map = {
    "1": "normal",
    "2": "warning",
    "3": "critical",
    "4": "shutdown",
    "5": "notPresent",
    "6": "notFunctioning",
}

dell_powerconnect_psu_supply_map = {
    "1": "Unknown",
    "2": "Alternating Current",
    "3": "Direct Current",
    "4": "External Power Supply",
    "5": "Internal Redundant",
}

dell_powerconnect_psu_status2nagios_map = {
    "normal": 0,
    "warning": 1,
    "critical": 2,
    "shutdown": 3,
    "notPresent": 1,
    "notFunctioning": 2,
}


def inventory_dell_powerconnect_psu(info):
    inventory = []
    if not info or not info[0]:
        return None
    hw_ident = info[0][0][0]
    for _device_id, name, state, _supply in info[1]:
        # M6220 are blade switches which report valid values only for the "Main"
        # sensor. The other one is reported as notFunctioning, but this is wrong.
        # Simply ignore the "System" sensor for those devices.
        if dell_powerconnect_psu_status_map[state] != "notPresent" and (
            "M6220" not in hw_ident or name != "System"
        ):
            inventory.append((name, None))
    return inventory


def check_dell_powerconnect_psu(item, _not_used, info):
    for _device_id, name, state, supply in info[1]:
        if name == item:
            dell_powerconnect_status = dell_powerconnect_psu_status_map[state]
            status = dell_powerconnect_psu_status2nagios_map[dell_powerconnect_status]

            return status, "Condition is {}, with source {}".format(
                dell_powerconnect_status,
                dell_powerconnect_psu_supply_map[supply],
            )

    return (3, "item not found in snmp data")


def parse_dell_powerconnect_psu(
    string_table: Sequence[StringTable],
) -> Sequence[StringTable]:
    return string_table


check_info["dell_powerconnect_psu"] = LegacyCheckDefinition(
    parse_function=parse_dell_powerconnect_psu,
    detect=any_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.674.10895"),
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.6027.1.3.22"),
    ),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.674.10895.3000.1.2.100.1",
            oids=["0"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.674.10895.3000.1.2.110.7.2.1",
            oids=["1", "2", "3", "4"],
        ),
    ],
    service_name="Sensor %s",
    discovery_function=inventory_dell_powerconnect_psu,
    check_function=check_dell_powerconnect_psu,
)
