from sqlalchemy import create_engine, text

from app.core.config import get_settings

brands = [
    {
        'brand_name_en': 'Rose',
        'brand_name_cn': 'Rose',
        'country_region': 'Germany',
        'brand_type': 'complete_bike',
        'market_positioning': 'Value-focused Performance DTC Brand',
        'sales_model': 'Direct-to-Consumer',
        'main_road_categories': 'race; aero; endurance; all-road',
        'official_website': 'https://www.rosebikes.com',
        'headquarters': 'Bocholt, Germany',
        'founded_year': '1907',
        'founder': 'Rose family origins',
        'parent_company': 'ROSE Bikes GmbH',
        'company_type': 'Direct-to-Consumer Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'Rose 在公路车领域定位为强调德国直销体系、配置效率与现代高性能整车表达的价值型品牌。其产品覆盖竞赛、空气动力、耐力与 all-road 场景，在欧洲市场尤其具有较强存在感。',
        'target_audience': '重视价格性能比、现代整车配置和直销模式的公路车用户，包括进阶骑手和偏好德系理性消费路径的消费者。',
        'price_tier': 'Mid to Mid-High',
        'brand_slogan': 'Ride Beyond',
        'brand_story': 'Rose 的历史可追溯到 1907 年，是德国具有悠久零售和整车背景的自行车品牌。品牌在现代市场中通过直销和高完成度整车配置建立差异化，在公路车领域通过 Xlite、Reveal、Backroad 等平台形成清晰矩阵。',
        'mission': 'Rose 长期通过更直接的销售模式和更高效率的产品配置，为骑手提供更实际、更现代的骑行选择。',
        'core_values': 'Value efficiency; German practicality; Direct customer relationship; Modern product design; Broad usability',
        'core_technologies': 'Integrated cockpit and routing; modern carbon road chassis; endurance and all-road geometry development; DTC-driven product optimization',
        'r_and_d_capabilities': 'Rose 在现代公路整车平台开发、配置效率设计、直销场景下的商品化能力和多用途公路平台设计方面具备较强能力。',
        'flagship_platforms': 'Xlite; Reveal; Backroad',
        'employee_count_range': 'Mid-sized European DTC brand scale',
        'annual_revenue_range': 'Private company; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; Urban bikes; E-bikes; Accessories and apparel',
        'road_product_lines': 'Xlite; Reveal',
        'data_sources': 'Official Rose brand and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'Rose 的吸引力在于配置效率与德系直销逻辑。对用户而言，它通常意味着更理性、更务实的高性能整车选择。',
    },
    {
        'brand_name_en': 'Fuji',
        'brand_name_cn': 'Fuji',
        'country_region': 'Japan',
        'brand_type': 'complete_bike',
        'market_positioning': 'Legacy Mainstream Performance Brand',
        'sales_model': 'Global Dealer Network',
        'main_road_categories': 'race; endurance; all-round',
        'official_website': 'https://www.fujibikes.com',
        'headquarters': 'Brand heritage rooted in Japan; modern business operations vary by market structure',
        'founded_year': '1899',
        'founder': 'Nichibei Fuji Cycle Company historical origins',
        'parent_company': 'Modern ownership and distribution context varies by region',
        'company_type': 'Legacy Bicycle Brand',
        'ownership_type': 'Brand under changing global ownership structures over time',
        'road_cycling_positioning': 'Fuji 在公路车领域定位为具有长期历史积累的大众性能品牌，强调可及性、传统品牌认知与较广价格带覆盖。其公路线更多面向大众性能、进阶入门与传统品牌偏好的用户群。',
        'target_audience': '希望选择历史悠久、认知稳定、产品覆盖较广的公路车品牌用户，包括入门升级和大众性能消费者。',
        'price_tier': 'Entry-Mid to Mid-High',
        'brand_slogan': 'Conquer the Earth',
        'brand_story': 'Fuji 创立于 1899 年，是日本历史最悠久的自行车品牌之一。品牌在全球市场长期保持较高认知度，并在公路车、场地和大众骑行市场都拥有长期存在感。',
        'mission': 'Fuji 长期通过覆盖广泛的产品线和稳定品牌认知，为更多骑手提供可进入、可持续升级的骑行产品。',
        'core_values': 'Legacy; Accessibility; Reliability; Broad product coverage; Enduring brand recognition',
        'core_technologies': 'Modern carbon and aluminum road frame development; mainstream race geometry; broad-range platform adaptation',
        'r_and_d_capabilities': 'Fuji 在广价格带整车平台、入门到进阶公路车和传统品牌平台延续方面具备成熟能力，但整体更偏稳定产品体系而非极端高端技术叙事。',
        'flagship_platforms': 'SL; Transonic; Gran Fondo',
        'employee_count_range': 'Legacy brand under broader global operations',
        'annual_revenue_range': 'Not typically disclosed as standalone brand',
        'product_lines': 'Road bikes; Track bikes; Gravel bikes; Mountain bikes; Urban bikes; Accessories',
        'road_product_lines': 'SL; Transonic; Gran Fondo',
        'data_sources': 'Official Fuji brand and product pages; public brand histories; cycling media summaries',
        'notes': 'Fuji 更像一条历史悠久但面向大众性能市场的稳定品牌线，对用户而言价值在于品牌熟悉度与产品覆盖面。',
    },
    {
        'brand_name_en': 'BH',
        'brand_name_cn': 'BH',
        'country_region': 'Spain',
        'brand_type': 'complete_bike',
        'market_positioning': 'Performance-oriented European Brand',
        'sales_model': 'Global Dealer Network',
        'main_road_categories': 'race; aero; endurance; e-road',
        'official_website': 'https://www.bhbikes.com',
        'headquarters': 'Vitoria-Gasteiz, Spain',
        'founded_year': '1909',
        'founder': 'Beistegui Hermanos',
        'parent_company': 'BH Bikes',
        'company_type': 'Performance Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'BH 在公路车领域定位为具有西班牙历史背景、覆盖竞赛与现代整车市场的欧洲性能品牌。其平台覆盖空气动力、综合竞赛和 e-road 方向，在欧洲市场拥有稳定存在感。',
        'target_audience': '希望获得成熟欧洲品牌、较完整产品覆盖和相对均衡性能价格比的公路车用户。',
        'price_tier': 'Mid to Mid-High',
        'brand_slogan': 'Be Ahead',
        'brand_story': 'BH 源自西班牙百年工业背景，是欧洲历史悠久的自行车品牌之一。品牌在现代公路车市场中通过 Aerolight、Ultralight、RS1 等平台继续覆盖竞赛与高性能市场。',
        'mission': 'BH 长期通过技术发展和整车平台演进，为骑手提供更高效、更全面的骑行产品选择。',
        'core_values': 'European heritage; Performance; Broad usability; Engineering continuity; Practical innovation',
        'core_technologies': 'Aero race frame development; lightweight all-round chassis; e-road integration; modern cable and cockpit integration',
        'r_and_d_capabilities': 'BH 在竞赛平台、空气动力平台和电助力公路整车开发方面具备成熟能力，整体风格偏均衡和市场导向。',
        'flagship_platforms': 'Aerolight; Ultralight; RS1',
        'employee_count_range': 'Heritage European brand scale',
        'annual_revenue_range': 'Private company; exact public figures limited',
        'product_lines': 'Road bikes; E-road bikes; Gravel bikes; Mountain bikes; Urban bikes; Accessories',
        'road_product_lines': 'Aerolight; Ultralight; RS1',
        'data_sources': 'Official BH brand and product pages; public cycling media summaries; brand history references',
        'notes': 'BH 是一条更偏均衡型的欧洲老牌线，对用户而言价值在于稳定、全面且更接近欧陆传统品牌逻辑。',
    },
    {
        'brand_name_en': 'Chapter2',
        'brand_name_cn': 'Chapter2',
        'country_region': 'New Zealand',
        'brand_type': 'complete_bike',
        'market_positioning': 'Boutique Design-led Premium Brand',
        'sales_model': 'Global Dealer Network + Select Direct Channels',
        'main_road_categories': 'race; aero; all-round; gravel',
        'official_website': 'https://www.chapter2bikes.com',
        'headquarters': 'Auckland, New Zealand',
        'founded_year': '2017',
        'founder': 'Mike Pryde',
        'parent_company': 'Chapter2 Bikes',
        'company_type': 'Boutique Premium Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'Chapter2 在公路车领域定位为强调设计感、精品品牌体验和现代高性能平台的小众高端品牌。其品牌形象更偏审美驱动、精品路线和国际化生活方式表达。',
        'target_audience': '重视设计、颜色方案、精品品牌气质与较小众高端平台体验的公路车用户，包括审美导向型消费者与发烧友。',
        'price_tier': 'Premium to Luxury',
        'brand_slogan': 'Designed in New Zealand',
        'brand_story': 'Chapter2 由 Mike Pryde 创建，是近年成长起来的精品高端自行车品牌。品牌在公路车市场通过更强调设计感、品牌故事和现代高性能平台的方式建立认知，在 Koko、Toa、Rira 等平台上体现其产品语言。',
        'mission': 'Chapter2 长期通过设计、品牌文化与高性能平台结合，为骑手提供更具个性和辨识度的高端骑行体验。',
        'core_values': 'Design-led identity; Boutique premium experience; Modern performance; Global lifestyle branding; Product individuality',
        'core_technologies': 'Modern carbon race chassis; aero road design; boutique paint and finish execution; integrated cockpit options',
        'r_and_d_capabilities': 'Chapter2 在高端小众平台开发、整车视觉语言塑造与精品品牌化表达方面具备较强能力，但整体更偏精品市场而非大规模矩阵覆盖。',
        'flagship_platforms': 'Koko; Toa; Rira; Aeolus',
        'employee_count_range': 'Boutique premium brand scale',
        'annual_revenue_range': 'Private boutique brand; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Framesets; Accessories and lifestyle-oriented brand products',
        'road_product_lines': 'Koko; Toa; Rira',
        'data_sources': 'Official Chapter2 product pages; public cycling media summaries; brand founder interviews and market coverage',
        'notes': 'Chapter2 的核心吸引力在于精品高端路线与设计感，对用户而言更像一条具有生活方式属性的小众高端公路线。',
    },
]


def next_brand_id(conn):
    rows = conn.execute(text("SELECT brand_id FROM brands WHERE brand_id LIKE 'brand_%'" )).fetchall()
    used = set()
    for (brand_id,) in rows:
        try:
            used.add(int(brand_id.split('_')[1]))
        except Exception:
            continue
    candidate = 1
    while candidate in used:
        candidate += 1
    return f'brand_{candidate:03d}'


def main():
    settings = get_settings()
    engine = create_engine(settings.database_url)
    insert_stmt = text("""
        INSERT INTO brands (
            brand_id, brand_name_en, brand_name_cn, country_region, brand_type, market_positioning,
            sales_model, main_road_categories, official_website, headquarters, founded_year, founder,
            parent_company, company_type, ownership_type, road_cycling_positioning, target_audience,
            price_tier, brand_slogan, brand_story, mission, core_values, core_technologies,
            r_and_d_capabilities, flagship_platforms, employee_count_range, annual_revenue_range,
            product_lines, road_product_lines, data_sources, notes
        ) VALUES (
            :brand_id, :brand_name_en, :brand_name_cn, :country_region, :brand_type, :market_positioning,
            :sales_model, :main_road_categories, :official_website, :headquarters, :founded_year, :founder,
            :parent_company, :company_type, :ownership_type, :road_cycling_positioning, :target_audience,
            :price_tier, :brand_slogan, :brand_story, :mission, :core_values, :core_technologies,
            :r_and_d_capabilities, :flagship_platforms, :employee_count_range, :annual_revenue_range,
            :product_lines, :road_product_lines, :data_sources, :notes
        )
    """)

    inserted = []
    with engine.begin() as conn:
        for brand in brands:
            payload = dict(brand)
            payload['brand_id'] = next_brand_id(conn)
            conn.execute(insert_stmt, payload)
            inserted.append((payload['brand_id'], payload['brand_name_en']))

    with engine.connect() as conn:
        for brand_id, _ in inserted:
            row = conn.execute(text("SELECT brand_id, brand_name_en, headquarters, founded_year, price_tier FROM brands WHERE brand_id = :brand_id"), {'brand_id': brand_id}).fetchone()
            print('\t'.join('' if value is None else str(value) for value in row))


if __name__ == '__main__':
    main()
