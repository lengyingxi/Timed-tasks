# Timed-tasks
添加任务，设置提醒时间，调用企业微信群机器人的webhook即可接收提醒！！！

图

## 部署流程

### 设置登录账号密码和群机器人 Webhook

图

### 编译镜像进行运行

```apl
# 构建镜像
docker build -t wechat-scheduler .

# 运行容器
docker run -d -p 5000:5000 --name scheduler wechat-scheduler
```





