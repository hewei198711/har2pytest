import os

from util.client import client

params = {
    "id": "",  # protocolId(必填)
    "protocolId": 0,  # protocolId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_protocol_getProtocol(params=params, headers=headers):
    """
    获取协议
    /mgmt/cms/protocol/getProtocol

    参数说明:
    - id: protocolId(必填)
    - protocolId: protocolId
    """

    url = "/mgmt/cms/protocol/getProtocol"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
