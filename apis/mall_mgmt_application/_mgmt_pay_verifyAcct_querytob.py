import os

from util.client import client

data = {
    "channelCode": 0,  # 支付渠道
    "companyNo": "",  # 分公司编号
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payDate": "",  # 支付日期
    "status": 0,  # 平账状态
    "storeCode": "",  # 服务中心编号
    "tradeTimeOrder": "",  # 支付完成时间顺序: ASC-正序,DESC-倒序,默认正序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_pay_verifyAcct_querytob(data=data, headers=headers):
    """
    查询对公支付对账结果信息
    /mgmt/pay/verifyAcct/querytob

    参数说明:
    - channelCode: 支付渠道
    - companyNo: 分公司编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - payDate: 支付日期
    - status: 平账状态
    - storeCode: 服务中心编号
    - tradeTimeOrder: 支付完成时间顺序: ASC-正序,DESC-倒序,默认正序
    """

    url = "/mgmt/pay/verifyAcct/querytob"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
