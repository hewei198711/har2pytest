import os

from util.client import client

data = {
    "idList": [],  # 主键id集合
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_handleDiffRemark(data=data, headers=headers):
    """
    秒返券调差修改备注接口
    /mgmt/fin/voucher/second/coupon/handleDiffRemark

    参数说明:
    - idList: 主键id集合
    - remark: 备注
    """

    url = "/mgmt/fin/voucher/second/coupon/handleDiffRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
