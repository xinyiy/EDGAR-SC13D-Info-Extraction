#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: yxy
"""

import edgar

# Download filings strating from 1994
edgar.download_index("/Users/yxy/Downloads/secfilings", 1994)