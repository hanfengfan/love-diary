# 恋爱记录网站

一个用于记录和展示恋爱期间美好回忆的个人网站，支持照片、视频、日记等多种形式的内容管理。

## 技术栈

- **前端**: Vue.js 3 + Vite + Element Plus
- **后端**: Flask + SQLAlchemy
- **数据库**: SQLite
- **部署环境**: Windows 10

## 项目结构

```
love-diary/
├── love-diary-backend/     # 后端 Flask 应用
│   ├── app/               # 应用代码
│   ├── uploads/           # 上传文件存储
│   ├── requirements.txt   # Python 依赖
│   ├── run.py            # 启动文件
│   └── setup.bat         # 安装脚本
├── love-diary-frontend/   # 前端 Vue 应用
│   ├── src/              # 源代码
│   ├── package.json      # Node.js 依赖
│   ├── vite.config.js    # Vite 配置
│   └── setup.bat         # 安装脚本
└── README.md             # 项目说明
```

## 快速开始

### 🔧 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **操作系统**: Windows 10+

### 📦 后端设置

1. 进入后端目录：
   ```bash
   cd love-diary-backend
   ```

2. 运行安装脚本（推荐）：
   ```bash
   setup.bat
   ```

3. 如果脚本运行失败，手动安装：
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. 启动后端服务：
   ```bash
   python run.py
   ```
   后端服务将在 http://localhost:5000 启动

5. 首次运行会自动创建默认管理员账号：
   - 用户名：admin
   - 密码：admin123

### 🎨 前端设置

1. 进入前端目录：
   ```bash
   cd love-diary-frontend
   ```

2. 运行安装脚本（推荐）：
   ```bash
   setup.bat
   ```

3. 如果脚本运行失败，手动安装：
   ```bash
   npm install
   ```

4. 启动前端服务：
   ```bash
   npm run dev
   ```
   前端服务将在 http://localhost:3000 启动

### 🌐 访问应用

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:5000
- **管理员登录**: admin / admin123

## 功能特性

### 访客功能
- 浏览所有公开内容（照片、视频、日记）
- 使用搜索功能
- 查看时间线
- 响应式设计

### 管理员功能
- 登录管理系统
- 照片管理（上传、编辑、删除）
- 视频管理（上传、编辑、删除）
- 日记管理（创建、编辑、删除）
- 数据统计
- 密码修改

## API 文档

### 认证相关
- `POST /api/auth/login` - 管理员登录
- `POST /api/auth/logout` - 管理员登出
- `GET /api/auth/check` - 检查登录状态
- `POST /api/auth/change-password` - 修改密码

### 照片管理
- `GET /api/photos` - 获取照片列表
- `POST /api/photos` - 上传照片（需要登录）
- `GET /api/photos/{id}` - 获取照片详情
- `PUT /api/photos/{id}` - 更新照片信息（需要登录）
- `DELETE /api/photos/{id}` - 删除照片（需要登录）

### 视频管理
- `GET /api/videos` - 获取视频列表
- `POST /api/videos` - 上传视频（需要登录）
- `GET /api/videos/{id}` - 获取视频详情
- `PUT /api/videos/{id}` - 更新视频信息（需要登录）
- `DELETE /api/videos/{id}` - 删除视频（需要登录）

### 日记管理
- `GET /api/diaries` - 获取日记列表
- `POST /api/diaries` - 创建日记（需要登录）
- `GET /api/diaries/{id}` - 获取日记详情
- `PUT /api/diaries/{id}` - 更新日记（需要登录）
- `DELETE /api/diaries/{id}` - 删除日记（需要登录）

### 搜索和时间线
- `GET /api/search` - 搜索内容
- `GET /api/timeline` - 获取时间线数据
- `GET /api/timeline/calendar` - 获取日历数据

### 统计数据
- `GET /api/statistics` - 获取统计数据（需要登录）

## 安全考虑

1. **文件上传安全**
   - 文件类型限制
   - 文件大小限制
   - 安全的文件名处理

2. **权限控制**
   - 管理员身份验证
   - API权限验证

3. **数据安全**
   - SQL注入防护
   - XSS攻击防护

## 开发说明

### 数据库
- 使用 SQLite 数据库
- 首次运行会自动创建数据库表
- 数据库文件：`love-diary-backend/database.db`

### 文件存储
- 上传的文件存储在 `love-diary-backend/uploads/` 目录
- 照片：`uploads/photos/`
- 视频：`uploads/videos/`
- 缩略图：`uploads/thumbnails/`

### 环境要求
- Python 3.8+
- Node.js 16+
- Windows 10（开发环境）

## 常见问题

1. **无法上传文件**
   - 检查上传目录是否存在且有写入权限
   - 检查文件大小是否超出限制

2. **登录失败**
   - 确认使用默认账号：admin / admin123
   - 检查后端服务是否正常运行

3. **前端无法访问后端API**
   - 确认后端服务在 http://localhost:5000 运行
   - 检查 CORS 配置

## 更新日志

### v1.0.0
- 基础功能实现
- 管理员登录系统
- 照片、视频、日记管理
- 搜索和时间线功能
- 响应式界面设计

## 许可证

MIT License