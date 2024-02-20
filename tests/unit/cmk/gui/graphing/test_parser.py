#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.gui.graphing._parser import parse_unit

from cmk.graphing.v1 import metrics, Title


@pytest.mark.parametrize(
    "unit, expected_symbol",
    [
        pytest.param(
            metrics.Unit.BAR,
            "bar",
            id="BAR",
        ),
        pytest.param(
            metrics.Unit.BIT_IEC,
            "bits",
            id="BIT_IEC",
        ),
        pytest.param(
            metrics.Unit.BITS_IEC_PER_SECOND,
            "bits/s",
            id="BITS_IEC_PER_SECOND,",
        ),
        pytest.param(
            metrics.Unit.BIT_SI,
            "bits",
            id="BIT_SI",
        ),
        pytest.param(
            metrics.Unit.BITS_SI_PER_SECOND,
            "bits/s",
            id="BITS_SI_PER_SECOND",
        ),
        pytest.param(
            metrics.Unit.BYTE_IEC,
            "bytes",
            id="BYTE_IEC",
        ),
        pytest.param(
            metrics.Unit.BYTES_IEC_PER_DAY,
            "bytes/d",
            id="BYTES_IEC_PER_DAY",
        ),
        pytest.param(
            metrics.Unit.BYTES_IEC_PER_OPERATION,
            "bytes/op",
            id="BYTES_IEC_PER_OPERATION",
        ),
        pytest.param(
            metrics.Unit.BYTES_IEC_PER_SECOND,
            "bytes/s",
            id="BYTES_IEC_PER_SECOND",
        ),
        pytest.param(
            metrics.Unit.BYTE_SI,
            "bytes",
            id="BYTE_SI",
        ),
        pytest.param(
            metrics.Unit.BYTES_SI_PER_DAY,
            "bytes/d",
            id="BYTES_SI_PER_DAY",
        ),
        pytest.param(
            metrics.Unit.BYTES_SI_PER_OPERATION,
            "bytes/op",
            id="BYTES_SI_PER_OPERATION",
        ),
        pytest.param(
            metrics.Unit.BYTES_SI_PER_SECOND,
            "bytes/s",
            id="BYTES_SI_PER_SECOND",
        ),
        pytest.param(
            metrics.Unit.COUNT,
            "",
            id="COUNT",
        ),
        pytest.param(
            metrics.Unit.DECIBEL,
            "dB",
            id="DECIBEL",
        ),
        pytest.param(
            metrics.Unit.DECIBEL_MILLIVOLT,
            "dBmV",
            id="DECIBEL_MILLIVOLT",
        ),
        pytest.param(
            metrics.Unit.DECIBEL_MILLIWATT,
            "dBm",
            id="DECIBEL_MILLIWATT",
        ),
        pytest.param(
            metrics.Unit.DOLLAR,
            "$",
            id="DOLLAR",
        ),
        pytest.param(
            metrics.Unit.ELETRICAL_ENERGY,
            "Wh",
            id="ELETRICAL_ENERGY",
        ),
        pytest.param(
            metrics.Unit.EURO,
            "€",
            id="EURO",
        ),
        pytest.param(
            metrics.Unit.LITER_PER_SECOND,
            "l/s",
            id="LITER_PER_SECOND",
        ),
        pytest.param(
            metrics.Unit.NUMBER,
            "",
            id="NUMBER",
        ),
        pytest.param(
            metrics.Unit.PARTS_PER_MILLION,
            "ppm",
            id="PARTS_PER_MILLION",
        ),
        pytest.param(
            metrics.Unit.PERCENTAGE,
            "%",
            id="PERCENTAGE",
        ),
        pytest.param(
            metrics.Unit.PERCENTAGE_PER_METER,
            "%/m",
            id="PERCENTAGE_PER_METER",
        ),
        pytest.param(
            metrics.Unit.PER_SECOND,
            "1/s",
            id="PER_SECOND",
        ),
        pytest.param(
            metrics.Unit.READ_CAPACITY_UNIT,
            "RCU",
            id="READ_CAPACITY_UNIT",
        ),
        pytest.param(
            metrics.Unit.REVOLUTIONS_PER_MINUTE,
            "rpm",
            id="REVOLUTIONS_PER_MINUTE",
        ),
        pytest.param(
            metrics.Unit.SECONDS_PER_SECOND,
            "s/s",
            id="SECONDS_PER_SECOND",
        ),
        pytest.param(
            metrics.Unit.VOLT_AMPERE,
            "VA",
            id="VOLT_AMPERE",
        ),
        pytest.param(
            metrics.Unit.WRITE_CAPACITY_UNIT,
            "WCU",
            id="WRITE_CAPACITY_UNIT",
        ),
        pytest.param(
            metrics.Unit.AMPERE,
            "A",
            id="AMPERE",
        ),
        pytest.param(
            metrics.Unit.CANDELA,
            "cd",
            id="CANDELA",
        ),
        pytest.param(
            metrics.Unit.KELVIN,
            "K",
            id="KELVIN",
        ),
        pytest.param(
            metrics.Unit.KILOGRAM,
            "kg",
            id="KILOGRAM",
        ),
        pytest.param(
            metrics.Unit.METRE,
            "m",
            id="METRE",
        ),
        pytest.param(
            metrics.Unit.MOLE,
            "mol",
            id="MOLE",
        ),
        pytest.param(
            metrics.Unit.SECOND,
            "s",
            id="SECOND",
        ),
        pytest.param(
            metrics.Unit.BECQUEREL,
            "Bq",
            id="BECQUEREL",
        ),
        pytest.param(
            metrics.Unit.COULOMB,
            "C",
            id="COULOMB",
        ),
        pytest.param(
            metrics.Unit.DEGREE_CELSIUS,
            "°C",
            id="DEGREE_CELSIUS",
        ),
        pytest.param(
            metrics.Unit.FARAD,
            "F",
            id="FARAD",
        ),
        pytest.param(
            metrics.Unit.GRAY,
            "Gy",
            id="GRAY",
        ),
        pytest.param(
            metrics.Unit.HENRY,
            "H",
            id="HENRY",
        ),
        pytest.param(
            metrics.Unit.HERTZ,
            "Hz",
            id="HERTZ",
        ),
        pytest.param(
            metrics.Unit.JOULE,
            "J",
            id="JOULE",
        ),
        pytest.param(
            metrics.Unit.KATAL,
            "kat",
            id="KATAL",
        ),
        pytest.param(
            metrics.Unit.LUMEN,
            "lm",
            id="LUMEN",
        ),
        pytest.param(
            metrics.Unit.LUX,
            "lx",
            id="LUX",
        ),
        pytest.param(
            metrics.Unit.NEWTON,
            "N",
            id="NEWTON",
        ),
        pytest.param(
            metrics.Unit.OHM,
            "Ω",
            id="OHM",
        ),
        pytest.param(
            metrics.Unit.PASCAL,
            "Pa",
            id="PASCAL",
        ),
        pytest.param(
            metrics.Unit.RADIAN,
            "rad",
            id="RADIAN",
        ),
        pytest.param(
            metrics.Unit.SIEMENS,
            "S",
            id="SIEMENS",
        ),
        pytest.param(
            metrics.Unit.SIEVERT,
            "Sv",
            id="SIEVERT",
        ),
        pytest.param(
            metrics.Unit.STERADIAN,
            "sr",
            id="STERADIAN",
        ),
        pytest.param(
            metrics.Unit.TESLA,
            "T",
            id="TESLA",
        ),
        pytest.param(
            metrics.Unit.VOLT,
            "V",
            id="VOLT",
        ),
        pytest.param(
            metrics.Unit.WATT,
            "W",
            id="WATT",
        ),
        pytest.param(
            metrics.Unit.WEBER,
            "Wb",
            id="WEBER",
        ),
    ],
)
def test_parse_unit(unit: metrics.Unit, expected_symbol: str) -> None:
    assert parse_unit(unit)["symbol"] == expected_symbol


def test_parse_physical_unit() -> None:
    unit_info = parse_unit(metrics.DecimalUnit(Title("Title"), "symbol"))
    assert unit_info["title"] == "Title"
    assert unit_info["symbol"] == "symbol"
    assert unit_info["render"](0.00024) == "240 µsymbol"
    assert unit_info["js_render"] == "v => cmk.number_format.physical_precision(v, 3, 'symbol')"


def test_parse_scientific_unit() -> None:
    unit_info = parse_unit(metrics.ScientificUnit(Title("Title"), "symbol"))
    assert unit_info["title"] == "Title"
    assert unit_info["symbol"] == "symbol"
    assert unit_info["render"](0.00024) == "2.40e-4 symbol"
    assert unit_info["js_render"] == "v => cmk.number_format.scientific(v, 2) + 'symbol'"
