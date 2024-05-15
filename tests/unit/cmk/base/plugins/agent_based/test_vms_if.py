#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.base.plugins.agent_based.vms_if import parse_vms_if

from cmk.plugins.lib import interfaces


def test_parse_vms_if() -> None:
    assert parse_vms_if(
        [
            ["SE0", "0", "6680", "0", "0", "0", "0", "0", "3649", "0", "0", "0", "0"],
            ["WE0", "-357453266", "0", "1246887166", "0", "0"],
            ["WE4", "6061662", "0", "4858067", "0", "0"],
        ]
    ) == [
        interfaces.InterfaceWithCounters(
            interfaces.Attributes(
                index="1",
                descr="SE0",
                alias="SE0",
                type="6",
                speed=1000000000,
                oper_status="1",
                oper_status_name="up",
            ),
            interfaces.Counters(
                in_octets=0,
                in_ucast=6680,
                in_mcast=0,
                in_bcast=0,
                in_disc=0,
                in_err=0,
                out_octets=0,
                out_ucast=3649,
                out_mcast=0,
                out_bcast=0,
                out_disc=0,
                out_err=0,
            ),
        ),
        interfaces.InterfaceWithCounters(
            interfaces.Attributes(
                index="2",
                descr="WE0",
                alias="WE0",
                type="6",
                speed=1000000000,
                oper_status="1",
                oper_status_name="up",
            ),
            interfaces.Counters(
                in_octets=3937514030,
                in_ucast=0,
                in_mcast=1246887166,
                in_bcast=0,
                in_disc=0,
            ),
        ),
        interfaces.InterfaceWithCounters(
            interfaces.Attributes(
                index="3",
                descr="WE4",
                alias="WE4",
                type="6",
                speed=1000000000,
                oper_status="1",
                oper_status_name="up",
            ),
            interfaces.Counters(
                in_octets=6061662,
                in_ucast=0,
                in_mcast=4858067,
                in_bcast=0,
                in_disc=0,
            ),
        ),
    ]
