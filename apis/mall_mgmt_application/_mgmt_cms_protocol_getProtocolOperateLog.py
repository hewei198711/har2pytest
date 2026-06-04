import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_protocol_getProtocolOperateLog(headers=headers):
    """
    获取协议操作日志
    /mgmt/cms/protocol/getProtocolOperateLog
    """

    url = "/mgmt/cms/protocol/getProtocolOperateLog"
    with client.post(url=url, headers=headers) as r:
        return r
