#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import cmk.gui.query_filters as query_filters
from cmk.gui.plugins.visuals import (  # type: ignore[attr-defined]  # pylint: disable=no-name-in-module
    filter_registry,
)
from cmk.gui.plugins.visuals.utils import (  # type: ignore[attr-defined]  # pylint: disable=no-name-in-module
    InputTextFilter,
)

filter_registry.register(
    InputTextFilter(
        title="test",
        sort_index=102,
        info="host",
        query_filter=query_filters.TextQuery(
            ident="test",
            op="~~",
            negateable=False,
            request_var="test",
            column="host_test",
        ),
        description="",
        is_show_more=True,
    )
)
