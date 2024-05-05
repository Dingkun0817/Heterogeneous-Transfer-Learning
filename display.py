from flask import Flask, render_template, url_for, request, session
import pandas as pd
import os

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
    datasets = [f'BNCI{code}.zip' for code in ('2014001','2014002','2014004','2015002')]
    if (request.form['source'] not in datasets) or (request.form['target'] not in datasets):
        return {'status':'未识别的数据集，请确认'}  # 数据集无效
    elif '' in request.form.values():
        return {'status':'存在未选择的参数'}
    else:
        session['compose'] = request.form
        return {'status':'OK'}  # 返回有效
    
@app.route('/train', methods=['GET'])
def train():
    if 'username' not in session:
        return login()
    if 'compose' not in session:
        return panel()
    framework=''
    if session['compose']['model'] == 'Ours':
        framework = '图8 我们提出的SOTA方法.png'
    else:
        for file in os.listdir('static/framework/'):
            if session['compose']['model'] in file:
                framework = file
                break
    epoch = session['compose']['epoch']
    return render_template('train.html', framework=framework
                           , loss=list(pd.read_csv(f"data/loss_{epoch}.csv", header=None)[0])
                           , teacher = list(pd.read_csv(f"data/accuracy_{epoch}.csv", header=None, sep='\t')[0]) 
                                        if session['compose']['model']=='Ours' else []
                           , student = list(pd.read_csv(f"data/accuracy_{epoch}.csv", header=None, sep='\t')[1]))

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
    return render_template('result.html')

@app.route('/getTable', methods=['GET', 'POST'])
def table():
    file = ext(session['compose'])
    df = pd.read_excel(f"data/{file}.xlsx")
    df.set_index(df.columns[0], inplace=True)
    return {'code':0, 'msg':'', 'count':0, 'data': [{'head':head.capitalize(), **{index:'%.3f'%df.loc[head, index] for index in [f's{i}' for i in range(9)]+['Average']}, 'Standard deviation': '0.000'} for head in ('accuracy', 'precision', 'recall', 'f1')]} \
        if file in ('LDA', 'LR', 'AdaBoost', 'GDBT', 'XGB') \
        else {'code':0, 'msg':'', 'count':0, 'data': [{'head':head.capitalize(), **{index:'%.3f'%df.loc[head, index] for index in [f's{i}' for i in range(9)]+['Average','Standard deviation']}} for head in ('accuracy', 'precision', 'recall', 'f1')]}

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
    # print('my_dict: ', my_dict)
    return my_dict['model']

# def signal_handler(sig, frame):
#     session.pop('username', None)
#     session.pop('compose', None)
#     print('Flask 服务器已经停止')
#     shutdown_func = request.environ.get('werkzeug.server.shutdown')
#     if shutdown_func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     shutdown_func()

if __name__ == '__main__':
    # signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True, port=8080, threaded=True)# host='0.0.0.0'