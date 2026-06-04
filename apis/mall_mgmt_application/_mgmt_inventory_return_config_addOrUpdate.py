import os

from util.client import client

data = {
    "availableAmount": 0.0,  # 当前可用押货余额
    "controlType": 0,  # 控制类型 1顾客自购单退货 2云商下单退货
    "id": 0,  # 主键id,有id则为调整
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "returnAmount": 0.0,  # 押货余额极限值
    "returnRatio": 0.0,  # 退货额度比例(0.01-1.00)
    "state": 0,  # 记录状态 0:失效 1:生效
    "storeCode": "",  # 服务中心编号不能为空
    "storeType": "",  # 网点类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_addOrUpdate(data=data, headers=headers):
    """
    添加/调整配置额度
    /mgmt/inventory/return/config/addOrUpdate

    参数说明:
    - availableAmount: 当前可用押货余额
    - controlType: 控制类型 1顾客自购单退货 2云商下单退货
    - id: 主键id,有id则为调整
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - returnAmount: 押货余额极限值
    - returnRatio: 退货额度比例(0.01-1.00)
    - state: 记录状态 0:失效 1:生效
    - storeCode: 服务中心编号不能为空
    - storeType: 网点类型
    """

    url = "/mgmt/inventory/return/config/addOrUpdate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
