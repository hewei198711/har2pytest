import os

from util.client import client

params = {
    "auditStauts": 0,  # 审核状态 1-所有，2-待审核，3-已通过，4-未通过
    "endTime": 0,  # 结束时间时间戳
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 商品编码
    "slogan": "",  # 宣传标语
    "startTime": 0,  # 开始时间时间戳
    "tagTitle": "",  # 产品标签
    "title": "",  # 商品名称
    "trademarkTitle": "",  # 商标产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_ctrl_batchExportFile(params=params, headers=headers):
    """
    批量导出审核列表--文件流方式
    /mgmt/product/ctrl/batchExportFile

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

    url = "/mgmt/product/ctrl/batchExportFile"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
