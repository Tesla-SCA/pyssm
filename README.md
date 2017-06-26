[![CircleCI](https://circleci.com/gh/Tesla-SCA/pyssm.svg?style=svg&circle-token=1d7309a30df178aeeffc39c581f3b261bdfd8dd8)](https://circleci.com/gh/Tesla-SCA/pyssm)
# pyssm
Provides a simple wrapper for getting, working with, and refreshing ssm_params. Does not allow explicit setting of AWS credentials so you need to set them in the environment (any of [options 3-8 in the docs](https://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials) will work).

Basic usage:
```python
from pyssm import SSMParam

secret = SSMParam("path.to.ssm.param")
print(secret.value)
> "SuperSecretValue"
```

With TTL:
```python
>>> secret = SSMParam("path.to.ssm.param.that.might.change", cache_for_ms=60000) #60 seconds
>>> print(secret.value)
"SuperSecretValue"
# ssm param changes after 10 seconds but cache has not expired
>>> print(secret.value)
"SuperSecretValue"
# wait for 51 more seconds for cache to expire
>>> print(secret.value)
"NewSuperSecretValue"
```

Return None if param does not exist instead of raising Boto3 ClientError:
```python
>>> secret = SSMParam("snoring.guys.bed", raise_if_null=false)
>>> print(secret.value)
None
```

Return a default value (if default is anything besides None, this will also prevent Boto3 errors):
```python
>>> secret = SSMParam("snoring.guys.bed", default="Charlie's Desk")
>>> print(secret.value)
"Charlie's desk"
```
