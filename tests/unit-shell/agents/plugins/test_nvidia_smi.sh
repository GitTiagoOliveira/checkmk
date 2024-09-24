#!/bin/bash
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

MK_NVIDIA_SMI_PLUGIN_PATH="${UNIT_SH_PLUGINS_DIR}/nvidia_smi"

nvidia-smi() {
    echo '
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nvidia_smi_log SYSTEM "nvsmi_device_v12.dtd">
<nvidia_smi_log>
    <timestamp>Fri Aug  4 11:44:30 2023</timestamp>
    <driver_version>535.54.03</driver_version>
    <cuda_version>12.2</cuda_version>
    <attached_gpus>4</attached_gpus>
    <gpu id="00000000:01:00.0">
        <product_name>NVIDIA A100-SXM4-80GB</product_name>
        <product_brand>NVIDIA</product_brand>
        <product_architecture>Ampere</product_architecture>
        <display_mode>Enabled</display_mode>
        <display_active>Disabled</display_active>
        <persistence_mode>Disabled</persistence_mode>
        <addressing_mode>None</addressing_mode>
        <mig_mode>
            <current_mig>Enabled</current_mig>
            <pending_mig>Enabled</pending_mig>
        </mig_mode>
        <mig_devices>
            <mig_device>
                <index>0</index>
                <gpu_instance_id>3</gpu_instance_id>
                <compute_instance_id>0</compute_instance_id>
                <device_attributes>
                    <shared>
                        <multiprocessor_count>14</multiprocessor_count>
                        <copy_engine_count>1</copy_engine_count>
                        <encoder_count>0</encoder_count>
                        <decoder_count>1</decoder_count>
                        <ofa_count>0</ofa_count>
                        <jpg_count>0</jpg_count>
                    </shared>
                </device_attributes>
                <ecc_error_count>
                    <volatile_count>
                        <sram_uncorrectable>0</sram_uncorrectable>
                    </volatile_count>
                </ecc_error_count>
                <fb_memory_usage>
                    <total>19968 MiB</total>
                    <reserved>0 MiB</reserved>
                    <used>12 MiB</used>
                    <free>19955 MiB</free>
                </fb_memory_usage>
                <bar1_memory_usage>
                    <total>32767 MiB</total>
                    <used>0 MiB</used>
                    <free>32767 MiB</free>
                </bar1_memory_usage>
            </mig_device>
            <mig_device>
                <index>1</index>
                <gpu_instance_id>4</gpu_instance_id>
                <compute_instance_id>0</compute_instance_id>
                <device_attributes>
                    <shared>
                        <multiprocessor_count>14</multiprocessor_count>
                        <copy_engine_count>1</copy_engine_count>
                        <encoder_count>0</encoder_count>
                        <decoder_count>1</decoder_count>
                        <ofa_count>0</ofa_count>
                        <jpg_count>0</jpg_count>
                    </shared>
                </device_attributes>
                <ecc_error_count>
                    <volatile_count>
                        <sram_uncorrectable>0</sram_uncorrectable>
                    </volatile_count>
                </ecc_error_count>
                <fb_memory_usage>
                    <total>19968 MiB</total>
                    <reserved>0 MiB</reserved>
                    <used>12 MiB</used>
                    <free>19955 MiB</free>
                </fb_memory_usage>
                <bar1_memory_usage>
                    <total>32767 MiB</total>
                    <used>0 MiB</used>
                    <free>32767 MiB</free>
                </bar1_memory_usage>
            </mig_device>
            <mig_device>
                <index>2</index>
                <gpu_instance_id>5</gpu_instance_id>
                <compute_instance_id>0</compute_instance_id>
                <device_attributes>
                    <shared>
                        <multiprocessor_count>14</multiprocessor_count>
                        <copy_engine_count>1</copy_engine_count>
                        <encoder_count>0</encoder_count>
                        <decoder_count>1</decoder_count>
                        <ofa_count>0</ofa_count>
                        <jpg_count>0</jpg_count>
                    </shared>
                </device_attributes>
                <ecc_error_count>
                    <volatile_count>
                        <sram_uncorrectable>0</sram_uncorrectable>
                    </volatile_count>
                </ecc_error_count>
                <fb_memory_usage>
                    <total>19968 MiB</total>
                    <reserved>0 MiB</reserved>
                    <used>12 MiB</used>
                    <free>19955 MiB</free>
                </fb_memory_usage>
                <bar1_memory_usage>
                    <total>32767 MiB</total>
                    <used>0 MiB</used>
                    <free>32767 MiB</free>
                </bar1_memory_usage>
            </mig_device>
            <mig_device>
                <index>3</index>
                <gpu_instance_id>6</gpu_instance_id>
                <compute_instance_id>0</compute_instance_id>
                <device_attributes>
                    <shared>
                        <multiprocessor_count>14</multiprocessor_count>
                        <copy_engine_count>1</copy_engine_count>
                        <encoder_count>0</encoder_count>
                        <decoder_count>1</decoder_count>
                        <ofa_count>0</ofa_count>
                        <jpg_count>0</jpg_count>
                    </shared>
                </device_attributes>
                <ecc_error_count>
                    <volatile_count>
                        <sram_uncorrectable>0</sram_uncorrectable>
                    </volatile_count>
                </ecc_error_count>
                <fb_memory_usage>
                    <total>19968 MiB</total>
                    <reserved>0 MiB</reserved>
                    <used>12 MiB</used>
                    <free>19955 MiB</free>
                </fb_memory_usage>
                <bar1_memory_usage>
                    <total>32767 MiB</total>
                    <used>0 MiB</used>
                    <free>32767 MiB</free>
                </bar1_memory_usage>
            </mig_device>
        </mig_devices>
        <accounting_mode>Disabled</accounting_mode>
        <accounting_mode_buffer_size>4000</accounting_mode_buffer_size>
        <driver_model>
            <current_dm>N/A</current_dm>
            <pending_dm>N/A</pending_dm>
        </driver_model>
        <serial>1650522003820</serial>
        <uuid>GPU-513536b6-7d19-9063-b049-1e69664bb298</uuid>
        <minor_number>1</minor_number>
        <vbios_version>92.00.36.00.02</vbios_version>
        <multigpu_board>No</multigpu_board>
        <board_id>0x100</board_id>
        <board_part_number>692-2G506-0212-002</board_part_number>
        <gpu_part_number>20B2-895-A1</gpu_part_number>
        <gpu_fru_part_number>N/A</gpu_fru_part_number>
        <gpu_module_id>4</gpu_module_id>
        <inforom_version>
            <img_version>G506.0212.00.01</img_version>
            <oem_object>2.0</oem_object>
            <ecc_object>6.16</ecc_object>
            <pwr_object>N/A</pwr_object>
        </inforom_version>
        <gpu_operation_mode>
            <current_gom>N/A</current_gom>
            <pending_gom>N/A</pending_gom>
        </gpu_operation_mode>
        <gsp_firmware_version>535.54.03</gsp_firmware_version>
        <gpu_virtualization_mode>
            <virtualization_mode>None</virtualization_mode>
            <host_vgpu_mode>N/A</host_vgpu_mode>
        </gpu_virtualization_mode>
        <gpu_reset_status>
            <reset_required>No</reset_required>
            <drain_and_reset_recommended>No</drain_and_reset_recommended>
        </gpu_reset_status>
        <ibmnpu>
            <relaxed_ordering_mode>N/A</relaxed_ordering_mode>
        </ibmnpu>
        <pci>
            <pci_bus>01</pci_bus>
            <pci_device>00</pci_device>
            <pci_domain>0000</pci_domain>
            <pci_device_id>20B210DE</pci_device_id>
            <pci_bus_id>00000000:01:00.0</pci_bus_id>
            <pci_sub_system_id>147F10DE</pci_sub_system_id>
            <pci_gpu_link_info>
                <pcie_gen>
                    <max_link_gen>4</max_link_gen>
                    <current_link_gen>4</current_link_gen>
                    <device_current_link_gen>4</device_current_link_gen>
                    <max_device_link_gen>4</max_device_link_gen>
                    <max_host_link_gen>4</max_host_link_gen>
                </pcie_gen>
                <link_widths>
                    <max_link_width>16x</max_link_width>
                    <current_link_width>16x</current_link_width>
                </link_widths>
            </pci_gpu_link_info>
            <pci_bridge_chip>
                <bridge_chip_type>N/A</bridge_chip_type>
                <bridge_chip_fw>N/A</bridge_chip_fw>
            </pci_bridge_chip>
            <replay_counter>0</replay_counter>
            <replay_rollover_counter>0</replay_rollover_counter>
            <tx_util>4000 KB/s</tx_util>
            <rx_util>0 KB/s</rx_util>
            <atomic_caps_inbound>N/A</atomic_caps_inbound>
            <atomic_caps_outbound>N/A</atomic_caps_outbound>
        </pci>
        <fan_speed>N/A</fan_speed>
        <performance_state>P0</performance_state>
        <clocks_event_reasons>
            <clocks_event_reason_gpu_idle>Not Active</clocks_event_reason_gpu_idle>
            <clocks_event_reason_applications_clocks_setting>Not Active</clocks_event_reason_applications_clocks_setting>
            <clocks_event_reason_sw_power_cap>Not Active</clocks_event_reason_sw_power_cap>
            <clocks_event_reason_hw_slowdown>Not Active</clocks_event_reason_hw_slowdown>
            <clocks_event_reason_hw_thermal_slowdown>Not Active</clocks_event_reason_hw_thermal_slowdown>
            <clocks_event_reason_hw_power_brake_slowdown>Not Active</clocks_event_reason_hw_power_brake_slowdown>
            <clocks_event_reason_sync_boost>Not Active</clocks_event_reason_sync_boost>
            <clocks_event_reason_sw_thermal_slowdown>Not Active</clocks_event_reason_sw_thermal_slowdown>
            <clocks_event_reason_display_clocks_setting>Not Active</clocks_event_reason_display_clocks_setting>
        </clocks_event_reasons>
        <fb_memory_usage>
            <total>81920 MiB</total>
            <reserved>869 MiB</reserved>
            <used>50 MiB</used>
            <free>80999 MiB</free>
        </fb_memory_usage>
        <bar1_memory_usage>
            <total>131072 MiB</total>
            <used>1 MiB</used>
            <free>131071 MiB</free>
        </bar1_memory_usage>
        <cc_protected_memory_usage>
            <total>0 MiB</total>
            <used>0 MiB</used>
            <free>0 MiB</free>
        </cc_protected_memory_usage>
        <compute_mode>Default</compute_mode>
        <utilization>
            <gpu_util>N/A</gpu_util>
            <memory_util>N/A</memory_util>
            <encoder_util>N/A</encoder_util>
            <decoder_util>N/A</decoder_util>
            <jpeg_util>N/A</jpeg_util>
            <ofa_util>N/A</ofa_util>
        </utilization>
        <encoder_stats>
            <session_count>0</session_count>
            <average_fps>0</average_fps>
            <average_latency>0</average_latency>
        </encoder_stats>
        <fbc_stats>
            <session_count>0</session_count>
            <average_fps>0</average_fps>
            <average_latency>0</average_latency>
        </fbc_stats>
        <ecc_mode>
            <current_ecc>Enabled</current_ecc>
            <pending_ecc>Enabled</pending_ecc>
        </ecc_mode>
        <ecc_errors>
            <volatile>
                <sram_correctable>0</sram_correctable>
                <sram_uncorrectable>0</sram_uncorrectable>
                <dram_correctable>0</dram_correctable>
                <dram_uncorrectable>0</dram_uncorrectable>
            </volatile>
            <aggregate>
                <sram_correctable>0</sram_correctable>
                <sram_uncorrectable>0</sram_uncorrectable>
                <dram_correctable>0</dram_correctable>
                <dram_uncorrectable>0</dram_uncorrectable>
            </aggregate>
        </ecc_errors>
        <retired_pages>
            <multiple_single_bit_retirement>
                <retired_count>N/A</retired_count>
                <retired_pagelist>N/A</retired_pagelist>
            </multiple_single_bit_retirement>
            <double_bit_retirement>
                <retired_count>N/A</retired_count>
                <retired_pagelist>N/A</retired_pagelist>
            </double_bit_retirement>
            <pending_blacklist>N/A</pending_blacklist>
            <pending_retirement>N/A</pending_retirement>
        </retired_pages>
        <remapped_rows>N/A</remapped_rows>
        <temperature>
            <gpu_temp>27 C</gpu_temp>
            <gpu_temp_tlimit>N/A</gpu_temp_tlimit>
            <gpu_temp_max_threshold>92 C</gpu_temp_max_threshold>
            <gpu_temp_slow_threshold>89 C</gpu_temp_slow_threshold>
            <gpu_temp_max_gpu_threshold>85 C</gpu_temp_max_gpu_threshold>
            <gpu_target_temperature>N/A</gpu_target_temperature>
            <memory_temp>44 C</memory_temp>
            <gpu_temp_max_mem_threshold>95 C</gpu_temp_max_mem_threshold>
        </temperature>
        <supported_gpu_target_temp>
            <gpu_target_temp_min>N/A</gpu_target_temp_min>
            <gpu_target_temp_max>N/A</gpu_target_temp_max>
        </supported_gpu_target_temp>
        <gpu_power_readings>
            <power_state>P0</power_state>
            <power_draw>67.03 W</power_draw>
            <current_power_limit>500.00 W</current_power_limit>
            <requested_power_limit>500.00 W</requested_power_limit>
            <default_power_limit>500.00 W</default_power_limit>
            <min_power_limit>100.00 W</min_power_limit>
            <max_power_limit>500.00 W</max_power_limit>
        </gpu_power_readings>
        <module_power_readings>
            <power_state>P0</power_state>
            <power_draw>N/A</power_draw>
            <current_power_limit>N/A</current_power_limit>
            <requested_power_limit>N/A</requested_power_limit>
            <default_power_limit>N/A</default_power_limit>
            <min_power_limit>N/A</min_power_limit>
            <max_power_limit>N/A</max_power_limit>
        </module_power_readings>
        <clocks>
            <graphics_clock>1275 MHz</graphics_clock>
            <sm_clock>1275 MHz</sm_clock>
            <mem_clock>1593 MHz</mem_clock>
            <video_clock>1275 MHz</video_clock>
        </clocks>
        <applications_clocks>
            <graphics_clock>1275 MHz</graphics_clock>
            <mem_clock>1593 MHz</mem_clock>
        </applications_clocks>
        <default_applications_clocks>
            <graphics_clock>1275 MHz</graphics_clock>
            <mem_clock>1593 MHz</mem_clock>
        </default_applications_clocks>
        <deferred_clocks>
            <mem_clock>N/A</mem_clock>
        </deferred_clocks>
        <max_clocks>
            <graphics_clock>1410 MHz</graphics_clock>
            <sm_clock>1410 MHz</sm_clock>
            <mem_clock>1593 MHz</mem_clock>
            <video_clock>1290 MHz</video_clock>
        </max_clocks>
        <max_customer_boost_clocks>
            <graphics_clock>1410 MHz</graphics_clock>
        </max_customer_boost_clocks>
        <clock_policy>
            <auto_boost>N/A</auto_boost>
            <auto_boost_default>N/A</auto_boost_default>
        </clock_policy>
        <voltage>
            <graphics_volt>912.500 mV</graphics_volt>
        </voltage>
        <fabric>
            <state>N/A</state>
            <status>N/A</status>
        </fabric>
        <supported_clocks>
            <supported_mem_clock>
                <value>1593 MHz</value>
                <supported_graphics_clock>1410 MHz</supported_graphics_clock>
                <supported_graphics_clock>1395 MHz</supported_graphics_clock>
                <supported_graphics_clock>1380 MHz</supported_graphics_clock>
                <supported_graphics_clock>1365 MHz</supported_graphics_clock>
                <supported_graphics_clock>1350 MHz</supported_graphics_clock>
                <supported_graphics_clock>1335 MHz</supported_graphics_clock>
                <supported_graphics_clock>1320 MHz</supported_graphics_clock>
                <supported_graphics_clock>1305 MHz</supported_graphics_clock>
                <supported_graphics_clock>1290 MHz</supported_graphics_clock>
                <supported_graphics_clock>1275 MHz</supported_graphics_clock>
                <supported_graphics_clock>1260 MHz</supported_graphics_clock>
                <supported_graphics_clock>1245 MHz</supported_graphics_clock>
                <supported_graphics_clock>1230 MHz</supported_graphics_clock>
                <supported_graphics_clock>1215 MHz</supported_graphics_clock>
                <supported_graphics_clock>1200 MHz</supported_graphics_clock>
                <supported_graphics_clock>1185 MHz</supported_graphics_clock>
                <supported_graphics_clock>1170 MHz</supported_graphics_clock>
                <supported_graphics_clock>1155 MHz</supported_graphics_clock>
                <supported_graphics_clock>1140 MHz</supported_graphics_clock>
                <supported_graphics_clock>1125 MHz</supported_graphics_clock>
                <supported_graphics_clock>1110 MHz</supported_graphics_clock>
                <supported_graphics_clock>1095 MHz</supported_graphics_clock>
                <supported_graphics_clock>1080 MHz</supported_graphics_clock>
                <supported_graphics_clock>1065 MHz</supported_graphics_clock>
                <supported_graphics_clock>1050 MHz</supported_graphics_clock>
                <supported_graphics_clock>1035 MHz</supported_graphics_clock>
                <supported_graphics_clock>1020 MHz</supported_graphics_clock>
                <supported_graphics_clock>1005 MHz</supported_graphics_clock>
                <supported_graphics_clock>990 MHz</supported_graphics_clock>
                <supported_graphics_clock>975 MHz</supported_graphics_clock>
                <supported_graphics_clock>960 MHz</supported_graphics_clock>
                <supported_graphics_clock>945 MHz</supported_graphics_clock>
                <supported_graphics_clock>930 MHz</supported_graphics_clock>
                <supported_graphics_clock>915 MHz</supported_graphics_clock>
                <supported_graphics_clock>900 MHz</supported_graphics_clock>
                <supported_graphics_clock>885 MHz</supported_graphics_clock>
                <supported_graphics_clock>870 MHz</supported_graphics_clock>
                <supported_graphics_clock>855 MHz</supported_graphics_clock>
                <supported_graphics_clock>840 MHz</supported_graphics_clock>
                <supported_graphics_clock>825 MHz</supported_graphics_clock>
                <supported_graphics_clock>810 MHz</supported_graphics_clock>
                <supported_graphics_clock>795 MHz</supported_graphics_clock>
                <supported_graphics_clock>780 MHz</supported_graphics_clock>
                <supported_graphics_clock>765 MHz</supported_graphics_clock>
                <supported_graphics_clock>750 MHz</supported_graphics_clock>
                <supported_graphics_clock>735 MHz</supported_graphics_clock>
                <supported_graphics_clock>720 MHz</supported_graphics_clock>
                <supported_graphics_clock>705 MHz</supported_graphics_clock>
                <supported_graphics_clock>690 MHz</supported_graphics_clock>
                <supported_graphics_clock>675 MHz</supported_graphics_clock>
                <supported_graphics_clock>660 MHz</supported_graphics_clock>
                <supported_graphics_clock>645 MHz</supported_graphics_clock>
                <supported_graphics_clock>630 MHz</supported_graphics_clock>
                <supported_graphics_clock>615 MHz</supported_graphics_clock>
                <supported_graphics_clock>600 MHz</supported_graphics_clock>
                <supported_graphics_clock>585 MHz</supported_graphics_clock>
                <supported_graphics_clock>570 MHz</supported_graphics_clock>
                <supported_graphics_clock>555 MHz</supported_graphics_clock>
                <supported_graphics_clock>540 MHz</supported_graphics_clock>
                <supported_graphics_clock>525 MHz</supported_graphics_clock>
                <supported_graphics_clock>510 MHz</supported_graphics_clock>
                <supported_graphics_clock>495 MHz</supported_graphics_clock>
                <supported_graphics_clock>480 MHz</supported_graphics_clock>
                <supported_graphics_clock>465 MHz</supported_graphics_clock>
                <supported_graphics_clock>450 MHz</supported_graphics_clock>
                <supported_graphics_clock>435 MHz</supported_graphics_clock>
                <supported_graphics_clock>420 MHz</supported_graphics_clock>
                <supported_graphics_clock>405 MHz</supported_graphics_clock>
                <supported_graphics_clock>390 MHz</supported_graphics_clock>
                <supported_graphics_clock>375 MHz</supported_graphics_clock>
                <supported_graphics_clock>360 MHz</supported_graphics_clock>
                <supported_graphics_clock>345 MHz</supported_graphics_clock>
                <supported_graphics_clock>330 MHz</supported_graphics_clock>
                <supported_graphics_clock>315 MHz</supported_graphics_clock>
                <supported_graphics_clock>300 MHz</supported_graphics_clock>
                <supported_graphics_clock>285 MHz</supported_graphics_clock>
                <supported_graphics_clock>270 MHz</supported_graphics_clock>
                <supported_graphics_clock>255 MHz</supported_graphics_clock>
                <supported_graphics_clock>240 MHz</supported_graphics_clock>
                <supported_graphics_clock>225 MHz</supported_graphics_clock>
                <supported_graphics_clock>210 MHz</supported_graphics_clock>
            </supported_mem_clock>
        </supported_clocks>
        <processes />
        <accounted_processes />
    </gpu>
</nvidia_smi_log>'
}

test_nvidia_smi_plugin() {
    # shellcheck source=agents/plugins/nvidia-smi
    response=$(. "$MK_NVIDIA_SMI_PLUGIN_PATH")
    assertEquals "XML output" "<<<nvidia_smi:sep(9)>>>
$(nvidia-smi)" "$response"
}

# shellcheck disable=SC1090 # Can't follow
. "$UNIT_SH_SHUNIT2"
