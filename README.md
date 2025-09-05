# Timed-tasks
添加任务，设置提醒时间，调用企业微信群机器人的webhook即可接收提醒！！！

<img width="2205" height="948" alt="image" src="https://github.com/user-attachments/assets/ee72c679-0081-4b45-b2c8-714e0570857e" />


## 部署流程

### 设置登录账号密码和群机器人 Webhook

<img width="1587" height="606" alt="image" src="https://github.com/user-attachments/assets/a404e679-f574-4058-ba52-de3f688555b6" />


### 编译镜像进行运行

```apl
# 构建镜像
docker build -t wechat-scheduler .

# 运行容器
docker run -d -p 5000:5000 --name scheduler wechat-scheduler
```
<img width="1608" height="528" alt="image" src="https://github.com/user-attachments/assets/bedd3756-94fe-4cc2-adb1-164aa0ac1950" />

### 访问
<img width="2229" height="1113" alt="image" src="https://github.com/user-attachments/assets/ed156f55-f913-4193-b1aa-5d98a2e6ff4d" />





