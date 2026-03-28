from sqlalchemy import create_engine, text

from app.core.config import get_settings

payload = {
    'country_region': 'Italy',
    'market_positioning': 'Premium Heritage Performance Brand',
    'sales_model': 'Global Dealer Network',
    'main_road_categories': 'race; aero; climbing; endurance',
    'official_website': 'https://www.bianchi.com',
    'headquarters': 'Treviglio, Italy',
    'founded_year': '1885',
    'founder': 'Edoardo Bianchi',
    'parent_company': 'Bianchi Milano / current corporate structure under modern ownership context',
    'company_type': 'Heritage Performance Bicycle Brand',
    'ownership_type': 'Privately controlled brand within modern bicycle ownership structures',
    'road_cycling_positioning': 'Bianchi 在公路车领域定位为兼具意大利历史传承、职业赛事记忆与现代高端竞赛平台的标志性品牌。其品牌价值不仅在性能平台本身，也在极高的历史认知度、Celeste 视觉语言和意式高端公路车文化中的长期地位。',
    'target_audience': '重视品牌历史、意大利设计语言、高辨识度外观与成熟竞赛平台的公路车用户，包括高端业余骑手、器材爱好者与品牌文化导向消费者。',
    'price_tier': 'Mid-High to Premium',
    'brand_slogan': 'Bianchi. Since 1885.',
    'brand_story': 'Bianchi 由 Edoardo Bianchi 于 1885 年创立，是世界上最古老、最具辨识度的自行车品牌之一。品牌与意大利自行车文化和职业公路赛事历史紧密相连，Celeste 配色更成为行业最具代表性的品牌视觉之一。在现代公路车市场，Bianchi 通过 Oltre、Specialissima、Sprint、Infinito 等平台延续其竞赛与高端品牌形象。',
    'mission': 'Bianchi 长期通过历史传承、设计语言与现代竞赛平台，为骑手提供兼具文化价值、品牌身份和骑行性能的高端体验。',
    'core_values': 'Italian heritage; Brand identity; Racing tradition; Design distinction; Performance with culture',
    'core_technologies': 'Aero race frame development; lightweight climbing chassis tuning; high-end carbon layup execution; integrated cockpit solutions; strong visual brand identity through paint and finish',
    'r_and_d_capabilities': 'Bianchi 在现代公路竞赛平台、空气动力学、轻量化平台与高端整车表达方面具备成熟研发能力。其研发与品牌叙事既关注平台性能，也高度重视历史感和视觉识别度。',
    'flagship_platforms': 'Oltre; Specialissima; Sprint; Infinito',
    'employee_count_range': 'Heritage premium brand scale',
    'annual_revenue_range': 'Private or group-owned premium brand context; exact public figures limited',
    'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; E-bikes; Urban bikes; Framesets; Accessories and apparel',
    'road_product_lines': 'Oltre; Specialissima; Sprint; Infinito',
    'data_sources': 'Official Bianchi history and product pages; public cycling media summaries; widely documented industry information',
    'notes': 'Bianchi 的价值非常依赖品牌历史和视觉辨识度，同时也具备成熟的现代竞赛平台。对用户而言，它既是性能平台，也是意大利公路车文化的象征性选择。',
    'brand_id': 'brand_013',
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
            SELECT brand_id, brand_name_en, headquarters, founded_year, price_tier
            FROM brands
            WHERE brand_id = 'brand_013'
        """)).fetchone()
        print('\t'.join('' if value is None else str(value) for value in row))


if __name__ == '__main__':
    main()
