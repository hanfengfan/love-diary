# 恋爱记录网站故障排除指南

## 常见问题及解决方案

### 1. RuntimeError: The current Flask app is not registered with this 'SQLAlchemy' instance

**问题描述**: 运行 `python run.py` 时出现SQLAlchemy实例注册错误。

**原因**: 数据库(db)实例在不同模块中有多个定义，导致Flask应用无法正确识别SQLAlchemy实例。

**解决方案**: ✅ **已修复**
- 统一了db实例的定义位置
- 确保所有模块都从同一个位置导入db
- 修复了import路径和依赖关系

### 2. ModuleNotFoundError: No module named 'xxx'

**问题描述**: 运行时缺少Python依赖包。

**解决方案**:
```bash
cd love-diary-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

或者直接运行安装脚本：
```bash
cd love-diary-backend
setup.bat
```

### 3. 数据库初始化失败

**问题描述**: 首次运行时数据库创建失败。

**解决方案**:
1. 确保有写入权限
2. 检查数据库文件路径
3. 重新运行应用，会自动创建

### 4. 文件上传目录权限问题

**问题描述**: 无法上传照片或视频。

**解决方案**:
1. 确保 `uploads/` 目录存在
2. 检查目录写入权限
3. 检查文件大小限制设置

### 5. 前端无法连接后端API

**问题描述**: 前端页面显示"网络错误"。

**解决方案**:
1. 确保后端服务在 http://localhost:5000 运行
2. 检查CORS配置
3. 验证前端代理配置

## 完整安装步骤

### 后端安装

```bash
# 1. 进入后端目录
cd love-diary-backend

# 2. 运行安装脚本
setup.bat

# 3. 启动应用
python run.py
```

**手动安装步骤**:
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动应用
python run.py
```

### 前端安装

```bash
# 1. 进入前端目录
cd love-diary-frontend

# 2. 运行安装脚本
setup.bat

# 3. 启动开发服务器
npm run dev
```

**手动安装步骤**:
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 访问地址

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:5000
- **默认管理员账号**: admin / admin123

## 依赖要求

### Python 环境
- Python 3.8+
- pip (Python包管理器)

### Node.js 环境
- Node.js 16+
- npm (Node.js包管理器)

## 主要修复内容

### 1. SQLAlchemy配置修复 ✅
- 统一db实例定义在 `app/models/database.py`
- 修复所有模型文件的导入路径
- 确保应用上下文正确初始化

### 2. 导入路径修复 ✅
- 修复循环导入问题
- 优化模块依赖关系
- 添加错误检查机制

### 3. 错误处理改进 ✅
- 添加依赖检查
- 提供清晰的错误信息
- 改进安装指南

## 测试验证

运行以下命令验证修复：

```bash
cd love-diary-backend
python run.py
```

如果看到以下输出，说明修复成功：
```
默认管理员账号创建成功: admin / admin123
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[你的IP]:5000
```

## 仍有问题？

如果遇到其他问题，请检查：

1. Python版本是否为3.8+
2. Node.js版本是否为16+
3. 是否有防火墙阻止端口访问
4. 是否有杀毒软件阻止文件操作

## 联系支持

如需进一步帮助，请提供：
1. 完整的错误信息
2. 操作系统版本
3. Python/Node.js版本
4. 运行的具体命令