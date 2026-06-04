import os

from util.client import client

data = {
    "batchMonth": "",  # 业绩月份YYYYMM
    "idList": [],  # 主键id集合
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_acceptWithdraw(data=data, headers=headers):
    """
    秒返券提现受理接口
    /mgmt/fin/voucher/second/coupon/acceptWithdraw

    参数说明:
    - batchMonth: 业绩月份YYYYMM
    - idList: 主键id集合
    - remark: 备注
    """

    url = "/mgmt/fin/voucher/second/coupon/acceptWithdraw"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
