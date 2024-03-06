#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""FormSpecs that can be composed of other FormSpecs"""

from dataclasses import dataclass
from typing import Any, Generic, Mapping, Sequence

from .._localize import Label, Message, Title
from ._base import DefaultValue, FormSpec, InputHint, ModelT


@dataclass(frozen=True, kw_only=True)
class CascadingSingleChoiceElement(Generic[ModelT]):
    """Specifies an element of a single choice cascading form.

    Arguments:
    **********
    """

    name: str
    """Identifier of the CascadingSingleChoiceElement. Must be a valid Python identifier."""
    title: Title
    """Human readable title that will be shown in the UI."""
    parameter_form: FormSpec[ModelT]
    """Configuration specification of this entry."""

    def __post_init__(self) -> None:
        if not self.name.isidentifier():
            raise ValueError(f"'{self.name}' is not a valid Python identifier")


@dataclass(frozen=True, kw_only=True)  # type: ignore[misc]
class CascadingSingleChoice(FormSpec[tuple[str, object]]):
    """Specification for a single-selection from multiple options.

    Every option can have its own configuration form.

    Consumer model:
    ***************
    **Type**: ``tuple[str, object]``

    The configured value will be presented as a 2-tuple consisting of the name of the choice and
    the consumer model of the selected form specification.

    **Example**: A CascadingSingleChoice with a selected :class:`Dictionary` form specification
    would result in ``("my_value", {...})``

    Arguments:
    **********
    """

    elements: Sequence[CascadingSingleChoiceElement[Any]]
    """Elements to choose from."""
    label: Label | None = None
    """Text displayed in front of the input field."""
    prefill: DefaultValue[str] | InputHint[Title] = InputHint(Title("Please choose"))
    """Name of pre-selected choice. If DefaultValue is used, it must be one of the elements names.
    If InputHint is used, its title will be shown as a placeholder in the UI, requiring the user to
    select a value."""

    def __post_init__(self) -> None:
        avail_idents = {elem.name for elem in self.elements}  # type: ignore[misc]
        if isinstance(self.prefill, DefaultValue) and self.prefill.value not in avail_idents:
            raise ValueError("Default element is not one of the specified elements")


@dataclass(frozen=True, kw_only=True)
class DictElement(Generic[ModelT]):
    """Specifies an element of a dictionary form.

    Arguments:
    **********
    """

    parameter_form: FormSpec[ModelT]
    """Configuration specification of this entry."""
    required: bool = False
    """Whether the user has to configure the value in question.

    If set to False, it may be omitted and values will be inherited from more general rules
    or the default configuration.
    """
    render_only: bool = False
    """Element that can't be edited. Can be used to store the discovered parameters."""


@dataclass(frozen=True, kw_only=True)  # type: ignore[misc]
class Dictionary(FormSpec[Mapping[str, object]]):
    """
    Specifies a (multi-)selection of configuration options.

    Consumer model:
    ***************
    **Type**: ``dict[str, object]``
    The configured value will be presented as a dictionary consisting of the names of provided
    configuration options and their respective consumer models.

    Arguments:
    **********
    """

    elements: Mapping[str, DictElement[Any]]
    """key-value mapping where the key identifies the option and the value specifies how
    the nested form can be configured. The key has to be a valid Python identifier."""

    no_elements_text: Message = Message("(no parameters)")
    """Text to show if no elements are specified"""

    deprecated_elements: tuple[str, ...] = ()
    """Elements that can no longer be configured, but aren't removed from the old rules that
    already have them configured. Can be used when deprecating elements, to avoid breaking the
    old configurations."""

    def __post_init__(self) -> None:
        for key in self.elements:  # type: ignore[misc]
            if not key.isidentifier():
                raise ValueError(f"'{key}' is not a valid Python identifier")


@dataclass(frozen=True, kw_only=True)
class List(FormSpec[Sequence[ModelT]]):
    """
    Specifies a list of configuration elements of the same type.

    Consumer model:
    ***************
    **Type**: ``list[object]``
    The configured value will be presented as a list consisting of the consumer models of the
    configured elements.

    Arguments:
    **********
    """

    element_template: FormSpec[ModelT]
    """Configuration specification of the list elements."""
    add_element_label: Label = Label("Add new entry")
    """Label used to customize the add element button."""
    remove_element_label: Label = Label("Remove this entry")
    """Label used to customize the remove element button."""
    no_element_label: Label = Label("No entries")
    """Label used in the rule summary if the list is empty."""

    editable_order: bool = True
    """Indicate if the users should be able to reorder the elements in the UI."""


@dataclass(frozen=True, kw_only=True)
class MultipleChoiceElement:
    """Specifies an element of a multiple choice form.

    Arguments:
    **********
    """

    name: str
    """Identifier of the MultipleChoiceElement. Must be a valid Python identifier."""
    title: Title
    """Human readable title that will be shown in the UI."""

    def __post_init__(self) -> None:
        if not self.name.isidentifier():
            raise ValueError(f"'{self.name}' is not a valid Python identifier")


@dataclass(frozen=True, kw_only=True)
class MultipleChoice(FormSpec[Sequence[str]]):
    """Specifies a multiple choice form.

    Consumer model:
    ***************
    **Type**: ``list[str]``
    The configured value will be presented as a list consisting of the names of the selected
    elements.

    Arguments:
    **********
    """

    elements: Sequence[MultipleChoiceElement]
    """Elements to choose from."""
    show_toggle_all: bool = False
    """Show toggle all elements option in the UI."""

    prefill: DefaultValue[Sequence[str]] = DefaultValue(())
    """Element names to select by default."""

    def __post_init__(self) -> None:
        available_names = {elem.name for elem in self.elements}
        if invalid := set(self.prefill.value) - available_names:
            raise ValueError(f"Invalid prefill element(s): {', '.join(invalid)}")
