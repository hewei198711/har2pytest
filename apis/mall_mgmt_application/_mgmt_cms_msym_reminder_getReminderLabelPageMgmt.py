import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 注册手机号
    "name": "",  # 姓名
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "reminderStatus": 0,  # 状态 0:待审核; 1:审核通过 2:审核不通过 3:管理员禁用 不传/其他值:全部
    "storeCode": "",  # 门店编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_msym_reminder_getReminderLabelPageMgmt(data=data, headers=headers):
    """
    获取运营后台店铺温馨提示语审核数据分页
    /mgmt/cms/msym/reminder/getReminderLabelPageMgmt

    参数说明:
    - cardNo: 会员卡号
    - mobile: 注册手机号
    - name: 姓名
    - pageNum: 页码
    - pageSize: 每页页数
    - reminderStatus: 状态 0:待审核; 1:审核通过 2:审核不通过 3:管理员禁用 不传/其他值:全部
    - storeCode: 门店编号
    """

    url = "/mgmt/cms/msym/reminder/getReminderLabelPageMgmt"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
