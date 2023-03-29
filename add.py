from flask import Flask, render_template, request, redirect
import json
import datetime
 
app = Flask(__name__)
 
# 从 messages.json 文件中读取留言数据
def get_messages():
    with open('messages.json', 'r') as f:
        messages = json.load(f)
    return sorted(messages, key=lambda x: x['timestamp'], reverse=True)
 
# 将留言数据写入 messages.json 文件中
def write_message(name, message):
    messages = get_messages()
    messages.append({
        "name": name,
        "message": message,
        "timestamp": str(datetime.datetime.now())
    })
    with open('messages.json', 'w') as f:
        json.dump(messages, f)
 
# 主页，展示留言板页面
@app.route('/', methods=['GET'])
def home():
    messages = get_messages()
    return render_template('index.html.jinja2', messages=messages)
 
# 留言接口，接收 POST 请求
@app.route('/message', methods=['POST'])
def message():
    # 从表单中获取留言数据
    name = request.form['name']
    message = request.form['message']
 
    # 添加留言到数据列表
    write_message(name, message)
 
    # 重定向到主页
    return redirect('/')
 
if __name__ == '__main__':
    app.run()