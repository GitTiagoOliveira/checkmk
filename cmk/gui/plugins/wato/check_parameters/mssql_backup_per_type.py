#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.plugins.wato.check_parameters.mssql_backup import _vs_mssql_backup_age


def _parameter_valuespec_mssql_backup_per_type():
    return Dictionary(elements=[
        ("levels", _vs_mssql_backup_age("Upper levels for the backup age")),
    ],)


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mssql_backup_per_type",
        group=RulespecGroupCheckParametersApplications,
        item_spec=lambda: TextAscii(title=_("Backup name"), allow_empty=False),
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_mssql_backup_per_type,
        title=lambda: _("MSSQL Backup"),
    ))
