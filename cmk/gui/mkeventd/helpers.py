#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence
from pathlib import Path

import cmk.utils.paths

import cmk.ec.export as ec  # pylint: disable=cmk-module-layer-violation

from cmk.gui.config import active_config
from cmk.gui.hooks import request_memoize
from cmk.gui.i18n import _


def service_levels() -> Sequence[tuple[int, str]]:
    return active_config.mkeventd_service_levels


def action_choices(omit_hidden: bool = False) -> list[tuple[str, str]]:
    # The possible actions are configured in mkeventd.mk,
    # not in multisite.mk (like the service levels). That
    # way we have not direct access to them but need
    # to load them from the configuration.
    return [("@NOTIFY", _("Send monitoring notification"))] + [
        (a["id"], a["title"])
        for a in eventd_configuration().get("actions", [])
        if not omit_hidden or not a.get("hidden")
    ]


@request_memoize()
def eventd_configuration() -> ec.ConfigFromWATO:
    return ec.load_config(
        ec.settings("", cmk.utils.paths.omd_root, Path(cmk.utils.paths.default_config_dir), [""])
    )
