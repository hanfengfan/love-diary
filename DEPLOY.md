# 🚀 恋爱日记网站 - 部署指南

## 前置条件

- Ubuntu 服务器（建议 20.04+），有公网IP
- 域名 `loveforever.mooo.com` 已解析到服务器 IP
- 服务器开放端口：`80`（HTTP）、`443`（HTTPS）

---

## 一、安装 Docker 和 Docker Compose

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sudo sh

# 将当前用户加入 docker 组（免 sudo）
sudo usermod -aG docker $USER

# 重新登录使权限生效
exit
# 重新 SSH 登录后继续

# 验证安装
docker --version
docker compose version
```

## 二、上传代码到服务器

**方式一：Git 拉取（推荐）**
```bash
# 在服务器上
cd ~
git clone <你的仓库地址> love-diary
cd love-diary
```

**方式二：手动上传**
```bash
# 在本地电脑执行（将项目压缩后上传）
scp -r ./test4 用户名@服务器IP:~/love-diary
```

## 三、配置环境变量

```bash
cd ~/love-diary

# 从模板创建配置文件
cp .env.example .env

# 编辑配置
nano .env
```

修改 `.env` 内容：
```
SECRET_KEY=改成一个随机的长字符串
ADMIN_PASSWORD=你的管理员密码
CORS_ORIGINS=https://loveforever.mooo.com
CERTBOT_EMAIL=你的邮箱@example.com
```

> **生成随机密钥：** `openssl rand -hex 32`

## 四、首次部署（含 HTTPS）

```bash
# 1. 构建并启动所有服务（先不启动 certbot）
docker compose up -d --build backend frontend

# 2. 运行 SSL 证书初始化脚本
chmod +x init-letsencrypt.sh
sudo bash init-letsencrypt.sh

# 3. 启动所有服务（含证书自动续期）
docker compose up -d
```

部署完成后访问：**https://loveforever.mooo.com**

> 默认管理员账号：`admin`，密码为 `.env` 中设置的 `ADMIN_PASSWORD`

---

## 五、日常运维命令

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f              # 所有服务
docker compose logs -f backend      # 仅后端
docker compose logs -f frontend     # 仅前端

# 重启服务
docker compose restart

# 更新代码后重新部署
git pull
docker compose up -d --build

# 停止服务
docker compose down

# 停止并删除数据（⚠️ 慎用！会删除所有数据）
docker compose down -v
```

## 六、数据备份

```bash
# 备份上传的照片/视频
docker cp love-diary-backend:/app/uploads ./backup_uploads_$(date +%Y%m%d)

# 备份数据库
docker cp love-diary-backend:/app/instance/database.db ./backup_db_$(date +%Y%m%d).db

# 恢复数据库
docker cp ./backup_db.db love-diary-backend:/app/instance/database.db
docker compose restart backend
```

## 七、常见问题

| 问题 | 解决方案 |
|------|----------|
| 网站打不开 | 检查防火墙：`sudo ufw allow 80 && sudo ufw allow 443` |
| 502 Bad Gateway | 后端未启动：`docker compose logs backend` 查看错误 |
| SSL 证书错误 | 域名是否解析到服务器 IP：`nslookup loveforever.mooo.com` |
| 上传文件失败 | 检查大小限制，Nginx 已配置 100MB |
| 手机访问不了 | 确认防火墙/安全组开放 80 和 443 端口 |
