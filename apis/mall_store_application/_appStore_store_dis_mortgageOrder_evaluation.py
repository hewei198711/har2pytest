import os

from util.client import client

data = {
    "comment": "",  # 评论留言
    "evaluation": 0,  # 物流评价 1非常好 2好 3差 4一般 5非常差
    "feedback": "",  # 物流反馈
    "fileUrls": [],  # 图片url
    "id": 0,  # 物流评价id(更新操作传)
    "orderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_evaluation(data=data, headers=headers):
    """
    添加押货单物流评价
    /appStore/store/dis/mortgageOrder/evaluation

    参数说明:
    - comment: 评论留言
    - evaluation: 物流评价 1非常好 2好 3差 4一般 5非常差
    - feedback: 物流反馈
    - fileUrls: 图片url
    - id: 物流评价id(更新操作传)
    - orderId: 押货单id
    """

    url = "/appStore/store/dis/mortgageOrder/evaluation"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
