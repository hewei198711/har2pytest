import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectAssistRecordList(params=params, headers=headers):
    """
    查询分享记录的助力信息
    /mgmt/prmt/share/selectAssistRecordList

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/share/selectAssistRecordList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
