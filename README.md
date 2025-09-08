# Timed-tasks
添加任务，设置提醒时间，调用企业微信群机器人的webhook即可接收提醒！！！

<img width="2208" height="1137" alt="image" src="https://github.com/user-attachments/assets/c62f7977-fdbf-4a66-9f65-fe2fbccd6af8" />


## 部署流程

### 设置登录账号密码和群机器人 Webhook

<img width="2232" height="1314" alt="image" src="https://github.com/user-attachments/assets/2c2abadf-cbd3-4883-922d-63666cab55b8" />


### 编译镜像进行运行

```apl
# 构建镜像
docker build -t wechat-scheduler .

# 运行容器
docker-compose up -d
```
<img width="1611" height="762" alt="image" src="https://github.com/user-attachments/assets/c667a3e5-9d04-4ccf-b090-c792e3aba922" />


### 访问并登录
<img width="2229" height="1131" alt="image" src="https://github.com/user-attachments/assets/1a33321d-c5c3-4dfe-8f7b-e617a87e4662" />


### 添加任务
<img width="2202" height="1133" alt="image" src="https://github.com/user-attachments/assets/76b424b7-b0d7-44ca-9e4e-96adb6264e7e" />
<img width="2135" height="380" alt="image" src="https://github.com/user-attachments/assets/e0875a01-38e9-4966-a70f-2bf76a401b82" />


### 提示内容
<img width="1476" height="186" alt="image" src="https://github.com/user-attachments/assets/10e15fb0-4f70-421d-beae-91cec790554c" />







