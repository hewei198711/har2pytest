import os

from util.client import client

params = {
    "detailType": "",  # 具体业务类型 1、可识别款项 2.无法识别款项 3、超额流水款项  4、手工录入款项  5、业务申请退款
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_getReasonByType(params=params, headers=headers):
    """
    款项选择与调整原因映射列表
    /mgmt/inventory/remit/getReasonByType

    参数说明:
    - detailType: 具体业务类型 1、可识别款项 2.无法识别款项 3、超额流水款项  4、手工录入款项  5、业务申请退款
    """

    url = "/mgmt/inventory/remit/getReasonByType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
