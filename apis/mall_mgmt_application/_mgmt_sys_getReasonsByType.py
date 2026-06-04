import os

from util.client import client

params = {
    "returnType": "",  # 订单的类型集，1.普通产品购买订单，2.普通产品退货订单，3.普通产品换货订单，4.单位团购订单，5.押货退货单，6.押货换货单
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getReasonsByType(params=params, headers=headers):
    """
    查找退换货层级原因
    /mgmt/sys/getReasonsByType

    参数说明:
    - returnType: 订单的类型集，1.普通产品购买订单，2.普通产品退货订单，3.普通产品换货订单，4.单位团购订单，5.押货退货单，6.押货换货单
    """

    url = "/mgmt/sys/getReasonsByType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
