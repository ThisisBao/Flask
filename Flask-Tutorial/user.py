from flask import Flask, redirect, url_for, render_template, request,\
    session, flash, Blueprint

user = Blueprint("user", __name__)
