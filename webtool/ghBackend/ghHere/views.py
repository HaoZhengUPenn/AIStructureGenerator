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

from django.core.mail import EmailMessage
def send_email(request):
    global emailaddress
    msg = EmailMessage(
        subject='Wing Structure Generator | PSL - Your result is ready!',
        body='Hello,\n\nThank you for using Wing Structure Generator from Polyhedral Structures Laboratory, University of Pennsylvania. Your structure has been successfully generated. Please download the data file (.CSV) in the attachment. You can upload it in the "File Manager" panel to restore the result. Have fun!\n\nBest,\nHao Zheng\nPh.D. Candidate at UPenn',
        from_email="359580720@qq.com",  # 也可以从settings中获取
        to=[emailaddress]
    )
    msg.attach_file(r'media/Default/output.csv')
    msg.send(fail_silently=False)
    return HttpResponse('OK')


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        prediction = {}
        prediction['status'] = 'uncompleted'
        
        fem = True
        for param in request.data.values():
            if str(param)[2]!="F":
                fem = False
            global emailaddress
            emailaddress = str(param).split(',')[-1][2:-2]
            print("email to",emailaddress)
            break
        if fem==False:
            with open(r'media/Default/done.txt', "r") as f:
                data = f.readlines()
                if int(data[0].strip('\n'))==0:
                    return Response(prediction)
            with open(r'media/Default/done.txt', 'w') as f:
                f.write('0'+'\n')
        if fem==True:
            with open(r'media/Default/done_FEM.txt', "r") as f:
                data = f.readlines()
                if int(data[0].strip('\n'))==0:
                    return Response(prediction)
            with open(r'media/Default/done_FEM.txt', 'w') as f:
                f.write('0'+'\n')
        
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
        
        if fem==False:
            with open(r'media/Default/input.txt', 'w') as f:
                for param in request.data.values():
                    f.write(str(param)+'\n')
        if fem==True:
            with open(r'media/Default/input_FEM.txt', 'w') as f:
                for param in request.data.values():
                    f.write(str(param)+'\n')
        print('Recorded!!!')
        
        if fem==False:
            try:
                os.remove(r'media/Default/output.csv')
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
                        if fn.endswith(".csv"):
                            fn_stl.append(fn)
                    fn_stl.sort(key=lambda fn:os.path.getmtime(r'media/Default/'+fn))
                    print(fn_stl[-1])
                    shutil.copyfile(r'media/Default/'+ fn_stl[-1], r'media/Default/output.csv')#show
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
                
            send_email(request)
            
        if fem==True:
            with open(r'media/Default/outputfem.txt', 'w') as f:
                f.write('0\n')
            prediction['status'] = 'completed'

        return Response(prediction)