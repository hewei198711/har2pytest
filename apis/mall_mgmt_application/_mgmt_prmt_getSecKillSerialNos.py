import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getSecKillSerialNos(headers=headers):
    """
    获取秒杀活动商品: 返回商品编码集合
    /mgmt/prmt/getSecKillSerialNos
    """

    url = "/mgmt/prmt/getSecKillSerialNos"
    with client.get(url=url, headers=headers) as r:
        return r
