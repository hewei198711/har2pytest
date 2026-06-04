import os

from util.client import client

data = {
    "endTime": "",  # 结束时间
    "mobile": "",  # 手机号
    "pageNumber": 0,  # 第几页,默认值为1
    "pageSize": 0,  # 每页数据量,默认值为10
    "province": "",  # 省份
    "sn": "",  # 签约卡号
    "startTime": "",  # 开始时间
    "username": "",  # 姓名/昵称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_exportListKosCourseReportDataByPage(data=data, headers=headers):
    """
    导出kos签约数据列表
    /mgmt/cms/kos/exportListKosCourseReportDataByPage

    参数说明:
    - endTime: 结束时间
    - mobile: 手机号
    - pageNumber: 第几页,默认值为1
    - pageSize: 每页数据量,默认值为10
    - province: 省份
    - sn: 签约卡号
    - startTime: 开始时间
    - username: 姓名/昵称
    """

    url = "/mgmt/cms/kos/exportListKosCourseReportDataByPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
