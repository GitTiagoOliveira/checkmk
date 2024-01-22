#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Callable
from dataclasses import dataclass
from enum import auto, Enum

from ._localize import Localizable
from .form_specs import Dictionary, FormSpec, ItemFormSpec, SingleChoice, Text


class Topic(Enum):
    AGENT_PLUGINS = "agent_plugins"
    APPLICATIONS = "applications"
    CACHING_MESSAGE_QUEUES = "cache_message_queues"
    CLOUD = "cloud"
    CONFIGURATION_DEPLOYMENT = "configuration_deployment"
    DATABASES = "databases"
    GENERAL = "general"
    ENVIRONMENTAL = "environmental"
    LINUX = "linux"
    NETWORKING = "networking"
    MIDDLEWARE = "middleware"
    NOTIFICATIONS = "notifications"
    OPERATING_SYSTEM = "operating_system"
    PERIPHERALS = "peripherals"
    POWER = "power"
    SERVER_HARDWARE = "server_hardware"
    STORAGE = "storage"
    VIRTUALIZATION = "virtualization"
    WINDOWS = "windows"


@dataclass(frozen=True)
class CustomTopic:
    """
    Args:
        title: human-readable title of this group
    """

    title: Localizable


class EvalType(Enum):
    MERGE = auto()
    ALL = auto()


@dataclass(frozen=True)
class HostCondition:
    ...


@dataclass(frozen=True)
class Host:
    """Specifies rule configurations for hosts

    Args:
        title: Human readable title
        topic: Categorization of the rule
        parameter_form: Configuration specification
        eval_type: How the rules of this RuleSpec are evaluated in respect to each other
        name: Identifier of the rule spec
        is_deprecated: Flag to indicate whether this rule is deprecated and should no longer be used
        help_text: Description to help the user with the configuration
    """

    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class ServiceMonitoringWithoutService:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class ServiceMonitoring:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class CheckParameterWithItem:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], Dictionary]
    item_form: ItemFormSpec
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None
    create_enforced_service: bool = True

    def __post_init__(self) -> None:
        assert isinstance(self.item_form, (Text, SingleChoice))
        if not isinstance(self.topic, (Topic, CustomTopic)):
            raise ValueError


@dataclass(frozen=True)
class CheckParameterWithoutItem:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], Dictionary]
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None
    create_enforced_service: bool = True


@dataclass(frozen=True)
class EnforcedServiceWithItem:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec] | None
    item_form: ItemFormSpec
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None

    def __post_init__(self) -> None:
        assert isinstance(self.item_form, (Text, SingleChoice))
        if not isinstance(self.topic, (Topic, CustomTopic)):
            raise ValueError


@dataclass(frozen=True)
class EnforcedServiceWithoutItem:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec] | None
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.topic, (Topic, CustomTopic)):
            raise ValueError


@dataclass(frozen=True)
class DiscoveryParameters:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class ActiveCheck:
    """Specifies rule configurations for active checks

    Args:
        title: Human readable title
        topic: Categorization of the rule
        parameter_form: Configuration specification
        eval_type: How the rules of this RuleSpec are evaluated in respect to each other
        name: Identifier of the rule spec
        is_deprecated: Flag to indicate whether this rule is deprecated and should no longer be used
        help_text: Description to help the user with the configuration
    """

    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class AgentConfig:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class SpecialAgent:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class AgentAccess:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class NotificationParameters:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class SNMP:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class InventoryParameters:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class ExtraHostConfEventConsole:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class ExtraHostConfHostMonitoring:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None


@dataclass(frozen=True)
class ExtraServiceConf:
    title: Localizable
    topic: Topic | CustomTopic
    parameter_form: Callable[[], FormSpec]
    eval_type: EvalType
    name: str
    is_deprecated: bool = False
    help_text: Localizable | None = None
