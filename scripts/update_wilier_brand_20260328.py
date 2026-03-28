from sqlalchemy import create_engine, text

from app.core.config import get_settings

payload = {
    'country_region': 'Italy',
    'market_positioning': 'Premium Heritage Racing Brand',
    'sales_model': 'Global Dealer Network',
    'main_road_categories': 'race; aero; endurance; gravel',
    'official_website': 'https://www.wilier.com',
    'headquarters': 'Rossano Veneto, Italy',
    'founded_year': '1906',
    'founder': 'Pietro Dal Molin',
    'parent_company': 'Wilier Triestina S.p.A.',
    'company_type': 'Heritage Performance Bicycle Brand',
    'ownership_type': 'Privately Held Company',
    'road_cycling_positioning': 'Wilier Triestina 在公路车领域定位为兼具意大利历史传承、现代竞赛性能与高端审美表达的精品高端品牌。其产品覆盖顶级竞赛、空气动力、耐力与 gravel 场景，在职业赛事与高端消费市场都具有较强识别度。',
    'target_audience': '重视意大利品牌历史、竞赛性能、外观设计和较高品牌辨识度的高端公路车用户，包括赛事爱好者、器材玩家和审美导向消费者。',
    'price_tier': 'Premium to Luxury',
    'brand_slogan': 'W il il l Italia',
    'brand_story': 'Wilier Triestina 创立于 1906 年，是意大利历史最悠久的公路车品牌之一。品牌名称中的 Triestina 具有鲜明历史背景，长期承载意大利工业、国家身份与自行车竞赛传统。在现代公路车领域，Wilier 通过 Filante SLR、Verticale SLR、Zero SLR、Granturismo 等平台，把意大利设计、高端工艺与职业赛事性能结合起来。',
    'mission': 'Wilier 长期通过高性能公路车和意大利设计语言，为骑手提供兼具速度、审美与品牌文化价值的高端骑行体验。',
    'core_values': 'Italian heritage; Racing spirit; Premium craftsmanship; Performance; Distinctive design identity',
    'core_technologies': 'SLR carbon race platform development; aerodynamic race frame shaping; lightweight climbing frame tuning; integrated cockpit systems; high-end paint and finishing identity',
    'r_and_d_capabilities': 'Wilier 在高端竞赛车架、空气动力平台、轻量化平台和整车设计表达方面具备成熟能力。品牌研发不仅关注平台性能，也高度重视高端整车的视觉完成度和品牌差异化。',
    'flagship_platforms': 'Filante SLR; Verticale SLR; Zero SLR; Granturismo SLR; Rave SLR',
    'employee_count_range': 'Premium heritage brand scale',
    'annual_revenue_range': 'Private premium brand; exact public figures limited',
    'product_lines': 'Road bikes; Gravel bikes; E-road and e-bikes; Mountain bikes; Framesets; Apparel and accessories',
    'road_product_lines': 'Filante SLR; Verticale SLR; Zero SLR; Granturismo SLR',
    'data_sources': 'Official Wilier history pages; Wilier official product pages; public cycling media brand histories; widely documented industry information',
    'notes': 'Wilier 的特点在于历史感、意大利高端品牌调性与现代竞赛平台的结合。对消费者而言，它通常代表更强的审美识别度和更浓厚的意式公路车文化氛围。',
    'brand_id': 'brand_014',
}


def main():
    settings = get_settings()
    engine = create_engine(settings.database_url)
    columns = [k for k in payload.keys() if k != 'brand_id']
    assignments = ',\n        '.join(f"{col} = :{col}" for col in columns)
    stmt = text(f"""
        UPDATE brands
        SET
        {assignments}
        WHERE brand_id = :brand_id
    """)

    with engine.begin() as conn:
        conn.execute(stmt, payload)

    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT brand_id, brand_name_en, brand_name_cn, headquarters, founded_year, price_tier
            FROM brands
            WHERE brand_id = 'brand_014'
        """)).fetchone()
        print('\t'.join('' if value is None else str(value) for value in row))


if __name__ == '__main__':
    main()
