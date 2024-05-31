#!/usr/bin/env python
# encoding: utf-8
# created by richie zhang, 2021/11/15 18:16:51

from tracking.kibana import Kibana
import datetime
import time
import json


class RetryAssert(object):
    """
    这是动态断言的方法类，提供两种检查的方法
    send - 检查Tracking data是否从Web/APP发出成功
    kibana - 检查Tracking data是否在kibana上报成功
    """
    def __init__(self, time_range, **filters):
        """Init to Set time range and filter

        :param time_range: the time(hour) range you want to filter
        :type time_range: int
        :param country: (optional) the country/region you want to filter
        :type country: string
        :param env: (optional) the service/app env you want to filter
        :type env: string
        :param page_type: (optional) the service/app env you want to filter
        :type page_type: string
        :param userid: (optional) the userid you want to filter
        :type userid: string
        :param platform: (optional) the platform you want to filter
        :type platform: string
        :param page_section: (optional) the page_section you want to filter
        :type page_section: string
        :param app_version: (optional) the app_version you want to filter
        :type app_version: string
        :param target_type: (optional) the target_type you want to filter
        :type target_type: string
        :param event_id: (optional) the event_id you want to filter
        :type event_id: string
        :param failed_reason: (optional) the failed_reason you want to filter
        :type failed_reason: string
        :param device_id: (optional) the device_id you want to filter
        :type device_id: string
        :param operation: (optional) the operation you want to filter
        :type operation: string
        :param platform_implementation: (optional) the platform_implementation you want to filter
        :type platform_implementation: string
        :param model: (optional) the model you want to filter
        :type model: string
        :param matched_testcase: (optional) the matched_testcase you want to filter
        :type matched_testcase: string
        :param _id: (optional) the _id you want to filter
        :type _id: string
        :param _type: (optional) the _type you want to filter
        :type _type: string
        :param os: (optional) the os you want to filter
        :type os: string
        :param tags: (optional) the tags you want to filter
        :type tags: string
        :param sequence_id: (optional) the model you want to filter
        :type sequence_id: string
        :param timestamp: (optional) the model you want to filter
        :type timestamp: string
        :param app_id: (optional) the model you want to filter
        :type app_id: string
        :param os_version: (optional) the model you want to filter
        :type os_version: string
        """
        self.time_range = time_range
        self.filters = filters

    @staticmethod
    def send(retry_times=30, interval=1, *args, **tracking_identifier):
        """

        :param retry_times:
        :param interval:
        :param args:
        :param tracking_identifier:
        :return:
        """
        print("send check succeed.")
        pass

    def kibana(self, trigger_time, *fields_list, fuzzy=False, retry_times=5, interval=60, **fields_dict):
        """Try search tracking record and check data

        :param trigger_time: the time you do the operation which can send tracking data
        :type trigger_time: string
        :param fuzzy: is open fuzzy check model or not(Default is False)
        :type fuzzy: bool
        :param retry_times: retry time when you assert fail
        :type retry_times: int
        :param interval: interval time
        :type interval: int
        :param fields_list: a list of fields you want to check
        :param fields_dict: a dict of fields-value you want to check
        :rtype bool
        """
        while retry_times > 0:
            # Log
            tracker_res = Assert(self.time_range, **self.filters).check_data(trigger_time, fuzzy, *fields_list, **fields_dict)
            if tracker_res is True:
                # Log
                print("kibana check succeed.")
                return True
            time.sleep(interval)
            retry_times -= 1
        # Log
        return False


class Assert(object):
    def __init__(self, time_range, **filters):
        """
        :param time_range: The time range you want to query
        :type time_range: int
        :param country: (optional)
        :type country: string
        :param env: (optional)
        :type env: string
        :param page_type: (optional)
        :type page_type: string
        :param page_section: (optional)
        :type page_section: string
        :param operation: (optional)
        :type operation: string
        """
        self.time_range = time_range
        self.filters = filters

    def check_data(self, trigger_time: str, *fields_list, fuzzy=False, **fields_dict):
        """ Check the fields you want to ensure in tracking data

        :param trigger_time: the time you do the operation which can send tracking data
        :type trigger_time: string
        :param fuzzy: is open fuzzy check model or not(Default is False)
        :type fuzzy: bool
        :param fields_list: list of fields you want check whether the field exists
        :param fields_dict: dict of fields-value you want check whether the field and value is same
        :rtype: bool
        """
        # Get Record
        # Set Filter and Range
        hit_record = Kibana(**self.filters).query_elastic_search(self.time_range, **self.filters)
        # filter by trigger time
        hit_record = Assert.trigger_time_filter(trigger_time, hit_record)
        if len(hit_record) == 0:
            return False
        # Checking
        hit_flag = 0
        fields_num = len(fields_list) + len(fields_dict)
        for hit in hit_record:
            hit_data = hit["data"].replace("=>", ":")
            data_dict = json.loads(hit_data)
            # check whether the field and value is same
            for t_field in fields_list:
                if t_field in data_dict:
                    hit_flag += 1
                    continue
                elif "viewed_objects" in data_dict:
                    if t_field in data_dict["viewed_objects"][0]:
                        hit += 1
            # check whether the field exists
            for t_field in fields_dict:
                if t_field in data_dict:
                    if data_dict.get(t_field) == fields_dict.get(t_field):
                        hit_flag += 1
                        continue
                elif "viewed_objects" in data_dict:
                    viewed_objects = data_dict["viewed_objects"][0]
                    if t_field in viewed_objects:
                        if data_dict.get(t_field) == viewed_objects.get(t_field):
                            hit_flag += 1
                            continue
            if fuzzy is True:
                if hit_flag == fields_num:
                    return True
                else:
                    hit_flag = 0
            else:
                if hit_flag % fields_num != 0:
                    return False
        if fuzzy is True:
            return False
        else:
            return True

    @staticmethod
    def trigger_time_filter(trigger_time, hit_records):
        """Filter hit records by trigger time

        :param trigger_time: the time you do the operation which can send tracking data
        :type trigger_time: string
        :param hit_records: the list of hit record you query from kibana
        :type hit_records: list
        :return trigger_record
        :rtype list
        """
        diff_range = 60.0
        format_time = datetime.datetime.strptime(trigger_time, '%Y-%m-%dT%H:%M:%S')
        trigger_record = []
        for hit in hit_records:
            h_time = datetime.datetime.strptime(hit.get("@timestamp").rsplit(".")[0], "%Y-%m-%dT%H:%M:%S")
            time_diff = format_time - h_time
            if time_diff.total_seconds() <= diff_range or time_diff.total_seconds() >= -diff_range:
                trigger_record.append(hit)
        return trigger_record


# Demo
if __name__ == "__main__":
    t_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
    res = Assert(
        1,
        country="sg",
        env="test",
        page_section="daily_discover",
        operation="click",
        platform="ios_app"
    ).check_data("2021-12-01T09:00:31", "layout_id", "location", fuzzy=True, is_mall=False, shopid=600219299)
    print(res)
