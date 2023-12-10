#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import time
from collections.abc import Iterable, Mapping

from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.cpu_util import check_cpu_util
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree

import cmk.plugins.lib.pulse_secure as pulse_secure
from cmk.agent_based.v2.type_defs import StringTable

Section = Mapping[str, int]

KEY_PULSE_SECURE_CPU = "cpu_util"


def parse_pulse_secure_cpu_util(string_table: StringTable) -> Section:
    return pulse_secure.parse_pulse_secure(string_table, KEY_PULSE_SECURE_CPU)


def discover_pulse_secure_cpu_util(section: Section) -> Iterable[tuple[None, dict]]:
    if section:
        yield None, {}


def check_pulse_secure_cpu(item, params, parsed):
    if not parsed:
        return None

    return check_cpu_util(parsed[KEY_PULSE_SECURE_CPU], params, this_time=time.time())


check_info["pulse_secure_cpu_util"] = LegacyCheckDefinition(
    detect=pulse_secure.DETECT_PULSE_SECURE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.12532",
        oids=["10"],
    ),
    parse_function=parse_pulse_secure_cpu_util,
    service_name="Pulse Secure IVE CPU utilization",
    discovery_function=discover_pulse_secure_cpu_util,
    check_function=check_pulse_secure_cpu,
    check_ruleset_name="cpu_utilization",
    check_default_parameters={"util": (80.0, 90.0)},
)
