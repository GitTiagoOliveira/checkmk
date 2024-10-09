#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from dataclasses import dataclass

from cmk.gui.watolib.configuration_entity.type_defs import ConfigEntityType

from cmk.rulesets.v1.form_specs import FormSpec


@dataclass(frozen=True, kw_only=True)
class SingleChoiceEditable(FormSpec[str]):
    entity_type: ConfigEntityType
    entity_type_specifier: str
