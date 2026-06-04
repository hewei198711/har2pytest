import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_protocol_getAllProtocol(headers=headers):
    """
    获取所有协议
    /mgmt/cms/protocol/getAllProtocol
    """

    url = "/mgmt/cms/protocol/getAllProtocol"
    with client.get(url=url, headers=headers) as r:
        return r
