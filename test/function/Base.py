#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
@Project :daily-discover-app
@File :Base.py
@Author :jing.wang@shopee.com
@Date :02/12/2021 09:50
"""
from szqa_framework import TopoAndroid
import szqa_mobile_ctrl as ctrl
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import time


class BaseFunction(TopoAndroid):
    def setup(self):
        TopoAndroid.setup(self)
        self.app = "com.shopee.sg.int"
        self.ctrl = self.topo.mobile
        self.ctrl.launch_app(self.app)
        dev = device()
        poco = AndroidUiautomationPoco(device=dev)
        return poco

    def widget_swipe_to(self, poco):
        """
        重新写widget_swipe_to
        """
        try:
            for i in range(2):
                start_app(self.app)
            # 这里后面需要加一个核查app启动成功的函数
            find_times = 10
            while not poco.exists() and find_times != 0:
                # swipe(Template(r"feature_collection.png"), vector=[0.16203703703703703, 0.4008547008547009])
                swipe((100, 1400), (100, 10), duration=10, steps=10)
                find_times -= 1
            return poco.get_text()
        except Exception as e:
            print("swipe_and_function error:%s" % (e))

    def widget_is_exist(self, poco):
        return poco["value"].exists()

    def widget_click(self, poco):
        poco["value"].click()
