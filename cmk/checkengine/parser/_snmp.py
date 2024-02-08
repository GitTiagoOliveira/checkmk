#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import logging
import time
from typing import Final

from cmk.utils.hostaddress import HostName
from cmk.utils.sectionname import MutableSectionMap, SectionMap, SectionName

from cmk.snmplib import SNMPRawData, SNMPRawDataElem

from ._parser import HostSections, Parser, SectionNameCollection
from ._sectionstore import SectionStore

__all__ = ["SNMPParser"]


class SNMPParser(Parser[SNMPRawData, SNMPRawData]):
    """A parser for SNMP data.

    Note:
        It's not a parser, there's nothing to parse here.

    """

    def __init__(
        self,
        hostname: HostName,
        section_store: SectionStore[SNMPRawDataElem],
        *,
        check_intervals: SectionMap[int | None],
        keep_outdated: bool,
        logger: logging.Logger,
    ) -> None:
        super().__init__()
        self.hostname: Final = hostname
        self.check_intervals: Final = check_intervals
        self.section_store: Final = section_store
        self.keep_outdated: Final = keep_outdated
        self._logger = logger

    def parse(
        self,
        raw_data: SNMPRawData,
        *,
        # The selection argument is ignored: Selection is done
        # in the fetcher for SNMP.
        selection: SectionNameCollection,
    ) -> HostSections[SNMPRawData]:
        sections = dict(raw_data)
        now = int(time.time())

        def lookup_persist(section_name: SectionName) -> tuple[int, int] | None:
            if (interval := self.check_intervals.get(section_name)) is not None:
                return now, now + interval
            return None

        cache_info: MutableSectionMap[tuple[int, int]] = {}
        new_sections = self.section_store.update(
            sections,
            cache_info,
            lookup_persist,
            now=now,
            keep_outdated=self.keep_outdated,
        )
        return HostSections[SNMPRawData](new_sections, cache_info=cache_info)
