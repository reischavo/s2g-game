#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veritabanı Güncelleme Script'i
ChatMessage tablosunu ekler
"""

from app import app, db

with app.app_context():
    db.create_all()
    print('✅ Veritabanı başarıyla güncellendi!')
    print('✅ ChatMessage tablosu eklendi!')
