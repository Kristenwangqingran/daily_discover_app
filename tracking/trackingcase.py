#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
@Project :daily-discover-app
@File :testtrackingcase.py
@Author :jing.wang@shopee.com
@Date :15/11/2021 16:51
"""
from szqa_framework import TopoAndroid
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import szqa_mobile_ctrl as mobile
from tracking.retryassert import RetryAssert


class TrackingCase(TopoAndroid):
    """
    这是Tracking的基类，本类应该继承开源的UI/APP自动化框架的用例基础类，复用基础类的load case，run case的能力
    一些每个Tracking case都需要做的事情可以写在这里，比如连接kibana

    所有tests/xxx.py 都应该继承这个基类
    """
    cls_name = ""
    priority = ""
    country = ""
    url = ""

    # 这里是所有TopoAndriod的一个更上层封装
    # def __init__(self):
    #     """
    #     self.ctrl.device是连接的设备，有如下参数
    #     device_id: str
    #     platform: Platform
    #     device_uri: str
    #     os_version: str
    #     window_size: tuple
    #     可以用来写原生代码时使用
    #     """
    #     dev = device()
    #     poco = AndroidUiautomationPoco(device=dev)
    # def __init__(self):
    #     TopoAndroid.__init__(self)

    def setup(self):
        TopoAndroid.setup(self)
        self.ctrl = self.topo.mobile
        self.package_name = "com.shopee.{}.int".format(self.country)
        self.ctrl.launch_app(self.package_name)
        dev = device()
        poco = AndroidUiautomationPoco(device=dev)
        """
        self.ctrl.device是连接的设备，有如下参数
        device_id: str
        platform: Platform
        device_uri: str
        os_version: str
        window_size: tuple
        可以用来写原生代码时使用
        """

    def widget_swipe_to(self, text):
        """
        重新写widget_swipe_to
        """
        ele = self.poco(text=text["alias"])
        try:
            for i in range(2):
                start_app(self.package_name)
            # 这里后面需要加一个核查app启动成功的函数
            find_times = 10
            while not ele.exists() and find_times != 0:
                # swipe(Template(r"feature_collection.png"), vector=[0.16203703703703703, 0.4008547008547009])
                swipe((100, 1400), (100, 10), duration=10, steps=10)
                find_times -= 1
            return ele.get_text()
        except Exception as e:
            print("swipe_and_function error:%s" % (e))

    def click_event(self, weight):
        try:
            self.ctrl.widget_click(weight)
        except Exception as e:
            print(e)

    def impression_event(self, weight, Direction="DOWN", find_times=10):
        """
        impression is for content displayed in a page
        """
        try:
            if Direction == "UP":
                self.ctrl.widget_swipe_to_find(weight, mobile.Direction.UP, find_times)
            elif Direction == "DOWN":
                self.ctrl.widget_swipe_to_find(weight, mobile.Direction.DOWN, find_times)
            elif Direction == "LEFT":
                self.ctrl.widget_swipe_to_find(weight, mobile.Direction.LEFT, find_times)
            else:
                self.ctrl.widget_swipe_to_find(weight, mobile.Direction.RIGHT, find_times)
        except Exception as e:
            print(e)

    def view_event(self, weight1, weight2, Direction="DOWN", find_times=10):
        """
        auto_view & view are for page view, can consider them the same
        """
        try:
            self.ctrl.widget_swipe_to_find(weight1, Direction, find_times)
            self.ctrl.widget_click(weight2)
        except Exception as e:
            print(e)
