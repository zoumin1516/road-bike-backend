from sqlalchemy import create_engine, text

from app.core.config import get_settings

profiles = {
    'brand_018': {
        'country_region': 'Belgium',
        'market_positioning': 'Premium Race and Classics-focused Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Beringen, Belgium',
        'founded_year': '1997',
        'founder': 'Jochim Aerts',
        'parent_company': 'Belgian Cycling Factory',
        'company_type': 'Performance Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'Ridley 在公路车领域定位为深受比利时赛事传统影响的高性能品牌，强调石头路古典赛血统、空气动力学竞赛平台与现代综合竞赛性能。其产品在职业公路和越野传统之间形成了鲜明的比利时竞赛品牌气质。',
        'target_audience': '重视赛事传统、空气动力性能、比利时古典赛文化与高性能竞赛平台的公路车用户，包括竞赛爱好者、发烧友和偏好欧陆赛事风格的消费者。',
        'price_tier': 'Mid-High to Premium',
        'brand_slogan': 'Performance in Every Fiber',
        'brand_story': 'Ridley 创立于 1997 年，是比利时最具代表性的高性能自行车品牌之一。品牌长期与职业车队及石头路赛事文化紧密相关，通过 Noah、Helium、Falcn、Grifn 等平台，在公路竞赛、全能性能与 gravel 方向形成了清晰布局。',
        'mission': 'Ridley 长期强调通过赛事验证和高性能平台开发，为骑手提供更直接、更高效且更具竞赛文化认同的骑行体验。',
        'core_values': 'Belgian racing heritage; Performance; Classics DNA; Aerodynamic efficiency; Versatility across modern road use',
        'core_technologies': 'Aero frame development; lightweight race chassis tuning; classics-inspired handling refinement; integrated cockpit and cable systems',
        'r_and_d_capabilities': 'Ridley 在竞赛车架空气动力学、石头路和古典赛场景下的操控调校、轻量化平台和多用途平台开发方面具有较强能力。品牌研发长期与欧洲赛事文化和职业应用场景相结合。',
        'flagship_platforms': 'Noah Fast; Falcn RS; Helium SLX; Grifn',
        'employee_count_range': 'Mid-sized premium brand scale',
        'annual_revenue_range': 'Private company; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Cyclocross bikes; Mountain bikes; Framesets; Accessories',
        'road_product_lines': 'Noah Fast; Falcn RS; Helium SLX',
        'data_sources': 'Official Ridley brand and product pages; Belgian Cycling Factory summaries; public cycling media brand coverage',
        'notes': 'Ridley 的强项在于鲜明的比利时赛事文化背景和竞赛平台表达。对很多用户而言，它代表更具赛事气质和更接近古典赛文化的欧陆竞赛体验。',
    },
    'brand_025': {
        'country_region': 'Canada',
        'market_positioning': 'Premium Performance and Fit-focused Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Montreal, Quebec, Canada',
        'founded_year': '1989',
        'founder': 'Gervais Rioux',
        'parent_company': 'Argon 18 Bikes Inc.',
        'company_type': 'Performance Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'Argon 18 在公路车领域定位为强调性能、骑行姿态优化与职业赛事应用的加拿大高端品牌。其产品覆盖公路竞赛、耐力与铁三领域，品牌在 fit、几何和系统化骑行效率方面具有明确特色。',
        'target_audience': '重视骑行姿态、整车效率和较小众高性能品牌体验的公路车用户，包括赛事骑手、铁三用户以及对 fitting 更敏感的高端消费者。',
        'price_tier': 'Premium',
        'brand_slogan': 'Real Performance',
        'brand_story': 'Argon 18 创立于 1989 年，总部位于加拿大蒙特利尔。品牌长期将空气动力、几何优化和 rider fit 作为重要产品哲学，并通过 Gallium、Nitrogen、Krypton、Sum 等平台建立在公路车与铁三市场中的独特形象。',
        'mission': 'Argon 18 长期通过性能工程、姿态优化和高效整车平台，帮助骑手更快、更舒适地输出自身能力。',
        'core_values': 'Fit-first thinking; Performance; Engineering precision; Rider efficiency; Boutique premium experience',
        'core_technologies': 'Argon Fit System concepts; aero race chassis; endurance geometry refinement; integrated front-end systems; triathlon platform expertise',
        'r_and_d_capabilities': 'Argon 18 在整车姿态优化、公路竞赛平台、铁三整车系统和高端小众品牌产品开发方面具备成熟能力。品牌研发叙事较强地围绕 fit 和 efficiency 展开。',
        'flagship_platforms': 'Sum Pro; Gallium; Krypton; Nitrogen',
        'employee_count_range': 'Boutique premium brand scale',
        'annual_revenue_range': 'Private company; exact public figures limited',
        'product_lines': 'Road bikes; Triathlon bikes; Gravel bikes; Framesets; Accessories',
        'road_product_lines': 'Sum Pro; Gallium; Krypton; Nitrogen',
        'data_sources': 'Official Argon 18 brand and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'Argon 18 的差异点在于更强调 fit、几何和效率平衡。对用户而言，它常常是更偏工程和实战输出导向的小众高端选择。',
    },
    'brand_022': {
        'country_region': 'France',
        'market_positioning': 'High-end Composite Craftsmanship Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Voreppe, France',
        'founded_year': '1987',
        'founder': 'TIME Sport brand origins in France',
        'parent_company': 'TIME Bicycles',
        'company_type': 'High-end Composite Performance Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'TIME 在公路车领域定位为强调高端复合材料工艺、法式技术传统与精品高性能体验的品牌。它在车架制造工艺层面具有很强独特性，面向更重视工艺与材料表达的高端公路车用户。',
        'target_audience': '重视高端复合材料工艺、品牌独特制造技术与精品公路车体验的高端用户，包括器材发烧友和工艺导向型消费者。',
        'price_tier': 'Premium to Luxury',
        'brand_slogan': 'Engineered with Time',
        'brand_story': 'TIME 起源于法国，在锁踏和复合材料领域都具有强烈技术标签。品牌在公路车市场中长期坚持更独特的复合材料制造工艺与高端精品路线，使其在现代高端公路车品牌中保持鲜明差异化。',
        'mission': 'TIME 长期通过更独特的制造工艺和高性能整车表达，提供兼具工艺价值、骑行体验和品牌独特性的精品产品。',
        'core_values': 'Composite craftsmanship; French engineering identity; Premium differentiation; Technical originality; Ride quality',
        'core_technologies': 'Braided carbon and resin-transfer-related frame craftsmanship heritage; high-end road chassis tuning; premium layup execution',
        'r_and_d_capabilities': 'TIME 在高端复合材料车架工艺、整车骑感调校和精品制造路线方面具有明显差异化优势。品牌研发重点更多体现在工艺路径和骑行质感，而非大规模平台覆盖。',
        'flagship_platforms': 'Alpe d’Huez; Scylon; ADHX',
        'employee_count_range': 'Boutique premium manufacturing brand scale',
        'annual_revenue_range': 'Private premium brand; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Framesets; Pedals; High-end accessories',
        'road_product_lines': 'Alpe d’Huez; Scylon',
        'data_sources': 'Official TIME brand and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'TIME 的价值高度体现在工艺和材料表达上。对用户而言，它是更偏精品和技术信仰型的高端公路车品牌。',
    },
    'brand_016': {
        'country_region': 'France',
        'market_positioning': 'Performance-oriented Mainstream Premium Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Dijon, France',
        'founded_year': '1946',
        'founder': 'Gaston Lapierre',
        'parent_company': 'Accell Group',
        'company_type': 'Performance Bicycle Brand',
        'ownership_type': 'Brand under a larger bicycle group structure',
        'road_cycling_positioning': 'Lapierre 在公路车领域定位为兼具法国赛事传统、现代竞赛平台与较高产品可及性的高性能品牌。其产品覆盖竞赛和耐力场景，在欧洲市场有较强存在感。',
        'target_audience': '希望获得成熟竞赛平台、法系品牌文化与相对均衡性能价格比的公路车用户，包括进阶骑手和赛事爱好者。',
        'price_tier': 'Mid-High to Premium',
        'brand_slogan': 'Over the Limits',
        'brand_story': 'Lapierre 创立于 1946 年，是法国历史悠久的自行车品牌之一。品牌长期与欧洲职业赛事和法国骑行文化相关联，在公路车方向通过 Xelius、Aircode、Pulsium 等平台建立了竞赛与耐力并行的产品结构。',
        'mission': 'Lapierre 长期强调通过技术创新与赛事验证，为骑手提供更高效、更有乐趣且更接近职业赛场体验的整车产品。',
        'core_values': 'Racing heritage; Accessibility to performance; French cycling culture; Balanced product value; Innovation',
        'core_technologies': 'Aero race platform development; lightweight all-round race chassis; endurance frame comfort design; integrated cockpit options',
        'r_and_d_capabilities': 'Lapierre 在竞赛平台、空气动力平台、耐力平台与多价格带覆盖方面具有成熟能力。品牌研发更偏向实用化与产品矩阵均衡，而非极端小众高端路线。',
        'flagship_platforms': 'Xelius; Aircode; Pulsium',
        'employee_count_range': 'Part of larger European bike group context',
        'annual_revenue_range': 'Not usually disclosed separately as standalone brand',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; E-bikes; Urban bikes; Accessories',
        'road_product_lines': 'Xelius; Aircode; Pulsium',
        'data_sources': 'Official Lapierre brand and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'Lapierre 的优势在于法系赛事背景与较完整的产品矩阵。对用户而言，它是兼顾性能、品牌传统和市场可及性的平衡型选择。',
    },
    'brand_021': {
        'country_region': 'Italy',
        'market_positioning': 'Boutique Heritage Premium Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Cusano Milanino, Italy',
        'founded_year': '1953',
        'founder': 'Ugo De Rosa',
        'parent_company': 'De Rosa Bikes',
        'company_type': 'Boutique Heritage Performance Bicycle Brand',
        'ownership_type': 'Privately Held Company',
        'road_cycling_positioning': 'De Rosa 在公路车领域定位为兼具意大利工艺传统、家族品牌历史与现代高端公路车性能表达的精品品牌。其价值不仅体现在竞赛平台上，也体现在品牌文化和意大利高端手工传统的延续上。',
        'target_audience': '重视意大利工艺、家族品牌传统、高端品牌情感价值与精品竞赛平台的公路车用户，包括收藏型和审美导向型消费者。',
        'price_tier': 'Premium to Luxury',
        'brand_slogan': 'Cuore Rosso',
        'brand_story': 'De Rosa 由 Ugo De Rosa 于 1953 年创立，是意大利最具传奇色彩的家族自行车品牌之一。品牌长期与职业赛事和意大利高端工艺相关联，在现代公路车市场中通过 Merak、70、IDOL 等平台延续其竞赛与审美传统。',
        'mission': 'De Rosa 长期通过意大利家族工艺、品牌历史和高性能平台，为骑手提供兼具文化价值和骑行表现的高端公路车体验。',
        'core_values': 'Italian craftsmanship; Family heritage; Premium emotional value; Racing tradition; Design identity',
        'core_technologies': 'High-end carbon race frame development; boutique frame finishing; race-oriented geometry refinement; premium design execution',
        'r_and_d_capabilities': 'De Rosa 在高端竞赛车架、精品工艺表达、品牌化设计和高端公路平台方面具备成熟能力。其研发叙事更偏向品牌文化与产品情感价值，而非大规模工业覆盖。',
        'flagship_platforms': 'Merak; 70; IDOL',
        'employee_count_range': 'Boutique heritage brand scale',
        'annual_revenue_range': 'Private premium brand; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Framesets; High-end accessories',
        'road_product_lines': 'Merak; 70; IDOL',
        'data_sources': 'Official De Rosa brand and product pages; public cycling media histories; widely documented industry information',
        'notes': 'De Rosa 的吸引力在于强烈的品牌文化和意大利精品传统。对用户而言，它更像是兼具骑行性能与品牌情感价值的高端选择。',
    },
}


def main():
    settings = get_settings()
    engine = create_engine(settings.database_url)
    columns = list(next(iter(profiles.values())).keys())
    assignments = ',\n        '.join(f"{col} = :{col}" for col in columns)
    stmt = text(f"""
        UPDATE brands
        SET
        {assignments}
        WHERE brand_id = :brand_id
    """)

    with engine.begin() as conn:
        for brand_id, payload in profiles.items():
            conn.execute(stmt, {**payload, 'brand_id': brand_id})

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT brand_id, brand_name_en, headquarters, founded_year, price_tier
            FROM brands
            WHERE brand_id IN ('brand_016','brand_018','brand_021','brand_022','brand_025')
            ORDER BY brand_id
        """)).fetchall()
        for row in rows:
            print('\t'.join('' if v is None else str(v) for v in row))


if __name__ == '__main__':
    main()
