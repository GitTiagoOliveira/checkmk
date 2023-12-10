#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.alcatel import check_alcatel_fans, inventory_alcatel_fans
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree

from cmk.agent_based.v2.type_defs import StringTable
from cmk.plugins.lib.alcatel import DETECT_ALCATEL


def parse_alcatel_fans(string_table: StringTable) -> StringTable:
    return string_table


check_info["alcatel_fans"] = LegacyCheckDefinition(
    parse_function=parse_alcatel_fans,
    detect=DETECT_ALCATEL,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.6486.800.1.1.1.3.1.1.11.1",
        oids=["2"],
    ),
    service_name="Fan %s",
    discovery_function=inventory_alcatel_fans,
    check_function=check_alcatel_fans,
)
