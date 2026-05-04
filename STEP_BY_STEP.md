# 📖 小白专属 · 超详细操作指南

## 前言
不用担心，跟着我一步一步来，很简单的！大概需要15-20分钟。

---

## 第一部分：提交代码更新（第一步，先做这个）

### 1. 把刚才改的代码提交到 GitHub

因为我刚才帮你改了几个文件，需要先把它们提交到 GitHub。

如果你本地操作：

1. 打开你的终端（Terminal / 命令行）
2. 进入项目文件夹

```bash
cd /Users/wuhuangjian/Desktop/Paper_gen
```

3. 查看修改了哪些文件

```bash
git status
```

你应该会看到：
- 修改了：`backend/requirements.txt`
- 修改了：`backend/run.py`
- 新增了：`backend/render.yaml`
- 新增了：`frontend/.env.example`
- 新增了：`DEPLOYMENT_FIX.md`

4. 提交代码

```bash
git add backend/requirements.txt backend/run.py backend/render.yaml frontend/.env.example DEPLOYMENT_FIX.md
git commit -m "修复部署配置：添加Render部署支持"
git push
```

（如果提示输入用户名密码，按提示操作）

---

## 第二部分：部署后端到 Render

### 2.1 注册/登录 Render

1. 打开浏览器访问：https://render.com
2. 点击右上角 **"Sign In"**
3. 选择 **"Continue with GitHub"**（直接用你的 GitHub 账号登录，方便）
4. 按提示授权，点允许就行

### 2.2 点击新建 Web Service

1. 登录成功后，进入 Render 控制台
2. 点击右上角那个很大的 **"+ New"** 按钮
3. 在下拉菜单里选 **"Web Service"**

### 2.3 连接 GitHub 仓库

1. 在 "Connect a repository" 区域
2. 找到你的 `Paper_gen` 仓库（或者你项目的名字）
3. 点击 **"Connect"** 按钮
4. 如果没看到？点击 **"Configure account"** 授权更多仓库

### 2.4 配置部署信息（关键步骤）

在 "Build & deploy" 页面，按下面填：

| 项目 | 填写内容 | 说明 |
|------|---------|------|
| **Name** | `paper-gen` 或你喜欢的名字 | 随便起，会变成你的网址前缀 |
| **Region** | 选离中国近的 | Singapore（新加坡）或者 Tokyo（东京）都行 |
| **Branch** | `main` 或 `master` | 用你代码在 GitHub 的默认分支 |
| **Root Directory** | `backend` | **这个很重要！** 一定要写 `backend` |
| **Runtime** | `Python 3` | 会自动选，选最新的 Python |

向下滚动，看到 **Build Command**：
```
pip install -r requirements.txt
```

然后是 **Start Command**：
```
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 2.5 选择套餐

1. 找到 "Instance Type" 区域
2. 选 **Free** 套餐（免费！）
3. 看到 "750 hours free" 那个

### 2.6 开始部署

1. 点击最下面的蓝色按钮 **"Create Web Service"**
2. 现在 Render 会开始部署，大概需要3-5分钟
3. 等它变成绿色的 **"Live"** 状态就好了

### 2.7 获取后端地址

部署成功后，页面上面会显示你的网址，像这样：
```
https://paper-gen-abc123.onrender.com
```

**把这个地址复制下来，后面要用！

---

## 第三部分：配置前端

### 3.1 在本地创建前端的 .env 文件

1. 回到你的项目文件夹
2. 进入 `frontend` 目录
3. 复制 `frontend/.env.example` 为 `frontend/.env`

在终端执行：

```bash
cd /Users/wuhuangjian/Desktop/Paper_gen/frontend
cp .env.example .env
```

### 3.2 编辑 .env 文件

用你常用的编辑器打开 `frontend/.env` 文件，填入内容：

```env
# 把下面的 YOUR_BACKEND_URL 换成你刚才复制的 Render 地址
VITE_API_URL=https://paper-gen-abc123.onrender.com/api
```

（注意：后面要加 `/api` 哦！）

### 3.3 测试一下（可选）

本地测试一下前端：

```bash
npm install
npm run dev
```

如果本地访问没问题的话，继续下一步。

---

## 第四部分：提交前端代码到 GitHub

### 4.1 提交更改

1. 回到项目根目录
2. 提交代码

```bash
cd /Users/wuhuangjian/Desktop/Paper_gen
git add frontend/.env.example
git commit -m "添加前端环境变量示例"
git push
```

（.env 文件不会提交（是本地配置）

---

## 第五部分：更新 Vercel

### 5.1 登录 Vercel

1. 访问 https://vercel.com
2. 用 GitHub 账号登录
3. 找到你的项目

### 5.2 在 Vercel 设置环境变量

1. 在 Vercel 项目的项目页面，点上面的 **Settings
2. 左边菜单选 **Environment Variables**
3. 点击 **Add New**
4. 填入：
   - **Name**: `VITE_API_URL`
   - **Value**: `https://paper-gen-abc123.onrender.com/api`
   - **Environment**: 选 Production 和 Preview 都选上
5. 点击 **Save**

### 5.3 重新部署

1. 回到 Vercel 项目页面
2. 点 **Deployments**
3. 选最新的那次部署
4. 点右上角 **Redeploy**
5. 等一下，部署成功了

---

## 第六部分：验证测试

### 6.1 测试后端

打开浏览器访问你的 Vercel 前端网址：
https://paper-gen-rho.vercel.app

试试上传文件，现在应该可以了！

### 6.2 如果还有问题？

1. 先测试 Render 后端地址：
   访问：https://paper-gen-abc123.onrender.com/docs
   应该能看到一个 API 文档页面

2. 如果上面显示说明后端是好的。

---

## 💡 小提示

1. Render 免费版如果15分钟没人用会"睡觉"，第一次访问要等几秒

2. 如果遇到问题，把错误信息发给我，我帮你解决

3. 上面步骤中哪一步不明白，直接问我，我再细讲

---

## 常见问题

### Q：我找不到 Root Directory 在哪里填？
**A**：在填写配置的页面，往下滑一点能看到。

### Q：git push 失败？
**A**：可能是网络问题，重试一下，或者用 GitHub Desktop（图形化工具）。

### Q：部署后还是500？
**A**：先访问后端地址，看是不是后端没部署成功。

---

有问题随时问我！😊
