# -*- coding: utf-8 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2018             mk@mathias-kettner.de |
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

from typing import Dict  # pylint: disable=unused-import
import os
import re

try:
    # First try python3
    from html import escape as html_escape
except ImportError:
    # Default to python2
    from cgi import escape as html_escape


def collect_context():
    # type: () -> Dict
    return {
        var[7:]: value.decode("utf-8")
        for (var, value) in os.environ.items()
        if var.startswith("NOTIFY_")
    }


def extend_context_with_link_urls(context, link_template):
    # type: (Dict, str) -> None
    if context.get("PARAMETER_URL_PREFIX"):
        url_prefix = context["PARAMETER_URL_PREFIX"]
    elif context.get("PARAMETER_URL_PREFIX_MANUAL"):
        url_prefix = context["PARAMETER_URL_PREFIX_MANUAL"]
    elif context.get("PARAMETER_URL_PREFIX_AUTOMATIC") == "http":
        url_prefix = "http://%s/%s" % (context["MONITORING_HOST"], context["OMD_SITE"])
    elif context.get("PARAMETER_URL_PREFIX_AUTOMATIC") == "https":
        url_prefix = "https://%s/%s" % (context["MONITORING_HOST"], context["OMD_SITE"])
    else:
        url_prefix = None

    if url_prefix:
        base_url = re.sub('/check_mk/?', '', url_prefix)
        host_url = base_url + context['HOSTURL']

        context['LINKEDHOSTNAME'] = link_template % (host_url, context['HOSTNAME'])

        if context['WHAT'] == 'SERVICE':
            service_url = base_url + context['SERVICEURL']
            context['LINKEDSERVICEDESC'] = link_template % (service_url, context['SERVICEDESC'])

    else:
        context['LINKEDHOSTNAME'] = context['HOSTNAME']
        context['LINKEDSERVICEDESC'] = context.get('SERVICEDESC', '')


def replace_variable_context(template, context):
    ascii_output = ""
    html_output = "<table class=context>\n"
    elements = context.items()
    elements.sort()
    for varname, value in elements:
        ascii_output += "%s=%s\n" % (varname, value)
        html_output += "<tr><td class=varname>%s</td><td class=value>%s</td></tr>\n" % (
            varname, html_escape(value))
    html_output += "</table>\n"
    return template.replace("$CONTEXT_ASCII$", ascii_output).replace("$CONTEXT_HTML$", html_output)


def substitute_context(template, context):
    # First replace all known variables
    for varname, value in context.items():
        template = template.replace('$' + varname + '$', value)

    # Debugging of variables. Create content only on demand
    if "$CONTEXT_ASCII$" in template or "$CONTEXT_HTML$" in template:
        template = replace_variable_context(template, context)

    if re.search(r"\$[A-Z_][A-Z_0-9]*\$", template):
        # Second pass to replace nested variables inside e.g. SERVICENOTESURL
        for varname, value in context.items():
            template = template.replace('$' + varname + '$', value)

    # Remove the rest of the variables and make them empty
    template = re.sub(r"\$[A-Z_][A-Z_0-9]*\$", "", template)
    return template


###############################################################################
# Mail


def set_mail_headers(target, subject, from_address, reply_to, mail):
    mail['Subject'] = subject
    mail['To'] = target

    # Set a few configurable headers
    if from_address:
        mail['From'] = from_address

    if reply_to:
        mail['Reply-To'] = reply_to
    elif len(target.split(",")) > 1:
        mail['Reply-To'] = target

    return mail
