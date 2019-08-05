#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
description: 该视图为测试视图，定义了接口类API的模块与规范
    主要介绍
            日志模块的导入渝使用
            标准输出模块的导入与使用
            捕获异常的通用函数
            字典参数转对象处理
"""
import os
import re

from rest_framework.views import APIView
from views.tasks import add
from resource.common import output
from resource.common.util import DictToObj
from resource.extension.log import logging
from resource.common.catch_exception import catch_exception
from django.shortcuts import render


class Test(APIView):
    """
    测试代码：

    """

    @catch_exception
    def get(self, request, *args, **kwargs):
        params = DictToObj(request.params)
        r = add.delay(4, 12)
        result = r.wait()
        logging.info("ok!")
        if not result:
            return output.ErrorResponse(msg="fail,no result", status=500)
        return output.NormalResponse({'detail': result}, status=200)


class Html(APIView):
    @catch_exception
    def get(self, request, *args, **kwargs):
        medias = os.listdir("static/media")
        imgs = os.listdir("static/media_img")
        result = []
        for one in medias:
            name = one.split(".")[0]
            for i in imgs:
                name_ = i.split(".")[0]
                if name == name_:
                    result.append({"name": one, "path": i, "title": name})
        return render(request, "index.html", {"data": result})


class Vedio(APIView):
    @catch_exception
    def get(self, request, *args, **kwargs):
        vedio_name = self.kwargs.get("vedio_name")
        data = {"vedio_name": vedio_name}
        return render(request, "vedio.html", data)
