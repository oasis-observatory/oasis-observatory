#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oasis/s_generator/cli.py
"""
Created on Sat Nov  8 16:06:18 2025

@author: mike
"""
# oasis/s_generator/cli.py
import typer
from oasis.s_generator.core import generate_scenario
from oasis.logger import log

app = typer.Typer()

@app.command()
def generate(n: int = 1):
    """Generate N ASI scenarios"""
    for i in range(n):
        log.info("generating", i=i+1)
        scenario = generate_scenario()
        if scenario:
            print(f"Generated: {scenario['title']}")

if __name__ == "__main__":
    app()