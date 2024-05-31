# -*- coding: utf-8 -*-
# @Time   : 2021/10/28 2:20 下午
# @Author : yubin.Zhan
# @File   : kibana_service.py
import re
import time
import requests
from enum import Enum


class Kibana(object):
    def __init__(self, **kwargs):
        """

        :param cookie: request cookie with auth info
        :type cookie: str
        :param kibana_version: request kibana_version (will add in request header)
        :type kibana_version: str
        """
        kibana_site = "https://kibana-di-logs-es.idata.shopeemobile.com"
        elastic_search_path = "internal/search/es"
        self.elastic_search_url = "{}/{}".format(kibana_site, elastic_search_path)

        self.cookie = "_oauth2_proxy_mesos=WXViaW4gWmhhbnx5dWJpbi56aGFuQHNob3BlZS5jb218aHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2hiaXp4U19XdXA2SGMtaWtIVF9GM0ZrNzhsa3dVcVUwMUhMZ3NMPXM5Ni1j|1637746247|QJwEo7D7DR5T5D2Wi9_wImRBlNI=; _ga=GA1.1.891205325.1631756434; _ga_7N8T3QXGY7=GS1.1.1638154818.27.1.1638154848.0; sid=Fe26.2**9ef700e7e5d7f1a0d9de01c860304c5e2fb0df3d4cf5c7c63852e82a25509bd6*7jvtsL-YZacZij_T-xMpNw*nbqln3yFqvQ5aBT6cyjSGh3YTEo-2ChL0lSc22ZDIvekZjZn55XpgmEH2iNcdHJ_cG1M9Oww_1Hmj-VuuUVk1baJ16SsCA5Pv5QpbmWMSI6kBqT8XZmpLMzhUZoaNJxajjyVhUJilsNbJYnpVOYB6RFgOOdu8D7BBJT-hwgSVyfHUGJB-5tLNkjiNTh4Gz3ytw-Fnbq9K8X9nlGYVUCn9SbVj6kOU_S-TSwMiyS-djcCM4Q3KTkcULIIyF0Mzf2y9n0d2AR5A88Y_BUEVDqVrg**53d5cc23e8aa23587807906d4a2991e8e51e31efaf80b19d52be825b9e57b9d4*Vbrp3G5y3lVTrBDgkShLFdu4Ie3gBZtJPvqrikPJuTM"
        self.kbn_version = "7.9.2"
        # Configurable Cookie and kbn_version
        if kwargs.get("cookie") is not None:
            self.cookie = kwargs.get("cookie")
        if kwargs.get("kbn_version") is not None:
            self.kbn_version = kwargs.get("kbn_version")

    def query_elastic_search(self, time_range, **filters):
        """ Kibana query api to get tracking record

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
        :return source_list: a list of hit records data
        :rtype list
        """
        # Send post request and get result
        response = requests.request(
            "POST",
            self.elastic_search_url,
            headers={"cookie": self.cookie, "kbn-version": self.kbn_version},
            json=self.convert_elastic_search_body(time_range, KibanaTemplateEnum.request_elastic_search, **filters)
        )
        # sometime can not get result immediately
        if "id" in response.json():
            search_id = response.json()["id"]
            res_json = requests.post(url=self.elastic_search_url,
                                     json={"id": search_id},
                                     headers={"cookie": self.cookie, "kbn-version": self.kbn_version},
                                     ).json()
        else:
            res_json = response.json()
        hits_record = res_json.get("rawResponse").get("hits").get("hits")
        source_list = []
        for hit in hits_record:
            source_list.append(hit.get("_source"))
        return source_list

    @staticmethod
    def convert_elastic_search_body(time_range, template_enum, **filters):
        """Convert filter and time_range in request body

        :param time_range: the time(hour) range you want to filter
        :type time_range: int
        :param template_enum: enum of request template (class KibanaTemplateEnum)
        :type template_enum: KibanaTemplateEnum
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
        :return body: dict of request
        :rtype dict
        """
        if template_enum == KibanaTemplateEnum.request_elastic_search:
            body = KibanaTemplate.request_elastic_search
            body["params"]["body"]["query"] = Query.convert_request(time_range, **filters)
            # body.get("params").get("body").get("query") = Query().convert_request(kwargs)
        else:
            raise ValueError("[TEMPLATE ERROR] Can't find template.")
        return body


class KibanaTemplate(object):
    request_elastic_search = {
        "params": {
            "ignoreThrottled": True,
            "index": "de_qa_tracker_validation_*_env-*",
            "body": {
                "version": True,
                "size": 500,
                "sort": [{
                    "@timestamp": {
                        "order": "desc",
                        "unmapped_type": "boolean"
                    }
                }],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "5m",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": ["*"],
                "script_fields": {},
                "docvalue_fields": [{
                    "field": "@timestamp",
                    "format": "date_time"
                }],
                "_source": {
                    "excludes": []
                },
                "query": {}
            },
            "rest_total_hits_as_int": True,
            "ignore_unavailable": True,
            "ignore_throttled": True,
            "preference": 1635389834067,
            "timeout": "30000ms"
        }
    }


class KibanaTemplateEnum(Enum):
    request_elastic_search = 0


class CheckTypeEnum(Enum):
    check_exist = 0
    check_value = 1


class Query(object):
    # Query Template
    template = {
        "bool": {
            "must": [],
            "filter": [
                {
                    "match_all": {}
                },
                {
                    "range": {
                        "@timestamp": {
                            "gte": "",
                            "lte": "",
                            "format": "strict_date_optional_time"}
                    }
                }
            ],
            "should": [],
            "must_not": []
        }
    }

    # Filter fields list
    # You can add fields here, If there is nothing you need
    fields_list = [
        "country",
        "userid",
        "platform",
        "platform_implementation",
        "model",
        "matched_testcase",
        "_id",
        "_type",
        "os",
        "os_version",
        "page_type",
        "page_section",
        "env",
        "app_version",
        "device_id",
        "event_id",
        "app_id",
        "failed_reason",
        "operation",
        "target_type",
        "timestamp",
        "tags",
        "sequence_id"
    ]

    @classmethod
    def convert_request(cls, time_range, **filters):
        """ Convert Request body return

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
        :return template: dict
        :rtype: dict
        """
        # Convert Filter Fields Dict
        for filter_field in filters:
            # Convert Filter Fields
            if filter_field in cls.fields_list:
                if filter_field == "timestamp":
                    # Convert timestamp
                    cls.template.get("bool").get("filter").append(
                        {"match_phrase": {"@" + filter_field: filters.get(filter_field)}}
                    )
                else:
                    # Convert other fields
                    cls.template.get("bool").get("filter").append(
                        {"match_phrase": {filter_field: filters.get(filter_field)}}
                    )
            else:
                raise ValueError(
                    "[FILTER] Can't find this field (" + filter_field + ") in fields_list.\n"
                    "If you want to use it you can add it to fields_list"
                )

        # Convert Time and Time Format check
        # Calculate Time
        lte_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 3600 * 8))
        gte_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 3600 * (time_range + 8)))
        gte = str(gte_time) + ".500Z"
        lte = str(lte_time) + ".500Z"
        time_pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}[T]\d{2}:\d{2}:\d{2}.\d{3}[Z]$')
        # Starting Time
        if time_pattern.match(gte) is None:
            raise ValueError(
                "Start time format is invalid: \"" + gte + "\"\n""Valid Example: '2021-10-28T22:35:59.475Z'"
            )
        else:
            cls.template.get("bool").get("filter")[1].get("range").get("@timestamp").update(
                {"gte": gte}
            )
        # End Time
        if time_pattern.match(lte) is None:
            raise ValueError(
                "End time format is invalid: \"" + lte + "\"\n""Valid Example: '2021-10-28T22:35:59.475Z'"
            )
        else:
            cls.template.get("bool").get("filter")[1].get("range").get("@timestamp").update(
                {"lte": lte}
            )
        return cls.template


if __name__ == "__main__":
    end_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 3600 * 8))
    start_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 3600 * (8 + 1)))

    hit_record = Kibana().query_elastic_search(1,
                                               country="sg",
                                               page_type="home",
                                               operation="click",
                                               platform="ios_app",
                                               page_section="daily_discover",
                                               env="test"
                                               )
    print(hit_record)
    print(len(hit_record))
