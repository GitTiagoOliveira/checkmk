#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    IgnoreResults,
    Result,
    Service,
    State,
    StringTable,
)

SectionDatabases = dict[str, dict[str, str]]


def parse_mssql_databases(string_table: StringTable) -> SectionDatabases:
    """
    >>> from pprint import pprint
    >>> pprint(parse_mssql_databases([
    ...     ['MSSQL_MSSQL46', 'CorreLog_Report_T', 'ONLINE', 'FULL', '0', '0'],
    ... ]))
    {'MSSQL_MSSQL46 CorreLog_Report_T': {'DBname': 'CorreLog_Report_T',
                                         'Instance': 'MSSQL_MSSQL46',
                                         'Recovery': 'FULL',
                                         'Status': 'ONLINE',
                                         'auto_close': '0',
                                         'auto_shrink': '0'}}

    """

    parsed: SectionDatabases = {}
    headers = ["Instance", "DBname", "Status", "Recovery", "auto_close", "auto_shrink"]

    for line in string_table:
        if line == headers:
            continue

        if len(line) == 6:
            data = dict(zip(headers, line))
        elif len(line) == 7:
            data = dict(zip(headers, line[:2] + [f"{line[2]} {line[3]}"] + line[-3:]))
        else:
            continue
        parsed.setdefault("{} {}".format(data["Instance"], data["DBname"]), data)

    return parsed


agent_section_mssql_databases = AgentSection(
    name="mssql_databases",
    parse_function=parse_mssql_databases,
)


def discover_mssql_databases(section: SectionDatabases) -> DiscoveryResult:
    for key in section:
        yield Service(item=key)


def check_mssql_databases(
    item: str,
    params: Mapping[str, Any],
    section: SectionDatabases,
) -> CheckResult:
    data = section.get(item)
    if data is None:
        yield IgnoreResults("Login into database failed")
        return

    map_states = {
        "1": (1, "on"),
        "0": (0, "off"),
    }

    db_state = data["Status"]
    if db_state.startswith("ERROR: "):
        yield Result(state=State.CRIT, summary=db_state[7:])
        return
    state_int = params.get("map_db_states", {}).get(db_state.replace(" ", "_").upper(), 0)
    yield Result(state=State(state_int), summary="Status: %s" % db_state)
    if should_be_reco_model := params.get("recovery_model"):
        if should_be_reco_model == data["Recovery"]:
            yield Result(state=State.OK, summary="Recovery: %s" % data["Recovery"])
        else:
            yield Result(
                state=State(params["if_not_reco_model"]),
                summary=f"Recovery: {data['Recovery']} (but should {should_be_reco_model})",
            )

    yield Result(state=State.OK, summary="Recovery: %s" % data["Recovery"])

    for what in ["close", "shrink"]:
        state_int, state_readable = map_states[data["auto_%s" % what]]
        state_int = params.get("map_auto_%s_state" % what, {}).get(state_readable, state_int)
        yield Result(state=State(state_int), summary=f"Auto {what}: {state_readable}")


def cluster_check_mssql_databases(
    item: str,
    params: Mapping[str, Any],
    section: Mapping[str, SectionDatabases | None],
) -> CheckResult:
    conflated_section: SectionDatabases = {}
    for node_data in section.values():
        conflated_section.update(node_data or {})
    yield from check_mssql_databases(item, params, conflated_section)


check_plugin_mssql_databases = CheckPlugin(
    name="mssql_databases",
    service_name="MSSQL %s Database",
    discovery_function=discover_mssql_databases,
    check_function=check_mssql_databases,
    check_default_parameters={"if_not_reco_model": 1},
    check_ruleset_name="mssql_databases",
    cluster_check_function=cluster_check_mssql_databases,
)
