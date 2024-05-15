#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""Contact groups

Contact groups are the link between hosts and services on one side and users on the other.
Every contact group represents a responsibility for a specific area in the IT landscape.

You can find an introduction to user management including contact groups in the
[Checkmk guide](https://docs.checkmk.com/latest/en/wato_user.html).

### Relations

A contact group object can have the following relations present in `links`:

 * `self` - The contact group itself.
 * `urn:org.restfulobject/rels:update` - An endpoint to change this contact group.
 * `urn:org.restfulobject/rels:delete` - An endpoint to delete this contact group.

"""
from collections.abc import Mapping
from typing import Any

from cmk.utils import version

from cmk.gui.http import Response
from cmk.gui.logged_in import user
from cmk.gui.openapi.endpoints.contact_group_config.request_schemas import (
    BulkDeleteContactGroup,
    BulkInputContactGroup,
    BulkUpdateContactGroup,
    InputContactGroup,
    UpdateContactGroupAttributes,
)
from cmk.gui.openapi.endpoints.contact_group_config.response_schemas import (
    ContactGroup,
    ContactGroupCollection,
)
from cmk.gui.openapi.endpoints.utils import (
    fetch_group,
    fetch_specific_groups,
    prepare_groups,
    serialize_group,
    serialize_group_list,
    serve_group,
    update_customer_info,
    update_groups,
    updated_group_details,
)
from cmk.gui.openapi.permission_tracking import disable_permission_tracking
from cmk.gui.openapi.restful_objects import constructors, Endpoint, response_schemas
from cmk.gui.openapi.restful_objects.parameters import GROUP_NAME_FIELD
from cmk.gui.openapi.restful_objects.registry import EndpointRegistry
from cmk.gui.openapi.utils import ProblemException, serve_json
from cmk.gui.session import SuperUserContext
from cmk.gui.utils import permission_verification as permissions
from cmk.gui.watolib.groups import (
    add_group,
    check_modify_group_permissions,
    delete_group,
    edit_group,
    GroupInUseException,
    UnknownGroupException,
)
from cmk.gui.watolib.groups_io import load_contact_group_information

PERMISSIONS = permissions.Perm("wato.users")

RW_PERMISSIONS = permissions.AllPerm(
    [
        permissions.Perm("wato.edit"),
        PERMISSIONS,
    ]
)


@Endpoint(
    constructors.collection_href("contact_group_config"),
    "cmk/create",
    method="post",
    etag="output",
    request_schema=InputContactGroup,
    response_schema=response_schemas.DomainObject,
    permissions_required=RW_PERMISSIONS,
)
def create(params: Mapping[str, Any]) -> Response:
    """Create a contact group"""
    user.need_permission("wato.edit")
    user.need_permission("wato.users")
    body = params["body"]
    name = body["name"]
    group_details = {"alias": body["alias"]}
    if version.edition() is version.Edition.CME:
        group_details = update_customer_info(group_details, body["customer"])
    add_group(name, "contact", group_details)
    group = fetch_group(name, "contact")
    return serve_group(group, serialize_group("contact_group_config"))


@Endpoint(
    constructors.domain_type_action_href("contact_group_config", "bulk-create"),
    "cmk/bulk_create",
    method="post",
    request_schema=BulkInputContactGroup,
    response_schema=ContactGroupCollection,
    permissions_required=RW_PERMISSIONS,
)
def bulk_create(params: Mapping[str, Any]) -> Response:
    """Bulk create contact groups"""
    user.need_permission("wato.edit")
    user.need_permission("wato.users")
    body = params["body"]
    entries = body["entries"]
    contact_group_details = prepare_groups("contact", entries)

    contact_group_names = []
    for group_name, group_details in contact_group_details.items():
        add_group(group_name, "contact", group_details)
        contact_group_names.append(group_name)

    contact_groups = fetch_specific_groups(contact_group_names, "contact")
    return serve_json(serialize_group_list("contact_group_config", contact_groups))


@Endpoint(
    constructors.collection_href("contact_group_config"),
    ".../collection",
    method="get",
    response_schema=ContactGroupCollection,
    permissions_required=PERMISSIONS,
)
def list_group(params: Mapping[str, Any]) -> Response:
    """Show all contact groups"""
    user.need_permission("wato.users")
    collection = [
        {"id": k, "alias": v["alias"]} for k, v in load_contact_group_information().items()
    ]
    return serve_json(
        serialize_group_list("contact_group_config", collection),
    )


@Endpoint(
    constructors.object_href("contact_group_config", "{name}"),
    "cmk/show",
    method="get",
    response_schema=ContactGroup,
    etag="output",
    path_params=[GROUP_NAME_FIELD],
    permissions_required=PERMISSIONS,
)
def show(params: Mapping[str, Any]) -> Response:
    """Show a contact group"""
    user.need_permission("wato.users")
    name = params["name"]
    group = fetch_group(name, "contact")
    return serve_group(group, serialize_group("contact_group_config"))


@Endpoint(
    constructors.object_href("contact_group_config", "{name}"),
    ".../delete",
    method="delete",
    path_params=[GROUP_NAME_FIELD],
    output_empty=True,
    permissions_required=RW_PERMISSIONS,
    additional_status_codes=[409],
)
def delete(params: Mapping[str, Any]) -> Response:
    """Delete a contact group"""
    user.need_permission("wato.edit")
    user.need_permission("wato.users")
    name = params["name"]
    check_modify_group_permissions("contact")
    with disable_permission_tracking():
        # HACK: We need to supress this, due to lots of irrelevant dashboard permissions
        try:
            delete_group(name, "contact")
        except GroupInUseException as exc:
            raise ProblemException(
                status=409,
                title="Group in use problem",
                detail=str(exc),
            )
        except UnknownGroupException as exc:
            raise ProblemException(
                status=404,
                title="Unknown group problem",
                detail=str(exc),
            )

    return Response(status=204)


@Endpoint(
    constructors.domain_type_action_href("contact_group_config", "bulk-delete"),
    ".../delete",
    method="post",
    request_schema=BulkDeleteContactGroup,
    output_empty=True,
    permissions_required=RW_PERMISSIONS,
    additional_status_codes=[404, 409],
)
def bulk_delete(params: Mapping[str, Any]) -> Response:
    """Bulk delete contact groups"""
    user.need_permission("wato.edit")
    user.need_permission("wato.users")
    body = params["body"]
    with disable_permission_tracking(), SuperUserContext():
        for group_name in body["entries"]:
            # We need to supress this, because a lot of dashboard permissions are checked for
            # various reasons.
            try:
                delete_group(group_name, "contact")
            except GroupInUseException as exc:
                raise ProblemException(
                    status=409,
                    title="Group in use problem",
                    detail=str(exc),
                )
            except UnknownGroupException as exc:
                raise ProblemException(
                    status=404,
                    title="Unknown group problem",
                    detail=str(exc),
                )

    return Response(status=204)


@Endpoint(
    constructors.object_href("contact_group_config", "{name}"),
    ".../update",
    method="put",
    path_params=[GROUP_NAME_FIELD],
    response_schema=ContactGroup,
    etag="both",
    request_schema=UpdateContactGroupAttributes,
    permissions_required=RW_PERMISSIONS,
)
def update(params: Mapping[str, Any]) -> Response:
    """Update a contact group"""
    user.need_permission("wato.edit")
    user.need_permission("wato.users")
    name = params["name"]
    group = fetch_group(name, "contact")
    constructors.require_etag(constructors.hash_of_dict(group))
    edit_group(name, "contact", updated_group_details(name, "contact", params["body"]))
    group = fetch_group(name, "contact")
    return serve_group(group, serialize_group("contact_group_config"))


@Endpoint(
    constructors.domain_type_action_href("contact_group_config", "bulk-update"),
    "cmk/bulk_update",
    method="put",
    request_schema=BulkUpdateContactGroup,
    response_schema=ContactGroupCollection,
    permissions_required=RW_PERMISSIONS,
)
def bulk_update(params: Mapping[str, Any]) -> Response:
    """Bulk update contact groups

    Please be aware that when doing bulk updates, it is not possible to prevent the
    [Updating Values]("lost update problem"), which is normally prevented by the ETag locking
    mechanism. Use at your own risk.
    """
    user.need_permission("wato.edit")
    user.need_permission("wato.users")
    body = params["body"]
    entries = body["entries"]
    updated_contact_groups = update_groups("contact", entries)
    return serve_json(serialize_group_list("contact_group_config", updated_contact_groups))


def register(endpoint_registry: EndpointRegistry) -> None:
    endpoint_registry.register(create)
    endpoint_registry.register(bulk_create)
    endpoint_registry.register(list_group)
    endpoint_registry.register(show)
    endpoint_registry.register(delete)
    endpoint_registry.register(bulk_delete)
    endpoint_registry.register(update)
    endpoint_registry.register(bulk_update)
