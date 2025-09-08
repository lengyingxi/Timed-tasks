from flask import Flask, request, render_template, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
import json
import os
import uuid
import time

app = Flask(__name__, template_folder="templates")
app.secret_key = "supersecretkey"

USERNAME = "admin"
PASSWORD = "admin"
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/xxxxxxxxxxxxxxxxxxxxxxxx"

TASK_FILE = "tasks.json"
tasks = []
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
scheduler.start()

# 登录失败锁定机制
login_attempts = {}  # {username: {"count": 0, "locked_until": timestamp}}

# ------------------- 工具函数 -------------------
def load_tasks():
    global tasks
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                # 重新加载到 scheduler
                for t in tasks:
                    try:
                        run_time = datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M")
                        if run_time > datetime.datetime.now():
                            scheduler.add_job(send_wechat_msg, "date", run_date=run_time, args=[t["content"]], id=t["job_id"])
                    except Exception as e:
                        print("加载任务失败:", e)
        except Exception as e:
            print("任务文件读取失败:", e)

def save_tasks():
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def send_wechat_msg(content):
    data = {"msgtype": "text", "text": {"content": content}}
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except Exception as e:
        print("发送失败:", e)

# ------------------- 路由 -------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 初始化用户尝试记录
        if username not in login_attempts:
            login_attempts[username] = {"count": 0, "locked_until": 0}

        # 检查锁定状态
        if time.time() < login_attempts[username].get("locked_until", 0):
            wait_time = int((login_attempts[username]["locked_until"] - time.time()) // 60) + 1
            error = f"账户已锁定，请 {wait_time} 分钟后再试"
            return render_template("login.html", error=error)

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            login_attempts.pop(username, None)  # 登录成功清除记录
            return redirect(url_for("index"))
        else:
            # 输入错误，计数 +1
            login_attempts[username]["count"] += 1
            if login_attempts[username]["count"] >= 3:
                # 锁定 10 分钟
                login_attempts[username]["locked_until"] = time.time() + 600
                login_attempts[username]["count"] = 0  # 重置计数
                error = "连续输错 3 次，账户已锁定 10 分钟"
            else:
                remaining = 3 - login_attempts[username]["count"]
                error = f"账号或密码错误，还可尝试 {remaining} 次"
    return render_template("login.html", error=error)

@app.route("/home")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html", tasks=tasks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/add", methods=["POST"])
def add_task():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    time_str = request.form["time"]
    content = request.form["content"]
    remark = request.form.get("remark", "")
    try:
        run_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return "时间格式错误，应为 YYYY-MM-DD HH:MM"
    job_id = str(uuid.uuid4())
    scheduler.add_job(send_wechat_msg, "date", run_date=run_time, args=[content], id=job_id)
    new_task = {"time": time_str, "content": content, "remark": remark, "job_id": job_id}
    tasks.append(new_task)
    save_tasks()
    return redirect(url_for("index"))

@app.route("/delete/<job_id>")
def delete_task(job_id):
    global tasks
    tasks = [t for t in tasks if t["job_id"] != job_id]
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass
    save_tasks()
    return redirect(url_for("index"))

@app.route("/edit/<job_id>", methods=["GET", "POST"])
def edit_task(job_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    task = next((t for t in tasks if t["job_id"] == job_id), None)
    if not task:
        return "任务不存在"
    if request.method == "POST":
        time_str = request.form["time"]
        content = request.form["content"]
        remark = request.form.get("remark", "")
        try:
            run_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return "时间格式错误，应为 YYYY-MM-DD HH:MM"
        # 更新任务
        task["time"] = time_str
        task["content"] = content
        task["remark"] = remark
        try:
            scheduler.remove_job(job_id)
        except Exception:
            pass
        scheduler.add_job(send_wechat_msg, "date", run_date=run_time, args=[content], id=job_id)
        save_tasks()
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)

@app.route("/test/<job_id>")
def test_task(job_id):
    for t in tasks:
        if t["job_id"] == job_id:
            send_wechat_msg(f"[测试消息]\n{t['content']}")
            break
    return redirect(url_for("index"))

# ------------------- 启动 -------------------
if __name__ == "__main__":
    load_tasks()
    app.run(host="0.0.0.0", port=5000, debug=True)

