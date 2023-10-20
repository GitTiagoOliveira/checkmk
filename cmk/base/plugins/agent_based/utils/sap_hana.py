#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import Any, Dict, List, NamedTuple, Tuple, Union

from ..agent_based_api.v1 import IgnoreResults, Metric, Result, State
from ..agent_based_api.v1.type_defs import StringTable


class CheckResults(NamedTuple):
    overall_state: State
    results: List[Union[IgnoreResults, Metric, Result]] = []


ParsedSection = Dict[str, Dict]


def parse_sap_hana(info: StringTable):
    parsed: Dict[str, List[Any]] = {}
    instance = None
    for line in info:
        joined_line = " ".join(line)
        if joined_line.startswith("[[") and joined_line.endswith("]]"):
            instance = parsed.setdefault(joined_line[2:-2], [])
        elif instance is not None:
            instance.append([e.strip('"') for e in line])
    return parsed


def parse_sap_hana_cluster_aware(info):
    parsed: Dict[Tuple, List[Any]] = {}
    instance = None
    for line in info:
        node, line = line[0], line[1:]
        joined_line = " ".join(line)
        if joined_line.startswith("[[") and joined_line.endswith("]]"):
            instance = parsed.setdefault((joined_line[2:-2], node), [])
        elif instance is not None:
            instance.append([e.strip('"') for e in line])
    return parsed


def get_replication_state(raw: str) -> tuple[State, str, str]:
    if raw == "0":
        return State.UNKNOWN, "unknown status from replication script", "state_unknown"
    if raw == "10":
        return State.CRIT, "no system replication", "state_no_replication"
    if raw == "11":
        return State.CRIT, "error", "state_error"
    if raw == "12":
        # "12" actually stands for "unknown replication status", but as per customer's information
        # (see SUP-1436), this should be indicated as "passive" replication aka secondary SAP HANA node.
        return State.OK, "passive", "state_replication_unknown"
    if raw == "13":
        return State.WARN, "initializing", "state_initializing"
    if raw == "14":
        return State.OK, "syncing", "state_syncing"
    if raw == "15":
        return State.OK, "active", "state_active"

    return State.UNKNOWN, "unknown[%s]" % raw, "state_unknown"
