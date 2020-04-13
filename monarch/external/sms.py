from urllib.parse import urljoin

import requests

from monarch import config

from monarch.exc.codes import (
    BIZ_CODE_OK,
    BIZ_REMOTE_SERIALIZE_NOT_VALID,
    BIZ_REMOTE_SERVICE_NOT_VALID,
    BIZ_REMOTE_DATA_NOT_VALID,
    BIZ_REMOTE_SERVICE_TIMEOUT,
)

from monarch.exc.consts import REQUESTS_TIMEOUT
from monarch.utils import logger


class SmsService(object):
    def __init__(self):
        self.base_url = config.SMS_BASE_URL
        self.s = self._requests()
        self.url = None

    @staticmethod
    def _requests():
        s = requests.session()
        return s

    def deal_response(self, response):
        try:
            if response and response.status_code == 200:
                resp = response.json()
                if resp:
                    return BIZ_CODE_OK, resp
                return BIZ_REMOTE_SERIALIZE_NOT_VALID, {}
            else:
                logger.info(
                    "远端服务器返回错误:{} {} {}".format(
                        response.status_code, self.url, str(response.content)
                    )
                )
                return BIZ_REMOTE_SERVICE_NOT_VALID, {}
        except Exception as err:
            logger.info("远端服务器返回数据无法解析:{} {}".format(str(response.content), err))
            return BIZ_REMOTE_DATA_NOT_VALID, {}

    def send_message(self, data, sign):
        url = urljoin(self.base_url, "/uips/insurance/sendmessage?sign=")
        headers = {"Content-Type": "text/plain"}

        try:
            response = self._requests().post(
                url + sign, headers=headers, data=data, timeout=REQUESTS_TIMEOUT
            )
            logger.info(
                "url: {}, data: {}, response: {}".format(
                    self.url, data, response.content
                )
            )
        except Exception as err:
            logger.info("url: {}, data: {}, err: {}".format(self.url, data, err))
            return BIZ_REMOTE_SERVICE_TIMEOUT, {}
        return self.deal_response(response)


sms_service = SmsService()
