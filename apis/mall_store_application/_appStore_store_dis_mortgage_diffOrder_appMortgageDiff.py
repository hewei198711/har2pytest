import os

from util.client import client

data = {
    "deliverDate": "",  # 发货日期
    "deliverSnList": [],  # 发货单编码
    "diffOtherProofs": [{"fileName": "", "fileUrl": ""}],  # 其他凭证,最多上传3张
    "diffPhotos": [{"fileName": "", "fileUrl": ""}],  # 货损照片,最多上传6张
    "diffProductList": [{"fileName": "", "fileUrl": ""}],  # 货物清单文件,最多上传3张
    "diffProofs": [{"fileName": "", "fileUrl": ""}],  # 货损货差证明文件最多上传3张
    "diffType": 0,  # 货损货差类型类型 1货损 2货差
    "orderRemark": "",  # 备注
    "productList": [
        {"deliverSn": "", "diffNum": 0, "mortgageOrderSn": "", "productCode": "", "productDiffDescId": ""}
    ],  # 货损货差商品列表
    "pushFlag": False,  # 推送标记(前端们不要传这个参数)
    "receiveDate": "",  # 收货日期
    "storeCode": "",  # 服务中心编号, 服务中心无需填写
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_appMortgageDiff(data=data, headers=headers):
    """
    APP下单
    /appStore/store/dis/mortgage/diffOrder/appMortgageDiff

    参数说明:
    - deliverDate: 发货日期
    - deliverSnList: 发货单编码
    - diffOtherProofs: 其他凭证,最多上传3张
    - diffOtherProofs.fileName: 文件名称
    - diffOtherProofs.fileUrl: 文件url
    - diffPhotos: 货损照片,最多上传6张
    - diffPhotos.fileName: 文件名称
    - diffPhotos.fileUrl: 文件url
    - diffProductList: 货物清单文件,最多上传3张
    - diffProductList.fileName: 文件名称
    - diffProductList.fileUrl: 文件url
    - diffProofs: 货损货差证明文件最多上传3张
    - diffProofs.fileName: 文件名称
    - diffProofs.fileUrl: 文件url
    - diffType: 货损货差类型类型 1货损 2货差
    - orderRemark: 备注
    - productList: 货损货差商品列表
    - productList.deliverSn: 对应的发货单号
    - productList.diffNum: 货损/货差数量
    - productList.mortgageOrderSn: 对应的押货单号
    - productList.productCode: 商品编码
    - productList.productDiffDescId: 详情描述id
    - pushFlag: 推送标记(前端们不要传这个参数)
    - receiveDate: 收货日期
    - storeCode: 服务中心编号, 服务中心无需填写
    """

    url = "/appStore/store/dis/mortgage/diffOrder/appMortgageDiff"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
