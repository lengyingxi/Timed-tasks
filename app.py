from flask import Flask, request, render_template, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime

app = Flask(__name__, template_folder="templates")
app.secret_key = "supersecretkey"

USERNAME = "admin"
PASSWORD = "admin"
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx"

tasks = []
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
scheduler.start()

def send_wechat_msg(content):
    # 替换 \n 为企业微信换行符
    content = content.replace("\n", "\n")
    data = {"msgtype": "text", "text": {"content": content}}
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except Exception as e:
        print("发送失败:", e)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="账号或密码错误")
    return render_template("login.html")

@app.route("/home")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    # 按时间排序任务
    sorted_tasks = sorted(tasks, key=lambda x: datetime.datetime.strptime(x["time"], "%Y-%m-%d %H:%M"))
    return render_template("index.html", tasks=sorted_tasks)

@app.route("/add", methods=["POST"])
def add_task():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    time_str = request.form["time"]
    content = request.form["content"]
    try:
        run_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        # 检查时间是否在当前时间之后
        if run_time <= datetime.datetime.now():
            return "提醒时间必须在当前时间之后", 400
        job = scheduler.add_job(send_wechat_msg, "date", run_date=run_time, args=[content])
        tasks.append({"time": time_str, "content": content, "job_id": job.id, "status": "pending"})
        return redirect(url_for("index"))
    except ValueError:
        return "时间格式错误，应为 YYYY-MM-DD HH:MM", 400

@app.route("/test/<job_id>")
def test_task(job_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    for t in tasks:
        if t["job_id"] == job_id:
            send_wechat_msg(f"[测试消息]\n{t['content']}")
            break
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
