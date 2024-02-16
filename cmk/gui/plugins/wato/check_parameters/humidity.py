#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersEnvironment,
)
from cmk.gui.valuespec import Dictionary, Migrate, Percentage, TextInput, Tuple


def _migrate_humidity(p: dict | tuple) -> dict[str, tuple[float, float]]:
    """
    >>> old = (1, 2, 3, 4)
    >>> new = {'levels_lower': (2.0, 1.0), 'levels': (3.0, 4.0)}
    >>> _migrate_humidity(old) == new
    True
    >>> _migrate_humidity(new) == new
    True
    >>> _migrate_humidity("arglrmf")
    {}
    """
    match p:
        case dict():
            return p
        case cl, wl, wh, ch:
            return {
                "levels_lower": (float(wl), float(cl)),
                "levels": (float(wh), float(ch)),
            }
        case _better_safe_than_sorry:
            return {}


def _item_spec_humidity():
    return TextInput(
        title=_("Sensor name"),
        help=_("The identifier of the sensor."),
    )


def _parameter_valuespec_humidity() -> Migrate:
    return Migrate(
        migrate=_migrate_humidity,
        valuespec=Dictionary(
            help=_("This Ruleset sets the threshold limits for humidity sensors"),
            elements=[
                (
                    "levels",
                    Tuple(
                        title=_("Upper levels"),
                        elements=[
                            Percentage(title=_("Warning at")),
                            Percentage(title=_("Critical at")),
                        ],
                    ),
                ),
                (
                    "levels_lower",
                    Tuple(
                        title=_("Lower levels"),
                        elements=[
                            Percentage(title=_("Warning below")),
                            Percentage(title=_("Critical below")),
                        ],
                    ),
                ),
            ],
            ignored_keys=["_item_key"],
        ),
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="humidity",
        group=RulespecGroupCheckParametersEnvironment,
        item_spec=_item_spec_humidity,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_humidity,
        title=lambda: _("Humidity Levels"),
    )
)
