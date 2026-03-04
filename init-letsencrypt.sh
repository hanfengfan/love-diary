#!/bin/bash
# ==========================================
# Let's Encrypt SSL 证书初始化脚本
# 用法: sudo bash init-letsencrypt.sh
# ==========================================

set -e

DOMAIN="loveforever.mooo.com"

# 从 .env 文件读取邮箱
if [ -f .env ]; then
    EMAIL=$(grep CERTBOT_EMAIL .env | cut -d '=' -f2)
fi
EMAIL=${EMAIL:-"your-email@example.com"}

echo "======================================"
echo "  初始化 Let's Encrypt SSL 证书"
echo "  域名: $DOMAIN"
echo "  邮箱: $EMAIL"
echo "======================================"

# 1. 创建临时的自签名证书（让 Nginx 能先启动起来）
echo ">>> 创建临时证书..."
mkdir -p ./certbot/conf/live/$DOMAIN
docker compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
    -keyout '/etc/letsencrypt/live/$DOMAIN/privkey.pem' \
    -out '/etc/letsencrypt/live/$DOMAIN/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo ""

# 2. 启动 Nginx
echo ">>> 启动 Nginx..."
docker compose up -d frontend
echo ""

# 3. 等待 Nginx 就绪
echo ">>> 等待 Nginx 启动..."
sleep 5

# 4. 删除临时证书
echo ">>> 删除临时证书..."
docker compose run --rm --entrypoint "\
  rm -rf /etc/letsencrypt/live/$DOMAIN && \
  rm -rf /etc/letsencrypt/archive/$DOMAIN && \
  rm -rf /etc/letsencrypt/renewal/$DOMAIN.conf" certbot
echo ""

# 5. 申请正式的 Let's Encrypt 证书
echo ">>> 申请 Let's Encrypt 证书..."
docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --email $EMAIL \
    -d $DOMAIN \
    --rsa-key-size 4096 \
    --agree-tos \
    --no-eff-email \
    --force-renewal" certbot
echo ""

# 6. 重新加载 Nginx 以使用正式证书
echo ">>> 重新加载 Nginx..."
docker compose exec frontend nginx -s reload

echo ""
echo "======================================"
echo "  ✅ SSL 证书配置完成！"
echo "  现在可以通过 https://$DOMAIN 访问"
echo "======================================"
