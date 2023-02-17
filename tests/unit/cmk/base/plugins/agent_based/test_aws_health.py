#!/usr/bin/env python3
# Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import random
import time

import pydantic_factories
import pytest

from cmk.base.plugins.agent_based import aws_health
from cmk.base.plugins.agent_based.agent_based_api import v1

CURRENT_TIME = aws_health.Seconds(1670000000.0)


def _random_time(oldest: float, newest: float) -> time.struct_time:
    return time.gmtime(random.uniform(oldest, newest))


class EntryFactory(pydantic_factories.ModelFactory):
    __model__ = aws_health.Entry

    @classmethod
    def published_parsed(cls) -> time.struct_time:
        return _random_time(
            oldest=1.0,
            newest=CURRENT_TIME,
        )


class RecentEntryFactory(EntryFactory):
    @classmethod
    def published_parsed(cls) -> time.struct_time:
        return _random_time(
            oldest=CURRENT_TIME - aws_health._IGNORE_ENTRIES_OLDER_THAN + 1.0,
            newest=CURRENT_TIME,
        )


class OutdatedEntryFactory(EntryFactory):
    @classmethod
    def published_parsed(cls) -> time.struct_time:
        return _random_time(
            oldest=1.0,
            newest=CURRENT_TIME - aws_health._IGNORE_ENTRIES_OLDER_THAN - 1.0,
        )


def test_parse_string_table() -> None:
    # Assemble
    rss_str = """
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title><![CDATA[Amazon Web Services Service Status]]></title>
        <link>http://status.aws.amazon.com/</link>
        <language>en-us</language>
        <lastBuildDate>Mon, 13 Feb 2023 00:05:51 PST</lastBuildDate>
        <generator>AWS Service Health Dashboard RSS Generator</generator>
        <description><![CDATA[Amazon Web Services Service Status]]></description>
        <ttl>5</ttl>
        <!-- You seem to care about knowing about your events, why not check out https://docs.aws.amazon.com/health/latest/ug/getting-started-api.html -->


         <item>
          <title><![CDATA[Service is operating normally: [RESOLVED] Connectivity issues affecting some instances]]></title>
          <link>http://status.aws.amazon.com/</link>
          <pubDate>Fri, 10 Feb 2023 15:48:00 PST</pubDate>
          <guid isPermaLink="false">http://status.aws.amazon.com/#rds-us-east-1_1676072880</guid>
          <description><![CDATA[Between 11:18 AM and 2:44 PM PST, some Amazon Aurora PostgreSQL customers experienced issues accessing their databases in the US-EAST-1 Region. The issue has been resolved and the service is operating normally.]]></description>
         </item>


         <item>
          <title><![CDATA[Informational message: Increased error rates when accessing Cost Explorer, Budgets, and Cost and Usage Reports]]></title>
          <link>http://status.aws.amazon.com/</link>
          <pubDate>Thu, 02 Feb 2023 14:19:24 PST</pubDate>
          <guid isPermaLink="false">http://status.aws.amazon.com/#billingconsole_1675376364</guid>
          <description><![CDATA[We are currently seeing early signs of recovery and we continue to work towards full mitigation.  We will provide you another update by 3:15 PM PST.]]></description>
         </item>

      </channel>
    </rss>
    """
    string_table = [[aws_health.AgentOutput(rss_str=rss_str).json()]]
    # Act
    section = aws_health.parse_string_table(string_table)
    # Assert
    assert section.entries


@pytest.mark.parametrize("size", [0, 2, 4])
def test_discovery_aws_health(size: int) -> None:
    section = aws_health.AWSRSSFeed(entries=EntryFactory.batch(size=size))
    discovery_results = list(aws_health.discover_aws_health(section))
    assert any(v1.Service(item="Global") == service for service in discovery_results)


@pytest.mark.parametrize(
    "entry, expected_id",
    [
        pytest.param(
            EntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#billingconsole_1660000000",
            ),
            "#billingconsole",
            id="Service is AWS Billing Console",
        ),
        pytest.param(
            EntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#rds-us-east-1_1676072880",
            ),
            "#rds-us-east-1",
            id="Service is Amazon Relational Database Service",
        ),
    ],
)
def test_service_region_id(entry: aws_health.Entry, expected_id: str) -> None:
    assert entry.service_region_id() == expected_id


@pytest.mark.parametrize(
    "entry, expected_region",
    [
        pytest.param(
            EntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#billingconsole_1660000000",
            ),
            "Global",
            id="This belongs to no region, it is Global",
        ),
        pytest.param(
            EntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#rds-us-east-1_1676072880",
            ),
            "US East (N. Virginia)",
            id="The region is US East (N. Virginia)",
        ),
    ],
)
def test_region(entry: aws_health.Entry, expected_region: str) -> None:
    assert entry.region() == expected_region


def test__check_aws_health_no_issues() -> None:
    section = aws_health.AWSRSSFeed(entries=[])
    check_result = list(aws_health._check_aws_health(CURRENT_TIME, "Global", section))
    assert [v1.Result(state=v1.State.OK, summary="No issues")] == check_result


def test__check_aws_health_remove_outdated() -> None:
    section = aws_health.AWSRSSFeed(
        entries=[
            OutdatedEntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#billingconsole_1660000000",
            ),
            OutdatedEntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#billingconsole_1660000001",
            ),
        ]
    )
    check_result = list(aws_health._check_aws_health(CURRENT_TIME, "Global", section))
    assert [v1.Result(state=v1.State.OK, summary="No issues")] == check_result


def test__check_aws_health_global_issues() -> None:
    section = aws_health.AWSRSSFeed(
        entries=[
            RecentEntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#billingconsole_1660000000",
            ),
            RecentEntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#billingconsole_1660000001",
            ),
        ]
    )
    check_result = list(aws_health._check_aws_health(CURRENT_TIME, "Global", section))
    assert len(check_result) == 1 + len(section.entries)


def test__restrict_to_region() -> None:
    entries = [
        EntryFactory.build(
            link="http://status.aws.amazon.com/",
            id="http://status.aws.amazon.com/#rds-us-east-1_1676072880",
        ),
        EntryFactory.build(
            link="http://status.aws.amazon.com/",
            id="http://status.aws.amazon.com/#billingconsole_1660000000",
        ),
        EntryFactory.build(
            link="http://status.aws.amazon.com/",
            id="http://status.aws.amazon.com/#billingconsole_1660000001",
        ),
    ]
    us_east_entries = aws_health._restrict_to_region(entries, "US East (N. Virginia)")
    assert us_east_entries == entries[:1]


def test__sort_newest_entry_first() -> None:
    times = [1.0, 3.0, 2.0]
    entries = [EntryFactory.build(published_parsed=time.localtime(t)) for t in times]
    sorted_entries = aws_health._sort_newest_entry_first(entries)
    assert [time.mktime(e.published_parsed) for e in sorted_entries] == [3.0, 2.0, 1.0]


def test__obtain_recent_entries() -> None:
    entries = aws_health._sort_newest_entry_first(RecentEntryFactory.batch(size=3))
    recent_entries = aws_health._obtain_recent_entries(CURRENT_TIME, entries)
    assert entries == recent_entries


def test__group_by_service_identifier_single() -> None:
    entries = aws_health.SortedEntries(
        [
            EntryFactory.build(
                link="http://status.aws.amazon.com/",
                id="http://status.aws.amazon.com/#rds-us-east-1_1676072880",
            ),
        ]
    )
    groups = aws_health._group_by_service_identifier(entries)
    assert groups == [entries]


def test__group_by_service_identifier_two() -> None:
    ids = [
        "http://status.aws.amazon.com/#rds-us-east-1_1600000001",
        "http://status.aws.amazon.com/#rds-us-east-1_1600000000",
        "http://status.aws.amazon.com/#supportcenter-us-east-1_1600000000",
        "http://status.aws.amazon.com/#supportcenter-us-east-1_1600000000",
    ]

    entries = aws_health._sort_newest_entry_first(
        [EntryFactory.build(link="http://status.aws.amazon.com/", id=id_) for id_ in ids]
    )
    groups = aws_health._group_by_service_identifier(entries)
    group_ids = sorted([{e.service_region_id() for e in group} for group in groups])
    assert group_ids == [{"#supportcenter-us-east-1"}, {"#rds-us-east-1"}]
    assert any(group == aws_health._sort_newest_entry_first(group) for group in groups)


def test__check_aws_health_for_service() -> None:
    # Assemble
    entries = aws_health._sort_newest_entry_first(RecentEntryFactory.batch(size=3))
    newest_entry = entries[0]
    # Act
    title_result, *entry_results = aws_health._check_aws_health_for_service(entries)
    # Assert
    assert title_result == v1.Result(
        state=aws_health._state_from_entry(newest_entry), summary=newest_entry.title
    )
    for r, e in zip(entry_results, entries):
        assert isinstance(r, v1.Result)
        assert e.published in r.details
        assert e.summary in r.details


@pytest.mark.parametrize(
    "title, expected_state",
    [
        pytest.param(
            "Service is operating normally: [RESOLVED] Connectivity issues affecting some instances",
            v1.State.OK,
            id="Message retrieved from real AWS rss feed. OK message.",
        ),
        pytest.param(
            "Informational message: Connectivity issues affecting some instances",
            v1.State.WARN,
            id="Message retrieved from real AWS rss feed. Problem message.",
        ),
        pytest.param(
            "Performance issue: AWS bad!",
            v1.State.WARN,
            id="Made up based on the AWS dashboard. Problem message.",
        ),
        pytest.param(
            "Service disruption: AWS bad!",
            v1.State.WARN,
            id="Another message made up based on the AWS dashboard. Problem message.",
        ),
        pytest.param(
            "OK: AWS good!",
            v1.State.OK,
            id="This is a made up based on how some others monitor the feed. OK message.",
        ),
        pytest.param(
            "AWS bad!",
            v1.State.WARN,
            id="If Checkmk does not know the message type, then it's considered a problem.",
        ),
    ],
)
def test__state_from_entry(title: str, expected_state: v1.State) -> None:
    entry = EntryFactory.build(title=title)
    assert expected_state == aws_health._state_from_entry(entry)
