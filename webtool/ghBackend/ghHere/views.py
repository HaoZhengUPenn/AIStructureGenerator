#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2022/03/21 17:44:11
@Author  :   HUANG Zixun
@Version :   1.0
@Contact :   zixunhuang@outlook.com
@License :   Copyright © 2007 Free Software Foundation, Inc
@Desc    :   None
'''
# here put the import lib
import json
import os

import time, shutil
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (generics, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import GHRequest


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        prediction = {}
        delay = int(self.request.query_params.get("delay", 60*15))
        interval = int(self.request.query_params.get("interval", 15))
        try:
            with transaction.atomic():
                gh_request = GHRequest(
                    input_data = request.data,
                    # canvas_points = request.data.get('canvas_points', None),
                    # reduce_rate = request.data.get('reduce_rate', None),
                    # tolerance_of_edge_length = request.data.get('tolerance_of_edge_length', None),
                    # length_constraint_maltiplier = request.data.get('length_constraint_maltiplier', None),
                    # boundary_constraint_magnitude = request.data.get('boundary_constraint_magnitude', None),
                    # perp_steps = request.data.get('perp_steps', None),
                    # minumum_radius = request.data.get('minumum_radius', None),
                    # maximum_radius = request.data.get('maximum_radius', None)
                )
                gh_request.save()
                code = gh_request.code
                print(code)
                print('Received !!!')
        except Exception as e:
            raise APIException(str(e))

        if not os.path.exists(os.getcwd()+r'/media/'+code):
            os.makedirs(os.getcwd()+r'/media/'+code)
        # print(gh_request.input_data)
        with open(r'media/Default/input.txt', 'w') as f:
            for param in request.data.values():
                f.write(str(param)+'\n')
        print('Recorded!!!')

        prediction['status'] = 'uncompleted'
        try:
            os.remove(r'media/Default/output.stl')
        except:
            pass
        for i in range(0, int(delay/interval)+1):
            print('Round',i)
            try:
                #shutil.copyfile(r'media/AIStructureGenerator_User_EFC_APW_Web_output.stl', r'media/Default/nnnnnnn.stl')#gan
                fn_all = os.listdir(r'media/Default/')
                #stl
                fn_stl = []
                for fn in fn_all:
                    if fn.endswith(".stl"):
                        fn_stl.append(fn)
                fn_stl.sort(key=lambda fn:os.path.getmtime(r'media/Default/'+fn))
                print(fn_stl[-1])
                shutil.copyfile(r'media/Default/'+ fn_stl[-1], r'media/Default/output.stl')#show
                shutil.move(r'media/Default/'+ fn_stl[-1], r'media/'+code+r'/'+ fn_stl[-1])#bake
                gh_request.gh_num = fn_stl[-1].split('.')[0]
                gh_request.stl_result = code+r'/'+ fn_stl[-1]
                gh_request.succeed = True
                gh_request.save(update_fields=['gh_num','stl_result','succeed'])
                prediction['fp'] = code+r'/'+ fn_stl[-1]
                print('Generated !!!')
                #txt
                # fn_txt = []
                # for fn in fn_all:
                #     if fn.endswith(".txt"):
                #         fn_txt.append(fn)
                # fn_txt.sort(key=lambda fn:os.path.getmtime(r'media/Default/'+fn))
                shutil.copyfile(r'media/Default/input.txt', r'media/'+code+r'/input.txt')
                time.sleep(interval)
                
                gh_request.txt_input = code+r'/input.txt'
                gh_request.save(update_fields=['txt_input'])
                #done
                # try:
                #     time.sleep(600)
                #     os.remove(r'media/Default/output.stl')
                # except:
                #     pass

                prediction['status'] = 'completed'
                break
            except:
                pass
            time.sleep(interval)

        return Response(prediction)