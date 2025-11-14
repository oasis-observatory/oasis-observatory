#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:06:48 2025

@author: mike
"""

def test_generate():
    from oasis.s_generator.core_s import generate_scenario
    scenario = generate_scenario()
    assert scenario is not None
    assert "narrative" in scenario["scenario_content"]