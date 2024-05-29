#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import os
from collections.abc import Iterable
from pathlib import Path
from unittest.mock import Mock

import pytest

from cmk.active_checks.check_sftp import Args, CheckSftp, parse_arguments, SecurityError


def _with_omd_root(path: str) -> Iterable[None]:
    old_omd_root = os.environ.get("OMD_ROOT")
    try:
        os.environ["OMD_ROOT"] = path
        yield
    finally:
        if old_omd_root is not None:
            os.environ["OMD_ROOT"] = old_omd_root
        else:
            del os.environ["OMD_ROOT"]


@pytest.fixture(name="mock_omd_root")
def fixture_mock_omd_root() -> Iterable[None]:
    yield from _with_omd_root("/omdroot")


@pytest.fixture(name="tmp_omd_root")
def fixture_omd_root(tmp_path: Path) -> Iterable[None]:
    yield from _with_omd_root(str(tmp_path))


class MockSSHClient(Mock):
    def open_sftp(self) -> Mock:
        connection = Mock()
        connection.getcwd.return_value = "."
        connection.stat.return_value.st_mtime = 42
        return connection


@pytest.mark.parametrize(
    "params,expected_args",
    [
        pytest.param(
            [],
            Args(
                host=None,
                user=None,
                pass_=None,
                port=22,
                get_remote=None,
                get_local=None,
                put_local=None,
                put_remote=None,
                timestamp=None,
                timeout=10.0,
                verbose=False,
                look_for_keys=False,
            ),
            id="defaults",
        ),
        pytest.param(
            [
                "--host=host",
                "--user=user",
                "--secret=pass",
                "--port=42",
                "--get-remote",
                "get_remote",
                "--put-remote=put_remote",
                "--get-local=get_local",
                "--put-local=put_local",
                "--get-timestamp=timestamp",
                "--timeout=42",
                "--look-for-keys",
                "-v",
            ],
            Args(
                host="host",
                user="user",
                pass_="pass",
                port=42,
                get_remote="get_remote",
                get_local="get_local",
                put_local="put_local",
                put_remote="put_remote",
                timestamp="timestamp",
                timeout=42.0,
                verbose=True,
                look_for_keys=True,
            ),
            id="all specified",
        ),
    ],
)
def test_parse_arguments(params: list[str], expected_args: Args) -> None:
    assert parse_arguments(params) == expected_args


@pytest.mark.parametrize(
    "arguments,expected_options",
    [
        pytest.param("", None, id="no args"),
        pytest.param(
            "--put-local local_file.txt",
            CheckSftp.TransferOptions(
                local="/omdroot/var/check_mk/active_checks/check_sftp/local_file.txt",
                remote="local_file.txt",
            ),
            id="put-local, implicit put-remote",
        ),
        pytest.param(
            "--put-local foo/bar/local_file.txt --put-remote foo/../bar",
            CheckSftp.TransferOptions(
                local="/omdroot/var/check_mk/active_checks/check_sftp/foo/bar/local_file.txt",
                remote="bar/local_file.txt",
            ),
            id="put-local and put-remote",
        ),
        pytest.param(
            "--put-local /etc/htpasswd --put-remote /dump/here",
            CheckSftp.TransferOptions(
                local="/omdroot/var/check_mk/active_checks/check_sftp/etc/htpasswd",
                remote="dump/here/htpasswd",
            ),
            id="absolute paths become relative",
        ),
        pytest.param(
            "--put-local htpasswd --put-remote ../etc",
            CheckSftp.TransferOptions(
                local="/omdroot/var/check_mk/active_checks/check_sftp/htpasswd",
                remote="../etc/htpasswd",
            ),
            id="path traversal on remote not handled by the check",
        ),
    ],
)
def test_put_options(
    mock_omd_root: None, arguments: str, expected_options: None | CheckSftp.TransferOptions
) -> None:
    """Check that testing file upload options work, given the put-local/put-remote arguments"""
    check = CheckSftp(MockSSHClient(), parse_arguments(arguments.split()))

    assert check.download_options is None
    assert check.timestamp_path is None

    assert check.upload_options == expected_options


@pytest.mark.parametrize(
    "arguments,expected_options",
    [
        pytest.param("--verbose", None, id="no args"),
        pytest.param(
            "--get-remote remote_file.txt",
            CheckSftp.TransferOptions(
                remote="remote_file.txt",
                local="/omdroot/var/check_mk/active_checks/check_sftp/remote_file.txt",
            ),
            id="get-remote",
        ),
        pytest.param(
            "--get-remote some/remote_file.txt --get-local my_sub_dir",
            CheckSftp.TransferOptions(
                remote="some/remote_file.txt",
                local="/omdroot/var/check_mk/active_checks/check_sftp/my_sub_dir/remote_file.txt",
            ),
            id="get-remote and get-local",
        ),
        pytest.param(
            "--get-remote /htpasswd --get-local /etc",
            CheckSftp.TransferOptions(
                local="/omdroot/var/check_mk/active_checks/check_sftp/etc/htpasswd",
                remote="htpasswd",
            ),
            id="absolute paths become relative",
        ),
        pytest.param(
            "--get-remote ../xyz/../../etc/htpasswd",
            CheckSftp.TransferOptions(
                local="/omdroot/var/check_mk/active_checks/check_sftp/htpasswd",
                remote="../../etc/htpasswd",
            ),
            id="path traversal on remote not handled by the check",
        ),
    ],
)
def test_get_options(
    mock_omd_root: None, arguments: str, expected_options: None | CheckSftp.TransferOptions
) -> None:
    """Check that testing file download options work, given the get-local/get-remote arguments"""
    check = CheckSftp(MockSSHClient(), parse_arguments(arguments.split()))

    assert check.upload_options is None
    assert check.timestamp_path is None

    assert check.download_options == expected_options


@pytest.mark.parametrize(
    "arguments,expected_options",
    [
        pytest.param("", None, id="no args"),
        pytest.param("--get-timestamp some_file.txt", "some_file.txt", id="get-timestamp"),
    ],
)
def test_timestamp_path(mock_omd_root: None, arguments: str, expected_options: None | str) -> None:
    check = CheckSftp(MockSSHClient(), parse_arguments(arguments.split()))

    assert check.upload_options is None
    assert check.download_options is None

    assert check.timestamp_path == expected_options


@pytest.mark.parametrize(
    "arguments",
    [
        "--put-local ./../../../etc/htpasswd",
        "--get-remote htpasswd --get-local ../../etc",
    ],
)
def test_path_traversal(mock_omd_root: None, arguments: str) -> None:
    with pytest.raises(SecurityError):
        CheckSftp(MockSSHClient(), parse_arguments(arguments.split()))


def test_run_optional_checks(tmp_omd_root: None) -> None:
    check = CheckSftp(
        MockSSHClient(),
        parse_arguments(
            [
                "--put-local=local_file.txt",
                "--get-remote=remote_file.txt",
                "--get-timestamp=timestamp.txt",
            ]
        ),
    )

    status, messages = check.run_optional_checks()

    assert os.path.isfile(f"{check.local_tempdir()}/local_file.txt"), "Test file was created"
    assert status == 0
    assert messages[0] == "Successfully put file to SFTP server"
    assert messages[1] == "Successfully got file from SFTP server"
    assert messages[2].startswith("Timestamp of timestamp.txt is:")


def test_optional_checks_fail(tmp_omd_root: None) -> None:
    check = CheckSftp(
        MockSSHClient(),
        parse_arguments(
            [
                "--put-local=local_file.txt",
                "--get-remote=remote_file.txt",
                "--get-timestamp=timestamp.txt",
            ]
        ),
    )
    check.connection.put.side_effect = Exception("fail")  # type: ignore[attr-defined]
    check.connection.get.side_effect = Exception("fail")  # type: ignore[attr-defined]
    check.connection.stat.side_effect = Exception("fail")  # type: ignore[attr-defined]

    status, messages = check.run_optional_checks()

    assert status == 2
    assert messages == [
        "Could not put file to SFTP server! (!!)",
        "Could not get file from SFTP server! (!!)",
        "Could not get timestamp of file! (!!)",
    ]


def test_optional_checks_fail_verbose(tmp_omd_root: None) -> None:
    check = CheckSftp(
        MockSSHClient(),
        parse_arguments(
            [
                "--put-local=local_file.txt",
                "--verbose",
            ]
        ),
    )
    check.connection.put.side_effect = Exception("fail")  # type: ignore[attr-defined]

    with pytest.raises(Exception, match="fail"):
        check.run_optional_checks()
