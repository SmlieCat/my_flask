from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


app.debug = True

#对cook进行加密, os.urandom作为随机数发生器
app.secret_key = os.urandom(24)

#根目录
APPS_DIR = os.path.dirname(__file__)
#静态目录
STATIC_DIR = os.path.join(APPS_DIR, 'static')
#数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123qwerty@127.0.0.1:3306/flask_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#用户上传文件目录
app.config['USERS_FILES'] = os.path.join(STATIC_DIR, 'users_files')


#1.配置上传文件保存地址
app.config['UPLOADED_FILE_DEST'] = app.config['USERS_FILES']


#全局限制上传文件大小
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024





#切记循环引用问题
import apps.views