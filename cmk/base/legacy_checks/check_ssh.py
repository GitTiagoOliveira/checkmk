#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.base.config import active_check_info


def check_ssh_desc(params):
    if params.get("description"):
        return "SSH %s" % params["description"]
    return "SSH"


def check_ssh_arguments(params):
    args = []

    if "timeout" in params:
        args += ["-t", params["timeout"]]
    if "port" in params:
        args += ["-p", params["port"]]
    if "remote_version" in params:
        args += ["-r", params["remote_version"]]
    if "remote_protocol" in params:
        args += ["-P", params["remote_protocol"]]

    args.append("$HOSTADDRESS$")

    return args


active_check_info["ssh"] = {
    "command_line": "check_ssh $ARG1$",
    "argument_function": check_ssh_arguments,
    "service_description": check_ssh_desc,
}
