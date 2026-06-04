import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 注册手机号
    "name": "",  # 姓名
    "operator": "",  # 操作人
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_msym_reminder_exportOperateLogPage(params=params, headers=headers):
    """
    导出运营后台店铺温馨提示语操作记录
    /mgmt/cms/msym/reminder/exportOperateLogPage

    参数说明:
    - cardNo: 会员卡号
    - mobile: 注册手机号
    - name: 姓名
    - operator: 操作人
    - storeCode: 服务中心编号
    """

    url = "/mgmt/cms/msym/reminder/exportOperateLogPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
