#!/usr/bin/env python

"""
crate_anon/linkage/bulk_hash.py

===============================================================================

    Copyright (C) 2015-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

Tool to hash multiple IDs from the command line.

"""

import argparse
import logging
from typing import TextIO

from cardinal_pythonlib.file_io import (
    smart_open,
    writeline_nl,
)
from cardinal_pythonlib.logs import main_only_quicksetup_rootlogger
from cardinal_pythonlib.hash import (
    HashMethods,
    make_hasher,
)

log = logging.getLogger(__name__)


def bulk_hash(input_filename: str,
              output_filename: str,
              hash_method: str,
              key: str,
              keep_id: bool = True):
    """
    Hash lines from one file to another.

    Args:
        input_filename:
            input filename, or "-" for stdin
        output_filename:
            output filename, or "-" for stdin
        hash_method:
            method to use; e.g. ``HMAC_SHA256``
        key:
            secret key for hasher
        keep_id:
            produce CSV with ``id,hash`` pairs, rather than just lines with
            the hashes?
    """
    log.info(f"Reading from: {input_filename}")
    log.info(f"Writing to: {output_filename}")
    log.info(f"Using hash method: {hash_method}")
    log.info(f"keep_id: {keep_id}")
    # log.debug(f"Using key: {key!r}")
    hasher = make_hasher(hash_method=hash_method, key=key)
    with smart_open(input_filename, "rt") as i:  # type: TextIO
        with smart_open(output_filename, "wt") as o:  # type: TextIO
            for line in i:
                line = line.partition('#')[0]  # the part before the first #
                line = line.rstrip()
                line = line.lstrip()
                hashed = hasher.hash(line) if line else ""
                outline = f"{line},{hashed}" if keep_id else hashed
                # log.debug(f"{line!r} -> {hashed!r}")
                writeline_nl(o, outline)


def main() -> None:
    """
    Command-line entry point.
    """
    parser = argparse.ArgumentParser(
        description="Hash IDs in bulk.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--infile', type=str, default="-",
        help="Input file, or '-' for stdin. "
             "Use one line per thing to be hashed. "
             "Lines beginning with the comment marker '#', and blank lines, "
             "are ignored. Lines have whitespace stripped left and right.")
    parser.add_argument(
        '--outfile', type=str, default="-",
        help="Output file, or '-' for stdout. "
             "One line will be written for every input line. "
             "Blank lines will be written for commented or blank input.")
    parser.add_argument(
        '--key', type=str, required=True,
        help="Secret key for hasher")
    parser.add_argument(
        '--method', choices=[HashMethods.HMAC_MD5,
                             HashMethods.HMAC_SHA256,
                             HashMethods.HMAC_SHA512],
        default=HashMethods.HMAC_SHA256,
        help="Hash method")
    parser.add_argument(
        '--keepid', action="store_true",
        help="Produce CSV output with (id,hash) rather than just the hash")
    parser.add_argument(
        '--verbose', '-v', action="store_true",
        help="Be verbose")

    args = parser.parse_args()
    main_only_quicksetup_rootlogger(logging.DEBUG if args.verbose
                                    else logging.INFO)
    bulk_hash(
        input_filename=args.infile,
        output_filename=args.outfile,
        hash_method=args.method,
        key=args.key,
        keep_id=args.keepid,
    )


if __name__ == "__main__":
    main()
