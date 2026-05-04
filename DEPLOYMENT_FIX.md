# 智能组卷系统 - 部署指南

## 问题说明

### 500错误原因
当前部署在 Vercel 上的网站出现 "Request failed with status code 500" 错误，原因是：
- **Vercel 不支持 Python 后端**
- 只能托管静态前端文件
- 文件上传等API请求无法处理

### 解决方案架构
```
┌─────────────────┐         ┌──────────────────┐
│   Vercel        │         │   Render         │
│  (前端静态)      │  ───▶   │  (Python后端)    │
│  https://...    │         │  https://...     │
└─────────────────┘         └──────────────────┘
```

---

## 第一步：部署后端到 Render

### 1.1 创建 Render 账号
1. 访问 https://render.com
2. 使用 GitHub 账号登录
3. 完成基本设置

### 1.2 部署后端服务

#### 方式一：使用 render.yaml（推荐，自动配置）

1. 在 GitHub 仓库中已经包含 `backend/render.yaml` 文件
2. 在 Render 中：
   - 点击 "New +" → "Blueprint"
   - 连接 GitHub 仓库
   - 选择 `backend/render.yaml` 文件
   - 点击 "Apply"

#### 方式二：手动部署

1. 在 Render 点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 配置以下设置：
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
4. 点击 "Create Web Service"

### 1.3 获取后端地址

部署成功后，Render 会提供类似以下的URL：
```
https://paper-gen-backend.onrender.com
```

记录这个地址，后面配置前端时需要用到。

---

## 第二步：更新前端配置

### 2.1 创建前端 .env 文件

在 `frontend` 目录下创建 `.env` 文件：

```bash
# 复制示例配置
cp .env.example .env
```

### 2.2 配置 API 地址

编辑 `frontend/.env` 文件：

```env
# 将 YOUR_BACKEND_URL 替换为你在 Render 获取的地址
VITE_API_URL=https://paper-gen-backend.onrender.com/api
```

### 2.3 重新构建前端

```bash
cd frontend
npm install
npm run build
```

---

## 第三步：更新 Vercel 前端部署

### 3.1 在 Vercel 重新部署

1. 登录 Vercel
2. 进入你的项目
3. 点击 "Deployments"
4. 点击右上角 "Redeploy"
5. 选择最新的提交

或者推送代码更新到 GitHub，自动触发部署。

### 3.2 配置环境变量（可选）

在 Vercel 项目设置中添加：
- **Name**: `VITE_API_URL`
- **Value**: `https://paper-gen-backend.onrender.com/api`

---

## 验证部署

### 测试后端
访问你的 Render 后端地址：
```
https://paper-gen-backend.onrender.com/docs
```
应该能看到 FastAPI 的 API 文档页面。

### 测试前端
访问你的 Vercel 前端地址：
```
https://paper-gen-rho.vercel.app/
```

尝试上传文件，应该不再出现 500 错误。

---

## 常见问题

### Q: Render 免费套餐有哪些限制？
A: 
- 免费的 Web Service 在 15 分钟无活动后会休眠
- 首次访问可能需要几秒唤醒时间
- 每月有 750 小时免费额度
- 没有信用卡要求

### Q: 如何提高响应速度？
A:
- Render Plus 套餐（$25/月）支持 Always On
- 或使用 Railway/Railway（稍贵但性能更好）

### Q: Redis 配置？
A:
- Render 提供免费的 Redis 实例
- 在 Render 创建 Redis 服务后，复制连接地址
- 在后端环境变量中设置 `REDIS_URL`

### Q: 遇到 CORS 错误？
A:
- 后端已经配置了允许所有源的 CORS
- 如果还有问题，检查浏览器控制台的具体错误信息

### Q: 如何更新代码？
A:
1. 更新代码并推送到 GitHub
2. Render 会自动检测并重新部署后端
3. Vercel 也会自动重新部署前端

---

## 备选方案

如果 Render 不满足需求，可以考虑：

### Railway
- 定价：$5/月起
- 优点：性能更好，部署更简单
- 缺点：比 Render 贵

### Coolify
- 开源自托管方案
- 需要自己的服务器
- 完全免费

### Zeabur
- 中文界面
- 免费额度较高
- 支持 Python

---

## 费用总结

| 平台 | 前端 | 后端 | 备注 |
|------|------|------|------|
| Vercel | 免费 | - | 静态托管 |
| Render | - | 免费* | 休眠后需唤醒 |
| Railway | - | $5/月 | 性能更好 |
| **总计** | **免费** | **免费起** | - |

*免费套餐限制：15分钟无活动会休眠
