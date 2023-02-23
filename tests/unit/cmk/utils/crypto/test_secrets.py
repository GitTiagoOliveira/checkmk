#!/usr/bin/env python3
# Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

import cmk.utils.crypto.secrets as secrets


def test_create_secret_and_hmac(tmp_path: Path) -> None:
    """A secret can be instantiated and the HMAC comes out as expected"""

    my_secret_file = tmp_path / "mytest.secret"
    my_secret_file.write_bytes(b"my test secret")

    class MySecret(secrets._LocalSecret):
        path = my_secret_file

    secret = MySecret()

    assert secret.path == my_secret_file
    assert (
        secret.hmac("hello") == "3bc5a0f1f479929f6c6330bd2dabf2d78ed389ab329f2c0b0baadfb3a01dbeae"
    )
