#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Alternative,
    Dictionary,
    Integer,
    Percentage,
    TextAscii,
    Transform,
    Tuple,
)
from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersApplications,
    register_check_parameters,
)


register_check_parameters(
    RulespecGroupCheckParametersApplications,
    "win_dhcp_pools",
    _("DHCP Pools for Windows and Linux"),
    Transform(
        Dictionary(
            elements = [
                ("free_leases",
                    Alternative(
                        title = _("Free leases levels"),
                        elements = [
                            Tuple(
                                title = _("Free leases levels in percent"),
                                elements = [
                                    Percentage(title = _("Warning if below"),  default_value = 10.0),
                                    Percentage(title = _("Critical if below"), default_value = 5.0)
                                ]
                            ),
                            Tuple(
                                title = _("Absolute free leases levels"),
                                elements = [
                                    Integer(title = _("Warning if below"),  unit = _("free leases")),
                                    Integer(title = _("Critical if below"), unit = _("free leases"))
                                ]
                            )
                        ]
                    )
                ),
                ("used_leases",
                    Alternative(
                        title = _("Used leases levels"),
                        elements = [
                            Tuple(
                                title = _("Used leases levels in percent"),
                                elements = [
                                    Percentage(title = _("Warning if below")),
                                    Percentage(title = _("Critical if below"))
                                ]
                            ),
                            Tuple(
                                title = _("Absolute used leases levels"),
                                elements = [
                                    Integer(title = _("Warning if below"),  unit = _("used leases")),
                                    Integer(title = _("Critical if below"), unit = _("used leases"))
                                ]
                            )
                        ]
                    )
                ),
            ]
        ),
        forth = lambda params: isinstance(params, tuple) and {"free_leases" : (float(params[0]), float(params[1]))} or params,
    ),
    TextAscii(
        title = _("Pool name"),
        allow_empty = False,
    ),
    match_type = "first",)
