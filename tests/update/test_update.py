#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
import logging

import pytest

from tests.testlib.site import Site
from tests.testlib.utils import current_base_branch_name, get_services_with_status, parse_files
from tests.testlib.version import CMKVersion, version_from_env

from cmk.utils.hostaddress import HostName
from cmk.utils.version import Edition

from .conftest import get_site_status, update_site

logger = logging.getLogger(__name__)


@pytest.mark.cee
def test_update(  # pylint: disable=too-many-branches
    test_setup: tuple[Site, bool],
) -> None:
    test_site, disable_interactive_mode = test_setup
    base_version = test_site.version

    hostname = HostName("test-host")
    ip_address = "127.0.0.1"
    logger.info("Creating new host: %s", hostname)
    test_site.openapi.create_host(
        hostname=hostname, attributes={"ipaddress": ip_address, "tag_agent": "cmk-agent"}
    )

    test_site.activate_changes_and_wait_for_core_reload()

    logger.info("Discovering services and waiting for completion...")
    test_site.openapi.bulk_discover_services_and_wait_for_completion([str(hostname)])
    test_site.openapi.activate_changes_and_wait_for_completion()
    test_site.schedule_check(hostname, "Check_MK", 0)

    # get baseline monitoring data for each host
    base_data = test_site.get_host_services(hostname)

    base_ok_services = get_services_with_status(base_data, 0)
    # used in debugging mode
    _ = get_services_with_status(base_data, 1)  # Warn
    _ = get_services_with_status(base_data, 2)  # Crit
    _ = get_services_with_status(base_data, 3)  # Unknown

    assert len(base_ok_services) > 0

    target_version = version_from_env(
        fallback_version_spec=CMKVersion.DAILY,
        fallback_edition=Edition.CEE,
        fallback_branch=current_base_branch_name(),
    )

    target_site = update_site(test_site, target_version, not disable_interactive_mode)

    # get the service status codes and check them
    assert get_site_status(target_site) == "running", "Invalid service status after updating!"

    logger.info("Successfully tested updating %s>%s!", base_version.version, target_version.version)

    logger.info("Discovering services and waiting for completion...")
    target_site.openapi.bulk_discover_services_and_wait_for_completion([str(hostname)])
    target_site.openapi.activate_changes_and_wait_for_completion()

    target_site.schedule_check(hostname, "Check_MK", 0)

    # get update monitoring data
    target_data = target_site.get_host_services(hostname)

    target_ok_services = get_services_with_status(target_data, 0)
    # used in debugging mode
    _ = get_services_with_status(target_data, 1)  # Warn
    _ = get_services_with_status(target_data, 2)  # Crit
    _ = get_services_with_status(target_data, 3)  # Unknown

    not_found_services = [service for service in base_data if service not in target_data]
    err_msg = (
        f"The following services were found in base-version but not in target-version: "
        f"{not_found_services}"
    )
    assert len(target_data) >= len(base_data), err_msg

    not_ok_services = [service for service in base_ok_services if service not in target_ok_services]
    err_details = [
        (s, "state: " + str(target_data[s].state), target_data[s].summary) for s in not_ok_services
    ]
    err_msg = (
        f"The following services were `OK` in base-version but not in target-version: "
        f"{not_ok_services}"
        f"\nDetails: {err_details})"
    )
    assert base_ok_services.issubset(target_ok_services), err_msg

    match_dict = parse_files(pathname=test_site.logs_dir / "/*log*", pattern="error")
    assert not match_dict, f"Error string found in one or more log files: {match_dict}"

    # TODO: Uncomment the following block once the following issues are resolved:
    #   * CMK-18519
    #   * CMK-18520
    # match_dict_subs = parse_files(pathname=test_site.logs_dir + "/**/*log*", pattern="error")
    # assert not match_dict_subs, f"Error string found in one or more log files: {match_dict}"
