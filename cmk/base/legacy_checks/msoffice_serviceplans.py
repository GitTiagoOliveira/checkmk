#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Example output:
# <<<msoffice_serviceplans>>>
# msonline:VISIOCLIENT ONEDRIVE_BASIC Success
# msonline:VISIOCLIENT VISIOONLINE Success
# msonline:VISIOCLIENT EXCHANGE_S_FOUNDATION Success
# msonline:VISIOCLIENT VISIO_CLIENT_SUBSCRIPTION Success
# msonline:POWER_BI_PRO EXCHANGE_S_FOUNDATION Success
# msonline:POWER_BI_PRO BI_AZURE_P2 Success
# msonline:WINDOWS_STORE EXCHANGE_S_FOUNDATION Success
# msonline:WINDOWS_STORE WINDOWS_STORE PendingActivation


from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.config import check_info

from cmk.agent_based.v2.type_defs import StringTable


def inventory_msoffice_serviceplans(info):
    for line in info:
        yield line[0], {}


def check_msoffice_serviceplans(item, params, info):
    success = 0
    pending = 0
    pending_list = []
    warn, crit = params.get("levels", (None, None))
    for line in info:
        bundle, plan, status = line[0], " ".join(line[1:-1]), line[-1]
        if bundle == item:
            if status == "Success":
                success += 1
            elif status == "PendingActivation":
                pending += 1
                pending_list.append(plan)
    state = 0
    infotext = "Success: %d, Pending: %d" % (success, pending)
    if crit and pending >= crit:
        state = 2
    elif warn and pending >= warn:
        state = 1
    if state:
        infotext += " (warn/crit at %d/%d)" % (warn, crit)
    yield state, infotext
    if pending_list:
        yield 0, "Pending Services: %s" % ", ".join(pending_list)


def parse_msoffice_serviceplans(string_table: StringTable) -> StringTable:
    return string_table


check_info["msoffice_serviceplans"] = LegacyCheckDefinition(
    parse_function=parse_msoffice_serviceplans,
    service_name="MS Office Serviceplans %s",
    discovery_function=inventory_msoffice_serviceplans,
    check_function=check_msoffice_serviceplans,
    check_ruleset_name="msoffice_serviceplans",
)
