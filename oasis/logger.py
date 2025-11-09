#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 15:35:04 2025

@author: mike
"""

# oasis/logger.py
import structlog
import logging

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logging.basicConfig(level="INFO")
log = structlog.get_logger()