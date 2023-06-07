"""
Authentication module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime, timedelta
from functools import wraps, reduce
import json

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

auth_basic = HTTPBasicAuth()
auth_token = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(auth_basic, auth_token)
