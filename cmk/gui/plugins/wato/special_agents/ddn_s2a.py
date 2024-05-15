#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.utils.rulesets.definition import RuleGroup

from cmk.gui.i18n import _
from cmk.gui.valuespec import Dictionary, NetworkPort, TextInput
from cmk.gui.wato import (
    MigrateToIndividualOrStoredPassword,
    RulespecGroupDatasourceProgramsHardware,
)
from cmk.gui.watolib.rulespecs import HostRulespec, rulespec_registry


def _valuespec_special_agents_ddn_s2a():
    return Dictionary(
        elements=[
            ("username", TextInput(title=_("Username"), allow_empty=False)),
            (
                "password",
                MigrateToIndividualOrStoredPassword(title=_("Password"), allow_empty=False),
            ),
            ("port", NetworkPort(title=_("Port"), default_value=8008)),
        ],
        optional_keys=["port"],
        title=_("DDN S2A"),
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name=RuleGroup.SpecialAgents("ddn_s2a"),
        valuespec=_valuespec_special_agents_ddn_s2a,
    )
)
