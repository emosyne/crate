#!/usr/bin/env python

"""
crate_anon/nlp_manager/nlp_manager.py

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

"""

from typing import Any, Dict, Generator, Tuple
from unittest import mock, TestCase

from crate_anon.nlp_manager.cloud_request import CloudRequestProcess
from crate_anon.nlp_manager.input_field_config import FN_SRCPKSTR, FN_SRCPKVAL
from crate_anon.nlp_manager.nlp_manager import send_cloud_requests
from crate_anon.nlprp.constants import NlprpKeys as NKeys


class SendCloudRequestsTestCase(TestCase):
    def get_text(self) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        for text, other_values in self.test_text:
            yield text, other_values

    def test_exits_when_no_available_processors(self) -> None:
        self.test_text = [
            ("", {"": None}),
        ]

        crinfo = mock.Mock(get_remote_processors=mock.Mock(return_value=[]))
        global_recnum_in = 123
        ifconfig = mock.Mock()
        cloud_request_factory = mock.Mock()

        cloud_requests, records_left, global_recnum_out = send_cloud_requests(
            cloud_request_factory,
            self.get_text(),
            crinfo,
            ifconfig,
            global_recnum_in
        )

        self.assertEqual(cloud_requests, [])
        self.assertFalse(records_left)
        self.assertEqual(global_recnum_out, global_recnum_in)

    def test_single_text_sent_in_single_request(self) -> None:
        self.test_text = [
            ("A woman, a plan, a canal. Panamowa!", {
                FN_SRCPKVAL: 1,
                FN_SRCPKSTR: "pkstr",
            }),
        ]

        remote_processors = {("name-version", None): mock.Mock()}
        cloud_config = mock.Mock(
            remote_processors=remote_processors,
            limit_before_commit=100,
            max_records_per_request=10,
            max_content_length=50000,
            has_gate_processors=False
        )
        # can't set name attribute in constructor here as it has special meaning
        nlpdef = mock.Mock(
            get_cloud_config_or_raise=mock.Mock(return_value=cloud_config)
        )
        nlpdef.name = ""  # so set it here

        crinfo = mock.Mock(
            get_remote_processors=mock.Mock(return_value=remote_processors),
            cloudcfg=cloud_config
        )
        global_recnum_in = 123
        ifconfig = mock.Mock()

        cloud_request = CloudRequestProcess(
            crinfo=crinfo,
            nlpdef=nlpdef,
        )

        # Unrealistic - we always return the same one
        def cloud_request_factory(crinfo) -> CloudRequestProcess:
            self.assertEqual(cloud_request_factory.call_count, 0)

            cloud_request_factory.call_count += 1

            return cloud_request

        cloud_request_factory.call_count = 0

        with mock.patch.object(
                cloud_request, "send_process_request") as mock_send:
            (cloud_requests,
             records_processed,
             global_recnum_out) = send_cloud_requests(
                cloud_request_factory,
                self.get_text(),
                crinfo,
                ifconfig,
                global_recnum_in
            )

            self.assertEqual(cloud_requests[0], cloud_request)
            self.assertTrue(records_processed)
            self.assertEqual(global_recnum_out, 124)

        mock_send.assert_called_once_with(
            queue=True,
            cookies=None,
            include_text_in_reply=False  # has_gate_processors
        )

        records = cloud_request._request_process[NKeys.ARGS][NKeys.CONTENT]

        self.assertEqual(records[0][NKeys.METADATA][FN_SRCPKVAL], 1)
        self.assertEqual(records[0][NKeys.METADATA][FN_SRCPKSTR], "pkstr")
        self.assertEqual(records[0][NKeys.TEXT],
                         "A woman, a plan, a canal. Panamowa!")

    def test_multiple_text_sent_in_single_request(self) -> None:
        self.test_text = [
            ("A woman, a plan, a canal. Panamowa!", {
                FN_SRCPKVAL: 1,
                FN_SRCPKSTR: "pkstr",
            }),
            ("A dog! A panic in a pagoda.", {
                FN_SRCPKVAL: 2,
                FN_SRCPKSTR: "pkstr",
            }),
            ("Won't lovers revolt now?", {
                FN_SRCPKVAL: 3,
                FN_SRCPKSTR: "pkstr",
            }),
        ]

        remote_processors = {("name-version", None): mock.Mock()}
        cloud_config = mock.Mock(
            remote_processors=remote_processors,
            limit_before_commit=100,
            max_records_per_request=10,
            max_content_length=50000,
            has_gate_processors=False
        )
        # can't set name attribute in constructor here as it has special meaning
        nlpdef = mock.Mock(
            get_cloud_config_or_raise=mock.Mock(return_value=cloud_config)
        )
        nlpdef.name = ""  # so set it here

        crinfo = mock.Mock(
            get_remote_processors=mock.Mock(return_value=remote_processors),
            cloudcfg=cloud_config
        )
        global_recnum_in = 123
        ifconfig = mock.Mock()

        cloud_request = CloudRequestProcess(
            crinfo=crinfo,
            nlpdef=nlpdef,
        )

        # Unrealistic - we always return the same one
        def cloud_request_factory(crinfo) -> CloudRequestProcess:
            self.assertEqual(cloud_request_factory.call_count, 0)

            cloud_request_factory.call_count += 1

            return cloud_request

        cloud_request_factory.call_count = 0

        with mock.patch.object(
                cloud_request, "send_process_request") as mock_send:
            (cloud_requests,
             records_processed,
             global_recnum_out) = send_cloud_requests(
                cloud_request_factory,
                self.get_text(),
                crinfo,
                ifconfig,
                global_recnum_in
            )

            self.assertEqual(cloud_requests[0], cloud_request)
            self.assertTrue(records_processed)
            self.assertEqual(global_recnum_out, 126)

        mock_send.assert_called_once_with(
            queue=True,
            cookies=None,
            include_text_in_reply=False  # has_gate_processors
        )

        records = cloud_request._request_process[NKeys.ARGS][NKeys.CONTENT]

        self.assertEqual(records[0][NKeys.METADATA][FN_SRCPKVAL], 1)
        self.assertEqual(records[1][NKeys.METADATA][FN_SRCPKSTR], "pkstr")
        self.assertEqual(records[2][NKeys.TEXT], "Won't lovers revolt now?")