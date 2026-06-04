import os

from util.client import client

data = {
    "commitEndTime": "",  # 提交结束时间(格式yyyy-MM-dd)
    "commitStartTime": "",  # 提交开始时间(格式yyyy-MM-dd)
    "companyCode": "",  # 所属分公司编号
    "effectEndTime": "",  # 生效结束时间(格式yyyy-MM-dd)
    "effectStartTime": "",  # 生效开始时间(格式yyyy-MM-dd)
    "leaderCardNo": "",  # 负责人卡号
    "loseEffectEndTime": "",  # 失效结束时间(格式yyyy-MM-dd)
    "loseEffectStartTime": "",  # 失效效开始时间(格式yyyy-MM-dd)
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页大小
    "productCode": "",  # 商品编号
    "status": 0,  # 状态 0 待生效 1生效中 2 已失效
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_listDistribution(data=data, headers=headers):
    """
    服务中心分配量列表
    /mgmt/inventory/distribution/listDistribution

    参数说明:
    - commitEndTime: 提交结束时间(格式yyyy-MM-dd)
    - commitStartTime: 提交开始时间(格式yyyy-MM-dd)
    - companyCode: 所属分公司编号
    - effectEndTime: 生效结束时间(格式yyyy-MM-dd)
    - effectStartTime: 生效开始时间(格式yyyy-MM-dd)
    - leaderCardNo: 负责人卡号
    - loseEffectEndTime: 失效结束时间(格式yyyy-MM-dd)
    - loseEffectStartTime: 失效效开始时间(格式yyyy-MM-dd)
    - pageNum: 页码
    - pageSize: 页大小
    - productCode: 商品编号
    - status: 状态 0 待生效 1生效中 2 已失效
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/distribution/listDistribution"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
