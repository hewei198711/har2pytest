import os

from util.client import client

data = {
    "fddCustomerId": "",  # 法大大客户编号
    "oaName": "",  # OA工号名称
    "oaNo": "",  # OA工号
    "signType": 0,  # 对账单签署类型：1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_updateStoreContractServiceFeeSettingInfo(data=data, headers=headers):
    """
    更新服务费申请公司签署人信息
    /mgmt/store/contract/updateStoreContractServiceFeeSettingInfo

    参数说明:
    - fddCustomerId: 法大大客户编号
    - oaName: OA工号名称
    - oaNo: OA工号
    - signType: 对账单签署类型：1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
    """

    url = "/mgmt/store/contract/updateStoreContractServiceFeeSettingInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
