import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_words_queryTrafficContrWordsList(headers=headers):
    """
    获取提示语列表
    /mgmt/sys/words/queryTrafficContrWordsList
    """

    url = "/mgmt/sys/words/queryTrafficContrWordsList"
    with client.get(url=url, headers=headers) as r:
        return r
