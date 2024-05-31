#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)
from cmk.gui.plugins.wato.utils.simple_levels import SimpleLevels
from cmk.gui.valuespec import Dictionary, Integer


def _parameter_valuespec_cisco_prime_wifi_connections():
    return Dictionary(
        elements=[
            (
                "levels_lower",
                SimpleLevels(
                    title=_("Minimum number of connections"),
                    spec=Integer,
                ),
            ),
        ],
        required_keys=["levels_lower"],  # There is only one value, so its required
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="cisco_prime_wifi_connections",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_cisco_prime_wifi_connections,
        title=lambda: _("Cisco Prime WiFi Connections"),
    )
)
