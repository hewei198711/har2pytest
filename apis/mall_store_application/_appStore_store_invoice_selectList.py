import os

from util.client import client

data = {
    "chargeType": "",  # 费用类型0：配送费,2：服务费
    "from": 0,  # TODO: 添加参数说明
    "memberNo": "",  # 会员编号
    "month": "",  # 月份，如果不传月份，查所有
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "progress": "",  # 发票进度已签收、未签收
    "serviceCentreNo": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_selectList(data=data, headers=headers):
    """
    selectList
    /appStore/store/invoice/selectList

    参数说明:
    - chargeType: 费用类型0：配送费,2：服务费
    - memberNo: 会员编号
    - month: 月份，如果不传月份，查所有
    - pageNum: 页数
    - pageSize: 每页显示数
    - progress: 发票进度已签收、未签收
    - serviceCentreNo: 服务中心编号
    """

    url = "/appStore/store/invoice/selectList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
