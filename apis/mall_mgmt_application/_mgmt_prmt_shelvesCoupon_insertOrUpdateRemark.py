import os

from util.client import client

data = {
    "remark": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_insertOrUpdateRemark(data=data, headers=headers):
    """
    新增或修改活动说明配置
    /mgmt/prmt/shelvesCoupon/insertOrUpdateRemark
    """

    url = "/mgmt/prmt/shelvesCoupon/insertOrUpdateRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
