#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import typing
from collections.abc import Callable
from pathlib import Path

import pytest

from tests.unit.cmk.base.plugins.agent_based.snmp import get_parsed_snmp_section, snmp_is_detected
from tests.unit.conftest import FixRegister

from cmk.utils.sectionname import SectionName

from cmk.base.plugins.agent_based import mcafee_webgateway_misc
from cmk.base.plugins.agent_based.agent_based_api import v1

from cmk.plugins.lib import mcafee_gateway

# SUP-13087
WALK_MCAFEE = """
.1.3.6.1.2.1.1.1.0 McAfee Web Gateway 7;Hyper-V;Microsoft Corporation
.1.3.6.1.4.1.1230.2.7.2.5.1.0 0
.1.3.6.1.4.1.1230.2.7.2.5.2.0 2
.1.3.6.1.4.1.1230.2.7.2.5.3.0 2
.1.3.6.1.4.1.1230.2.7.2.5.4.0 0
.1.3.6.1.4.1.1230.2.7.2.5.5.0 0
.1.3.6.1.4.1.1230.2.7.2.5.6.0 0
.1.3.6.1.4.1.1230.2.7.2.5.7.0 0
.1.3.6.1.4.1.1230.2.7.2.5.8.0 0
.1.3.6.1.4.1.1230.2.7.2.5.9.0 0
.1.3.6.1.4.1.1230.2.7.2.5.10.0 0
.1.3.6.1.4.1.1230.2.7.2.5.11.0 0
.1.3.6.1.4.1.1230.2.7.2.5.12.0 0
.1.3.6.1.4.1.1230.2.7.2.5.13.0 0
.1.3.6.1.4.1.1230.2.7.2.5.14.0 0
.1.3.6.1.4.1.1230.2.7.2.5.15.0 41
"""

WALK_SKYHIGH = """
.1.3.6.1.2.1.1.2.0 1.3.6.1.4.1.59732.2.7.1.1
.1.3.6.1.4.1.59732.2.7.2.5.1.0 0
.1.3.6.1.4.1.59732.2.7.2.5.2.0 2
.1.3.6.1.4.1.59732.2.7.2.5.3.0 2
.1.3.6.1.4.1.59732.2.7.2.5.4.0 0
.1.3.6.1.4.1.59732.2.7.2.5.5.0 0
.1.3.6.1.4.1.59732.2.7.2.5.6.0 0
.1.3.6.1.4.1.59732.2.7.2.5.7.0 0
.1.3.6.1.4.1.59732.2.7.2.5.8.0 0
.1.3.6.1.4.1.59732.2.7.2.5.9.0 0
.1.3.6.1.4.1.59732.2.7.2.5.10.0 0
.1.3.6.1.4.1.59732.2.7.2.5.11.0 0
.1.3.6.1.4.1.59732.2.7.2.5.12.0 0
.1.3.6.1.4.1.59732.2.7.2.5.13.0 0
.1.3.6.1.4.1.59732.2.7.2.5.14.0 0
.1.3.6.1.4.1.59732.2.7.2.5.15.0 41
"""


@pytest.mark.parametrize(
    "walk, detected_section",
    [(WALK_MCAFEE, "mcafee_webgateway_misc"), (WALK_SKYHIGH, "skyhigh_security_webgateway_misc")],
)
def test_detect(
    walk: str, detected_section: str, fix_register: FixRegister, as_path: Callable[[str], Path]
) -> None:
    assert snmp_is_detected(SectionName(detected_section), as_path(walk))


@pytest.mark.parametrize(
    "walk, detected_section",
    [(WALK_MCAFEE, "mcafee_webgateway_misc"), (WALK_SKYHIGH, "skyhigh_security_webgateway_misc")],
)
def test_parse(
    walk: str, detected_section: str, fix_register: FixRegister, as_path: Callable[[str], Path]
) -> None:
    # Act
    section = get_parsed_snmp_section(SectionName(detected_section), as_path(walk))

    # Assert
    assert section is not None


@pytest.mark.parametrize(
    "walk, detected_section",
    [(WALK_MCAFEE, "mcafee_webgateway_misc"), (WALK_SKYHIGH, "skyhigh_security_webgateway_misc")],
)
def test_discovery(
    walk: str, detected_section: str, fix_register: FixRegister, as_path: Callable[[str], Path]
) -> None:
    # Assemble
    section = get_parsed_snmp_section(SectionName(detected_section), as_path(walk))
    assert section is not None

    # Act
    services = list(mcafee_webgateway_misc.discovery_webgateway_misc(section=section))

    # Assert
    assert services == [v1.Service()]


@pytest.mark.parametrize(
    "walk, detected_section, params_misc, expected_results",
    [
        pytest.param(
            WALK_MCAFEE,
            "mcafee_webgateway_misc",
            {"clients": None, "network_sockets": None},
            [
                v1.Result(state=v1.State.OK, summary="Clients: 2"),
                v1.Result(state=v1.State.OK, summary="Open network sockets: 2"),
            ],
            id="No levels mcafee",
        ),
        pytest.param(
            WALK_SKYHIGH,
            "skyhigh_security_webgateway_misc",
            {"clients": None, "network_sockets": None},
            [
                v1.Result(state=v1.State.OK, summary="Clients: 2"),
                v1.Result(state=v1.State.OK, summary="Open network sockets: 2"),
            ],
            id="No levels skyhigh",
        ),
        pytest.param(
            WALK_MCAFEE,
            "mcafee_webgateway_misc",
            {"clients": (3, 3), "network_sockets": (3, 3)},
            [
                v1.Result(state=v1.State.OK, summary="Clients: 2"),
                v1.Result(state=v1.State.OK, summary="Open network sockets: 2"),
            ],
            id="Levels, but OK",
        ),
        pytest.param(
            WALK_MCAFEE,
            "mcafee_webgateway_misc",
            {"clients": (2, 3), "network_sockets": (2, 3)},
            [
                v1.Result(state=v1.State.WARN, summary="Clients: 2 (warn/crit at 2/3)"),
                v1.Result(
                    state=v1.State.WARN, summary="Open network sockets: 2 (warn/crit at 2/3)"
                ),
            ],
            id="Critical",
        ),
        pytest.param(
            WALK_SKYHIGH,
            "skyhigh_security_webgateway_misc",
            {"clients": (2, 3), "network_sockets": (2, 3)},
            [
                v1.Result(state=v1.State.WARN, summary="Clients: 2 (warn/crit at 2/3)"),
                v1.Result(
                    state=v1.State.WARN, summary="Open network sockets: 2 (warn/crit at 2/3)"
                ),
            ],
            id="Critical skyhigh",
        ),
        pytest.param(
            WALK_MCAFEE,
            "mcafee_webgateway_misc",
            {"clients": (1, 2), "network_sockets": (1, 2)},
            [
                v1.Result(state=v1.State.CRIT, summary="Clients: 2 (warn/crit at 1/2)"),
                v1.Result(
                    state=v1.State.CRIT, summary="Open network sockets: 2 (warn/crit at 1/2)"
                ),
            ],
            id="Warning",
        ),
    ],
)
def test_check_results(
    walk: str,
    detected_section: str,
    fix_register: FixRegister,
    params_misc: dict[str, object],
    expected_results: list[v1.Result],
    as_path: Callable[[str], Path],
) -> None:
    # Assemble
    section = get_parsed_snmp_section(SectionName(detected_section), as_path(walk))
    assert section is not None
    params = typing.cast(
        mcafee_gateway.MiscParams, mcafee_gateway.MISC_DEFAULT_PARAMS | params_misc
    )

    # Act
    results = [
        r
        for r in mcafee_webgateway_misc.check_webgateway_misc(params=params, section=section)
        if isinstance(r, v1.Result)
    ]

    # Assert
    assert results == expected_results


def test_check_metrics(fix_register: FixRegister, as_path: Callable[[str], Path]) -> None:
    # Assemble
    section = get_parsed_snmp_section(SectionName("mcafee_webgateway_misc"), as_path(WALK_MCAFEE))
    assert section is not None

    # Act
    metrics = [
        r
        for r in mcafee_webgateway_misc.check_webgateway_misc(
            params=mcafee_gateway.MISC_DEFAULT_PARAMS, section=section
        )
        if isinstance(r, v1.Metric)
    ]

    # Assert
    assert metrics == [v1.Metric("connections", 2.0), v1.Metric("open_network_sockets", 2.0)]


INVALID_WALK = """
.1.3.6.1.4.1.1230.2.7.2.5.2.0
.1.3.6.1.4.1.1230.2.7.2.5.3.0
"""


def test_check_invalid_values(fix_register: FixRegister, as_path: Callable[[str], Path]) -> None:
    # Assemble
    # This walk is made up.
    section = get_parsed_snmp_section(SectionName("mcafee_webgateway_misc"), as_path(INVALID_WALK))

    # Assume
    assert section is not None

    # Act
    results = list(
        mcafee_webgateway_misc.check_webgateway_misc(
            params=mcafee_gateway.MISC_DEFAULT_PARAMS,
            section=section,
        )
    )

    # Assert
    assert not results
