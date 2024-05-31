#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
@Project :daily-discover-app
@File :testcase.py
@Author :jing.wang@shopee.com
@Date :06/12/2021 21:03
"""
from .Base import BaseFunction
import time


class FeatureCollection(BaseFunction):
    def test_case1(self):
        poco = self.setup()
        time.sleep(10)
        if self.widget_is_exist({"type": "poco",
                                 "value": poco("android:id/content").child("android.widget.FrameLayout")[1].child(
                                     "android.widget.FrameLayout").child(
                                     "android.widget.ImageView")}):
            self.widget_click(
                {"type": "poco", "value": poco("android:id/content").child("android.widget.FrameLayout")[1].child(
                    "android.widget.FrameLayout").child(
                    "android.widget.ImageView")})
        else:
            self.widget_swipe_to({"type": "poco", "value": poco(text='FEATURED COLLECTIONS')})
            self.widget_is_exist({"type": "poco", "value": poco(text='See More')})
            self.widget_click({"type": "poco", "value": poco(text='See More')})
