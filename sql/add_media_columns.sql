USE road_bike_db;

ALTER TABLE brands
  ADD COLUMN logo_url VARCHAR(512) NULL AFTER official_website,
  ADD COLUMN hero_image_url VARCHAR(512) NULL AFTER logo_url;

ALTER TABLE models
  ADD COLUMN image_url VARCHAR(512) NULL AFTER official_model_url,
  ADD COLUMN hero_image_url VARCHAR(512) NULL AFTER image_url;

ALTER TABLE builds
  ADD COLUMN image_url VARCHAR(512) NULL AFTER official_build_url,
  ADD COLUMN hero_image_url VARCHAR(512) NULL AFTER image_url;

ALTER TABLE components
  ADD COLUMN image_url VARCHAR(512) NULL AFTER official_url,
  ADD COLUMN hero_image_url VARCHAR(512) NULL AFTER image_url;
