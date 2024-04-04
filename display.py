from flask import Flask, render_template, url_for, request, session, redirect
app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXXXXX'
@app.route('/')
def launch():
    return render_template('main.html', username=session.get('username'))

@app.route('/panel')
def panel():
    if 'username' not in session:
        return login()
    return render_template('panel.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('compose', None)
    return render_template('main.html')

@app.route('/login/check', methods=['POST'])
def check():
    if request.form.get('username') == 'ldk' and request.form.get('password') == '1234':
        session['username'] = request.form.get('username')
        return {'success': True}
    else:
        return {'success': False}

@app.route('/run', methods=['POST'])
def run():
    print(request.form)
    dataset = ('BNCI2014001.zip', 'BNCI2014004.zip')
    if (request.form['source'] not in dataset) or (request.form['target'] not in dataset):
        return '未识别的数据集，请确认'  # 数据集无效
    elif '' in request.form.values():
        return '存在未选择的参数'
    else:
        session['compose'] = request.form
        return 'true'  # 返回有效

@app.route('/comparision', methods=['GET'])
def comparision():
    return render_template('comparision.html')
@app.route('/framework', methods=['GET'])
def framework():
    return render_template('framework.html')

@app.route('/result', methods=['GET'])
def result():
    if 'username' not in session:
        return login()
    if 'compose' not in session:
        return panel()
    print(type(session['compose']))
    sss = ext(session['compose'])
    print(sss)
    # return sss
    return render_template('result.html')

@app.route('/getTable', methods=['GET', 'POST'])
def table():
    return {'code':0, 'msg':'', 'count':0, 'data':
            [{'head':'accuracy', 's0':65.667, 's1':55.853,'s2':65.667, 's3':55.853,'s4':65.667, 's5':55.853,'s6':65.667, 's7':55.853,'s8':65.667, 'Average':55.853,'Standard deviation':1.224},
             {'head':'accuracy', 's0':65.667, 's1':55.853,'s2':65.667, 's3':55.853,'s4':65.667, 's5':55.853,'s6':65.667, 's7':55.853,'s8':65.667, 'Average':55.853,'Standard deviation':1.224},
             {'head':'accuracy', 's0':65.667, 's1':55.853,'s2':65.667, 's3':55.853,'s4':65.667, 's5':55.853,'s6':65.667, 's7':55.853,'s8':65.667, 'Average':55.853,'Standard deviation':1.224},
             {'head':'accuracy', 's0':65.667, 's1':55.853,'s2':65.667, 's3':55.853,'s4':65.667, 's5':55.853,'s6':65.667, 's7':55.853,'s8':65.667, 'Average':55.853,'Standard deviation':1.224}]}

'''
解析
my_dict = {
    'task': '脑电帽迁移',
    'model': 'XXX',
    'epoch': '50',
    'source': 'BNCI2014001.zip',
    'target': 'BNCI2014002.zip',
    'batchsize': '8',
    'optimizer': 'SGD',
    'ea': 'true'
}
ext(my_dict)
'''
def ext(my_dict):
    print(my_dict)
    if my_dict['task'] == '脑电帽迁移':
        res = '1_'
    elif my_dict['task'] == '模态迁移':
        res = '2_'
    elif my_dict['task'] == '范式迁移':
        res = '3_'

    res += my_dict['model'] + '_' \
        + my_dict['epoch'] + '_' \
        + my_dict['source'][0:11] + '_' \
        + my_dict['target'][0:11] + '_' \
        + my_dict['batchsize'] + '_' \
        + my_dict['optimizer'] + '_'
    
    if my_dict['ea'] == 'true':
        res += 'EA'
    elif my_dict['ea'] == 'false':
        res += 'woEA'
    
    return res

if __name__ == '__main__':
    app.run(debug=True, port=8080, threaded=True)  # host='0.0.0.0'
