# 公路车资料查询网站后端技术设计文档

## 1. 项目目标

本项目的目标不是做自行车评分系统，也不是做社区论坛，而是做一个面向公路自行车用户、内容创作者、买车决策者的资料查询网站后端。

后端要解决的核心问题很明确：

- 能查品牌
- 能查车型
- 能查配置版本
- 能查套件与零部件
- 能按条件筛选
- 能支撑前端展示、搜索和后续数据维护

这个项目的第一阶段更偏“数据型产品”，重点是信息结构、查询效率和接口清晰度，而不是复杂的交互系统。

---

## 2. 产品定位

网站定位为一个 `公路车资料库 / 查询站`，用户来到这里，主要是为了回答这些问题：

- 某个品牌有哪些公路车型？
- 某个车型有哪些配置版本？
- 某个配置用了什么套件和轮组？
- 某个零部件被哪些整车使用？
- 某类公路车有哪些主流品牌和主流车型？

因此，后端设计优先服务于以下场景：

- 列表查询
- 条件过滤
- 详情查看
- 全站搜索
- 基础关联关系展示

---

## 3. 技术方案结论

本项目推荐采用以下后端技术栈：

- Web 框架：`FastAPI`
- ORM：`SQLAlchemy 2.0`
- 数据验证：`Pydantic`
- 数据库：`MySQL`
- 数据库迁移：`Alembic`
- 服务部署：`Uvicorn / Gunicorn + Uvicorn workers`
- 配置管理：`.env + Pydantic Settings`
- API 文档：`FastAPI OpenAPI / Swagger`

选择这套方案的原因：

- FastAPI 对查询型 API 特别友好
- 自动生成接口文档，便于前后端协作
- Python 生态方便后续做采集脚本、清洗脚本、数据导入脚本
- SQLAlchemy 适合逐步扩展关系模型
- MySQL 足以支撑第一阶段的资料查询网站

---

## 4. 为什么选择 FastAPI

本项目的第一阶段目标是做一个结构清晰、查询高效、接口规范的后端，而不是先做一个重后台系统。

FastAPI 的优势刚好贴合需求：

- 适合 REST API 开发
- 支持类型提示，代码可读性高
- Swagger 文档自动生成，便于调试
- 与 SQLAlchemy、Pydantic 搭配自然
- 后续扩展搜索、缓存、异步任务都比较顺手

相比之下：

- Django 更适合后台管理、录入和运营系统较重的场景
- 当前项目更像“资料查询 API 服务”，所以 FastAPI 更轻、更快、更贴题

结论：

- 第一阶段优先选 `FastAPI`
- 后续如果需要强运营后台，再补 Django Admin 风格的独立管理端，或者补一个内部 CMS

---

## 5. 系统边界

第一阶段后端只负责这些能力：

- 提供品牌、车型、配置、零部件的查询 API
- 提供条件筛选和分页
- 提供关键词搜索
- 返回结构化 JSON 给前端
- 为后续数据导入和数据维护留出接口与模型空间

第一阶段暂不做：

- 用户系统
- 评论系统
- 评分系统
- 收藏系统
- 推荐系统
- 复杂权限系统
- 爬虫平台化系统

这意味着第一阶段后端的重点是：

- 数据模型稳定
- 接口清晰
- 查询快
- 便于后续维护

---

## 6. 数据模型设计

当前推荐的核心数据表有 4 张，足够支撑第一阶段查询站：

- `brands`
- `models`
- `builds`
- `components`

另外保留扩展表：

- `geometry`
- `ranking_scores`（当前先不用）

### 6.1 brands 品牌表

作用：记录品牌基础信息。

核心字段：

- `brand_id`
- `brand_name_en`
- `brand_name_cn`
- `country_region`
- `brand_type`
- `market_positioning`
- `sales_model`
- `main_road_categories`
- `official_website`
- `notes`

### 6.2 models 车型表

作用：记录车型平台，而不是具体配置版本。

核心字段：

- `model_id`
- `brand_id`
- `model_name`
- `series_name`
- `bike_category`
- `frame_material`
- `brake_type`
- `tire_clearance_mm`
- `release_year_first`
- `current_generation_year`
- `is_active`
- `official_model_url`
- `notes`

### 6.3 builds 配置版本表

作用：记录整车的具体配置版本，是网站最重要的查询对象之一。

核心字段：

- `build_id`
- `model_id`
- `build_name`
- `model_year`
- `market_region`
- `msrp_currency`
- `msrp_price`
- `groupset_brand`
- `groupset_series`
- `wheel_brand`
- `wheel_model`
- `power_meter`
- `cockpit_type`
- `claimed_weight_kg`
- `is_disc`
- `is_electronic_shifting`
- `is_stock_complete_bike`
- `official_build_url`
- `notes`

### 6.4 components 零部件表

作用：记录套件、轮组、轮胎、码表、功率计等核心零部件。

核心字段：

- `component_id`
- `component_category`
- `brand_name`
- `component_name`
- `series`
- `weight_g`
- `msrp_currency`
- `msrp_price`
- `official_url`
- `notes`

### 6.5 geometry 几何表（第二阶段）

作用：记录车型几何信息，用于更专业的车型比较。

第一阶段不是必须，但建议预留。

---

## 7. 实体关系设计

核心关系如下：

- 一个 `brand` 对应多个 `model`
- 一个 `model` 对应多个 `build`
- 一个 `build` 可以引用多个零部件信息
- 一个 `component` 未来可以被多个 `build` 关联使用

简化关系图：

```text
Brand 1 -> N Model
Model 1 -> N Build
Build -> uses -> Component
```

第一阶段为了快速落地，`builds` 中可以先保留部分反规范化字段：

- `groupset_brand`
- `groupset_series`
- `wheel_brand`
- `wheel_model`

后续如果要做更强关联，再逐步拆成组件关系表。

---

## 8. API 设计

第一阶段建议采用 REST 风格接口。

### 8.1 品牌接口

- `GET /api/brands`
  - 品牌列表
  - 支持分页、筛选、排序

- `GET /api/brands/{brand_id}`
  - 品牌详情
  - 附带品牌下的车型摘要

支持筛选参数示例：

- `country_region`
- `market_positioning`
- `sales_model`
- `keyword`

### 8.2 车型接口

- `GET /api/models`
  - 车型列表

- `GET /api/models/{model_id}`
  - 车型详情
  - 附带配置版本摘要

支持筛选参数示例：

- `brand_id`
- `bike_category`
- `frame_material`
- `brake_type`
- `year`

### 8.3 配置版本接口

- `GET /api/builds`
  - 配置版本列表

- `GET /api/builds/{build_id}`
  - 配置版本详情

支持筛选参数示例：

- `brand_id`
- `model_id`
- `groupset_brand`
- `groupset_series`
- `wheel_brand`
- `is_electronic_shifting`
- `is_disc`
- `min_price`
- `max_price`

### 8.4 零部件接口

- `GET /api/components`
  - 零部件列表

- `GET /api/components/{component_id}`
  - 零部件详情

支持筛选参数示例：

- `component_category`
- `brand_name`
- `series`
- `keyword`

### 8.5 搜索接口

- `GET /api/search?q=...`

用于全站搜索品牌、车型、配置和零部件。

第一阶段可用简单搜索策略：

- 品牌名匹配
- 车型名匹配
- 配置名匹配
- 组件名匹配

---

## 9. API 返回结构建议

建议统一返回格式，便于前端处理。

列表接口返回示例：

```json
{
  "items": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100
  },
  "filters": {
    "brand_id": "brand_001"
  }
}
```

详情接口返回示例：

```json
{
  "data": {
    "brand_id": "brand_001",
    "brand_name_en": "Specialized"
  }
}
```

错误返回建议：

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Brand not found"
  }
}
```

---

## 10. 项目目录结构建议

建议采用清晰的分层结构，便于后续扩展。

```text
backend/
├─ app/
│  ├─ main.py
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ database.py
│  │  └─ logging.py
│  ├─ models/
│  │  ├─ brand.py
│  │  ├─ model.py
│  │  ├─ build.py
│  │  └─ component.py
│  ├─ schemas/
│  │  ├─ brand.py
│  │  ├─ model.py
│  │  ├─ build.py
│  │  └─ component.py
│  ├─ api/
│  │  ├─ brands.py
│  │  ├─ models.py
│  │  ├─ builds.py
│  │  ├─ components.py
│  │  └─ search.py
│  ├─ services/
│  │  ├─ brand_service.py
│  │  ├─ model_service.py
│  │  ├─ build_service.py
│  │  ├─ component_service.py
│  │  └─ search_service.py
│  └─ repositories/
│     ├─ brand_repository.py
│     ├─ model_repository.py
│     ├─ build_repository.py
│     └─ component_repository.py
├─ alembic/
├─ tests/
├─ requirements.txt
└─ .env
```

---

## 11. ORM 设计建议

推荐使用 SQLAlchemy 2.0 的声明式写法。

建议定义以下 ORM 模型：

- `Brand`
- `RoadModel`
- `Build`
- `Component`

其中：

- `Brand.models`
- `RoadModel.brand`
- `RoadModel.builds`
- `Build.model`

第一阶段对 `Build -> Component` 的关系可以先不用完全建多对多，而是保留反规范化字段，后续再重构。

这样可以让网站先跑起来，再逐步优化结构。

---

## 12. 查询策略

这是一个典型的查询站，因此性能重点在：

- 列表查询
- 条件过滤
- 模糊搜索
- 详情页关联读取

建议：

- 列表页统一支持分页
- 对常用筛选字段加索引
- 详情页使用按需加载，不一次性把所有关联数据塞进去
- 搜索第一阶段先用 MySQL LIKE / FULLTEXT

建议重点加索引的字段：

- `brands.country_region`
- `brands.market_positioning`
- `models.brand_id`
- `models.bike_category`
- `builds.model_id`
- `builds.groupset_brand`
- `builds.is_electronic_shifting`
- `components.component_category`
- `components.brand_name`

---

## 13. 数据导入与维护策略

当前数据库已经有一批 SQL seed 文件。后续建议采用三类数据维护方式：

### 13.1 初始化种子数据

通过 SQL 文件导入：

- `schema.sql`
- `seed_brands.sql`
- `seed_models.sql`
- `seed_builds.sql`
- `seed_components.sql`

### 13.2 批量导入脚本

后续建议用 Python 写导入脚本：

- CSV -> MySQL
- Excel -> MySQL
- 官网抓取结果 -> MySQL

### 13.3 手工修正

第一阶段可以不用做完整后台，先允许：

- 直接改 SQL / CSV
- 使用内部脚本导入更新

等数据规模大了，再考虑内部管理界面。

---

## 14. 搜索设计

搜索会是这个网站的高频功能。

第一阶段建议做一个简单全站搜索：

- 搜品牌名
- 搜车型名
- 搜配置版本名
- 搜套件名 / 零部件名

搜索结果可按类型分组：

- 品牌
- 车型
- 配置
- 零部件

例如：

```text
搜索词：Ultegra
- 零部件：Shimano Ultegra Di2
- 配置：Tarmac SL8 Expert
- 配置：Ultimate CF SLX 8 Di2
```

后续如果搜索需求变复杂，再考虑引入：

- Elasticsearch
- Meilisearch

---

## 15. 管理后台策略

第一阶段不建议马上做复杂后台。

更现实的策略是：

- 先把公开查询站做好
- 后端提供稳定 API
- 数据维护先靠 SQL / CSV / Python 导入脚本

如果后面数据维护压力上来，再补：

- 简单内部管理页
- 或单独管理端

也就是说，后台不是第一阶段阻塞项。

---

## 16. 缓存与性能优化策略

第一阶段不需要过度优化，但建议预留思路。

可以考虑的策略：

- 热门品牌页缓存
- 热门车型页缓存
- 常用筛选结果缓存
- 首页数据缓存

如果后面流量明显增加，可以逐步加：

- Redis 缓存
- CDN 缓存
- 查询结果缓存

但第一阶段先不把复杂度拉太高。

---

## 17. 部署建议

开发环境：

- Python 3.11+
- FastAPI
- MySQL
- Uvicorn

生产环境：

- Nginx
- Gunicorn + Uvicorn workers
- MySQL
- systemd / Docker / PM2 类进程管理（任选其一）

如果未来前后端分离：

- 后端只负责 API
- 前端可单独部署

---

## 18. 第一阶段开发优先级

建议按这个顺序推进：

### 阶段 1：后端可用
- 完成数据库建表
- 完成品牌、车型、配置、零部件 4 类 ORM
- 完成 4 类基础查询接口
- 完成分页和筛选

### 阶段 2：网站能查
- 完成搜索接口
- 完成品牌详情与车型详情的关联数据输出
- 完成基础错误处理和日志

### 阶段 3：数据可持续更新
- 完成 CSV/SQL 导入脚本
- 完成批量更新机制
- 补更多车型和 build 数据

---

## 19. 风险与注意事项

### 19.1 数据准确性问题
自行车品牌官网、地区站、电商站的数据可能不一致。

解决策略：

- 先以官网为主
- 电商价格作为补充参考
- 对种子数据保留备注字段

### 19.2 数据结构过早复杂化
第一阶段最容易犯的错是：

- 还没把站做出来，就先把数据库设计得过重

建议：

- 先保留适度反规范化
- 优先做可查、可用、可展示
- 等真正出现维护压力再拆表升级

### 19.3 搜索与筛选过多导致接口复杂
建议第一阶段先控制筛选项数量，不要把所有字段都开放成筛选条件。

---

## 20. 最终结论

这个项目当前最适合的后端路线是：

- 用 `FastAPI + SQLAlchemy + MySQL` 搭一个资料查询型后端
- 围绕 `brands / models / builds / components` 四张核心表提供查询接口
- 优先解决“能查、能筛、能展示”的问题
- 暂不引入评分系统、复杂后台和社区功能

一句话总结：

这不是一个要先做“观点输出”的网站，而是一个要先做“结构化资料查询”的网站；后端的首要任务，不是复杂，而是稳定、清楚、好查、可扩展。
