import os
from urllib.parse import urlencode

from util.client import client

data = {
    "picUrlJsonStr": "",  # picUrlJsonStr
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_awardRecord_importBatchAndCommit(data=data, headers=headers):
    """
    获奖记录批量导入/提交
    /mgmt/store/awardRecord/importBatchAndCommit

    参数说明:
    - picUrlJsonStr: picUrlJsonStr
    """

    url = "/mgmt/store/awardRecord/importBatchAndCommit"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
