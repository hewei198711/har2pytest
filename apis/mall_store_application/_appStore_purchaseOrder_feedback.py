import os

from util.client import client

data = {
    "comment": "",  # 评论留言
    "feedbacks": [],  # 物流反馈 1送货不及时 2产品破损 3少货 4物流服务态度不好 5发货不及时 6不送货上门 7快递包装简陋 8快递包装破损 9其他 10不配合开箱验货 11分批送货
    "fileUrls": [],  # 图片url
    "orderId": 0,  # 押货单id
    "orderSn": "",  # TODO: 添加参数说明
    "otherComment": "",  # 其他留言
    "storeCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_feedback(data=data, headers=headers):
    """
    添加押货单物流反馈
    /appStore/purchaseOrder/feedback

    参数说明:
    - comment: 评论留言
    - feedbacks: 物流反馈 1送货不及时 2产品破损 3少货 4物流服务态度不好 5发货不及时 6不送货上门 7快递包装简陋 8快递包装破损 9其他 10不配合开箱验货 11分批送货
    - fileUrls: 图片url
    - orderId: 押货单id
    - otherComment: 其他留言
    """

    url = "/appStore/purchaseOrder/feedback"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
