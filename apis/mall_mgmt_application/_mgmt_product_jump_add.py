import os

from util.client import client

data = {
    "articles": [
        {"articleTitle": "", "articleUrl": "", "officialAccountName": "", "picUrl": "", "sort": 0}
    ],  # 精选推文集合
    "id": 0,  # 跳转内容配置id
    "noticeContent": "",  # 温馨提示内容
    "noticeZoneId": 0,  # 温馨提示关联专区id
    "serialNo": "",  # 商品编码
    "type": 0,  # 跳转内容类型 1-精选推文 2-温馨提示
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_jump_add(data=data, headers=headers):
    """
    新增
    /mgmt/product/jump/add

    参数说明:
    - articles: 精选推文集合
    - articles.articleTitle: 推文标题
    - articles.articleUrl: 跳转对象链接
    - articles.officialAccountName: 公众号名称
    - articles.picUrl: 展示图片地址
    - articles.sort: 排序
    - id: 跳转内容配置id
    - noticeContent: 温馨提示内容
    - noticeZoneId: 温馨提示关联专区id
    - serialNo: 商品编码
    - type: 跳转内容类型 1-精选推文 2-温馨提示
    """

    url = "/mgmt/product/jump/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
