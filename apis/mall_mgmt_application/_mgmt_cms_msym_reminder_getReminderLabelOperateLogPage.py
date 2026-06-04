import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 注册手机号
    "name": "",  # 姓名
    "operator": "",  # 操作人
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "storeCode": "",  # 门店编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_msym_reminder_getReminderLabelOperateLogPage(data=data, headers=headers):
    """
    获取运营后台店铺温馨提示语操作记录分页
    /mgmt/cms/msym/reminder/getReminderLabelOperateLogPage

    参数说明:
    - cardNo: 会员卡号
    - mobile: 注册手机号
    - name: 姓名
    - operator: 操作人
    - pageNum: 页码
    - pageSize: 每页页数
    - storeCode: 门店编号
    """

    url = "/mgmt/cms/msym/reminder/getReminderLabelOperateLogPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
