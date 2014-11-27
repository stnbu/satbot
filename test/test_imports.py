# -*- coding: utf-8 -*-

import os
import sys
import runpy

this_dir = os.path.dirname(__file__)
this_dir = os.path.abspath(this_dir)

test_packages_path = os.path.join(this_dir, '..')
sys.path.insert(0, test_packages_path)

def test_all():
    """Trivial/silly first pass at writing some tests.
    """
    import satbot
    for name in 'satbot.main', 'satbot.run', 'satbot.calibration':
        runpy.run_module(name)

