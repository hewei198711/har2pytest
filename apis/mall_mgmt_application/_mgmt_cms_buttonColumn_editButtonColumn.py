import os

from util.client import client

data = {
    "bgColor": "",  # 底部背景色
    "columnName": "",  # 名称
    "icon1Name": "",  # icon1名称
    "icon1Selected": "",  # icon1已选中图标
    "icon1Unselect": "",  # icon1未选中图标
    "icon2Name": "",  # icon2名称
    "icon2Selected": "",  # icon2已选中图标
    "icon2Unselect": "",  # icon2未选中图标
    "icon3Name": "",  # icon3名称
    "icon3Selected": "",  # icon3已选中图标
    "icon3Unselect": "",  # icon3未选中图标
    "icon4Name": "",  # icon4名称
    "icon4Selected": "",  # icon4已选中图标
    "icon4Unselect": "",  # icon4未选中图标
    "icon5Name": "",  # icon5名称
    "icon5Selected": "",  # icon5已选中图标
    "icon5Unselect": "",  # icon5未选中图标
    "iconNameColorSelected": "",  # icon名称已选中颜色
    "iconNameColorUnselect": "",  # icon名称未选中颜色
    "id": 0,  # id(编辑时传入)
    "location": 0,  # 端口：2.APP 3.小程序
    "shelfConfig": 0,  # 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    "shelfOffTime": "",  # 下架时间
    "shelfUpTime": "",  # 上架时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_buttonColumn_editButtonColumn(data=data, headers=headers):
    """
    编辑底部栏配置
    /mgmt/cms/buttonColumn/editButtonColumn

    参数说明:
    - bgColor: 底部背景色
    - columnName: 名称
    - icon1Name: icon1名称
    - icon1Selected: icon1已选中图标
    - icon1Unselect: icon1未选中图标
    - icon2Name: icon2名称
    - icon2Selected: icon2已选中图标
    - icon2Unselect: icon2未选中图标
    - icon3Name: icon3名称
    - icon3Selected: icon3已选中图标
    - icon3Unselect: icon3未选中图标
    - icon4Name: icon4名称
    - icon4Selected: icon4已选中图标
    - icon4Unselect: icon4未选中图标
    - icon5Name: icon5名称
    - icon5Selected: icon5已选中图标
    - icon5Unselect: icon5未选中图标
    - iconNameColorSelected: icon名称已选中颜色
    - iconNameColorUnselect: icon名称未选中颜色
    - id: id(编辑时传入)
    - location: 端口：2.APP 3.小程序
    - shelfConfig: 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    - shelfOffTime: 下架时间
    - shelfUpTime: 上架时间
    """

    url = "/mgmt/cms/buttonColumn/editButtonColumn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
