# 公路车资料查询网站 API 接口清单

本文档基于《公路车资料查询网站后端技术设计文档》细化第一阶段 API 设计，目标是让后端开发、前端联调和后续扩展有一份明确的接口参考。

---

## 1. API 设计原则

第一阶段 API 以“查询展示”为核心，遵循以下原则：

- REST 风格优先
- 统一分页格式
- 统一错误返回格式
- 筛选条件尽量明确
- 第一阶段不做复杂写接口，优先做读接口
- 字段尽量贴近数据库，但不直接暴露所有内部实现细节

接口前缀统一使用：

```text
/api
```

---

## 2. 通用约定

### 2.1 分页参数

所有列表接口建议统一支持：

- `page`：页码，默认 `1`
- `page_size`：每页数量，默认 `20`
- `sort_by`：排序字段
- `sort_order`：`asc` 或 `desc`

示例：

```text
GET /api/brands?page=1&page_size=20&sort_by=brand_name_en&sort_order=asc
```

### 2.2 列表返回格式

```json
{
  "items": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  },
  "filters": {
    "country_region": "Italy"
  }
}
```

### 2.3 详情返回格式

```json
{
  "data": {}
}
```

### 2.4 错误返回格式

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Brand not found"
  }
}
```

常见错误码建议：

- `BAD_REQUEST`
- `NOT_FOUND`
- `VALIDATION_ERROR`
- `INTERNAL_ERROR`

---

## 3. 品牌接口

## 3.1 获取品牌列表

**接口**

```text
GET /api/brands
```

**用途**

用于品牌列表页、筛选页、搜索建议页。

**支持查询参数**

- `page`
- `page_size`
- `keyword`
- `country_region`
- `market_positioning`
- `sales_model`
- `brand_type`
- `main_road_category`
- `sort_by`
- `sort_order`

**示例请求**

```text
GET /api/brands?country_region=Italy&market_positioning=top_tier&page=1&page_size=20
```

**示例返回**

```json
{
  "items": [
    {
      "brand_id": "brand_011",
      "brand_name_en": "Pinarello",
      "brand_name_cn": "皮娜瑞罗",
      "country_region": "Italy",
      "market_positioning": "top_tier",
      "sales_model": "dealer",
      "main_road_categories": "race,aero,endurance",
      "official_website": "https://www.pinarello.com"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "total_pages": 1
  },
  "filters": {
    "country_region": "Italy",
    "market_positioning": "top_tier"
  }
}
```

---

## 3.2 获取品牌详情

**接口**

```text
GET /api/brands/{brand_id}
```

**用途**

用于品牌详情页。

**路径参数**

- `brand_id`

**示例请求**

```text
GET /api/brands/brand_011
```

**示例返回**

```json
{
  "data": {
    "brand_id": "brand_011",
    "brand_name_en": "Pinarello",
    "brand_name_cn": "皮娜瑞罗",
    "country_region": "Italy",
    "brand_type": "complete_bike",
    "market_positioning": "top_tier",
    "sales_model": "dealer",
    "main_road_categories": "race,aero,endurance",
    "official_website": "https://www.pinarello.com",
    "notes": "意大利顶级竞赛品牌，Dogma 系列辨识度极高。"
  }
}
```

---

## 3.3 获取品牌下的车型列表

**接口**

```text
GET /api/brands/{brand_id}/models
```

**用途**

用于品牌详情页下挂车型列表。

**支持查询参数**

- `bike_category`
- `frame_material`
- `brake_type`
- `is_active`
- `page`
- `page_size`

**示例请求**

```text
GET /api/brands/brand_001/models?bike_category=race
```

---

## 4. 车型接口

## 4.1 获取车型列表

**接口**

```text
GET /api/models
```

**用途**

用于车型列表页和条件筛选页。

**支持查询参数**

- `page`
- `page_size`
- `keyword`
- `brand_id`
- `bike_category`
- `frame_material`
- `brake_type`
- `is_active`
- `release_year_first`
- `current_generation_year`
- `sort_by`
- `sort_order`

**示例请求**

```text
GET /api/models?brand_id=brand_001&bike_category=race&page=1&page_size=20
```

**示例返回**

```json
{
  "items": [
    {
      "model_id": "model_001",
      "brand_id": "brand_001",
      "model_name": "Tarmac SL8",
      "series_name": "Tarmac",
      "bike_category": "race",
      "frame_material": "carbon",
      "brake_type": "disc",
      "tire_clearance_mm": 32,
      "current_generation_year": 2026,
      "official_model_url": "https://www.specialized.com"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "total_pages": 1
  },
  "filters": {
    "brand_id": "brand_001",
    "bike_category": "race"
  }
}
```

---

## 4.2 获取车型详情

**接口**

```text
GET /api/models/{model_id}
```

**用途**

用于车型详情页。

**路径参数**

- `model_id`

**示例请求**

```text
GET /api/models/model_001
```

**示例返回**

```json
{
  "data": {
    "model_id": "model_001",
    "brand_id": "brand_001",
    "model_name": "Tarmac SL8",
    "series_name": "Tarmac",
    "bike_category": "race",
    "frame_material": "carbon",
    "brake_type": "disc",
    "tire_clearance_mm": 32,
    "release_year_first": 2023,
    "current_generation_year": 2026,
    "is_active": true,
    "official_model_url": "https://www.specialized.com",
    "notes": "Specialized 旗舰竞赛公路平台。"
  }
}
```

---

## 4.3 获取车型下的配置版本列表

**接口**

```text
GET /api/models/{model_id}/builds
```

**用途**

用于车型详情页下挂配置版本列表。

**支持查询参数**

- `model_year`
- `groupset_brand`
- `is_electronic_shifting`
- `page`
- `page_size`

---

## 5. 配置版本接口

## 5.1 获取配置版本列表

**接口**

```text
GET /api/builds
```

**用途**

用于配置查询页、价格筛选页、套件筛选页。

**支持查询参数**

- `page`
- `page_size`
- `keyword`
- `brand_id`
- `model_id`
- `model_year`
- `market_region`
- `groupset_brand`
- `groupset_series`
- `wheel_brand`
- `is_electronic_shifting`
- `is_disc`
- `min_price`
- `max_price`
- `cockpit_type`
- `sort_by`
- `sort_order`

**示例请求**

```text
GET /api/builds?groupset_brand=Shimano&is_electronic_shifting=1&min_price=5000&max_price=9000
```

**示例返回**

```json
{
  "items": [
    {
      "build_id": "build_001",
      "model_id": "model_001",
      "build_name": "Tarmac SL8 Expert",
      "model_year": 2026,
      "market_region": "global",
      "msrp_currency": "USD",
      "msrp_price": 6500,
      "groupset_brand": "Shimano",
      "groupset_series": "Ultegra Di2",
      "wheel_brand": "Roval",
      "wheel_model": "Rapide CL II",
      "power_meter": "No",
      "cockpit_type": "integrated",
      "claimed_weight_kg": 7.8,
      "is_disc": true,
      "is_electronic_shifting": true
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "total_pages": 1
  },
  "filters": {
    "groupset_brand": "Shimano",
    "is_electronic_shifting": true,
    "min_price": 5000,
    "max_price": 9000
  }
}
```

---

## 5.2 获取配置版本详情

**接口**

```text
GET /api/builds/{build_id}
```

**用途**

用于配置版本详情页。

**示例返回**

```json
{
  "data": {
    "build_id": "build_001",
    "model_id": "model_001",
    "build_name": "Tarmac SL8 Expert",
    "model_year": 2026,
    "market_region": "global",
    "msrp_currency": "USD",
    "msrp_price": 6500,
    "groupset_brand": "Shimano",
    "groupset_series": "Ultegra Di2",
    "wheel_brand": "Roval",
    "wheel_model": "Rapide CL II",
    "power_meter": "No",
    "cockpit_type": "integrated",
    "claimed_weight_kg": 7.8,
    "is_disc": true,
    "is_electronic_shifting": true,
    "is_stock_complete_bike": true,
    "official_build_url": "https://www.specialized.com",
    "notes": "Tarmac SL8 中高端电变配置。"
  }
}
```

---

## 5.3 获取配置版本关联的车型与品牌摘要

**接口**

```text
GET /api/builds/{build_id}/summary
```

**用途**

前端配置详情页需要同时拿到配置、车型、品牌的最简摘要时使用。

---

## 6. 零部件接口

## 6.1 获取零部件列表

**接口**

```text
GET /api/components
```

**用途**

用于零部件库查询页面。

**支持查询参数**

- `page`
- `page_size`
- `keyword`
- `component_category`
- `brand_name`
- `series`
- `sort_by`
- `sort_order`

**示例请求**

```text
GET /api/components?component_category=groupset&brand_name=Shimano
```

**示例返回**

```json
{
  "items": [
    {
      "component_id": "component_002",
      "component_category": "groupset",
      "brand_name": "Shimano",
      "component_name": "Ultegra Di2",
      "series": "R8100",
      "official_url": "https://bike.shimano.com"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "total_pages": 1
  },
  "filters": {
    "component_category": "groupset",
    "brand_name": "Shimano"
  }
}
```

---

## 6.2 获取零部件详情

**接口**

```text
GET /api/components/{component_id}
```

**用途**

用于零部件详情页。

---

## 6.3 获取零部件被哪些配置使用（第二阶段）

**接口**

```text
GET /api/components/{component_id}/builds
```

**说明**

这个接口需要后续把 `builds` 和 `components` 的关系进一步结构化后再做。

第一阶段可以暂不实现，或者只做简单搜索型映射。

---

## 7. 搜索接口

## 7.1 全站搜索

**接口**

```text
GET /api/search
```

**支持查询参数**

- `q`：关键词，必填
- `page`
- `page_size`
- `type`：可选，限制搜索类型，如 `brand`、`model`、`build`、`component`

**示例请求**

```text
GET /api/search?q=Ultegra
```

**示例返回**

```json
{
  "items": [
    {
      "type": "component",
      "id": "component_002",
      "title": "Shimano Ultegra Di2",
      "subtitle": "Groupset / R8100"
    },
    {
      "type": "build",
      "id": "build_001",
      "title": "Tarmac SL8 Expert",
      "subtitle": "Shimano Ultegra Di2"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 2,
    "total_pages": 1
  },
  "filters": {
    "q": "Ultegra"
  }
}
```

---

## 8. 辅助接口

## 8.1 获取筛选项枚举

**接口**

```text
GET /api/meta/filters
```

**用途**

前端一次性拉取筛选面板所需选项。

**示例返回**

```json
{
  "data": {
    "country_regions": ["USA", "Italy", "Germany", "China"],
    "bike_categories": ["race", "aero", "climbing", "endurance", "all-road"],
    "frame_materials": ["carbon", "aluminum", "titanium", "steel"],
    "groupset_brands": ["Shimano", "SRAM", "Campagnolo"],
    "component_categories": ["groupset", "wheelset", "tire", "power_meter", "cockpit", "saddle", "pedal", "bike_computer"]
  }
}
```

---

## 8.2 健康检查接口

**接口**

```text
GET /api/health
```

**用途**

用于服务探活、部署检查。

**示例返回**

```json
{
  "status": "ok"
}
```

---

## 9. 推荐的第一阶段实现顺序

建议按以下顺序开发接口：

### 第一批
- `GET /api/health`
- `GET /api/brands`
- `GET /api/brands/{brand_id}`
- `GET /api/models`
- `GET /api/models/{model_id}`

### 第二批
- `GET /api/builds`
- `GET /api/builds/{build_id}`
- `GET /api/components`
- `GET /api/components/{component_id}`

### 第三批
- `GET /api/brands/{brand_id}/models`
- `GET /api/models/{model_id}/builds`
- `GET /api/search`
- `GET /api/meta/filters`

这样做的好处是：
- 可以尽快支撑品牌页与车型页
- 然后补配置页与零部件页
- 最后再做搜索与筛选增强

---

## 10. 第一阶段暂不做的接口

以下接口建议暂缓：

- `POST /api/brands`
- `PUT /api/brands/{brand_id}`
- `DELETE /api/brands/{brand_id}`
- 后台写接口
- 用户收藏接口
- 评论接口
- 天梯评分接口

原因很简单：
- 当前产品核心是“可查、可展示”，不是后台运营系统

---

## 11. 接口实现建议

### 11.1 列表接口

统一支持：
- 分页
- 筛选
- 排序
- 轻量字段返回

### 11.2 详情接口

返回完整字段，但不要无限递归嵌套。

例如：
- 品牌详情返回品牌本身
- 品牌下车型走独立接口

### 11.3 搜索接口

第一阶段用轻搜索即可：
- `LIKE`
- 标题优先
- 类型分组

---

## 12. 最终结论

第一阶段 API 目标非常明确：

- 先把 `brands / models / builds / components` 四类核心资源的查询接口做好
- 通过分页、筛选、详情和搜索，支撑一个结构清楚的公路车资料查询网站
- 先不做复杂写接口，也不做评分接口

一句话总结：

这套 API 不是为了花哨，而是为了让用户能够快速、清楚、稳定地查到公路车品牌、车型、配置和零部件信息。
