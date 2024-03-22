#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""Code for support of Nagios (and compatible) cores"""

# I am not saying this should be the API, but that's the status quo.
from ._create_config import (
    create_config,
    create_nagios_config_commands,
    create_nagios_host_spec,
    create_nagios_servicedefs,
    format_nagios_object,
    NagiosConfig,
    NagiosCore,
)
from ._precompile_host_checks import dump_precompiled_hostcheck, HostCheckStore

__all__ = [
    "format_nagios_object",
    "create_config",
    "create_nagios_config_commands",
    "create_nagios_host_spec",
    "create_nagios_servicedefs",
    "NagiosConfig",
    "NagiosCore",
    "dump_precompiled_hostcheck",
    "HostCheckStore",
]
