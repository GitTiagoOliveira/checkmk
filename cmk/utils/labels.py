#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""Helper functions for dealing with Checkmk labels of all kind"""

import sys
import abc
from typing import Callable, List, Dict  # pylint: disable=unused-import
import six

# Explicitly check for Python 3 (which is understood by mypy)
if sys.version_info[0] >= 3:
    from pathlib import Path  # pylint: disable=import-error,unused-import
else:
    from pathlib2 import Path

import cmk.utils.paths
import cmk.utils.store as store
from cmk.utils.rulesets.ruleset_matcher import RulesetMatcher, RulesetMatchObject  # pylint: disable=unused-import
from cmk.utils.type_defs import (  # pylint: disable=unused-import
    HostName, ServiceName, Labels, LabelSources,
)


class LabelManager(object):
    """Helper class to manage access to the host and service labels"""
    def __init__(self, explicit_host_labels, host_label_rules, service_label_rules,
                 discovered_labels_of_service):
        # type: (Dict, List, List, Callable[[HostName, ServiceName], Labels]) -> None
        super(LabelManager, self).__init__()
        self._explicit_host_labels = explicit_host_labels
        self._host_label_rules = host_label_rules
        self._service_label_rules = service_label_rules
        self._discovered_labels_of_service = discovered_labels_of_service

    def labels_of_host(self, ruleset_matcher, hostname):
        # type: (RulesetMatcher, HostName) -> Labels
        """Returns the effective set of host labels from all available sources

        1. Discovered labels
        2. Ruleset "Host labels"
        3. Explicit labels (via host/folder config)

        Last one wins.
        """
        labels = {}  # type: Labels
        labels.update(self._discovered_labels_of_host(hostname))
        labels.update(self._ruleset_labels_of_host(ruleset_matcher, hostname))
        labels.update(self._explicit_host_labels.get(hostname, {}))
        return labels

    def label_sources_of_host(self, ruleset_matcher, hostname):
        # type: (RulesetMatcher, HostName) -> LabelSources
        """Returns the effective set of host label keys with their source
        identifier instead of the value Order and merging logic is equal to
        _get_host_labels()"""
        labels = {}  # type: LabelSources
        labels.update({k: "discovered" for k in self._discovered_labels_of_host(hostname).keys()})
        labels.update(
            {k: "ruleset" for k in self._ruleset_labels_of_host(ruleset_matcher, hostname)})
        labels.update({k: "explicit" for k in self._explicit_host_labels.get(hostname, {}).keys()})
        return labels

    def _ruleset_labels_of_host(self, ruleset_matcher, hostname):
        # type: (RulesetMatcher, HostName) -> Labels
        match_object = RulesetMatchObject(hostname, service_description=None)
        return ruleset_matcher.get_host_ruleset_merged_dict(match_object, self._host_label_rules)

    def _discovered_labels_of_host(self, hostname):
        # type: (HostName) -> Labels
        return {
            label_id: label["value"]
            for label_id, label in DiscoveredHostLabelsStore(hostname).load().items()
        }

    def labels_of_service(self, ruleset_matcher, hostname, service_desc):
        # type: (RulesetMatcher, HostName, ServiceName) -> Labels
        """Returns the effective set of service labels from all available sources

        1. Discovered labels
        2. Ruleset "Host labels"

        Last one wins.
        """
        labels = {}  # type: Labels
        labels.update(self._discovered_labels_of_service(hostname, service_desc))
        labels.update(self._ruleset_labels_of_service(ruleset_matcher, hostname, service_desc))

        return labels

    def label_sources_of_service(self, ruleset_matcher, hostname, service_desc):
        # type: (RulesetMatcher, HostName, ServiceName) -> LabelSources
        """Returns the effective set of host label keys with their source
        identifier instead of the value Order and merging logic is equal to
        _get_host_labels()"""
        labels = {}  # type: LabelSources
        labels.update(
            {k: "discovered" for k in self._discovered_labels_of_service(hostname, service_desc)})
        labels.update({
            k: "ruleset"
            for k in self._ruleset_labels_of_service(ruleset_matcher, hostname, service_desc)
        })

        return labels

    def _ruleset_labels_of_service(self, ruleset_matcher, hostname, service_desc):
        # type: (RulesetMatcher, HostName, ServiceName) -> Labels
        match_object = RulesetMatchObject(hostname, service_description=service_desc)
        return ruleset_matcher.get_service_ruleset_merged_dict(match_object,
                                                               self._service_label_rules)


class ABCDiscoveredLabelsStore(six.with_metaclass(abc.ABCMeta, object)):
    """Managing persistance of discovered labels"""
    @abc.abstractproperty
    def file_path(self):
        # type: () -> Path
        raise NotImplementedError()

    def load(self):
        # type: () -> Dict
        # Skip labels discovered by the previous HW/SW inventory approach (which was addded+removed in 1.6 beta)
        return {
            k: v
            for k, v in store.load_object_from_file(str(self.file_path), default={}).items()
            if isinstance(v, dict)
        }

    def save(self, labels):
        # type: (Dict) -> None
        if not labels:
            if self.file_path.exists():
                self.file_path.unlink()
            return

        self.file_path.parent.mkdir(parents=True, exist_ok=True)  # pylint: disable=no-member
        store.save_object_to_file(str(self.file_path), labels)


class DiscoveredHostLabelsStore(ABCDiscoveredLabelsStore):
    def __init__(self, hostname):
        # type: (str) -> None
        super(DiscoveredHostLabelsStore, self).__init__()
        self._hostname = hostname

    @property
    def file_path(self):
        # type: () -> Path
        return (cmk.utils.paths.discovered_host_labels_dir / self._hostname).with_suffix(".mk")
