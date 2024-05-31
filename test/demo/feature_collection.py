#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
@Project :daily-discover-app
@File :Base.py
@Author :jing.wang@shopee.com
@Date :26/11/2021 11:02
"""
from tracking.trackingcase import TrackingCase
import szqa_mobile_ctrl as ctrl
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class FeatureCollectionDemo(TrackingCase):
    cls_name = "Demo case"
    priority = "P0"
    country = "sg"
    url = ""

    def test_case1(self):
        self.impression_event({"alias": "feature_collection", "page_name": "HomePage"}, Direction="UP", find_times=10)
        # self.click_event({"alias": "feature_collection", "page_name": "HomePage"})
        # self.view_event({"alias": "feature_collection", "page_name": "HomePage"},
        #                 {"alias": "See More", "page_name": "HomePage"}, 'DOWN', find_times=10)

# if __name__ == "__main__":
#     FeatureCollectionDemo().test_case1()
# 后续加pagetype
