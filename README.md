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
docker-compose up -d
```
<img width="1613" height="759" alt="image" src="https://github.com/user-attachments/assets/bbd3c4ec-779d-464e-9eeb-6d47d387ab17" />


### 访问并登录
<img width="2232" height="1140" alt="image" src="https://github.com/user-attachments/assets/ae972f6e-924a-4f08-ba81-2cfc4a7a23c6" />

### 添加任务
<img width="2211" height="1143" alt="image" src="https://github.com/user-attachments/assets/437ab263-6232-4c85-80d9-47bfa2e1f496" />

### 提示内容
<img width="678" height="189" alt="image" src="https://github.com/user-attachments/assets/812690cb-e940-41bd-a6d1-0be909201016" />






