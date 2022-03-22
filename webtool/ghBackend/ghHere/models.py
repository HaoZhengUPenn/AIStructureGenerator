#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2022/03/20 18:45:10
@Author  :   HUANG Zixun
@Version :   1.0
@Contact :   zixunhuang@outlook.com
@License :   Copyright © 2007 Free Software Foundation, Inc
@Desc    :   None
'''
# here put the import lib
from django.db import models
import random, string

# Create your models here.
def generate_code():
    length = 8
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if GHRequest.objects.filter(code = code).count() == 0:
            break
    return code

def canvasDefault():
    return {
        'x0':  0.1,
        'y0':  0.9,
        'x1':  0.9,
        'y1':  0.2,
        'x2':  0.9,
        'y2':  0.1,
        'x3':  0.4,
        'y3':  0.6,
        'x4':  0.1,
        'y4':  0.8,
    }

def inputDefault():
    return {
        "canvas_points": "0.1,0.9,0.9,0.2,0.9,0.1,0.4,0.6,0.1,0.8",
        "reduce_rate": 0.5,
        "tolerance_of_edge_length": 0.3,
        "length_constraint_maltiplier": 0.5,
        "boundary_constraint_magnitude": 5,
        "perp_steps": 10000,
        "minumum_radius": 1,
        "maximum_radius": 10
    }

class GHRequest(models.Model):
    code = models.CharField(primary_key=True, max_length = 10, default=generate_code)
    gh_num = models.CharField(max_length = 128, null=True)

    input_data = models.JSONField(null=True, default=inputDefault)
    # canvas_points = models.JSONField(null=True, default=canvasDefault)
    # reduce_rate = models.FloatField(null=True, default=0.5)
    # tolerance_of_edge_length = models.FloatField(null=True, default=0.3)
    # length_constraint_maltiplier = models.FloatField(null=True, default=0.5)
    # boundary_constraint_magnitude = models.FloatField(null=True, default=5)
    # perp_steps = models.IntegerField(null=True, default=10000)
    # minumum_radius = models.FloatField(null=True, default=1)
    # maximum_radius = models.FloatField(null=True, default=10)

    txt_input = models.FileField(default = 'Default/input.txt', null = True)
    stl_result = models.FileField(default = 'Default/DFW-V0-3d_file_with_various_height.stl', null = True)
    succeed = models.BooleanField(default = False)

    updated_at = models.DateTimeField(auto_now=True, null=True)


