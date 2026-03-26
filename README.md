# Road Bike Backend

基于 `FastAPI + SQLAlchemy + MySQL` 的公路车资料查询网站后端。

## 本地启动

```bash
cd /Users/jyxc-dz-0100528/Project/road-bike-backend
source .venv/bin/activate
cp .env.example .env
uvicorn app.main:app --reload
```

接口文档：
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 项目结构

```text
app/
  api/
  core/
  db/
  models/
  repositories/
  schemas/
  services/
```

## Docker 部署

### 构建镜像

```bash
docker build -t road-bike-backend:latest .
```

### 运行容器

```bash
docker run -d \
  --name road-bike-backend \
  -p 8000:8000 \
  -e APP_ENV=prod \
  -e DEBUG=false \
  -e MYSQL_HOST=host.docker.internal \
  -e MYSQL_PORT=3306 \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=change_me \
  -e MYSQL_DATABASE=road_bike_db \
  road-bike-backend:latest
```

健康检查：
- `http://127.0.0.1:8000/api/health`

## 下一步

- 把 MySQL 实例准备好并更新 `.env`
- 导入已有 SQL 种子数据
- 再补 Alembic 迁移和更多查询接口
