import os

from util.client import client

params = {
    "accOrderNo": "",  # 服务单号
    "applicantEndTime": "",  # 申请时间(结束)(格式:yyyy-MM-dd)
    "applicantMobile": "",  # 申请人手机
    "applicantStartTime": "",  # 申请时间(开始)(格式:yyyy-MM-dd)
    "cleanerCardNo": "",  # 服务人员卡号
    "cleanerMobile": "",  # 服务人员手机
    "cleanerName": "",  # 服务人员姓名
    "orderStatus": 0,  # 状态 -1：已取消 0：待接单（默认）1：待服务 2：已完成
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "serviceNo": "",  # 服务码
    "serviceTimeEnd": "",  # 服务结束时间(格式:yyyy-MM-dd)
    "serviceTimeStart": "",  # 服务开始时间(格式:yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_order_page(params=params, headers=headers):
    """
    分页查询订单信息
    /mgmt/acc/order/page

    参数说明:
    - accOrderNo: 服务单号
    - applicantEndTime: 申请时间(结束)(格式:yyyy-MM-dd)
    - applicantMobile: 申请人手机
    - applicantStartTime: 申请时间(开始)(格式:yyyy-MM-dd)
    - cleanerCardNo: 服务人员卡号
    - cleanerMobile: 服务人员手机
    - cleanerName: 服务人员姓名
    - orderStatus: 状态 -1：已取消 0：待接单（默认）1：待服务 2：已完成
    - pageNum: 页数
    - pageSize: 页大小
    - serviceNo: 服务码
    - serviceTimeEnd: 服务结束时间(格式:yyyy-MM-dd)
    - serviceTimeStart: 服务开始时间(格式:yyyy-MM-dd)
    """

    url = "/mgmt/acc/order/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
