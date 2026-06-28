# PDF Tools Website

一个功能丰富的PDF处理工具网站，仿照 SmallPDF.com 的风格，使用Django框架构建。

## 🚀 功能特性

- 📄 **PDF转换**: PDF转Word、Excel、PowerPoint、图片等
- 🔀 **PDF合并**: 合并多个PDF文件
- ✂️ **PDF分割**: 提取或删除特定页面
- 🔐 **PDF加密/解密**: 保护或解锁PDF文件
- 🎨 **PDF压缩**: 减小PDF文件大小
- 🖼️ **图片转PDF**: 将图片转换为PDF
- 📝 **PDF编辑**: 添加水印、注释等
- 👤 **用户系统**: 注册、登录、文件管理
- ⚡ **异步处理**: 使用Celery处理耗时任务

## 🛠️ 技术栈

- **后端**: Django 4.2
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **PDF处理**: PyPDF2, ReportLab, pdf2image
- **异步任务**: Celery + Redis
- **服务器**: Gunicorn

## 📋 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/coding1018/pdf-tools-website.git
cd pdf-tools-website
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库迁移

```bash
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
python manage.py runserver
```

访问 `http://localhost:8000`

## 📁 项目结构

```
pdf-tools-website/
├── manage.py
├── requirements.txt
├── .gitignore
├── pdf_tools/                    # Django项目配置
│   ├── __init__.py
│   ├── settings.py              # 项目设置
│   ├── urls.py                  # 主URL配置
│   ├── wsgi.py
│   └── asgi.py
├── tools/                        # PDF工具应用
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                # 数据模型
│   ├── views.py                 # 视图函数
│   ├── urls.py                  # URL路由
│   ├── forms.py                 # 表单类
│   ├── utils.py                 # PDF处理工具
│   ├── tasks.py                 # Celery异步任务
│   ├── tests.py
│   └── templates/               # HTML模板
│       ├── base.html
│       ├── index.html
│       ├── merge.html
│       ├── split.html
│       └── ...
├── accounts/                     # 用户认证应用
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       ├── register.html
│       ├── login.html
│       └── profile.html
├── static/                       # 静态文件
│   ├── css/
│   │   ├── style.css
│   │   └── bootstrap.css
│   ├── js/
│   │   ├── main.js
│   │   └── upload.js
│   └── images/
└── media/                        # 用户上传文件
```

## 🔧 配置说明

### 环境变量 (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://localhost:6379/0
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

## 📚 API文档

### 合并PDF

```bash
POST /api/merge/
Content-Type: multipart/form-data

Files: [pdf1.pdf, pdf2.pdf, ...]
```

### 分割PDF

```bash
POST /api/split/
Content-Type: multipart/form-data

File: pdf_file.pdf
Pages: 1-5
```

## 🚀 部署

### Docker部署

```bash
docker build -t pdf-tools .
docker run -p 8000:8000 pdf-tools
```

### Heroku部署

```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

## 📝 许可证

MIT License

## 👤 作者

Coding1018

## 🤝 贡献

欢迎提交Issue和Pull Request！
