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
    # print(type(session['compose']))
    # sss = ext(session['compose'])
    # print('SSS:',sss)
    # return sss
    return render_template('result.html')

@app.route('/getTable', methods=['GET', 'POST'])
def table():
    file = ext(session['compose'])
    df = pd.read_excel(os.path.join('data', file) + '.xlsx')
    df.set_index(df.columns[0], inplace=True)
    return {'code':0, 'msg':'', 'count':0, 'data': [{'head':head.capitalize(), **{index:'%.3f'%df.loc[head, index] for index in [f's{i}' for i in range(9)]+['Average']}, 'Standard deviation': '0.000'} for head in ('accuracy', 'precision', 'recall', 'f1')]} if file in ('LDA', 'LR', 'AdaBoost', 'GDBT', 'XGB') \
        else {'code':0, 'msg':'', 'count':0, 'data': [{'head':head.capitalize(), **{index:'%.3f'%df.loc[head, index] for index in [f's{i}' for i in range(9)]+['Average','Standard deviation']}} for head in ('accuracy', 'precision', 'recall', 'f1')]}
                # [{'head':head, 's0':df.loc['accuracy', 's0'], 's1':df.loc['accuracy', 's1'], 's2':df.loc['accuracy', 's2'], 's3':df.loc['accuracy', 's3'], 's4':df.loc['accuracy', 's4'], 's5':df.loc['accuracy', 's5'], 's6':df.loc['accuracy', 's6'], 's7':df.loc['accuracy', 's7'], 's8':df.loc['accuracy', 's8'], 'Average':df.loc['accuracy', 'Average']} for head in ('Accuracy', 'Precision', 'Recall', 'F1')]}
            # [{'head':'accuracy', 's0':df.loc['accuracy', 's0'], 's1':df.loc['accuracy', 's1'], 's2':df.loc['accuracy', 's2'], 's3':df.loc['accuracy', 's3'], 's4':df.loc['accuracy', 's4'], 's5':df.loc['accuracy', 's5'], 's6':df.loc['accuracy', 's6'], 's7':df.loc['accuracy', 's7'], 's8':df.loc['accuracy', 's8'], 'Average':df.loc['accuracy', 'Average']},
            #  {'head':'precision', 's0':df.loc['precision', 's0'], 's1':df.loc['precision', 's1'], 's2':df.loc['precision', 's2'], 's3':df.loc['precision', 's3'], 's4':df.loc['precision', 's4'], 's5':df.loc['precision', 's5'], 's6':df.loc['precision', 's6'], 's7':df.loc['precision', 's7'], 's8':df.loc['precision', 's8'], 'Average':df.loc['precision', 'Average']},
            #  {'head':'recall', 's0':df.loc['recall', 's0'], 's1':df.loc['recall', 's1'], 's2':df.loc['recall', 's2'], 's3':df.loc['recall', 's3'], 's4':df.loc['recall', 's4'], 's5':df.loc['recall', 's5'], 's6':df.loc['recall', 's6'], 's7':df.loc['recall', 's7'], 's8':df.loc['recall', 's8'], 'Average':df.loc['recall', 'Average']},
            #  {'head':'f1', 's0':df.loc['f1', 's0'], 's1':df.loc['f1', 's1'], 's2':df.loc['f1', 's2'], 's3':df.loc['f1', 's3'], 's4':df.loc['f1', 's4'], 's5':df.loc['accuracy', 's5'], 's6':df.loc['f1', 's6'], 's7':df.loc['f1', 's7'], 's8':df.loc['f1', 's8'], 'Average':df.loc['f1', 'Average']}]}

            #  {'head':'precision', 's0':round(df.loc['precision', 's0'], 3), 's1':round(df.loc['precision', 's1'], 3), 's2':round(df.loc['precision', 's2'], 3), 's3':round(df.loc['precision', 's3'], 3), 's4':round(df.loc['precision', 's4'], 3), 's5':round(df.loc['precision', 's5'], 3), 's6':round(df.loc['precision', 's6'], 3), 's7':round(df.loc['precision', 's7'], 3), 's8':round(df.loc['precision', 's8'], 3), 'Average':round(df.loc['precision', 'Average'], 3), 'Standard deviation':round(df.loc['precision', 'Standard deviation'], 3)},
            #  {'head':'recall', 's0':round(df.loc['recall', 's0'], 3), 's1':round(df.loc['recall', 's1'], 3), 's2':round(df.loc['recall', 's2'], 3), 's3':round(df.loc['recall', 's3'], 3), 's4':round(df.loc['recall', 's4'], 3), 's5':round(df.loc['recall', 's5'], 3), 's6':round(df.loc['recall', 's6'], 3), 's7':round(df.loc['recall', 's7'], 3), 's8':round(df.loc['recall', 's8'], 3), 'Average':round(df.loc['recall', 'Average'], 3), 'Standard deviation':round(df.loc['recall', 'Standard deviation'], 3)},
            #  {'head':'f1', 's0':round(df.loc['f1', 's0'], 3), 's1':round(df.loc['f1', 's1'], 3), 's2':round(df.loc['f1', 's2'], 3), 's3':round(df.loc['f1', 's3'], 3), 's4':round(df.loc['f1', 's4'], 3), 's5':round(df.loc['f1', 's5'], 3), 's6':round(df.loc['f1', 's6'], 3), 's7':round(df.loc['f1', 's7'], 3), 's8':round(df.loc['f1', 's8'], 3), 'Average':round(df.loc['f1', 'Average'], 3), 'Standard deviation':round(df.loc['f1', 'Standard deviation'], 3)}]}


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
    print('my_dict: ', my_dict)
    return my_dict['model']
    # if my_dict['task'] == '脑电帽迁移':
    #     res = '1_'
    # elif my_dict['task'] == '模态迁移':
    #     res = '2_'
    # elif my_dict['task'] == '范式迁移':
    #     res = '3_'
    #
    # res += my_dict['model'] + '_' \
    #     + my_dict['epoch'] + '_' \
    #     + my_dict['source'][0:11] + '_' \
    #     + my_dict['target'][0:11] + '_' \
    #     + my_dict['batchsize'] + '_' \
    #     + my_dict['optimizer'] + '_'
    #
    # if my_dict['ea'] == 'true':
    #     res += 'EA'
    # elif my_dict['ea'] == 'false':
    #     res += 'woEA'

    # res = my_dict['model']
    # print("=====")
    # print(res)

if __name__ == '__main__':
    app.run(debug=True, port=8080, threaded=True)  # host='0.0.0.0'
