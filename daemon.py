import os
import sys
import json
import flask
import hashlib
import platform
from controllers import *
from controllers.api import *
from flask import Flask

xcraft_path = sys.path[0]
app = Flask("xcraft", static_folder=os.path.join(xcraft_path, "static"),
            template_folder=os.path.join(xcraft_path, "templates"))


# 写文件
def write_file(filename, value):
    f = open(filename, 'w')
    f.write(value)
    f.close()


# 保存配置
def save_config(name, config):
    if isinstance(config, dict) is False: return False
    print(' * 正在自动更新配置文件 (Exception:{})'.format(None))
    try:
        json.dump(config, open(os.path.join(xcraft_path, 'config', name + '.json'), 'w'), ensure_ascii=False, indent=4)
        if json.load(open(os.path.join(xcraft_path, 'config', name + '.json'), 'r')) == config: return True
    except Exception as ex:
        print(' * 配置文件已完全损坏且无法写入 (Exception:{})'.format(ex))
        return False
    return False


# 生成标准配置
def make_default_config(name):
    if name == 'web':
        return {'panel_ip': '0.0.0.0',
                'panel_port': '2333',
                'panel_name': 'Xcraft',
                'debug': True,
                'username': 'dhdj',
                'password': 'dhdj_Niubi233',
                'theme_primary': 'mdui-theme-primary-indigo',
                'theme_accent': 'mdui-theme-accent-pink',
                'session_secret_key': hashlib.md5(os.urandom(128)).hexdigest()}
    elif name == 'multicraft':
        return {'multicraft_daemon_ip': '127.0.0.1', 'enable_multicraft': False}
    else:
        return False


# 如果config里没有应该有的key就会给这个key生成默认值
def fix_missing_config(name, config):
    print(' * 检查配置文件中 (Exception:{})'.format(None))
    if isinstance(config, dict) is False: return False
    for _, value in enumerate(make_default_config(name)):
        if value not in config:
            # 可能会导致session_secret_key重置！
            config[value] = make_default_config(name)[value]
    return config


# 读取配置文件
def read_config(name):
    if os.path.exists(os.path.join(xcraft_path, 'config', name + '.json')):
        try:
            config = json.load(open(os.path.join(xcraft_path, 'config', name + '.json'), 'r'))
        except Exception as ex:
            config = make_default_config(name)
            # 配置文件损坏会导致所有配置重置
            print(' * 配置文件无法读取,正在尝试自动修复 (Exception:{})'.format(ex))

        config = fix_missing_config(name, config)
        if isinstance(config, dict) is False: config = make_default_config(name)
    else:
        config = make_default_config(name)

    if isinstance(config, dict) is False: return False
    if save_config(name, config) is False: return False
    return config


# 所谓petch就是page-fetch，引用了pjax的名字~但是并不是pjax
def render_petch(base, view, petch, **kwargs):
    return flask.render_template(template_name_or_list='petch_wrapper.html',
                                 base=base,
                                 view=view,
                                 petch=petch,
                                 **kwargs)


@app.errorhandler(404)
def page_not_found(error):
    # petch = flask.request.args.get('petch', False)
    petch = flask.request.headers.get('X_PJAX', False)
    return render_petch(base='logined.html',
                        view='404.html',
                        petch=petch,
                        page='404',
                        name=config['panel_name'],
                        theme_primary=config['theme_primary'],
                        theme_accent=config['theme_accent'])


# 状态-Xcraft
@app.route('/', methods=['GET'])
def index():
    flask.session['username'] = 'dhdj'
    petch = flask.request.headers.get('X_PJAX', False)
    return render_petch(base='logined.html',
                        view='index.html',
                        petch=petch,
                        page='状态',
                        name=config['panel_name'],
                        theme_primary=config['theme_primary'],
                        theme_accent=config['theme_accent'])


@app.route('/files', methods=['GET'])
def files():
    petch = flask.request.headers.get('X_PJAX', False)
    if 'username' in flask.session:
        return render_petch(base='logined.html',
                            view='files.html',
                            petch=petch,
                            page='文件',
                            name=config['panel_name'],
                            theme_primary=config['theme_primary'],
                            theme_accent=config['theme_accent'])
    else:
        return need_login_controller.activate()


@app.route('/security', methods=['GET'])
def security():
    petch = flask.request.headers.get('X_PJAX', False)
    if 'username' in flask.session:
        return render_petch(base='logined.html',
                            view='security.html',
                            petch=petch,
                            page='安全',
                            name=config['panel_name'],
                            theme_primary=config['theme_primary'],
                            theme_accent=config['theme_accent'])
    else:
        return need_login_controller.activate()


@app.route('/settings', methods=['GET'])
def settings():
    petch = flask.request.headers.get('X_PJAX', False)
    if 'username' in flask.session:
        return render_petch(base='logined.html',
                            view='settings.html',
                            petch=petch,
                            page='设置',
                            name=config['panel_name'],
                            theme_primary=config['theme_primary'],
                            theme_accent=config['theme_accent'])
    else:
        return need_login_controller.activate()


@app.route('/multicraft', methods=['GET'])
def multicraft():
    petch = flask.request.headers.get('X_PJAX', False)
    if 'username' in flask.session:
        return render_petch(base='logined.html',
                            view='multicraft.html',
                            petch=petch,
                            page='Multicraft',
                            name=config['panel_name'],
                            theme_primary=config['theme_primary'],
                            theme_accent=config['theme_accent'])
    else:
        return need_login_controller.activate()


@app.route('/pterodactyl', methods=['GET'])
def pterodactyl():
    petch = flask.request.headers.get('X_PJAX', False)
    if 'username' in flask.session:
        return render_petch(base='logined.html',
                            view='pterodactyl.html',
                            petch=petch,
                            page='翼龙面板',
                            name=config['panel_name'],
                            theme_primary=config['theme_primary'],
                            theme_accent=config['theme_accent'])
    else:
        return need_login_controller.activate()


@app.route('/amadeus', methods=['GET'])
def amadeus():
    petch = flask.request.headers.get('X_PJAX', False)
    if 'username' in flask.session:
        return render_petch(base='logined.html',
                            view='amadeus.html',
                            petch=petch,
                            page='Amadeus',
                            name=config['panel_name'],
                            theme_primary=config['theme_primary'],
                            theme_accent=config['theme_accent'])
    else:
        return need_login_controller.activate()


@app.route('/api/status', methods=['POST', 'GET'])
def status():
    if 'username' in flask.session:
        return status_controller.activate()
    else:
        return need_login_controller.activate()


# 主程序
if __name__ == '__main__':
    config = read_config('web')
    if isinstance(config, dict) is False: exit(1)
    print(' * Running on {}'.format(platform.system()))
    # with app.test_request_context():
    # print(flask.url_for('static', filename='style.css'))
    app.secret_key = config['session_secret_key']
    app.run(host=config['panel_ip'], port=config['panel_port'], debug=config['debug'])
