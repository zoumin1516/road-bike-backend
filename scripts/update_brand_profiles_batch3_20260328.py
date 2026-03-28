from sqlalchemy import create_engine, text

from app.core.config import get_settings

profiles = {
    'brand_006': {
        'country_region': 'Germany',
        'market_positioning': 'High-value Premium DTC Brand',
        'sales_model': 'Direct-to-Consumer',
        'headquarters': 'Koblenz, Germany',
        'founded_year': '2002',
        'founder': 'Roman Arnold',
        'parent_company': 'Canyon Bicycles GmbH',
        'company_type': 'Direct-to-Consumer Performance Bicycle Brand',
        'ownership_type': 'Privately controlled company with investment backing over time',
        'road_cycling_positioning': 'Canyon 在公路车领域定位为以 DTC 模式驱动的高性能价值型品牌，强调更高配置效率、现代整车设计与清晰的平台分层。其产品覆盖空气动力、轻量竞赛、耐力与计时铁三，并依靠直销模式在全球公路车市场建立强势存在感。',
        'target_audience': '重视配置效率、价格性能比、现代整车设计和线上购买体验的公路车用户，包括进阶骑手、高性能消费者与愿意接受 DTC 模式的全球用户。',
        'price_tier': 'Mid-High to Premium',
        'brand_slogan': 'Inspired by Cycling',
        'brand_story': 'Canyon 创立于 2002 年，总部位于德国 Koblenz，是最具代表性的 DTC 自行车品牌之一。品牌通过直销模式、高完成度整车配置与强职业赛事曝光迅速建立国际影响力。在公路车方向，Canyon 通过 Aeroad、Ultimate、Endurace、Speedmax 等平台，构建了覆盖竞赛、耐力和铁三的完整体系。',
        'mission': 'Canyon 长期强调通过更直接的商业模式和高性能产品设计，让更多骑手获得更高效率、更具现代感的骑行产品体验。',
        'core_values': 'Value efficiency; Direct customer relationship; Modern engineering; Racing validation; Clean platform segmentation',
        'core_technologies': 'Integrated cockpit and cable routing; aerodynamic frame development; lightweight race chassis; modular fit-oriented cockpit options; direct-sales platform optimization',
        'r_and_d_capabilities': 'Canyon 在空气动力学、轻量竞赛平台、一体化座舱设计和整车商品化效率方面具备强项。其研发不仅体现在平台本身，也体现在如何通过 DTC 模式构建更具竞争力的整车配置。',
        'flagship_platforms': 'Aeroad; Ultimate; Endurace; Speedmax',
        'employee_count_range': '1000-5000',
        'annual_revenue_range': 'High hundreds of millions EUR equivalent (varies by year)',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; Triathlon bikes; E-bikes; Fitness and urban bikes; Accessories and apparel',
        'road_product_lines': 'Aeroad; Ultimate; Endurace; Speedmax',
        'data_sources': 'Official Canyon brand and product pages; public company summaries; widely documented industry information',
        'notes': 'Canyon 的核心优势是 DTC 模式带来的配置效率和现代整车完成度。对用户而言，它通常意味着更强的性价比与更鲜明的现代产品语言，但购买与售后体验也更依赖品牌直销体系。',
    },
    'brand_017': {
        'country_region': 'United Kingdom',
        'market_positioning': 'Boutique High-end Performance Brand',
        'sales_model': 'Dealer + Select Direct and Partner Channels',
        'headquarters': 'Norfolk, United Kingdom',
        'founded_year': '2007',
        'founder': 'Rob Gitelis is closely associated with the brand development context',
        'parent_company': 'Factor Bikes',
        'company_type': 'Boutique High-performance Bicycle Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'Factor 在公路车领域定位为精品化高性能品牌，强调顶级竞赛性能、空气动力学、高端用料与更小众的高端品牌气质。品牌在职业赛事平台和高端消费级竞赛车市场中具有很强的技术与形象辨识度。',
        'target_audience': '追求顶级竞赛性能、小众品牌识别度、高端工艺与职业赛事同源平台的高端公路车用户。',
        'price_tier': 'Premium to Luxury',
        'brand_slogan': 'Advanced Engineering for Speed',
        'brand_story': 'Factor 于 2000 年代后期建立品牌影响力，并逐步从高端工程和空气动力性能表达切入顶级公路车市场。品牌通过与职业车队合作，以及在 Ostro VAM、O2 VAM、Monza 等平台上的产品推进，形成了精品高端竞赛品牌定位。',
        'mission': 'Factor 长期强调通过先进工程与顶级性能平台，为高水平骑手和高端消费者提供更纯粹的速度体验。',
        'core_values': 'Advanced engineering; Exclusive performance; Boutique brand identity; Race-driven design; Lightweight and aero balance',
        'core_technologies': 'High-end carbon race chassis development; aero race optimization; lightweight VAM platform tuning; integrated cockpit systems',
        'r_and_d_capabilities': 'Factor 在高端碳架平台开发、空气动力学与轻量化平衡、整车一体化和职业赛事平台表达方面具备较强能力。其研发更强调旗舰产品精度和高端市场表达，而非大规模覆盖。',
        'flagship_platforms': 'Ostro VAM; O2 VAM; Monza; LS',
        'employee_count_range': 'Boutique premium brand scale',
        'annual_revenue_range': 'Private boutique brand; exact figures not typically public',
        'product_lines': 'Road bikes; Gravel bikes; High-end framesets; Accessories and apparel',
        'road_product_lines': 'Ostro VAM; O2 VAM; Monza',
        'data_sources': 'Official Factor product pages; public cycling media brand summaries; widely documented industry information',
        'notes': 'Factor 的最大特征是精品化高端定位。对用户而言，它通常意味着更小众、更有辨识度的高性能选择，同时价格也更高、更偏发烧友市场。',
    },
    'brand_015': {
        'country_region': 'France',
        'market_positioning': 'Heritage Innovation Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Nevers, France',
        'founded_year': '1951',
        'founder': 'Jean Beyl (brand founder context)',
        'parent_company': 'LOOK Cycle International',
        'company_type': 'Performance Bicycle and Pedal Systems Brand',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'LOOK 在公路车领域定位为兼具历史创新价值、法式技术传统与高端竞赛平台表达的品牌。它不仅因锁踏系统而具有行业级影响力，也在碳纤维公路车架和高端竞赛平台中保持独特品牌地位。',
        'target_audience': '重视品牌历史、技术创新传统与高端法系公路车气质的用户，包括高端爱好者、器材控和希望获得不同于主流大品牌审美与品牌体验的骑手。',
        'price_tier': 'Premium',
        'brand_slogan': 'Look Cycle',
        'brand_story': 'LOOK 由 Jean Beyl 于 1951 年创立，最初与滑雪固定系统相关，后在公路车领域因锁踏技术和碳纤维车架创新建立重要地位。品牌在现代公路车市场中通过 795、785 等平台延续其高端法式技术品牌形象。',
        'mission': 'LOOK 长期通过创新技术与独特品牌传统，为骑手提供兼具效率、历史感与差异化体验的高性能产品。',
        'core_values': 'Innovation heritage; French engineering identity; Technical originality; Premium riding experience; Distinct brand character',
        'core_technologies': 'Clipless pedal system heritage; carbon frame innovation; aero endurance race integration; high-end cockpit and chassis solutions',
        'r_and_d_capabilities': 'LOOK 在高端碳架开发、技术创新表达和配套骑行系统研发上具备长期积累。与主流大规模品牌相比，其研发更强调品牌技术传统和差异化体验。',
        'flagship_platforms': '795 Blade RS; 785 Huez; 765 Optimum',
        'employee_count_range': 'Specialized premium brand scale',
        'annual_revenue_range': 'Private brand; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Pedals; Framesets; Accessories',
        'road_product_lines': '795 Blade RS; 785 Huez; 765 Optimum',
        'data_sources': 'Official LOOK brand and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'LOOK 的公路车价值不只在参数层面，更在其作为行业创新者的历史地位。对用户而言，它是一种更小众但更有技术文化积累的高端选择。',
    },
    'brand_010': {
        'country_region': 'Spain',
        'market_positioning': 'Performance-oriented Mainstream Premium Brand',
        'sales_model': 'Global Dealer Network + Customization Channels',
        'headquarters': 'Mallabia, Basque Country, Spain',
        'founded_year': '1840',
        'founder': 'Orbea family origins in arms manufacturing; bicycle brand evolution came later',
        'parent_company': 'Orbea S. Coop.',
        'company_type': 'Worker-owned Cooperative Bicycle Company',
        'ownership_type': 'Cooperative',
        'road_cycling_positioning': 'Orbea 在公路车领域定位为兼具历史传承、现代竞赛平台与个性化定制表达的西班牙高性能品牌。其产品覆盖轻量竞赛、空气动力和耐力方向，并通过品牌定制服务形成差异化体验。',
        'target_audience': '希望获得成熟竞赛平台、品牌历史感和个性化配置体验的公路车用户，包括高端业余骑手、审美导向型消费者和重视品牌文化的用户。',
        'price_tier': 'Mid-High to Premium',
        'brand_slogan': 'Your Ride. Your Way.',
        'brand_story': 'Orbea 的历史可追溯至 19 世纪，是西班牙最具历史的工业品牌之一，后逐步发展为全球知名自行车品牌。其在公路车领域通过 Orca、Orca Aero 等平台形成清晰产品体系，并借助 MyO 等定制化路径强化品牌个性体验。',
        'mission': 'Orbea 长期强调让骑行体验更贴近个人表达，并通过设计、性能和定制化手段为更多用户提供高质量骑行产品。',
        'core_values': 'Heritage; Rider personalization; Performance; Design clarity; Cooperative culture',
        'core_technologies': 'OMX and OMR carbon platform development; aero race optimization; rider-specific customization via MyO; balanced climbing and aero chassis design',
        'r_and_d_capabilities': 'Orbea 在竞赛平台开发、品牌定制化体验、一体化产品设计和欧洲高端整车体系中具备成熟能力。其优势在于产品完成度与品牌个性化服务结合。',
        'flagship_platforms': 'Orca; Orca Aero; Avant',
        'employee_count_range': 'Mid-sized global brand with cooperative structure',
        'annual_revenue_range': 'Private cooperative; exact public figures vary by reporting context',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; Urban bikes; E-bikes; Triathlon-related offerings in some eras; Accessories',
        'road_product_lines': 'Orca; Orca Aero; Avant',
        'data_sources': 'Official Orbea history and product pages; public brand summaries; widely documented industry information',
        'notes': 'Orbea 的优势在于历史感、竞赛平台成熟度以及定制化体验。对用户而言，它通常是兼顾性能与品牌个性的平衡型高端选择。',
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
            WHERE brand_id IN ('brand_006','brand_010','brand_015','brand_017')
            ORDER BY brand_id
        """)).fetchall()
        for row in rows:
            print('\t'.join('' if v is None else str(v) for v in row))


if __name__ == '__main__':
    main()
