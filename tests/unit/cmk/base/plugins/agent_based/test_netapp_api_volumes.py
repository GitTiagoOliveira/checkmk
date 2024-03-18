#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import datetime
from collections.abc import Iterable
from zoneinfo import ZoneInfo

import pytest
import time_machine

from cmk.base.plugins.agent_based import netapp_api_volumes as nav
from cmk.base.plugins.agent_based.agent_based_api.v1 import Metric, Result, Service, State

from cmk.plugins.lib.df import (
    FILESYSTEM_DEFAULT_LEVELS,
    INODES_DEFAULT_PARAMS,
    MAGIC_FACTOR_DEFAULT_PARAMS,
    TREND_DEFAULT_PARAMS,
)

STRING_TABLE = [
    [
        "volume 99efd228-e2d3-4d31-980e-470e19389806",
        "size-total 3068834836480",
        "node euedcnas1011",
        "files-total 31876696",
        "vserver_name euedcnas1011",
        "name vol_1011_root",
        "state online",
        "size-available 2996744216576",
        "files-used 63106",
        "fcp_write_data 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "read_latency 641571331962",
        "nfs_write_ops 0",
        "fcp_read_ops 0",
        "fcp_read_data 0",
        "cifs_write_ops 0",
        "iscsi_read_latency 0",
        "nfs_write_latency 0",
        "iscsi_read_ops 0",
        "read_ops 1023923957",
        "cifs_read_latency 0",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name vol_1011_root",
        "san_read_ops 0",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 1733658177396",
        "cifs_write_data 0",
        "iscsi_write_data 0",
        "san_write_latency 0",
        "san_write_data 0",
        "iscsi_write_ops 0",
        "san_write_ops 0",
        "fcp_write_latency 0",
        "fcp_write_ops 0",
        "nfs_read_ops 0",
        "read_data 6745251997344",
        "cifs_read_ops 0",
        "write_latency 103955282923",
        "cifs_read_data 0",
        "nfs_read_data 0",
        "write_ops 539245772",
        "nfs_write_data 0",
        "cifs_write_latency 0",
    ],
    [
        "volume 0bec3d74-a3ca-4269-be10-5bb890c5bfe2",
        "size-total 3068834836480",
        "node euedcnas1012",
        "files-total 31876696",
        "vserver_name euedcnas1012",
        "name vol_1012_root",
        "state online",
        "size-available 3034830319616",
        "files-used 62894",
        "fcp_write_data 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "read_latency 492694300156",
        "nfs_write_ops 0",
        "fcp_read_ops 0",
        "fcp_read_data 0",
        "cifs_write_ops 0",
        "iscsi_read_latency 0",
        "nfs_write_latency 0",
        "iscsi_read_ops 0",
        "read_ops 339222081",
        "cifs_read_latency 0",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name vol_1012_root",
        "san_read_ops 0",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 1512773163403",
        "cifs_write_data 0",
        "iscsi_write_data 0",
        "san_write_latency 0",
        "san_write_data 0",
        "iscsi_write_ops 0",
        "san_write_ops 0",
        "fcp_write_latency 0",
        "fcp_write_ops 0",
        "nfs_read_ops 0",
        "read_data 2064285089001",
        "cifs_read_ops 0",
        "write_latency 36447123810",
        "cifs_read_data 0",
        "nfs_read_data 0",
        "write_ops 391736081",
        "nfs_write_data 0",
        "cifs_write_latency 0",
    ],
    [
        "volume e585741f-5e66-4bb9-9d21-3966a28174af",
        "size-total 161061273600",
        "node euedcnas1012",
        "files-total 4669444",
        "vserver_name euedcnas1710",
        "name v_1710_a2mac1",
        "msid 2155257036",
        "state broken",
        "size-available 34452643840",
        "files-used 329535",
        "fcp_write_data 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "read_latency 5690194839",
        "nfs_write_ops 0",
        "fcp_read_ops 0",
        "fcp_read_data 0",
        "cifs_write_ops 269223",
        "iscsi_read_latency 0",
        "nfs_write_latency 0",
        "iscsi_read_ops 0",
        "read_ops 1046981",
        "cifs_read_latency 5651491277",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name v_1710_a2mac1",
        "san_read_ops 0",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 21266276975",
        "cifs_write_data 20676268249",
        "iscsi_write_data 0",
        "san_write_latency 0",
        "san_write_data 0",
        "iscsi_write_ops 0",
        "san_write_ops 0",
        "fcp_write_latency 0",
        "fcp_write_ops 0",
        "nfs_read_ops 0",
        "read_data 45020886427",
        "cifs_read_ops 856082",
        "write_latency 63998626",
        "cifs_read_data 44361557879",
        "nfs_read_data 0",
        "write_ops 291850",
        "nfs_write_data 0",
        "cifs_write_latency 60204543",
    ],
    [
        "volume 004379ad-59c3-443f-bc01-9dab2f12e54f",
        "size-total 322122547200",
        "node euedcnas1012",
        "files-total 9338875",
        "vserver_name euedcnas1710",
        "name v_1710_aspera",
        "msid 2155257034",
        "state online",
        "size-available 128706699264",
        "files-used 3414",
        "fcp_write_data 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "read_latency 8121797",
        "nfs_write_ops 0",
        "fcp_read_ops 0",
        "fcp_read_data 0",
        "cifs_write_ops 0",
        "iscsi_read_latency 0",
        "nfs_write_latency 0",
        "iscsi_read_ops 0",
        "read_ops 135861",
        "cifs_read_latency 0",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name v_1710_aspera",
        "san_read_ops 0",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 640774",
        "cifs_write_data 0",
        "iscsi_write_data 0",
        "san_write_latency 0",
        "san_write_data 0",
        "iscsi_write_ops 0",
        "san_write_ops 0",
        "fcp_write_latency 0",
        "fcp_write_ops 0",
        "nfs_read_ops 0",
        "read_data 70677732",
        "cifs_read_ops 0",
        "write_latency 342316",
        "cifs_read_data 0",
        "nfs_read_data 0",
        "write_ops 1954",
        "nfs_write_data 0",
        "cifs_write_latency 0",
    ],
    [
        "volume 619e3283-7151-4f15-ad32-81e241613ecd",
        "size-total 1099511627776",
        "node euedcnas1012",
        "files-total 31876696",
        "vserver_name euedcnas1710",
        "name v_1710_data",
        "msid 2155256942",
        "state online",
        "size-available 1098808291328",
        "files-used 315",
        "fcp_write_data 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "read_latency 22911925",
        "nfs_write_ops 0",
        "fcp_read_ops 0",
        "fcp_read_data 0",
        "cifs_write_ops 0",
        "iscsi_read_latency 0",
        "nfs_write_latency 0",
        "iscsi_read_ops 0",
        "read_ops 137695",
        "cifs_read_latency 13502252",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name v_1710_data",
        "san_read_ops 0",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 1363374",
        "cifs_write_data 0",
        "iscsi_write_data 0",
        "san_write_latency 0",
        "san_write_data 0",
        "iscsi_write_ops 0",
        "san_write_ops 0",
        "fcp_write_latency 0",
        "fcp_write_ops 0",
        "nfs_read_ops 0",
        "read_data 808349225",
        "cifs_read_ops 1642",
        "write_latency 1096990",
        "cifs_read_data 736920818",
        "nfs_read_data 0",
        "write_ops 3864",
        "nfs_write_data 0",
        "cifs_write_latency 0",
    ],
    [
        "volume vol0",
        "size-available 209570025472",
        "state online",
        "files-total 7782396",
        "files-used 10737",
        "size-total 228170137600",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 0",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 788111488271",
        "nfs_write_latency 108420",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 20135569973",
        "cifs_read_latency 0",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 19007164",
        "iscsi_read_data 0",
        "instance_name vol0",
        "cifs_read_data 0",
        "nfs_read_data 180684471",
        "write_latency 127083421865",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 470709801331",
        "nfs_write_data 6121275",
        "cifs_write_latency 0",
    ],
    [
        "volume vol_bronze1_fundorado_cifs",
        "size-available 5681445965824",
        "state online",
        "files-total 31876689",
        "files-used 3058888",
        "size-total 9400824418304",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 5993355785148",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 10083880638990",
        "nfs_write_latency 0",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 62090615998",
        "cifs_read_latency 59464480059",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_fundorado_cifs",
        "cifs_read_data 9748984278714",
        "nfs_read_data 0",
        "write_latency 132180118822",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 6300214716764",
        "nfs_write_data 0",
        "cifs_write_latency 128809541597",
    ],
    [
        "volume vol_bronze1_ftpfreenet_nfs",
        "size-available 2348812120064",
        "state online",
        "files-total 31876689",
        "files-used 2694615",
        "size-total 4947802324992",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 0",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 14495321097272",
        "nfs_write_latency 436623773693",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 1321841542993",
        "cifs_read_latency 0",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 1318276162059",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_ftpfreenet_nfs",
        "cifs_read_data 0",
        "nfs_read_data 14038673026364",
        "write_latency 441267513699",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 5516992855944",
        "nfs_write_data 5106734367496",
        "cifs_write_latency 0",
    ],
    [
        "volume vol_bronze1_nfs",
        "size-available 18063153672192",
        "state online",
        "files-total 392536979",
        "files-used 32824906",
        "size-total 33425153486848",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 629525512283",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 258198800160064",
        "nfs_write_latency 3284753782325",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 18906485485409",
        "cifs_read_latency 59911208593",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 18738739813315",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_nfs",
        "cifs_read_data 1373882337514",
        "nfs_read_data 245196278213658",
        "write_latency 3412600142574",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 241225507897086",
        "nfs_write_data 229575392006609",
        "cifs_write_latency 6374158509",
    ],
    [
        "volume vol_bronze1_enterprise_vault",
        "size-available 6317505187840",
        "state online",
        "files-total 386818032",
        "files-used 233640753",
        "size-total 17757112791040",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 2797504453226",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 13198309405534",
        "nfs_write_latency 0",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 1332614234054",
        "cifs_read_latency 1332014859907",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 0",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_enterprise_vault",
        "cifs_read_data 13060307696514",
        "nfs_read_data 0",
        "write_latency 75431342425",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 2935420540154",
        "nfs_write_data 0",
        "cifs_write_latency 73712224394",
    ],
    [
        "volume vol_bronze1_cifs",
        "size-available 12137213788160",
        "state online",
        "files-total 31876689",
        "files-used 10483961",
        "size-total 16712576745472",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 6531283943261",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 4002760800079",
        "nfs_write_latency 13176712585",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 958566213067",
        "cifs_read_latency 878519925020",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 76274494693",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_cifs",
        "cifs_read_data 3017117067272",
        "nfs_read_data 513505960083",
        "write_latency 439931061563",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 8408643107314",
        "nfs_write_data 1445857053805",
        "cifs_write_latency 422105859254",
    ],
    [
        "volume vol_bronze1_firebirdbackup_nfs",
        "size-available 457455501312",
        "state online",
        "files-total 31876689",
        "files-used 145",
        "size-total 831230795776",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 0",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 14518295021500",
        "nfs_write_latency 284302930608",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 287461642429",
        "cifs_read_latency 0",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 283857474274",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_firebirdbackup_nfs",
        "cifs_read_data 0",
        "nfs_read_data 14143837216272",
        "write_latency 289091386833",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 31787066083361",
        "nfs_write_data 31122622092264",
        "cifs_write_latency 0",
    ],
    [
        "volume vol_bronze1_singlescm_nfs",
        "size-available 68105011200",
        "state offline",
        "files-total 3112959",
        "files-used 154127",
        "size-total 107374182400",
        "fcp_write_data 0",
        "fcp_read_data 0",
        "cifs_write_data 0",
        "iscsi_read_latency 0",
        "iscsi_write_data 0",
        "read_data 1675013596",
        "nfs_write_latency 32687796",
        "san_write_latency 0",
        "san_write_data 0",
        "read_latency 334395407",
        "cifs_read_latency 0",
        "fcp_write_latency 0",
        "fcp_read_latency 0",
        "iscsi_write_latency 0",
        "nfs_read_latency 330848378",
        "iscsi_read_data 0",
        "instance_name vol_bronze1_singlescm_nfs",
        "cifs_read_data 0",
        "nfs_read_data 284389248",
        "write_latency 248329456",
        "san_read_data 0",
        "san_read_latency 0",
        "write_data 50241577605",
        "nfs_write_data 5550238259",
        "cifs_write_latency 0",
    ],
]

DISCOVERY_PARAMS = [
    {
        "groups": [
            {
                "group_name": "euedcnas1710.v_1710_data",
                "patterns_include": ["euedcnas1710.v_1710_data"],
                "patterns_exclude": [],
            },
            {"group_name": "group1", "patterns_include": ["vol0"], "patterns_exclude": []},
            {"group_name": "group2", "patterns_include": ["vol_bronze1*"], "patterns_exclude": []},
            {
                "group_name": "group2",
                "patterns_include": [],
                "patterns_exclude": ["vol_bronze1_cifs"],
            },
            {"group_name": "group3", "patterns_include": [], "patterns_exclude": []},
        ],
    }
]


@pytest.fixture(name="section", scope="module")
def _get_section() -> nav.Section:
    return nav.parse_netapp_api_volumes(STRING_TABLE)


def test_discovery(section: nav.Section) -> None:
    assert sorted(nav.discover_netapp_api_volumes(DISCOVERY_PARAMS, section)) == sorted(
        [
            Service(item="euedcnas1011.vol_1011_root"),
            Service(item="euedcnas1012.vol_1012_root"),
            Service(item="euedcnas1710.v_1710_a2mac1"),
            Service(item="euedcnas1710.v_1710_aspera"),
            Service(
                item="euedcnas1710.v_1710_data",
                parameters={"patterns": (["euedcnas1710.v_1710_data"], [])},
            ),
            Service(item="group1", parameters={"patterns": (["vol0"], [])}),
            Service(
                item="group2", parameters={"patterns": (["vol_bronze1*"], ["vol_bronze1_cifs"])}
            ),
            Service(item="vol_bronze1_cifs"),
        ]
    )


def test_check_broken_volume(section: nav.Section) -> None:
    assert list(
        nav.check_netapp_api_volumes(
            "euedcnas1710.v_1710_a2mac1",
            {},
            section,
        )
    ) == [
        Result(state=State.WARN, summary="Volume is broken"),
    ]


def test_check_grouped(section: nav.Section, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        nav,
        "get_value_store",
        lambda: {"group1.delta": (1591789747, 0)},
    )
    with time_machine.travel(
        datetime.datetime(2020, 6, 10, 13, 50, 21, tzinfo=ZoneInfo("UTC")), tick=False
    ):
        assert list(
            nav.check_netapp_api_volumes(
                "group1",
                {
                    **FILESYSTEM_DEFAULT_LEVELS,
                    **MAGIC_FACTOR_DEFAULT_PARAMS,
                    **INODES_DEFAULT_PARAMS,
                    **TREND_DEFAULT_PARAMS,
                    "patterns": (["vol0"], []),
                },
                section,
            )
        ) == [
            Metric(
                "fs_used", 17738.44921875, levels=(174080.0, 195840.0), boundaries=(0.0, 217600.0)
            ),
            Metric("fs_free", 199861.55078125, boundaries=(0.0, None)),
            Metric(
                "fs_used_percent", 8.151860854204964, levels=(80.0, 90.0), boundaries=(0.0, 100.0)
            ),
            Result(state=State.OK, summary="Used: 8.15% - 18.6 GB of 228 GB"),
            Metric("fs_size", 217600.0, boundaries=(0.0, None)),
            Metric("growth", 210695.9049353863),
            Result(state=State.OK, summary="trend per 1 day 0 hours: +221 GB"),
            Result(state=State.OK, summary="trend per 1 day 0 hours: +96.83%"),
            Metric("trend", 210695.9049353863),
            Result(state=State.OK, summary="Time left until disk full: 22 hours 45 minutes"),
            Metric(
                "inodes_used",
                10737.0,
                levels=(7004156.4, 7393276.199999999),
                boundaries=(0.0, 7782396.0),
            ),
            Result(
                state=State.OK, notice="Inodes used: 0.14%, Inodes available: 7,771,659 (99.86%)"
            ),
            Result(state=State.OK, notice="1 volume(s) in group"),
        ]


def _create_keys() -> Iterable[str]:
    for mode in ("read", "write"):
        for field in ("data", "ops", "latency"):
            yield f"{mode}_{field}"
            yield from (
                f"{proto}_{mode}_{field}" for proto in ("nfs", "cifs", "san", "fcp", "iscsi")
            )


def test_check_with_perf_data(section: nav.Section, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        nav,
        "get_value_store",
        lambda: {
            "euedcnas1710.v_1710_aspera.delta": (1591789747, 0),
            **{k: (1591789747, 0) for k in _create_keys()},
        },
    )
    with time_machine.travel(
        datetime.datetime(2020, 6, 10, 13, 50, 21, tzinfo=ZoneInfo("UTC")), tick=False
    ):
        assert list(
            nav.check_netapp_api_volumes(
                "euedcnas1710.v_1710_aspera",
                {
                    "levels": (10.0, 20.0),
                    "magic_normsize": 20,
                    "levels_low": (50.0, 60.0),
                    "trend_range": 24,
                    "trend_perfdata": True,
                    "show_levels": "onmagic",
                    "inodes_levels": (10.0, 5.0),
                    "show_inodes": "always",
                    "show_reserved": False,
                    "perfdata": ["", "nfs", "cifs", "san", "fcp", "iscsi"],
                    "magic": 0.8,
                    "trend_bytes": (104857600, 209715200),
                    "trend_perc": (5.0, 10.0),
                    "trend_timeleft": (12, 6),
                    "trend_showtimeleft": True,
                },
                section,
            )
        ) == [
            Metric(
                "fs_used", 184455.7265625, levels=(153600.0, 184320.0), boundaries=(0.0, 307200.0)
            ),
            Metric("fs_free", 122744.2734375, boundaries=(0.0, None)),
            Metric(
                "fs_used_percent", 60.04418182373047, levels=(50.0, 60.0), boundaries=(0.0, 100.0)
            ),
            Result(
                state=State.CRIT,
                summary="Used: 60.04% - 193 GB of 322 GB (warn/crit at 50.00%/60.00% used)",
            ),
            Metric("fs_size", 307200.0, boundaries=(0.0, None)),
            Metric("growth", 2190950.615204839),
            Result(
                state=State.CRIT,
                summary="trend per 1 day 0 hours: +2.30 TB (warn/crit at +105 MB/+210 MB)",
            ),
            Result(
                state=State.CRIT,
                summary="trend per 1 day 0 hours: +713.20% (warn/crit at +5.00%/+10.00%)",
            ),
            Metric("trend", 2190950.615204839, levels=(100.0, 200.0)),
            Result(
                state=State.CRIT,
                summary="Time left until disk full: 1 hour 20 minutes (warn/crit below 12 hours 0 minutes/6 hours 0 minutes)",
            ),
            Metric("trend_hoursleft", 1.3445590886696375),
            Metric(
                "inodes_used", 3414.0, levels=(8404987.5, 8871931.25), boundaries=(0.0, 9338875.0)
            ),
            Result(
                state=State.OK, summary="Inodes used: 0.04%, Inodes available: 9,335,461 (99.96%)"
            ),
            Metric("read_data", 9716.487764641188),
            Metric("read_ops", 18.67761891668958),
            Metric("read_latency", 0.05978019446345899),
            Metric("write_data", 88.09100907341215),
            Metric("write_ops_s", 0.2686279901017322),
            Metric("write_latency", 0.17518730808597746),
            Metric("nfs_read_data", 0.0),
            Metric("nfs_read_ops", 0.0),
            Metric("nfs_read_latency", 0.0),
            Metric("nfs_write_data", 0.0),
            Metric("nfs_write_ops", 0.0),
            Metric("nfs_write_latency", 0.0),
            Metric("cifs_read_data", 0.0),
            Metric("cifs_read_ops", 0.0),
            Metric("cifs_read_latency", 0.0),
            Metric("cifs_write_data", 0.0),
            Metric("cifs_write_ops", 0.0),
            Metric("cifs_write_latency", 0.0),
            Metric("san_read_data", 0.0),
            Metric("san_read_ops", 0.0),
            Metric("san_read_latency", 0.0),
            Metric("san_write_data", 0.0),
            Metric("san_write_ops", 0.0),
            Metric("san_write_latency", 0.0),
            Metric("fcp_read_data", 0.0),
            Metric("fcp_read_ops", 0.0),
            Metric("fcp_read_latency", 0.0),
            Metric("fcp_write_data", 0.0),
            Metric("fcp_write_ops", 0.0),
            Metric("fcp_write_latency", 0.0),
            Metric("iscsi_read_data", 0.0),
            Metric("iscsi_read_ops", 0.0),
            Metric("iscsi_read_latency", 0.0),
            Metric("iscsi_write_data", 0.0),
            Metric("iscsi_write_ops", 0.0),
            Metric("iscsi_write_latency", 0.0),
        ]
