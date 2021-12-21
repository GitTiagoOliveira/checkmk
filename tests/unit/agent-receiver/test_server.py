#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import io
import json
import os
import stat
from pathlib import Path
from unittest import mock
from uuid import UUID

import pytest
from agent_receiver import constants
from agent_receiver.checkmk_rest_api import CMKEdition
from agent_receiver.models import HostTypeEnum
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def deactivate_certificate_validation(mocker: MockerFixture) -> None:
    mocker.patch(
        "agent_receiver.certificates._invalid_certificate_response",
        lambda _h: None,
    )


def test_register_with_labels_unauthenticated(
    mocker: MockerFixture,
    client: TestClient,
    uuid: UUID,
) -> None:
    mocker.patch(
        "agent_receiver.server.cmk_edition",
        side_effect=HTTPException(
            status_code=401,
            detail="User authentication failed",
        ),
    )
    response = client.post(
        "/register_with_labels",
        auth=("herbert", "joergl"),
        json={
            "uuid": str(uuid),
            "agent_labels": {},
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "User authentication failed"}


def test_register_with_labels_cre(
    mocker: MockerFixture,
    client: TestClient,
    uuid: UUID,
) -> None:
    mocker.patch(
        "agent_receiver.server.cmk_edition",
        lambda _c: CMKEdition["cre"],
    )
    response = client.post(
        "/register_with_labels",
        auth=("herbert", "joergl"),
        json={
            "uuid": str(uuid),
            "agent_labels": {"a": "b"},
        },
    )
    assert response.status_code == 501
    assert response.json() == {
        "detail": "The Checkmk Raw edition does not support registration with agent labels"
    }


def _test_register_with_labels(
    mocker: MockerFixture,
    client: TestClient,
    uuid: UUID,
) -> None:
    mocker.patch(
        "agent_receiver.server.cmk_edition",
        lambda _c: CMKEdition["cee"],
    )
    response = client.post(
        "/register_with_labels",
        auth=("monitoring", "supersafe"),
        json={
            "uuid": str(uuid),
            "agent_labels": {
                "a": "b",
                "c": "d",
            },
        },
    )
    assert response.status_code == 204
    assert json.loads((constants.REGISTRATION_REQUESTS / "NEW" / f"{uuid}.json").read_text()) == {
        "uuid": str(uuid),
        "username": "monitoring",
        "agent_labels": {
            "a": "b",
            "c": "d",
        },
    }
    assert (
        oct(stat.S_IMODE((constants.REGISTRATION_REQUESTS / "NEW" / f"{uuid}.json").stat().st_mode))
        == "0o660"
    )


def test_register_with_labels_folder_missing(
    mocker: MockerFixture,
    client: TestClient,
    uuid: UUID,
) -> None:
    assert not (constants.REGISTRATION_REQUESTS / "NEW").exists()
    _test_register_with_labels(
        mocker,
        client,
        uuid,
    )
    assert oct(stat.S_IMODE((constants.REGISTRATION_REQUESTS / "NEW").stat().st_mode)) == "0o770"


def test_register_with_labels_folder_exists(
    mocker: MockerFixture,
    client: TestClient,
    uuid: UUID,
) -> None:
    (constants.REGISTRATION_REQUESTS / "NEW").mkdir(parents=True)
    _test_register_with_labels(
        mocker,
        client,
        uuid,
    )


def test_agent_data_no_host(
    client: TestClient,
    uuid: UUID,
) -> None:
    mock_file = io.StringIO("mock file")
    response = client.post(
        f"/agent_data/{uuid}",
        headers={"certificate": "irrelevant"},
        files={"monitoring_data": ("filename", mock_file)},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Host is not registered"}


def test_agent_data_pull_host(
    tmp_path: Path,
    client: TestClient,
    uuid: UUID,
) -> None:
    source = constants.AGENT_OUTPUT_DIR / str(uuid)
    source.symlink_to(tmp_path / "hostname")

    response = client.post(
        f"/agent_data/{uuid}",
        headers={"certificate": "irrelevant"},
        files={
            "monitoring_data": (
                "filename",
                io.StringIO("mock file"),
            )
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Host is not a push host"}


def test_agent_data_success(
    tmp_path: Path,
    client: TestClient,
    uuid: UUID,
) -> None:
    mock_file = io.StringIO("mock file")

    source = constants.AGENT_OUTPUT_DIR / str(uuid)
    target_dir = tmp_path / "hostname"
    os.mkdir(target_dir)
    source.symlink_to(target_dir)

    response = client.post(
        f"/agent_data/{uuid}",
        headers={"certificate": "irrelevant"},
        files={"monitoring_data": ("filename", mock_file)},
    )

    file_path = tmp_path / "hostname" / "agent_output"
    assert file_path.exists()

    assert response.status_code == 204


def test_agent_data_move_error(
    tmp_path: Path,
    caplog,
    client: TestClient,
    uuid: UUID,
) -> None:
    mock_file = io.StringIO("mock file")

    os.mkdir(constants.REGISTRATION_REQUESTS / "READY")
    Path(constants.REGISTRATION_REQUESTS / "READY" / f"{uuid}.json").touch()
    os.mkdir(constants.REGISTRATION_REQUESTS / "DISCOVERABLE")

    source = constants.AGENT_OUTPUT_DIR / str(uuid)
    target_dir = tmp_path / "hostname"
    os.mkdir(target_dir)
    source.symlink_to(target_dir)

    with mock.patch("agent_receiver.server.Path.rename") as move_mock:
        move_mock.side_effect = FileNotFoundError()
        response = client.post(
            f"/agent_data/{uuid}",
            headers={"certificate": "irrelevant"},
            files={"monitoring_data": ("filename", mock_file)},
        )

    assert response.status_code == 204
    assert caplog.records[0].message == f"uuid={uuid} Agent data saved"


def test_agent_data_move_ready(
    tmp_path: Path,
    client: TestClient,
    uuid: UUID,
) -> None:
    mock_file = io.StringIO("mock file")

    os.mkdir(constants.REGISTRATION_REQUESTS / "READY")
    Path(constants.REGISTRATION_REQUESTS / "READY" / f"{uuid}.json").touch()
    os.mkdir(constants.REGISTRATION_REQUESTS / "DISCOVERABLE")

    source = constants.AGENT_OUTPUT_DIR / str(uuid)
    target_dir = tmp_path / "hostname"
    os.mkdir(target_dir)
    source.symlink_to(target_dir)

    client.post(
        f"/agent_data/{uuid}",
        headers={"certificate": "irrelevant"},
        files={"monitoring_data": ("filename", mock_file)},
    )

    registration_request = constants.REGISTRATION_REQUESTS / "DISCOVERABLE" / f"{uuid}.json"
    assert registration_request.exists()


def test_registration_status_declined(
    client: TestClient,
    uuid: UUID,
) -> None:
    os.mkdir(constants.REGISTRATION_REQUESTS / "DECLINED")
    with open(constants.REGISTRATION_REQUESTS / "DECLINED" / f"{uuid}.json", "w") as file:
        registration_request = {"message": "Registration request declined"}
        json.dump(registration_request, file)

    response = client.get(
        f"/registration_status/{uuid}",
        headers={"certificate": "cert", "authentication": "auth"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "hostname": None,
        "status": "declined",
        "type": None,
        "message": "Registration request declined",
    }


def test_registration_status_host_not_registered(
    client: TestClient,
    uuid: UUID,
) -> None:
    response = client.get(
        f"/registration_status/{uuid}",
        headers={"certificate": "cert", "authentication": "auth"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Host is not registered"}


def test_registration_status_push_host(
    tmp_path: Path,
    client: TestClient,
    uuid: UUID,
) -> None:
    source = constants.AGENT_OUTPUT_DIR / str(uuid)
    target_dir = tmp_path / "hostname"
    os.mkdir(target_dir)
    source.symlink_to(target_dir)

    os.mkdir(constants.REGISTRATION_REQUESTS / "DISCOVERABLE")
    Path(constants.REGISTRATION_REQUESTS / "DISCOVERABLE" / f"{uuid}.json").touch()

    response = client.get(
        f"/registration_status/{uuid}",
        headers={"certificate": "cert", "authentication": "auth"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "hostname": "hostname",
        "status": "discoverable",
        "type": HostTypeEnum.PUSH.value,
        "message": "Host registered",
    }


def test_registration_status_pull_host(
    tmp_path: Path,
    client: TestClient,
    uuid: UUID,
) -> None:
    source = constants.AGENT_OUTPUT_DIR / str(uuid)
    target_dir = tmp_path / "hostname"
    source.symlink_to(target_dir)

    response = client.get(
        f"/registration_status/{uuid}",
        headers={"certificate": "cert", "authentication": "auth"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "hostname": "hostname",
        "status": None,
        "type": HostTypeEnum.PULL.value,
        "message": "Host registered",
    }
