import unittest
import datetime
from random import randint
from botocore.stub import Stubber
from botocore.exceptions import ClientError
from freezegun import freeze_time
from pyssm import SSMParam


class TestSSMParam(unittest.TestCase):

    def test_value(self):
        self.stub_param("foobar")
        self.add_stub_response("baz")
        self.assertEqual("baz", self.get_stubbed_param_value())

    def test_caching(self):
        ms_to_wait = randint(1, 100000) * 1000
        self.stub_param("foo", cache_for_ms=ms_to_wait)
        initial_time = datetime.datetime.now()
        with freeze_time(initial_time) as frozen_time:
            self.add_stub_response("bar")
            self.assertEqual("bar", self.get_stubbed_param_value())
            self.add_stub_response("fiz")
            self.assertEqual("bar", self.get_stubbed_param_value())
            frozen_time.tick(delta=datetime.timedelta(milliseconds=ms_to_wait-1))
            self.assertEqual("bar", self.get_stubbed_param_value())
            frozen_time.tick(delta=datetime.timedelta(milliseconds=1))
            self.assertEqual("fiz", self.get_stubbed_param_value())
            self.add_stub_response("baz")
            self.assertEqual("fiz", self.get_stubbed_param_value())

    def test_raises_error_when_key_miss(self):
        self.stub_param("foo")
        self.add_stub_error()
        with self.assertRaises(ClientError):
            self.get_stubbed_param_value()

    def test_catch_error(self):
        self.stub_param("foo", raise_if_null=False)
        self.add_stub_error()
        self.assertIsNone(self.get_stubbed_param_value())

    def stub_param(self, name, **kwargs):
        self.param = SSMParam(name, **kwargs)
        self.stubber = Stubber(self.param.ssm)

    def add_stub_response(self, value):
        response = {
            'Parameter': {
                'Name': self.param.name,
                'Type': 'SecureString',
                'Value': value
            }
        }
        self.stubber.add_response('get_parameter', response, self.get_expected_params())

    def add_stub_error(self):
        self.stubber.add_client_error('get_parameter', expected_params=self.get_expected_params())

    def get_stubbed_param_value(self):
        with self.stubber:
            return self.param.value

    def get_expected_params(self):
        return {"Name": self.param.name, "WithDecryption": True}