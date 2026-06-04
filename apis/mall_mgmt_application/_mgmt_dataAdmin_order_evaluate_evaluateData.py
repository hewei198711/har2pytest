import os

from util.client import client

data = {
    "dimension": "",  # 评价维度
    "endDate": "",  # 结束日期（格式：yyyy-MM-dd）
    "level": "",  # 评价等级
    "logisticsTags": [],  # 物流评价标签
    "productTags": [],  # 产品评价标签
    "shoppingExperienceTags": [],  # 购物体验标签
    "startDate": "",  # 开始日期（格式：yyyy-MM-dd）
    "subDimension": "",  # 二级评价维度
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_order_evaluate_evaluateData(data=data, headers=headers):
    """
    评价数据查询
    /mgmt/dataAdmin/order/evaluate/evaluateData

    参数说明:
    - dimension: 评价维度
    - endDate: 结束日期（格式：yyyy-MM-dd）
    - level: 评价等级
    - logisticsTags: 物流评价标签
    - productTags: 产品评价标签
    - shoppingExperienceTags: 购物体验标签
    - startDate: 开始日期（格式：yyyy-MM-dd）
    - subDimension: 二级评价维度
    """

    url = "/mgmt/dataAdmin/order/evaluate/evaluateData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
