USE road_bike_db;

UPDATE brands
SET logo_url = 'https://www.logo.wine/a/logo/Canyon_Bicycles/Canyon_Bicycles-Logo.wine.svg'
WHERE brand_id = 'brand_006';

UPDATE models
SET image_url = 'https://dma.canyon.com/image/upload/w_2500,h_2500,c_fit/b_rgb:F2F2F2/f_auto/q_auto/v1749831869/2026_FULL_aeroad_cfr-di2_4039_R108_P01_bh6wi2'
WHERE model_id = 'model_016';

UPDATE builds
SET image_url = 'https://dma.canyon.com/image/upload/w_2500,h_2500,c_fit/b_rgb:F2F2F2/f_auto/q_auto/v1750063987/2026_FULL_aeroad_cfr-axs_4040_R108_P01_n51lb9'
WHERE build_id = 'build_017';

UPDATE components
SET image_url = 'https://www.merlincycles.com/assets/images/productImage_470_470_ffffff_image-jpeg/105032_shimano_ultegra_r8170_di2_disc_groupset_12_speed.jpg'
WHERE component_id = 'component_002';
