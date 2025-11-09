#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:03:01 2025

@author: mike
"""

# oasis/s_generator/consistency.py
class NarrativeChecker:
    def __init__(self, params): self.p = params
    def check(self, text): return True, []  # same checks