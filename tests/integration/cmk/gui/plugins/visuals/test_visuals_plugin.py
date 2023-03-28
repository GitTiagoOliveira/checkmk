#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterator

import pytest

from tests.testlib.site import Site


@pytest.fixture()
def plugin_path(site: Site) -> Iterator[str]:
    base_dir = "local/lib/check_mk/gui/plugins/visuals"
    site.makedirs(base_dir)
    path = f"{base_dir}/test_plugin.py"
    site.write_text_file(
        path,
        """
from cmk.gui.plugins.visuals.utils import filter_registry
from cmk.gui.plugins.visuals.filters import InputTextFilter
import cmk.gui.query_filters as query_filters

filter_registry.register(
    InputTextFilter(
        title="test",
        sort_index=102,
        info="host",
        query_filter=query_filters.TextQuery(
            ident="test", op="~~", negateable=False, request_var="test", column="host_test"
        ),
        description="",
        is_show_more=True,
    )
)
""",
    )
    yield path
    site.delete_file(path)


@pytest.mark.usefixtures("plugin_path")
def test_load_visuals_plugin(site: Site) -> None:
    assert (
        site.python_helper("helper_test_load_visuals_plugin.py").check_output().rstrip() == "True"
    )


@pytest.fixture()
def legacy_plugin_path(site: Site) -> Iterator[str]:
    base_dir = "local/share/check_mk/web/plugins/visuals"
    site.makedirs(base_dir)
    path = f"{base_dir}/test_plugin.py"
    site.write_text_file(
        path,
        """
from cmk.gui.plugins.visuals import filter_registry
from cmk.gui.plugins.visuals.filters import InputTextFilter
import cmk.gui.query_filters as query_filters

filter_registry.register(
    InputTextFilter(
        title="test",
        sort_index=102,
        info="host",
        query_filter=query_filters.TextQuery(
            ident="test", op="~~", negateable=False, request_var="test", column="host_test"
        ),
        description="",
        is_show_more=True,
    )
)
""",
    )
    yield path
    site.delete_file(path)


@pytest.mark.usefixtures("legacy_plugin_path")
def test_load_legacy_visuals_plugin(site: Site) -> None:
    assert (
        site.python_helper("helper_test_load_visuals_plugin.py").check_output().rstrip() == "True"
    )
