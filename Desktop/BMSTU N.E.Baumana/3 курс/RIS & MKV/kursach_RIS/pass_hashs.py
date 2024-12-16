import hashlib
from flask import render_template, Flask, request, redirect, url_for, flash, Blueprint, session
from acces import login_required
import os
from database.db_conect import db_config
from database.reqst import select, select_string
from database.sql_provider import SQLprovider
from acces import login_required, group_required


def pass_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def pass_from_db():
    passwords = select(db_config, 'SELECT *  FROM client')
    for i in range(10):
        passew = passwords[i][5]
        i+=1
        print(pass_hash(passew))

pass_from_db()