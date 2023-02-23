#!/usr/bin/env python3
# Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import hashlib
import hmac
import secrets
from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path

import cmk.utils.paths as paths


class _LocalSecret(ABC):
    def __init__(self) -> None:
        """Read the secret; create it if the file doesn't exist.

        Loading an existing but empty file raises an error.
        """
        # TODO: reading and writing could use some locking, once our locking utilities are improved

        if self.path.exists():
            self.secret = self.path.read_bytes()
            if self.secret:
                return

        self.secret = secrets.token_bytes(32)
        # TODO: mkdir is probably not really required here, just some cmc test failing.
        #       Better way would be to fix the test setup.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(mode=0o600)
        self.path.write_bytes(self.secret)

    @property
    @abstractmethod
    def path(self) -> Path:
        raise NotImplementedError

    def hmac(self, msg: str) -> str:
        """Calculate the HMAC(SHA256) of `msg` using this secret and return the digest in hex"""
        return hmac.new(key=self.secret, msg=msg.encode("utf-8"), digestmod=sha256).hexdigest()

    def derive_secret_key(self, salt: bytes) -> bytes:
        """Derive a symmetric key from the local secret"""
        # TODO: in a future step (that requires migration of passwords) we could switch to HKDF.
        # Scrypt is slow by design but that isn't necessary here because the secret is not just a
        # password but "real" random data.
        # Note that key derivation and encryption/decryption of passwords is duplicated in omd
        # cmk_password_store.h and must be kept compatible!
        return hashlib.scrypt(self.secret, salt=salt, n=2**14, r=8, p=1, dklen=32)


class AuthenticationSecret(_LocalSecret):
    """Secret used to derive cookie authentication hash"""

    path = paths.auth_secret_file


class PasswordStoreSecret(_LocalSecret):
    """Secret used to obfuscate passwords in the password store

    Note: Previously these secrets were created as 256 letters and uppercase digits.
    These existing secrets will be loaded and used, even if they look different from
    the secrets created now.
    """

    path = paths.password_store_secret_file


class EncrypterSecret(_LocalSecret):
    """Secret used to encrypt and authenticate secrets passed _through_ the GUI"""

    # TODO: Use a different secret for separation of concerns. If possible, rotate often. CMK-11925
    path = paths.auth_secret_file
