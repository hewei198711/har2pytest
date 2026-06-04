import os

from util.client import client

params = {
    "remitType": "",  # 具体银行流水类型  全部则不传 1、银行流水款项映射 2.手工录入银行流水款项映射
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_getSourceTypeByRemitType(params=params, headers=headers):
    """
    按银行流水类型获取款项映射列表
    /mgmt/inventory/remit/getSourceTypeByRemitType

    参数说明:
    - remitType: 具体银行流水类型  全部则不传 1、银行流水款项映射 2.手工录入银行流水款项映射
    """

    url = "/mgmt/inventory/remit/getSourceTypeByRemitType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
