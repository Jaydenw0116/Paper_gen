# 智能组卷系统部署指南

## 本地开发

### 前提条件
- Python 3.8+
- Node.js 18+
- Redis（可选，未安装时使用内存缓存）

### 启动步骤

1. **启动后端服务**
```bash
cd backend
pip install -r requirements.txt
python run.py
```
后端将运行在 http://localhost:8000

2. **启动前端服务**
```bash
cd frontend
npm install
npm run dev
```
前端将运行在 http://localhost:5173

3. **访问应用**
打开浏览器访问 http://localhost:5173

## 生产环境部署

### 方案一：使用支持 Python 的云平台

由于 Vercel 不支持 Python 后端，建议使用以下平台：

#### 1. Render（推荐）
- 免费套餐支持 Python
- 自动 HTTPS
- 持续部署

**部署步骤：**
1. 将代码推送到 GitHub
2. 在 Render 创建新服务
3. 选择 Web Service
4. 连接 GitHub 仓库
5. 配置环境变量：
   - `REDIS_URL`（可选）
   - `TEMP_DIR`（默认 /tmp）
6. 部署后端

**前端部署到 Vercel：**
1. 在 Vercel 创建新项目
2. 连接 GitHub 仓库
3. 配置根目录为 `frontend`
4. 部署

#### 2. Railway
- 免费套餐支持 Python
- 简单易用

#### 3. Heroku
- 支持 Python
- 需要绑定信用卡

### 方案二：使用 Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["python", "run.py"]
```

### 方案三：本地部署 + 内网穿透

使用 ngrok 或 frp 将本地服务暴露到公网：

```bash
# 安装 ngrok
brew install ngrok

# 启动后端服务
cd backend && python run.py

# 在另一个终端启动 ngrok
ngrok http 8000
```

将前端 API 地址改为 ngrok 提供的 URL。

## 当前问题说明

### Vercel 部署问题

当前 Vercel 部署（https://paper-gen-rho.vercel.app/）只能运行前端静态文件，无法处理文件上传等需要后端的功能。

**解决方案：**
1. 将后端部署到 Render/Railway/Heroku
2. 修改前端 API 地址为生产环境地址
3. 重新部署前端到 Vercel

### API 地址配置

前端会自动根据环境选择 API 地址：
- 本地开发：`http://localhost:8000/api`
- 生产环境：`${window.location.origin}/api`

如需自定义 API 地址，设置环境变量 `VITE_API_URL`。

## 环境变量

| 变量名 | 说明 | 默认值 |
|---------|------|---------|
| `REDIS_URL` | Redis 连接地址 | redis://localhost:6379/0 |
| `TEMP_DIR` | 临时文件目录 | /tmp/paper_gen |
| `MAX_FILE_SIZE` | 最大文件大小（字节） | 20971520 (20MB) |
| `MAX_QUESTIONS` | 最大题目数量 | 100 |
| `VITE_API_URL` | 前端 API 地址（可选） | 自动检测 |

## 故障排查

### 上传失败
1. 检查后端服务是否运行：`curl http://localhost:8000/`
2. 检查 Redis 连接（如使用 Redis）
3. 查看后端日志

### 前端无法访问
1. 检查端口 5173 是否被占用
2. 检查 Node.js 是否安装
3. 重新运行 `npm run dev`

### Vercel 部署后上传失败
- Vercel 不支持 Python 后端
- 需要将后端部署到其他平台
- 更新前端 API 地址
