# solar-vue-web-backend
# For ES Vue Version of 99M and SPS, Taipower Vue 
REVISION = 'v1.0.8'
#======================================================================================================
from flask import Flask, request, Response, session, g
from flask_login import LoginManager, current_user
import os
import datetime
import traceback
#======================================================================================================
# 通用函式與功能
from app_common import bad_request, conn
#======================================================================================================
# # ======================================================================================================
# # 設定環境變數
# os.environ["web_backend_secret_key"] = "serect"
# os.environ["MONGODB_USERNAME"] = "unicorn"
# os.environ["MONGODB_PASSWORD"] = "uni152"
# os.environ["web_backend_project_name"] = "taipower"
# os.environ["MONGODB_HOSTNAME"] = "140.118.171.31"
# os.environ["MONGODB_PORT"] = "20017"
# os.environ["web_backend_login_enable"] = "false"
# # ======================================================================================================
# ======================================================================================================
# 設定環境變數
os.environ["web_backend_secret_key"] = "serect"
os.environ["MONGODB_USERNAME"] = "admin"
os.environ["MONGODB_PASSWORD"] = "admin"
os.environ["web_backend_project_name"] = "taipower"
os.environ["MONGODB_HOSTNAME"] = "localhost"
os.environ["MONGODB_PORT"] = "27017"
os.environ["web_backend_login_enable"] = "false"
# ======================================================================================================
# Create Flask Instance and Basic Setting
application = Flask(__name__)
#  Compress(application)
#  application.config.from_object(DevConfig)
#-------------------------------------------------------------------------------
UPLOAD_FOLDER = os.path.abspath(os.getenv('static_file_path', '/usr/share/nginx/solar_static/'))
application.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#-------------------------------------------------------------------------------
#為安全考量 token置於環境變數中
if os.getenv('web_backend_secret_key', None) == None:
    print('Secret Key Not Found.')
    print('Check environment variable.')
    exit()
application.secret_key= os.getenv('web_backend_secret_key', None)
#======================================================================================================
# 為了最大化程度共用台電與99M的API
# 採用 Flask Blueprint，將API分為共用、台電專用與99M專用
# More About Flask Blueprint, Take a Look at
# https://flask.palletsprojects.com/en/2.0.x/blueprints/

# 共用的API 
from app_common import application_common, LOGIN_ENABLE
application.register_blueprint(application_common)
#-------------------------------------------------------------------------------
# Include Specify Blueprint Base on 99M or Taipower project
PROJECT_NAME = os.getenv('web_backend_project_name', '99M')
#-------------------------------------------------------------------------------
if PROJECT_NAME == 'taipower':
    # Taipower 專用API
    from app_taipower import application_taipower
    application.register_blueprint(application_taipower)
    # Taipower 派工系統
    from app_taipower_dispatch import application_dispatch
    application.register_blueprint(application_dispatch)
    # App 小工具 API (iOS)
    from app_app_widget import application_app_widget
    application.register_blueprint(application_app_widget)
elif PROJECT_NAME == '99M':
    # 99M 專用API
    from app_99M import application_99M
    application.register_blueprint(application_99M)
    # Taipower 派工系統
    from app_taipower_dispatch import application_dispatch
    application.register_blueprint(application_dispatch)
#======================================================================================================
# Flask的登入設定
from app_common import User, user_list
# Flask LoginManager Setup
login_manger=LoginManager()
login_manger.session_protection='strong'
login_manger.init_app(application)
#-------------------------------------------------------------------------------
# Flask Session Lifetime
@application.before_request
def before_request():
    session.permanent = True
    application.permanent_session_lifetime = datetime.timedelta(minutes=60)
    session.modified = True
    g.user = current_user
#-------------------------------------------------------------------------------
#如果用戶存在則構建一新用戶類對象，並使用user_id當id
@login_manger.user_loader
def load_user(user_id):
    user_info = user_list(user_id)
    if user_info is not None:
        curr_user = User()
        curr_user.id = user_info['user_id']
        
        return curr_user
#-------------------------------------------------------------------------------
#當沒登入時導入login頁面
@login_manger.unauthorized_handler
def unauthorized_handler():
    return bad_request(401, 'Unauthorized.')
#======================================================================================================
# Flask Http Exception Handler
#處理404路徑
@application.errorhandler(404)
def page_not_found(e):
    return bad_request(404, 'Not Found. API not found')
#-------------------------------------------------------------------------------
# Flask Limiter 429
@application.errorhandler(429)
def ratelimit_handler(e):
    return bad_request(429, 'Too many request.')
#-------------------------------------------------------------------------------
# Flask Handle Internal Server Error 500
@application.errorhandler(500)
def internal_server_error(e):
    try:
        conn['pv']['web_server_error_log'].insert_one({
            'time': datetime.datetime.now(),
            'source': request.url,
            'code': e.code,
            'exception': str(e.original_exception),
            'traceback': str(traceback.format_exc())
        })
    except Exception as ee:
        print(ee)
    return bad_request(500, "Internal Server Error. {}".format(e.original_exception))
#-------------------------------------------------------------------------------
@application.route('/APIINFO')
def APIINFO():
    return Response('API Info: {}\nenv_project_name: {}\nenv_login_authentication: {}\nproject_name: {}\nlogin_authentication: {}\nAll Right Reserved'.format(
        REVISION, 
        os.getenv('web_backend_project_name', None),
        os.getenv('web_backend_login_enable', None),
        LOGIN_ENABLE,
        PROJECT_NAME
    ), mimetype='text')
#======================================================================================================
if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5005)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
