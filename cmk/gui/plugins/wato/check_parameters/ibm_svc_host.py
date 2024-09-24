#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersStorage,
)
from cmk.gui.valuespec import Dictionary, Integer, Tuple


def _parameter_valuespec_ibm_svc_host() -> Dictionary:
    return Dictionary(
        elements=[
            (
                "active_hosts",
                Tuple(
                    title=_("Count of active hosts"),
                    elements=[
                        Integer(
                            title=_("Warning at or below"),
                            minvalue=0,
                            unit=_("active hosts"),
                        ),
                        Integer(
                            title=_("Critical at or below"),
                            minvalue=0,
                            unit=_("active hosts"),
                        ),
                    ],
                ),
            ),
            (
                "inactive_hosts",
                Tuple(
                    title=_("Count of inactive hosts"),
                    elements=[
                        Integer(
                            title=_("Warning at or above"),
                            minvalue=0,
                            unit=_("inactive hosts"),
                        ),
                        Integer(
                            title=_("Critical at or above"),
                            minvalue=0,
                            unit=_("inactive hosts"),
                        ),
                    ],
                ),
            ),
            (
                "degraded_hosts",
                Tuple(
                    title=_("Count of degraded hosts"),
                    elements=[
                        Integer(
                            title=_("Warning at or above"),
                            minvalue=0,
                            unit=_("degraded hosts"),
                        ),
                        Integer(
                            title=_("Critical at or above"),
                            minvalue=0,
                            unit=_("degraded hosts"),
                        ),
                    ],
                ),
            ),
            (
                "offline_hosts",
                Tuple(
                    title=_("Count of offline hosts"),
                    elements=[
                        Integer(
                            title=_("Warning at or above"),
                            minvalue=0,
                            unit=_("offline hosts"),
                        ),
                        Integer(
                            title=_("Critical at or above"),
                            minvalue=0,
                            unit=_("offline hosts"),
                        ),
                    ],
                ),
            ),
            (
                "other_hosts",
                Tuple(
                    title=_("Count of other hosts"),
                    elements=[
                        Integer(
                            title=_("Warning at or above"),
                            minvalue=0,
                            unit=_("other hosts"),
                        ),
                        Integer(
                            title=_("Critical at or above"),
                            minvalue=0,
                            unit=_("other hosts"),
                        ),
                    ],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="ibm_svc_host",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_ibm_svc_host,
        title=lambda: _("IBM SVC Hosts"),
    )
)
