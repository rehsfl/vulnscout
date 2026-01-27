#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Database configuration and initialization for VulnScout
#
# Copyright (C) 2024 Savoir-faire Linux, Inc.
# SPDX-License-Identifier: GPL-3.0-only

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
