import os

from util.client import client

data = {
    "deliverDate": "",  # 发货日期
    "deliverySnList": [],  # 发货单编码
    "diffOtherProofs": [{"name": "", "url": ""}],  # 其他凭证,最多上传3张
    "diffPhotos": [{"name": "", "url": ""}],  # 货损照片,最多上传6张
    "diffProductList": [{"name": "", "url": ""}],  # 货物清单文件,最多上传3张
    "diffProofs": [{"name": "", "url": ""}],  # 货损货差证明文件最多上传3张
    "diffType": 0,  # 货损货差类型类型 1货损 2货差
    "orderRemarks": "",  # 备注
    "productList": [
        {
            "deliverySn": "",
            "mortgageOrderSn": "",
            "productCode": "",
            "productDiffDescId": "",
            "productNum": 0,
            "productSecCode": "",
        }
    ],  # 货损货差商品列表
    "pushFlag": False,  # 推送标记(前端们不要传这个参数)
    "receiveDate": "",  # 收货日期
    "storeCode": "",  # 服务中心编号, 服务中心无需填写
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_appOrder(data=data, headers=headers):
    """
    APP新建货损货差
    /appStore/productDiff/appOrder

    参数说明:
    - deliverDate: 发货日期
    - deliverySnList: 发货单编码
    - diffOtherProofs: 其他凭证,最多上传3张
    - diffOtherProofs.name: 文件名称
    - diffOtherProofs.url: 文件url
    - diffPhotos: 货损照片,最多上传6张
    - diffPhotos.name: 文件名称
    - diffPhotos.url: 文件url
    - diffProductList: 货物清单文件,最多上传3张
    - diffProductList.name: 文件名称
    - diffProductList.url: 文件url
    - diffProofs: 货损货差证明文件最多上传3张
    - diffProofs.name: 文件名称
    - diffProofs.url: 文件url
    - diffType: 货损货差类型类型 1货损 2货差
    - orderRemarks: 备注
    - productList: 货损货差商品列表
    - productList.deliverySn: 对应的发货单号
    - productList.mortgageOrderSn: 对应的押货单号
    - productList.productCode: 商品编码
    - productList.productDiffDescId: 详情描述id
    - productList.productNum: 货损/货差数量
    - productList.productSecCode: 商品二级编码
    - pushFlag: 推送标记(前端们不要传这个参数)
    - receiveDate: 收货日期
    - storeCode: 服务中心编号, 服务中心无需填写
    """

    url = "/appStore/productDiff/appOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
