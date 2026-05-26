import os

from util.client import client

data = {
    "auditStauts": "1",  # 审核状态 1-所有，2-待审核，3-已通过，4-未通过
    "pageNum": 1,  # 页码
    "pageSize": 10,  # 页面大小
    "serialNo": None,  # 商品编码
    "title": None,  # 商品名称
    "timeRange": [None, None],  # TODO: 添加参数说明
    "tagTitle": None,  # 产品标签
    "slogan": None,  # 宣传标语
    "trademarkTitle": None,  # 商标产品名称
    "startTime": "",  # 开始时间时间戳
    "endTime": "",  # 结束时间时间戳
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_product_ctrl_listInfoAudit(data=data, headers=headers):
    """
    待产品审核商品版本列表
    /mgmt/product/ctrl/listInfoAudit

    参数说明:
    - auditStauts: 审核状态 1-所有，2-待审核，3-已通过，4-未通过
    - endTime: 结束时间时间戳
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 商品编码
    - slogan: 宣传标语
    - startTime: 开始时间时间戳
    - tagTitle: 产品标签
    - title: 商品名称
    - trademarkTitle: 商标产品名称
    """

    url = "/mgmt/product/ctrl/listInfoAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
