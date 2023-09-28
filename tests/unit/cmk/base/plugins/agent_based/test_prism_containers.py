#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from collections.abc import Mapping, Sequence
from typing import Any

import pytest

from cmk.base.plugins.agent_based.agent_based_api.v1 import Metric, Result, Service, State
from cmk.base.plugins.agent_based.prism_containers import (
    check_prism_container,
    discovery_prism_container,
)
from cmk.base.plugins.agent_based.utils.df import FILESYSTEM_DEFAULT_PARAMS

SECTION = {
    "NutanixManagementShare": {
        "name": "NutanixManagementShare",
        "markedForRemoval": False,
        "maxCapacity": 41713429587402,
        "totalExplicitReservedCapacity": 0,
        "totalImplicitReservedCapacity": 0,
        "replicationFactor": 2,
        "oplogReplicationFactor": 2,
        "compressionEnabled": True,
        "compressionDelayInSecs": 0,
        "isNutanixManaged": True,
        "enableSoftwareEncryption": False,
        "vstoreNameList": ["NutanixManagementShare"],
        "stats": {
            "avg_io_latency_usecs": "-1",
            "avg_read_io_latency_usecs": "-1",
            "avg_write_io_latency_usecs": "-1",
            "controller_avg_io_latency_usecs": "-1",
            "controller_avg_read_io_latency_usecs": "-1",
            "controller_avg_read_io_size_kbytes": "-1",
            "controller_avg_write_io_latency_usecs": "-1",
            "controller_avg_write_io_size_kbytes": "-1",
            "controller_io_bandwidth_kBps": "-1",
            "controller_num_io": "-1",
            "controller_num_iops": "-1",
            "controller_num_random_io": "-1",
            "controller_num_read_io": "-1",
            "controller_num_read_iops": "-1",
            "controller_num_seq_io": "-1",
            "controller_num_write_io": "-1",
            "controller_num_write_iops": "-1",
            "controller_random_io_ppm": "-1",
            "controller_read_io_bandwidth_kBps": "-1",
            "controller_read_io_ppm": "-1",
            "controller_seq_io_ppm": "-1",
            "controller_timespan_usecs": "-1",
            "controller_total_io_size_kbytes": "-1",
            "controller_total_io_time_usecs": "-1",
            "controller_total_read_io_size_kbytes": "-1",
            "controller_total_read_io_time_usecs": "-1",
            "controller_total_transformed_usage_bytes": "-1",
            "controller_write_io_bandwidth_kBps": "-1",
            "controller_write_io_ppm": "-1",
            "hypervisor_avg_io_latency_usecs": "-1",
            "hypervisor_avg_read_io_latency_usecs": "-1",
            "hypervisor_avg_write_io_latency_usecs": "-1",
            "hypervisor_io_bandwidth_kBps": "-1",
            "hypervisor_num_io": "-1",
            "hypervisor_num_iops": "-1",
            "hypervisor_num_read_io": "-1",
            "hypervisor_num_read_iops": "-1",
            "hypervisor_num_write_io": "-1",
            "hypervisor_num_write_iops": "-1",
            "hypervisor_read_io_bandwidth_kBps": "-1",
            "hypervisor_timespan_usecs": "-1",
            "hypervisor_total_io_size_kbytes": "-1",
            "hypervisor_total_io_time_usecs": "-1",
            "hypervisor_total_read_io_size_kbytes": "-1",
            "hypervisor_total_read_io_time_usecs": "-1",
            "hypervisor_write_io_bandwidth_kBps": "-1",
            "io_bandwidth_kBps": "-1",
            "num_io": "-1",
            "num_iops": "-1",
            "num_random_io": "-1",
            "num_read_io": "-1",
            "num_read_iops": "-1",
            "num_seq_io": "-1",
            "num_write_io": "-1",
            "num_write_iops": "-1",
            "random_io_ppm": "-1",
            "read_io_bandwidth_kBps": "-1",
            "read_io_ppm": "-1",
            "seq_io_ppm": "-1",
            "timespan_usecs": "-1",
            "total_io_size_kbytes": "-1",
            "total_io_time_usecs": "-1",
            "total_read_io_size_kbytes": "-1",
            "total_read_io_time_usecs": "-1",
            "total_transformed_usage_bytes": "-1",
            "total_untransformed_usage_bytes": "-1",
            "write_io_bandwidth_kBps": "-1",
            "write_io_ppm": "-1",
        },
        "usageStats": {
            "data_reduction.clone.saving_ratio_ppm": "1000000",
            "data_reduction.clone.user_saved_bytes": "0",
            "data_reduction.compression.post_reduction_bytes": "29041786880",
            "data_reduction.compression.pre_reduction_bytes": "41346924544",
            "data_reduction.compression.saving_ratio_ppm": "1423704",
            "data_reduction.compression.user_post_reduction_bytes": "14520893440",
            "data_reduction.compression.user_pre_reduction_bytes": "20673462272",
            "data_reduction.compression.user_saved_bytes": "6152568832",
            "data_reduction.dedup.post_reduction_bytes": "41320529050",
            "data_reduction.dedup.pre_reduction_bytes": "41320529050",
            "data_reduction.dedup.saving_ratio_ppm": "1000000",
            "data_reduction.dedup.user_saved_bytes": "0",
            "data_reduction.erasure_coding.parity_bytes": "0",
            "data_reduction.erasure_coding.post_reduction_bytes": "29041786880",
            "data_reduction.erasure_coding.pre_reduction_bytes": "29041786880",
            "data_reduction.erasure_coding.saving_ratio_ppm": "1000000",
            "data_reduction.erasure_coding.user_post_reduction_bytes": "14520893440",
            "data_reduction.erasure_coding.user_pre_reduction_bytes": "14520893440",
            "data_reduction.erasure_coding.user_saved_bytes": "0",
            "data_reduction.overall.saving_ratio_ppm": "1423704",
            "data_reduction.overall.user_saved_bytes": "6152568832",
            "data_reduction.post_reduction_bytes": "29041786880",
            "data_reduction.pre_reduction_bytes": "41346924544",
            "data_reduction.saved_bytes": "12305137664",
            "data_reduction.saving_ratio_ppm": "1423704",
            "data_reduction.thin_provision.saving_ratio_ppm": "-1",
            "data_reduction.thin_provision.user_saved_bytes": "-1",
            "data_reduction.user_post_reduction_bytes": "14520893440",
            "data_reduction.user_pre_reduction_bytes": "20673462272",
            "data_reduction.user_saved_bytes": "6152568832",
            "storage_tier.das-sata.usage_bytes": "0",
            "storage_tier.ssd.usage_bytes": "29518307328",
            "storage.capacity_bytes": "32459915634122",
            "storage.container_reserved_capacity_bytes": "0",
            "storage.disk_physical_usage_bytes": "29518307328",
            "storage.free_bytes": "32430397326794",
            "storage.logical_usage_bytes": "41249931264",
            "storage.recycle_bin_logical_usage_bytes": "30164078",
            "storage.recycle_bin_usage_bytes": "60366848",
            "storage.reserved_capacity_bytes": "0",
            "storage.reserved_free_bytes": "0",
            "storage.reserved_usage_bytes": "0",
            "storage.unreserved_capacity_bytes": "32459915634122",
            "storage.unreserved_free_bytes": "32430397326794",
            "storage.unreserved_own_usage_bytes": "29518307328",
            "storage.unreserved_usage_bytes": "29518307328",
            "storage.usage_bytes": "29518307328",
            "storage.user_capacity_bytes": "16229957817061",
            "storage.user_container_own_usage_bytes": "14759153664",
            "storage.user_container_reserved_capacity_bytes": "0",
            "storage.user_disk_physical_usage_bytes": "14759153664",
            "storage.user_free_bytes": "16215198663397",
            "storage.user_other_containers_reserved_capacity_bytes": "0",
            "storage.user_reserved_capacity_bytes": "0",
            "storage.user_reserved_free_bytes": "0",
            "storage.user_reserved_usage_bytes": "0",
            "storage.user_storage_pool_capacity_bytes": "20856714793701",
            "storage.user_unreserved_capacity_bytes": "16229957817061",
            "storage.user_unreserved_free_bytes": "16215198663397",
            "storage.user_unreserved_own_usage_bytes": "14759153664",
            "storage.user_unreserved_shared_usage_bytes": "4626756976640",
            "storage.user_unreserved_usage_bytes": "14759153664",
            "storage.user_usage_bytes": "14759153664",
        },
    },
    "SelfServiceContainer": {
        "name": "SelfServiceContainer",
        "markedForRemoval": False,
        "maxCapacity": 41713429587402,
        "totalExplicitReservedCapacity": 0,
        "totalImplicitReservedCapacity": 0,
        "replicationFactor": 2,
        "oplogReplicationFactor": 2,
        "compressionEnabled": False,
        "compressionDelayInSecs": 0,
        "isNutanixManaged": None,
        "enableSoftwareEncryption": False,
        "vstoreNameList": ["SelfServiceContainer"],
        "stats": {
            "avg_io_latency_usecs": "-1",
            "avg_read_io_latency_usecs": "-1",
            "avg_write_io_latency_usecs": "-1",
            "controller_avg_io_latency_usecs": "0",
            "controller_avg_read_io_latency_usecs": "0",
            "controller_avg_read_io_size_kbytes": "0",
            "controller_avg_write_io_latency_usecs": "0",
            "controller_avg_write_io_size_kbytes": "0",
            "controller_io_bandwidth_kBps": "0",
            "controller_num_io": "0",
            "controller_num_iops": "0",
            "controller_num_random_io": "-1",
            "controller_num_read_io": "0",
            "controller_num_read_iops": "0",
            "controller_num_seq_io": "-1",
            "controller_num_write_io": "0",
            "controller_num_write_iops": "0",
            "controller_random_io_ppm": "-1",
            "controller_read_io_bandwidth_kBps": "0",
            "controller_read_io_ppm": "0",
            "controller_seq_io_ppm": "-1",
            "controller_timespan_usecs": "20000000",
            "controller_total_io_size_kbytes": "0",
            "controller_total_io_time_usecs": "0",
            "controller_total_read_io_size_kbytes": "0",
            "controller_total_read_io_time_usecs": "0",
            "controller_total_transformed_usage_bytes": "-1",
            "controller_write_io_bandwidth_kBps": "0",
            "controller_write_io_ppm": "0",
            "hypervisor_avg_io_latency_usecs": "-1",
            "hypervisor_avg_read_io_latency_usecs": "-1",
            "hypervisor_avg_write_io_latency_usecs": "-1",
            "hypervisor_io_bandwidth_kBps": "-1",
            "hypervisor_num_io": "-1",
            "hypervisor_num_iops": "-1",
            "hypervisor_num_read_io": "-1",
            "hypervisor_num_read_iops": "-1",
            "hypervisor_num_write_io": "-1",
            "hypervisor_num_write_iops": "-1",
            "hypervisor_read_io_bandwidth_kBps": "-1",
            "hypervisor_timespan_usecs": "-1",
            "hypervisor_total_io_size_kbytes": "-1",
            "hypervisor_total_io_time_usecs": "-1",
            "hypervisor_total_read_io_size_kbytes": "-1",
            "hypervisor_total_read_io_time_usecs": "-1",
            "hypervisor_write_io_bandwidth_kBps": "-1",
            "io_bandwidth_kBps": "-1",
            "num_io": "-1",
            "num_iops": "-1",
            "num_random_io": "-1",
            "num_read_io": "-1",
            "num_read_iops": "-1",
            "num_seq_io": "-1",
            "num_write_io": "-1",
            "num_write_iops": "-1",
            "random_io_ppm": "-1",
            "read_io_bandwidth_kBps": "-1",
            "read_io_ppm": "-1",
            "seq_io_ppm": "-1",
            "timespan_usecs": "-1",
            "total_io_size_kbytes": "-1",
            "total_io_time_usecs": "-1",
            "total_read_io_size_kbytes": "-1",
            "total_read_io_time_usecs": "-1",
            "total_transformed_usage_bytes": "-1",
            "total_untransformed_usage_bytes": "-1",
            "write_io_bandwidth_kBps": "-1",
            "write_io_ppm": "-1",
        },
        "usageStats": {
            "data_reduction.clone.saving_ratio_ppm": "1000000",
            "data_reduction.clone.user_saved_bytes": "0",
            "data_reduction.compression.post_reduction_bytes": "11576016896",
            "data_reduction.compression.pre_reduction_bytes": "11576016896",
            "data_reduction.compression.saving_ratio_ppm": "1000000",
            "data_reduction.compression.user_post_reduction_bytes": "5788008448",
            "data_reduction.compression.user_pre_reduction_bytes": "5788008448",
            "data_reduction.compression.user_saved_bytes": "0",
            "data_reduction.dedup.post_reduction_bytes": "11563630912",
            "data_reduction.dedup.pre_reduction_bytes": "11563630912",
            "data_reduction.dedup.saving_ratio_ppm": "1000000",
            "data_reduction.dedup.user_saved_bytes": "0",
            "data_reduction.erasure_coding.parity_bytes": "0",
            "data_reduction.erasure_coding.post_reduction_bytes": "11576016896",
            "data_reduction.erasure_coding.pre_reduction_bytes": "11576016896",
            "data_reduction.erasure_coding.saving_ratio_ppm": "1000000",
            "data_reduction.erasure_coding.user_post_reduction_bytes": "5788008448",
            "data_reduction.erasure_coding.user_pre_reduction_bytes": "5788008448",
            "data_reduction.erasure_coding.user_saved_bytes": "0",
            "data_reduction.overall.saving_ratio_ppm": "743034230",
            "data_reduction.overall.user_saved_bytes": "4294900396032",
            "data_reduction.post_reduction_bytes": "11576016896",
            "data_reduction.pre_reduction_bytes": "11576016896",
            "data_reduction.saved_bytes": "0",
            "data_reduction.saving_ratio_ppm": "1000000",
            "data_reduction.thin_provision.saving_ratio_ppm": "64199840813",
            "data_reduction.thin_provision.user_saved_bytes": "4294900396032",
            "data_reduction.user_post_reduction_bytes": "5788008448",
            "data_reduction.user_pre_reduction_bytes": "5788008448",
            "data_reduction.user_saved_bytes": "0",
            "storage_tier.das-sata.usage_bytes": "0",
            "storage_tier.ssd.usage_bytes": "11576016896",
            "storage.capacity_bytes": "32441973343690",
            "storage.container_reserved_capacity_bytes": "0",
            "storage.disk_physical_usage_bytes": "11576016896",
            "storage.free_bytes": "32430397326794",
            "storage.logical_usage_bytes": "11616124928",
            "storage.recycle_bin_logical_usage_bytes": "12528598",
            "storage.recycle_bin_usage_bytes": "25100288",
            "storage.reserved_capacity_bytes": "0",
            "storage.reserved_free_bytes": "0",
            "storage.reserved_usage_bytes": "0",
            "storage.unreserved_capacity_bytes": "32441973343690",
            "storage.unreserved_free_bytes": "32430397326794",
            "storage.unreserved_own_usage_bytes": "11576016896",
            "storage.unreserved_usage_bytes": "11576016896",
            "storage.usage_bytes": "11576016896",
            "storage.user_capacity_bytes": "16220986671845",
            "storage.user_container_own_usage_bytes": "5788008448",
            "storage.user_container_reserved_capacity_bytes": "0",
            "storage.user_disk_physical_usage_bytes": "5788008448",
            "storage.user_free_bytes": "16215198663397",
            "storage.user_other_containers_reserved_capacity_bytes": "0",
            "storage.user_reserved_capacity_bytes": "0",
            "storage.user_reserved_free_bytes": "0",
            "storage.user_reserved_usage_bytes": "0",
            "storage.user_storage_pool_capacity_bytes": "20856714793701",
            "storage.user_unreserved_capacity_bytes": "16220986671845",
            "storage.user_unreserved_free_bytes": "16215198663397",
            "storage.user_unreserved_own_usage_bytes": "5788008448",
            "storage.user_unreserved_shared_usage_bytes": "4635728121856",
            "storage.user_unreserved_usage_bytes": "5788008448",
            "storage.user_usage_bytes": "5788008448",
        },
    },
    "VMs": {
        "name": "VMs",
        "markedForRemoval": False,
        "maxCapacity": 41713429587402,
        "totalExplicitReservedCapacity": 0,
        "totalImplicitReservedCapacity": 0,
        "replicationFactor": 2,
        "oplogReplicationFactor": 2,
        "compressionEnabled": True,
        "compressionDelayInSecs": 0,
        "isNutanixManaged": None,
        "enableSoftwareEncryption": False,
        "vstoreNameList": ["VMs"],
        "stats": {
            "avg_io_latency_usecs": "-1",
            "avg_read_io_latency_usecs": "-1",
            "avg_write_io_latency_usecs": "-1",
            "controller_avg_io_latency_usecs": "1078",
            "controller_avg_read_io_latency_usecs": "677",
            "controller_avg_read_io_size_kbytes": "18",
            "controller_avg_write_io_latency_usecs": "1089",
            "controller_avg_write_io_size_kbytes": "16",
            "controller_io_bandwidth_kBps": "5391",
            "controller_num_io": "6573",
            "controller_num_iops": "328",
            "controller_num_random_io": "-1",
            "controller_num_read_io": "176",
            "controller_num_read_iops": "8",
            "controller_num_seq_io": "-1",
            "controller_num_write_io": "6397",
            "controller_num_write_iops": "319",
            "controller_random_io_ppm": "-1",
            "controller_read_io_bandwidth_kBps": "162",
            "controller_read_io_ppm": "26776",
            "controller_seq_io_ppm": "-1",
            "controller_timespan_usecs": "20000000",
            "controller_total_io_size_kbytes": "107835",
            "controller_total_io_time_usecs": "7088413",
            "controller_total_read_io_size_kbytes": "3254",
            "controller_total_read_io_time_usecs": "119324",
            "controller_total_transformed_usage_bytes": "-1",
            "controller_write_io_bandwidth_kBps": "5229",
            "controller_write_io_ppm": "973223",
            "hypervisor_avg_io_latency_usecs": "-1",
            "hypervisor_avg_read_io_latency_usecs": "-1",
            "hypervisor_avg_write_io_latency_usecs": "-1",
            "hypervisor_io_bandwidth_kBps": "-1",
            "hypervisor_num_io": "-1",
            "hypervisor_num_iops": "-1",
            "hypervisor_num_read_io": "-1",
            "hypervisor_num_read_iops": "-1",
            "hypervisor_num_write_io": "-1",
            "hypervisor_num_write_iops": "-1",
            "hypervisor_read_io_bandwidth_kBps": "-1",
            "hypervisor_timespan_usecs": "-1",
            "hypervisor_total_io_size_kbytes": "-1",
            "hypervisor_total_io_time_usecs": "-1",
            "hypervisor_total_read_io_size_kbytes": "-1",
            "hypervisor_total_read_io_time_usecs": "-1",
            "hypervisor_write_io_bandwidth_kBps": "-1",
            "io_bandwidth_kBps": "-1",
            "num_io": "-1",
            "num_iops": "-1",
            "num_random_io": "-1",
            "num_read_io": "-1",
            "num_read_iops": "-1",
            "num_seq_io": "-1",
            "num_write_io": "-1",
            "num_write_iops": "-1",
            "random_io_ppm": "-1",
            "read_io_bandwidth_kBps": "-1",
            "read_io_ppm": "-1",
            "seq_io_ppm": "-1",
            "timespan_usecs": "-1",
            "total_io_size_kbytes": "-1",
            "total_io_time_usecs": "-1",
            "total_read_io_size_kbytes": "-1",
            "total_read_io_time_usecs": "-1",
            "total_transformed_usage_bytes": "-1",
            "total_untransformed_usage_bytes": "-1",
            "write_io_bandwidth_kBps": "-1",
            "write_io_ppm": "-1",
        },
        "usageStats": {
            "data_reduction.clone.saving_ratio_ppm": "1825060",
            "data_reduction.clone.user_saved_bytes": "9057520083968",
            "data_reduction.compression.post_reduction_bytes": "9180763971584",
            "data_reduction.compression.pre_reduction_bytes": "14166480715776",
            "data_reduction.compression.saving_ratio_ppm": "1543061",
            "data_reduction.compression.user_post_reduction_bytes": "4590381985792",
            "data_reduction.compression.user_pre_reduction_bytes": "7083240357888",
            "data_reduction.compression.user_saved_bytes": "2492858372096",
            "data_reduction.dedup.post_reduction_bytes": "12895263298560",
            "data_reduction.dedup.pre_reduction_bytes": "12895263298560",
            "data_reduction.dedup.saving_ratio_ppm": "1000000",
            "data_reduction.dedup.user_saved_bytes": "0",
            "data_reduction.erasure_coding.parity_bytes": "0",
            "data_reduction.erasure_coding.post_reduction_bytes": "9180763971584",
            "data_reduction.erasure_coding.pre_reduction_bytes": "9180763971584",
            "data_reduction.erasure_coding.saving_ratio_ppm": "1000000",
            "data_reduction.erasure_coding.user_post_reduction_bytes": "4590381985792",
            "data_reduction.erasure_coding.user_pre_reduction_bytes": "4590381985792",
            "data_reduction.erasure_coding.user_saved_bytes": "0",
            "data_reduction.overall.saving_ratio_ppm": "5302539",
            "data_reduction.overall.user_saved_bytes": "19750301553152",
            "data_reduction.post_reduction_bytes": "9180763971584",
            "data_reduction.pre_reduction_bytes": "14166480715776",
            "data_reduction.saved_bytes": "4985716744192",
            "data_reduction.saving_ratio_ppm": "1543061",
            "data_reduction.thin_provision.saving_ratio_ppm": "2285186",
            "data_reduction.thin_provision.user_saved_bytes": "8199923097088",
            "data_reduction.user_post_reduction_bytes": "4590381985792",
            "data_reduction.user_pre_reduction_bytes": "7083240357888",
            "data_reduction.user_saved_bytes": "2492858372096",
            "storage_tier.das-sata.usage_bytes": "0",
            "storage_tier.ssd.usage_bytes": "9241937936384",
            "storage.capacity_bytes": "41672335263178",
            "storage.container_reserved_capacity_bytes": "0",
            "storage.disk_physical_usage_bytes": "9241937936384",
            "storage.free_bytes": "32430397326794",
            "storage.logical_usage_bytes": "20148721287168",
            "storage.recycle_bin_logical_usage_bytes": "22040888832",
            "storage.recycle_bin_usage_bytes": "21529051136",
            "storage.reserved_capacity_bytes": "0",
            "storage.reserved_free_bytes": "0",
            "storage.reserved_usage_bytes": "0",
            "storage.unreserved_capacity_bytes": "41672335263178",
            "storage.unreserved_free_bytes": "32430397326794",
            "storage.unreserved_own_usage_bytes": "9241937936384",
            "storage.unreserved_usage_bytes": "9241937936384",
            "storage.usage_bytes": "9241937936384",
            "storage.user_capacity_bytes": "20836167631589",
            "storage.user_container_own_usage_bytes": "4620968968192",
            "storage.user_container_reserved_capacity_bytes": "0",
            "storage.user_disk_physical_usage_bytes": "4620968968192",
            "storage.user_free_bytes": "16215198663397",
            "storage.user_other_containers_reserved_capacity_bytes": "0",
            "storage.user_reserved_capacity_bytes": "0",
            "storage.user_reserved_free_bytes": "0",
            "storage.user_reserved_usage_bytes": "0",
            "storage.user_storage_pool_capacity_bytes": "20856714793701",
            "storage.user_unreserved_capacity_bytes": "20836167631589",
            "storage.user_unreserved_free_bytes": "16215198663397",
            "storage.user_unreserved_own_usage_bytes": "4620968968192",
            "storage.user_unreserved_shared_usage_bytes": "20547162112",
            "storage.user_unreserved_usage_bytes": "4620968968192",
            "storage.user_usage_bytes": "4620968968192",
        },
    },
}


@pytest.mark.parametrize(
    ["section", "expected_discovery_result"],
    [
        pytest.param(
            SECTION,
            [
                Service(item="NutanixManagementShare"),
                Service(item="SelfServiceContainer"),
                Service(item="VMs"),
            ],
            id="For every disk container, a Service is discovered.",
        ),
        pytest.param(
            {},
            [],
            id="If there are no items in the input, nothing is discovered.",
        ),
    ],
)
def test_discovery_prism_container(
    section: Mapping[str, Any],
    expected_discovery_result: Sequence[Service],
) -> None:
    assert list(discovery_prism_container(section)) == expected_discovery_result


@pytest.mark.usefixtures("initialised_item_state")
@pytest.mark.parametrize(
    ["item", "params", "section", "expected_check_result"],
    [
        pytest.param(
            "NutanixManagementShare",
            FILESYSTEM_DEFAULT_PARAMS,
            SECTION,
            [
                Metric(
                    "fs_used",
                    14075.42578125,
                    levels=(12382475.141189575, 13930284.533838272),
                    boundaries=(0.0, 15478093.926487923),
                ),
                Metric("fs_free", 15464018.500706673, boundaries=(0.0, None)),
                Metric(
                    "fs_used_percent",
                    0.0909377204202288,
                    levels=(79.99999999999507, 89.99999999999446),
                    boundaries=(0.0, 100.0),
                ),
                Result(state=State.OK, summary="Used: 0.09% - 13.7 GiB of 14.8 TiB"),
                Metric("fs_size", 15478093.926487923, boundaries=(0.0, None)),
            ],
            id="If ..., the check result is OK.",
        ),
        pytest.param(
            "VMs",
            FILESYSTEM_DEFAULT_PARAMS,
            SECTION,
            [
                Metric(
                    "fs_used",
                    4406899.421875,
                    levels=(15896734.338065147, 17883826.13032341),
                    boundaries=(0.0, 19870917.922581673),
                ),
                Metric("fs_free", 15464018.500706673, boundaries=(0.0, None)),
                Metric(
                    "fs_used_percent",
                    22.177633861931056,
                    levels=(79.99999999999903, 89.99999999999952),
                    boundaries=(0.0, 100.0),
                ),
                Result(state=State.OK, summary="Used: 22.18% - 4.20 TiB of 19.0 TiB"),
                Metric("fs_size", 19870917.922581673, boundaries=(0.0, None)),
            ],
            id="If ..., the check result is WARN.",
        ),
    ],
)
def test_check_prism_container(
    item: str,
    params: Mapping[str, Any],
    section: Mapping[str, Any],
    expected_check_result: Sequence[Result],
) -> None:
    assert (
        list(
            check_prism_container(
                item=item,
                params=params,
                section=section,
            )
        )
        == expected_check_result
    )
