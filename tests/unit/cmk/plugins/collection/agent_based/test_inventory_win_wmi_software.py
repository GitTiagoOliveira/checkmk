#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import time

import pytest

from cmk.agent_based.v2 import InventoryResult, StringTable, TableRow
from cmk.plugins.collection.agent_based.inventory_win_wmi_software import (
    inventory_win_wmi_software,
    parse_win_wmi_software,
    parse_win_wmi_software_json,
)

_INSTALLED_DATE = 123


def test_inventory_win_wmi_software_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(time, "mktime", lambda s: _INSTALLED_DATE)
    assert list(
        inventory_win_wmi_software(
            parse_win_wmi_software_json(
                [
                    [
                        '{ "ProductName":"Product|Name", "Publisher":"rehsilbup", '
                        '"VersionString":"14.0.1000.169", "InstallDate":"20180209",'
                        ' "Language":"1033"}'
                    ],
                    [
                        '{ "ProductName":"Microsoft .NET Framework 4.5.1 Multi-Targeting Pack",'
                        ' "Publisher":"Microsoft Corporation", '
                        '"VersionString":"4.5.50932", '
                        '"InstallDate":"19170629", '
                        '"Language":"1033"}'
                    ],
                ]
            )
        )
    ) == [
        TableRow(
            path=["software", "packages"],
            key_columns={
                "name": "Product|Name",
            },
            inventory_columns={
                "version": "14.0.1000.169",
                "vendor": "rehsilbup",
                "install_date": 123,
                "language": "1033",
                "package_type": "wmi",
            },
        ),
        TableRow(
            path=["software", "packages"],
            key_columns={
                "name": "Microsoft .NET Framework 4.5.1 Multi-Targeting Pack",
            },
            inventory_columns={
                "version": "4.5.50932",
                "vendor": "Microsoft Corporation",
                "install_date": None,
                "language": "1033",
                "package_type": "wmi",
            },
        ),
    ]


@pytest.mark.parametrize(
    "string_table, expected_result",
    [
        ([], []),
        (
            [
                ["64 Bit HP CIO Components Installer", "Hewlett-Packard", "15.2.1"],
                [
                    "Adobe Flash Player 12 ActiveX",
                    "Adobe Systems Incorporated",
                    "12.0.0.70",
                    "20161130",
                ],
                [
                    "Microsoft Visio 2010 Interactive Guide DEU",
                    "Microsoft",
                    "1.2.1",
                    "20161130",
                    "1033",
                ],
            ],
            [
                TableRow(
                    path=["software", "packages"],
                    key_columns={
                        "name": "64 Bit HP CIO Components Installer",
                    },
                    inventory_columns={
                        "version": "15.2.1",
                        "vendor": "Hewlett-Packard",
                        "install_date": None,
                        "language": "",
                        "package_type": "wmi",
                    },
                    status_columns={},
                ),
                TableRow(
                    path=["software", "packages"],
                    key_columns={
                        "name": "Adobe Flash Player 12 ActiveX",
                    },
                    inventory_columns={
                        "version": "12.0.0.70",
                        "vendor": "Adobe Systems Incorporated",
                        "install_date": _INSTALLED_DATE,
                        "language": "",
                        "package_type": "wmi",
                    },
                    status_columns={},
                ),
                TableRow(
                    path=["software", "packages"],
                    key_columns={
                        "name": "Microsoft Visio 2010 Interactive Guide DEU",
                    },
                    inventory_columns={
                        "version": "1.2.1",
                        "vendor": "Microsoft",
                        "install_date": _INSTALLED_DATE,
                        "language": "1033",
                        "package_type": "wmi",
                    },
                    status_columns={},
                ),
            ],
        ),
    ],
)
def test_inventory_win_wmi_software(
    monkeypatch: pytest.MonkeyPatch, string_table: StringTable, expected_result: InventoryResult
) -> None:
    monkeypatch.setattr(time, "mktime", lambda s: _INSTALLED_DATE)
    assert list(inventory_win_wmi_software(parse_win_wmi_software(string_table))) == expected_result
