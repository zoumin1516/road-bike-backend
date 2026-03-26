# 数据导入说明

## 1. 前提

先确认：

- MySQL 已安装并运行
- 已更新项目根目录下的 `.env`
- 虚拟环境已激活

## 2. 检查数据库连接

```bash
cd /Users/jyxc-dz-0100528/Project/road-bike-backend
source .venv/bin/activate
python scripts/check_db_connection.py
```

如果成功，会打印 MySQL 版本号。

## 3. 导入 schema 和种子数据

当前脚本会按顺序导入以下文件：

- `/Users/jyxc-dz-0100528/.openclaw/workspace/road_bike_mysql_schema.sql`
- `/Users/jyxc-dz-0100528/.openclaw/workspace/road_bike_seed_brands.sql`
- `/Users/jyxc-dz-0100528/.openclaw/workspace/road_bike_seed_models.sql`
- `/Users/jyxc-dz-0100528/.openclaw/workspace/road_bike_seed_builds.sql`
- `/Users/jyxc-dz-0100528/.openclaw/workspace/road_bike_seed_components.sql`

执行命令：

```bash
cd /Users/jyxc-dz-0100528/Project/road-bike-backend
source .venv/bin/activate
python scripts/import_seed_data.py
```

## 4. 启动 API 服务

```bash
uvicorn app.main:app --reload
```

接口文档：

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## 5. 当前限制

当前导入脚本假设：

- MySQL 用户有建库权限
- SQL 文件位于工作空间固定路径
- schema 与 seed 文件是一致版本

后续可以再升级成：

- 支持参数化数据库名
- 支持 CSV 导入
- 支持增量导入
- 支持 Alembic 管理 schema
