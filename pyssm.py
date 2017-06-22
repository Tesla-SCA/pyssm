import boto3
from botocore.exceptions import ClientError
from time import time


class SSMParam(object):
    _value = None
    expires_at = float('inf')
    ssm = boto3.client('ssm')

    def __init__(self, name, cache_for_ms=None, raise_if_null=True):
        self.name = name
        self.cache_for_ms = cache_for_ms
        self.raise_if_null = raise_if_null

    @property
    def value(self):
        if self._value is None or self.expires_at <= time() * 1000:
            self._value = self._fetch()
            self._reset_clock()
        return self._value

    def _reset_clock(self):
        self.expires_at = time() * 1000 + self.cache_for_ms if self.cache_for_ms is not None else float('inf')

    def _fetch(self):
        self._value = None
        try:
            return self.ssm.get_parameter(Name=self.name, WithDecryption=True)["Parameter"]["Value"]
        except ClientError as e:
            if self.raise_if_null:
                raise e
            else:
                return None
