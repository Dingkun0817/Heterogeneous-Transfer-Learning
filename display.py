from flask import Flask, render_template, url_for, request, session, redirect
app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXXXXX'
@app.route('/')
def launch():
    return render_template('main.html', username=session.get('username'))

@app.route('/panel')
def panel():
    return render_template('panel.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    if (session.get('username')):
        session.pop('username')
    return render_template('main.html')

@app.route('/login/check', methods=['POST'])
def check():
    if request.form.get('username') == 'ldk' and request.form.get('password') == '1234':
        session['username'] = request.form.get('username')
        return {'success': True}
    else:
        return {'success': False}

# 非空字符串代表跳转
@app.route('/run', methods=['POST'])
def run():
    print(request.form)
    dataset = ('BNCI2014001.zip', 'BNCI2014002.zip', 'BNCI2014005.zip')
    if( (request.form['source'] not in dataset) or (request.form['target'] not in dataset)):
        return ''  # 返回为空串, 假
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
    print(type(session['compose']))
    sss = ext(session['compose'])
    print(sss)
    # return sss
    return render_template('result.html')

@app.route('/getTable', methods=['GET', 'POST'])
def table():
    return {'code':0, 'msg':'', 'count':0, 'data':
            [{'head':'accuracy', 's0':65.667, 's1':55.853}, 
             {'head':'precision', 's0':70.113}]}

def ext (my_dict):
     # 解析
    res = ''
    for i in range (8):
        if (i==0):
            if(my_dict['task'] == '脑电帽迁移'):
                res += '1_'
            if(my_dict['task'] == '模态迁移'):
                res += '2_'
            if(my_dict['task'] == '范式迁移'):
                res += '3_'
        if (i==1):
            res += my_dict['model']
            res += '_'
            print('res', res)

        if (i==2):
            res += my_dict['epoch']
            res += '_'

        if (i==3):
            res += my_dict['source'][0:11]
            res += '_'

        if (i==4):
            res += my_dict['target'][0:11]
            res += '_'

        if (i==5):
            res += my_dict['batchsize']
            res += '_'

        if (i==6):
            res += my_dict['optimizer']
            res += '_'

        if (i==7):
            if (my_dict['ea'] == 'on'):
                res += 'EA'
            else:
                res += 'woEA'
    return res

if __name__ == '__main__':
    app.run(debug=True, port=8080, threaded=True)  # host='0.0.0.0'
    # my_dict = {
    #     'task': '脑电帽迁移',
    #     'model': 'XXX',
    #     'epoch': '50',
    #     'source': 'BNCI2014001.zip',
    #     'target': 'BNCI2014002.zip',
    #     'batchsize': '8',
    #     'optimizer': 'SGD',
    #     'ea': 'on'
    # }
    # ext(my_dict)