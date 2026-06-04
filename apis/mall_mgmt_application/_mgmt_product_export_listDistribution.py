import os

from util.client import client

data = {
    "companyCode": "",  # 所属分公司编号
    "effectTimeEnd": "",  # 生效时间开始
    "effectTimeStart": "",  # 生效时间开始
    "endTime": "",  # 提交时间结束
    "leaderCardNo": "",  # 负责人卡号
    "leaderName": "",  # 店负责人姓名
    "loseEffectTimeEnd": "",  # 失效时间结束
    "loseEffectTimeStart": "",  # 失效时间开始
    "name": "",  # 服务中心名称
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 商品编码
    "startTime": "",  # 提交时间开始
    "status": 0,  # 状态 0 待生效 1生效中 2 已失效;为空查全部
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_export_listDistribution(data=data, headers=headers):
    """
    产品管理-销售分配量导出
    /mgmt/product/export/listDistribution

    参数说明:
    - companyCode: 所属分公司编号
    - effectTimeEnd: 生效时间开始
    - effectTimeStart: 生效时间开始
    - endTime: 提交时间结束
    - leaderCardNo: 负责人卡号
    - leaderName: 店负责人姓名
    - loseEffectTimeEnd: 失效时间结束
    - loseEffectTimeStart: 失效时间开始
    - name: 服务中心名称
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 商品编码
    - startTime: 提交时间开始
    - status: 状态 0 待生效 1生效中 2 已失效;为空查全部
    - storeCode: 服务中心编号
    """

    url = "/mgmt/product/export/listDistribution"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
