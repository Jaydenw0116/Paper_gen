# 智能组卷系统

基于Word底层XML的智能组卷系统，专注于解决包含复杂数学公式(微软OMML格式)、表格和浮动图片的Word文档的智能组卷需求。

## 技术架构

### 后端技术栈
- **框架**: FastAPI
- **语言**: Python 3.8+
- **文档处理**: python-docx, docxcompose
- **缓存**: Redis

### 前端技术栈
- **框架**: Vue 3
- **构建工具**: Vite
- **样式**: Tailwind CSS 3
- **拖拽**: vuedraggable
- **图标**: lucide-vue-next

## 项目结构

```
Paper_gen/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   └── routes.py      # 核心API端点
│   │   ├── core/              # 核心模块
│   │   │   ├── config.py      # 配置管理
│   │   │   ├── cache.py       # 缓存管理
│   │   │   ├── xml_parser.py  # XML切割引擎
│   │   │   └── xml_composer.py# XML重编号与合并引擎
│   │   └── main.py            # FastAPI应用入口
│   ├── tests/                 # 测试代码
│   ├── requirements.txt       # 依赖声明
│   └── run.py                 # 启动脚本
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/        # Vue组件
│   │   │   ├── FileUploader.vue      # 文件上传组件
│   │   │   ├── QuestionList.vue      # 题目列表组件
│   │   │   ├── QuestionPreview.vue   # 题目预览组件
│   │   │   ├── ComposeConfig.vue     # 组卷配置组件
│   │   │   └── DownloadPanel.vue     # 下载面板组件
│   │   ├── utils/
│   │   │   └── api.py         # API调用工具
│   │   ├── App.vue            # 主应用组件
│   │   ├── main.js            # 入口文件
│   │   └── style.css          # 全局样式
│   ├── index.html
│   ├── vite.config.js         # Vite配置
│   ├── tailwind.config.js     # Tailwind配置
│   ├── postcss.config.js      # PostCSS配置
│   └── package.json           # 前端依赖
└── README.md
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 18+
- Redis

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

## API接口

### 1. 上传文档
- **POST** `/api/upload`
- 上传题目和答案文档进行切割

### 2. 获取题目列表
- **GET** `/api/questions/{session_id}`
- 获取切割后的题目列表

### 3. 组卷
- **POST** `/api/compose`
- 根据选定题目生成试卷和答案

### 4. 下载文档
- **GET** `/api/download/{session_id}/{doc_type}`
- 下载生成的试卷或答案文档

## 核心算法

### XML切割引擎
1. 解析Word文档的XML结构
2. 使用正则表达式识别题号边界
3. 采用倒序方式删除边界外的节点
4. 保护页面属性节点和必要的空段落

### 重编号引擎
1. 根据前端顺序修改题号
2. 跳过图片、形状和公式节点
3. 确保只替换文本中的题号

### 文档合并
1. 加载模板文档
2. 使用docxcompose按顺序合并题目块
3. 确保每个文档有正确的section配置

## 许可证

MIT License