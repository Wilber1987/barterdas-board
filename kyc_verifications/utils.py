import time
import os
import hashlib
import hmac

import requests

from django.conf import settings


def sign_request(request: requests.Request) -> requests.PreparedRequest:
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    path_url = prepared_request.path_url  # includes encoded query params
    # could be None so we use an empty **byte** string here
    body = b"" if prepared_request.body is None else prepared_request.body
    if type(body) == str:
        body = body.encode("utf-8")
    data_to_sign = (
        str(now).encode("utf-8")
        + method.encode("utf-8")
        + path_url.encode("utf-8")
        + body
    )
    # hmac needs bytes
    signature = hmac.new(
        str(settings.SUMSUB_SECRET_KEY).encode("utf-8"), data_to_sign, digestmod=hashlib.sha256
    )
    prepared_request.headers["X-App-Token"] = str(settings.SUMSUB_APP_TOKEN)
    prepared_request.headers["X-App-Access-Ts"] = str(now)
    prepared_request.headers["X-App-Access-Sig"] = signature.hexdigest()
    return prepared_request
