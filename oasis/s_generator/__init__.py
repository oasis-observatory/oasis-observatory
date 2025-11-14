#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:13:54 2025

@author: mike
"""

# oasis/s_generator/__init__.py
from .core_s import generate_scenario
from .params import sample_parameters
from oasis.s_generator.abbreviator import abbreviate
from .timeline import dynamic_timeline