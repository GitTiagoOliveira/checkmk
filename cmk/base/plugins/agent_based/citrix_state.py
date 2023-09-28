#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

from cmk.base.plugins.agent_based.agent_based_api import v1
from cmk.base.plugins.agent_based.utils.citrix_state import Section

Params = Mapping[str, Mapping[str, int]]
DEFAULT_PARAMS = {
    "registrationstate": {
        "Unregistered": 2,
        "Initializing": 1,
        "Registered": 0,
        "AgentError": 2,
    },
}
_CONSTANTS_MAP = {
    "maintenancemode": {
        "False": 0,
        "True": 1,
    },
    "powerstate": {
        "Unmanaged": 1,
        "Unknown": 1,
        "Unavailable": 2,
        "Off": 2,
        "On": 0,
        "Suspended": 2,
        "TurningOn": 1,
        "TurningOff": 1,
    },
    "vmtoolsstate": {
        "NotPresent": 2,
        "Unknown": 3,
        "NotStarted": 1,
        "Running": 0,
    },
    "faultstate": {
        "None": 0,
        "FailedToStart": 2,
        "StuckOnBoot": 2,
        "Unregistered": 2,
        "MaxCapacity": 1,
    },
}


def discovery_citrix_state_controller(section: Section) -> v1.type_defs.DiscoveryResult:
    if "controller" in section:
        yield v1.Service()


def check_citrix_state_controller(section: Section) -> v1.type_defs.CheckResult:
    yield v1.Result(state=v1.State.OK, summary=section["controller"] or "Machine powered off")


v1.register.check_plugin(
    name="citrix_state_controller",
    sections=["citrix_state"],
    discovery_function=discovery_citrix_state_controller,
    check_function=check_citrix_state_controller,
    service_name="Citrix Controller",
)


def discovery_citrix_state_hosting_server(section: Section) -> v1.type_defs.DiscoveryResult:
    if "hosting_server" in section:
        yield v1.Service()


def check_citrix_state_hosting_server(section: Section) -> v1.type_defs.CheckResult:
    yield v1.Result(state=v1.State.OK, summary=section["hosting_server"])


v1.register.check_plugin(
    name="citrix_state_hosting_server",
    sections=["citrix_state"],
    discovery_function=discovery_citrix_state_controller,
    check_function=check_citrix_state_hosting_server,
    service_name="Citrix Hosting Server",
)


def discovery_citrix_state(section: Section) -> v1.type_defs.DiscoveryResult:
    if section["instance"]:
        yield v1.Service()


def check_citrix_state(params: Params, section: Section) -> v1.type_defs.CheckResult:
    for state_type, state in section["instance"].items():
        if (
            monitoring_map := (
                params.get(state_type.lower()) or _CONSTANTS_MAP.get(state_type.lower())
            )
        ) is not None:
            yield v1.Result(state=v1.State(monitoring_map[state]), summary=f"{state_type} {state}")


v1.register.check_plugin(
    name="citrix_state",
    discovery_function=discovery_citrix_state,
    check_function=check_citrix_state,
    service_name="Citrix Instance State",
    check_ruleset_name="citrix_state",
    check_default_parameters=DEFAULT_PARAMS,
)
