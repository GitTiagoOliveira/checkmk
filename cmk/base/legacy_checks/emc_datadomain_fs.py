#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.df import df_check_filesystem_list, FILESYSTEM_DEFAULT_PARAMS
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree
from cmk.base.plugins.agent_based.utils.df import EXCLUDED_MOUNTPOINTS
from cmk.base.plugins.agent_based.utils.emc import DETECT_DATADOMAIN


def inventory_emc_datadomain_fs(info):
    mplist = []
    for line in info:
        if line[1] in EXCLUDED_MOUNTPOINTS:
            continue
        mplist.append((line[1], None))
    return mplist


def check_emc_datadomain_fs(item, params, info):
    fslist = []
    for line in info:
        if item == line[1] or "patterns" in params:
            size_mb = float(line[2]) * 1024.0
            avail_mb = float(line[4]) * 1024.0
            fslist.append((item, size_mb, avail_mb, 0))
    return df_check_filesystem_list(item, params, fslist)


check_info["emc_datadomain_fs"] = LegacyCheckDefinition(
    detect=DETECT_DATADOMAIN,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.19746.1.3.2.1.1",
        oids=["1", "3", "4", "5", "6", "7", "8"],
    ),
    service_name="DD-Filesystem %s",
    discovery_function=inventory_emc_datadomain_fs,
    check_function=check_emc_datadomain_fs,
    check_ruleset_name="filesystem",
    check_default_parameters=FILESYSTEM_DEFAULT_PARAMS,
)
