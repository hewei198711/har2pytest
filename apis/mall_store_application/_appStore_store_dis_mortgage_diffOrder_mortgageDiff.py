import os

from util.client import client

data = {
    "deliverDate": "",  # 发货日期
    "deliverSnList": [],  # 发货单编码
    "diffOtherProofs": [],  # 其他凭证,最多上传3张
    "diffPhotos": [],  # 货损照片,最多上传6张
    "diffProductList": [],  # 货物清单文件,最多上传3张
    "diffProofs": [],  # 货损货差证明文件最多上传3张
    "diffType": 0,  # 货损货差类型类型 1货损 2货差
    "orderRemark": "",  # 备注
    "productList": [],  # 货损货差商品列表
    "pushFlag": False,  # 推送标记(前端们不要传这个参数)
    "receiveDate": "",  # 收货日期
    "storeCode": "",  # 服务中心编号, 服务中心无需填写
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_mortgageDiff(data=data, headers=headers):
    """
    下单
    /appStore/store/dis/mortgage/diffOrder/mortgageDiff

    参数说明:
    - deliverDate: 发货日期
    - deliverSnList: 发货单编码
    - diffOtherProofs: 其他凭证,最多上传3张
    - diffPhotos: 货损照片,最多上传6张
    - diffProductList: 货物清单文件,最多上传3张
    - diffProofs: 货损货差证明文件最多上传3张
    - diffType: 货损货差类型类型 1货损 2货差
    - orderRemark: 备注
    - productList: 货损货差商品列表
    - pushFlag: 推送标记(前端们不要传这个参数)
    - receiveDate: 收货日期
    - storeCode: 服务中心编号, 服务中心无需填写
    """

    url = "/appStore/store/dis/mortgage/diffOrder/mortgageDiff"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
