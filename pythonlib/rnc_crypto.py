#!/usr/bin/python
# -*- encoding: utf8 -*-

"""Support functions involving cryptography.

Author: Rudolf Cardinal (rudolf@pobox.com)
Created: October 2012
Last update: 22 Feb 2015

Copyright/licensing:

    Copyright (C) 2012-2015 Rudolf Cardinal (rudolf@pobox.com).

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import base64
import bcrypt  # sudo apt-get install python-bcrypt
import hashlib
import M2Crypto  # sudo apt-get install python-m2crypto


# =============================================================================
# bcrypt
# =============================================================================

BCRYPT_DEFAULT_LOG_ROUNDS = 12  # bcrypt default; work factor is 2^this.


def create_base64encoded_randomness(num_bytes):
    """Create num_bytes of random data.

    Result is encoded in a string with URL-safe base64 encoding.
    Used (for example) to generate session tokens.
    """
    return base64.urlsafe_b64encode(M2Crypto.m2.rand_bytes(num_bytes))

# http://crackstation.net/hashing-security.htm
# http://www.mindrot.org/projects/py-bcrypt/
# http://codahale.com/how-to-safely-store-a-password/


def hash_password(plaintextpw, log_rounds=BCRYPT_DEFAULT_LOG_ROUNDS):
    """Makes a hashed password (using a new salt) using bcrypt.

    The hashed password includes the salt at its start, so no need to store a
    separate salt.
    """
    salt = bcrypt.gensalt(log_rounds)  # optional parameter governs complexity
    hashedpw = bcrypt.hashpw(plaintextpw, salt)
    return hashedpw


def is_password_valid(plaintextpw, storedhash):
    """Checks if a plaintext password matches a stored hash.

    Uses bcrypt. The stored hash includes its own incorporated salt.
    """
    if storedhash is None:
        storedhash = ""
    if isinstance(storedhash, unicode):
        # Became necessary upon downgrade of CamCOPS from MySQL 5.5.34 (Ubuntu)
        # to 5.1.71 (CentOS 6.5); the VARCHAR was retrieved as Unicode.
        storedhash = str(storedhash)

    if plaintextpw is None:
        plaintextpw = ""
    if isinstance(plaintextpw, unicode):
        plaintextpw = str(plaintextpw)

    try:
        h = bcrypt.hashpw(plaintextpw, storedhash)
    except ValueError:  # e.g. ValueError: invalid salt
        return False
    return (h == storedhash)


# =============================================================================
# MD5
# =============================================================================

class MD5Hasher(object):
    def __init__(self, salt):
        self.salt = salt

    def hash(self, raw):
        raw = str(raw)
        return hashlib.md5(self.salt + raw).hexdigest()


if False:
    TEST_NO_COLLISIONS = """
import hashlib

class MD5Hasher(object):
    def __init__(self, salt):
        self.salt = salt
    def hash(self, raw):
        raw = str(raw)
        return hashlib.md5(self.salt + raw).hexdigest()

MAX_PID_STR = "9" * 10  # e.g. NHS numbers are 10-digit
MAX_PID_NUM = int(MAX_PID_STR)
# sets are MUCH, MUCH faster than lists for "have-I-seen-it" tests
hasher = MD5Hasher("dummysalt")
used_hashes = set()
for i in xrange(MAX_PID_NUM):
    if i % 1000000 == 0:
        print("... " + str(i))
    x = hasher.hash(i)
    if x in used_hashes:
        raise Exception("Collision! i={}".format(i))
    used_hashes.add(x)

# This gets increasingly slow but is certainly fine up to
#     282,000,000
# and we want to test
#   9,999,999,999
# Anyway, other people have done the work:
#   http://crypto.stackexchange.com/questions/15873
# ... and the value is expected to be at least 2^64, whereas an NHS number
# is less than 2^34 -- from math.log(9999999, 2).

"""