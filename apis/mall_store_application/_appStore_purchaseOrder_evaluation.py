import os

from util.client import client

data = {
    "comment": "",  # 评论留言
    "evaluation": 0,  # 物流评价 1非常好 2好 3差 4一般 5非常差
    "feedback": {
        "comment": "",
        "feedbacks": [],
        "fileUrls": [],
        "orderId": 0,
        "orderSn": "",
        "otherComment": "",
        "storeCode": "",
    },  # 物流反馈
    "fileUrls": [],  # 图片url
    "id": 0,  # 物流评价id(更新操作传)
    "orderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_evaluation(data=data, headers=headers):
    """
    添加押货单物流评价
    /appStore/purchaseOrder/evaluation

    参数说明:
    - comment: 评论留言
    - evaluation: 物流评价 1非常好 2好 3差 4一般 5非常差
    - feedback: 物流反馈
    - feedback.comment: 评论留言
    - feedback.feedbacks: 物流反馈 1送货不及时 2产品破损 3少货 4物流服务态度不好 5发货不及时 6不送货上门 7快递包装简陋 8快递包装破损 9其他 10不配合开箱验货 11分批送货
    - feedback.fileUrls: 图片url
    - feedback.orderId: 押货单id
    - feedback.otherComment: 其他留言
    - fileUrls: 图片url
    - id: 物流评价id(更新操作传)
    - orderId: 押货单id
    """

    url = "/appStore/purchaseOrder/evaluation"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
