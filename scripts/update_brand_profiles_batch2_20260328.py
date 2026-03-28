from sqlalchemy import create_engine, text

from app.core.config import get_settings

profiles = {
    'brand_004': {
        'country_region': 'United States',
        'market_positioning': 'Performance-focused Mainstream to High-end Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Wilton, Connecticut, United States',
        'founded_year': '1971',
        'founder': 'Joe Montgomery',
        'parent_company': 'Pon.Bike (current ownership context)',
        'company_type': 'Performance Bicycle Brand',
        'ownership_type': 'Privately Owned under a larger mobility group',
        'road_cycling_positioning': 'Cannondale 在公路车领域定位为强调工程创新、骑行乐趣与高性能体验的主流高端品牌。其公路线覆盖顶级竞赛、耐力、公路铝架性能与大众升级市场，在轻量化、操控与品牌个性表达上具备鲜明辨识度。',
        'target_audience': '希望获得成熟竞赛平台、工程感强的产品体验和更鲜明品牌调性的公路车用户，包括进阶骑手、赛事用户与偏好美式性能品牌的消费者。',
        'price_tier': 'Mid-High to Premium',
        'brand_slogan': 'Never Stop Riding',
        'brand_story': 'Cannondale 创立于 1971 年，早期以骑行装备起家，随后凭借铝合金车架创新和更具实验性的工程表达在整车市场建立声誉。品牌在公路车方向长期强调操控、轻量和独特技术路线，通过 SuperSix EVO、Synapse、CAAD 系列等平台覆盖竞赛、耐力和高性能铝架市场。',
        'mission': 'Cannondale 长期把让骑行更有乐趣、更高性能、更有个性作为品牌表达的重要方向，并强调通过工程创新改善骑行体验。',
        'core_values': 'Engineering-led innovation; Ride feel; Distinctive design; Performance accessibility; Brand individuality',
        'core_technologies': 'SystemSix aero integration heritage; SAVE micro-suspension concepts; CAAD aluminum frame development; carbon race platform tuning; integrated front-end development',
        'r_and_d_capabilities': 'Cannondale 在轻量竞赛车架、铝架平台开发、舒适性结构设计与整车操控调校方面具有长期积累。品牌擅长把工程创新与骑行体验叙事结合，在主流高端市场中保持较强差异化。',
        'flagship_platforms': 'SuperSix EVO; Synapse; CAAD13; SystemSix',
        'employee_count_range': 'Part of larger global cycling group; exact standalone figures vary',
        'annual_revenue_range': 'Not typically disclosed separately from parent context',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; Urban bikes; E-bikes; Apparel and accessories',
        'road_product_lines': 'SuperSix EVO; Synapse; CAAD13; SystemSix',
        'data_sources': 'Official Cannondale history and product pages; public brand summaries; widely documented industry information',
        'notes': 'Cannondale 的优势在于平台个性明显、工程路线清晰、铝架和碳架都有强记忆点。对用户而言，它通常意味着更鲜明的品牌性格与较强的骑行感导向。',
    },
    'brand_005': {
        'country_region': 'Canada',
        'market_positioning': 'Premium Aero and Race-focused Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Toronto, Ontario, Canada',
        'founded_year': '1995',
        'founder': 'Gerard Vroomen; Phil White',
        'parent_company': 'Pon.Bike (current ownership context)',
        'company_type': 'Performance Bicycle Brand',
        'ownership_type': 'Privately Owned under a larger mobility group',
        'road_cycling_positioning': 'Cervelo 在公路车领域定位为强调空气动力学、竞赛性能与工程效率的高端品牌。品牌长期与铁三和职业公路竞赛有强关联，在高性能竞赛平台、爬坡平台和耐力平台方面都形成了清晰产品结构。',
        'target_audience': '偏好竞赛性能、空气动力效率和职业赛事同源平台的公路车用户，包括高性能爱好者、铁三用户和更重视工程理性的消费者。',
        'price_tier': 'Premium',
        'brand_slogan': 'Simply Faster',
        'brand_story': 'Cervelo 创立于 1995 年，以工程先行的产品方法论迅速在高性能公路与铁三市场建立影响力。品牌擅长通过空气动力学、结构设计与竞赛验证塑造高端平台，在 S5、R5、Caledonia 与 P 系列等车型中形成鲜明产品个性。',
        'mission': 'Cervelo 长期围绕速度、效率和工程最优解构建品牌价值，强调通过数据和设计让骑手更快。',
        'core_values': 'Engineering efficiency; Speed; Aerodynamic advantage; Race validation; Data-driven product development',
        'core_technologies': 'Aero race chassis development; lightweight climbing platform tuning; integrated cockpit systems; race-driven geometry refinement; triathlon-focused aerodynamic design heritage',
        'r_and_d_capabilities': 'Cervelo 在空气动力学、公路竞赛几何、轻量高性能平台与铁三平台设计方面具有强项。品牌研发叙事高度集中于性能最优化与职业赛事应用场景。',
        'flagship_platforms': 'S5; R5; Soloist; Caledonia; P-Series',
        'employee_count_range': 'Specialized premium brand scale; exact standalone figures vary',
        'annual_revenue_range': 'Not usually disclosed separately from parent context',
        'product_lines': 'Road bikes; Triathlon and TT bikes; Gravel bikes; Framesets; Accessories',
        'road_product_lines': 'S5; R5; Soloist; Caledonia',
        'data_sources': 'Official Cervelo history and product pages; public brand summaries; widely documented industry information',
        'notes': 'Cervelo 的核心优势在于工程叙事清晰、竞赛平台强、空气动力学品牌认知突出。对消费者而言，它通常意味着更鲜明的速度机器属性。',
    },
    'brand_008': {
        'country_region': 'Switzerland',
        'market_positioning': 'Premium Performance Cycling Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Grenchen, Switzerland',
        'founded_year': '1986',
        'founder': 'Bob Bigelow',
        'parent_company': 'BMC Switzerland AG',
        'company_type': 'Premium Performance Bicycle Brand',
        'ownership_type': 'Privately Held Company',
        'road_cycling_positioning': 'BMC 在公路车领域定位为强调瑞士工程、职业赛事性能与高端整车系统化体验的品牌。其产品覆盖竞赛、耐力和空气动力公路场景，整体风格偏理性、精密和现代高端。',
        'target_audience': '注重工程感、品牌高级感与职业赛事背书的公路车用户，包括高端骑手、赛事爱好者以及偏好瑞士高性能品牌的消费者。',
        'price_tier': 'Premium',
        'brand_slogan': 'Speed Uncompromised',
        'brand_story': 'BMC 创立于 1986 年，总部位于瑞士 Grenchen。品牌长期将瑞士工程、职业赛事验证与高端整车体验结合起来，在公路车方向通过 Teammachine、Roadmachine、Timemachine 等平台建立全球影响力。',
        'mission': 'BMC 强调通过高性能工程与系统化整车设计为骑手提供更快、更完整的骑行体验。',
        'core_values': 'Swiss engineering; Precision; Integrated performance; Racing validation; Premium user experience',
        'core_technologies': 'ACE frame design concepts; integrated cockpit systems; aerodynamic frame shaping; race platform tuning; endurance-comfort engineering',
        'r_and_d_capabilities': 'BMC 在整车一体化设计、空气动力学优化、竞赛车架调校与高端用户体验层面具备成熟研发能力。其产品往往强调系统整合度和整车完成度。',
        'flagship_platforms': 'Teammachine; Roadmachine; Timemachine',
        'employee_count_range': 'Premium brand scale; exact public figure varies',
        'annual_revenue_range': 'Private premium brand; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; Triathlon and TT bikes; E-bikes; Accessories',
        'road_product_lines': 'Teammachine; Roadmachine; Timemachine',
        'data_sources': 'Official BMC corporate and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'BMC 的优势在于整车完成度高、设计语言统一、工程感强。对很多用户而言，它代表高端、理性和职业赛事导向的整车体验。',
    },
    'brand_011': {
        'country_region': 'Italy',
        'market_positioning': 'Top-tier Heritage Racing Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Villorba, Treviso, Italy',
        'founded_year': '1952',
        'founder': 'Giovanni Pinarello',
        'parent_company': 'Cicli Pinarello S.r.l.',
        'company_type': 'Heritage Performance Bicycle Brand',
        'ownership_type': 'Privately controlled premium brand',
        'road_cycling_positioning': 'Pinarello 在公路车领域定位为意大利顶级竞赛品牌，兼具职业赛事荣耀、品牌辨识度与高端消费象征属性。其平台长期与顶级车队和大环赛胜利绑定，在高端竞赛整车市场拥有极强品牌影响力。',
        'target_audience': '重视顶级赛事血统、品牌象征意义和高辨识度外观设计的高端公路车用户，包括竞赛发烧友、品牌导向型消费者和高端收藏或体验型骑手。',
        'price_tier': 'Premium to Luxury',
        'brand_slogan': 'The True Soul of a Bicycle',
        'brand_story': 'Pinarello 由 Giovanni Pinarello 于 1952 年创立，是现代职业公路赛事中最具代表性的意大利品牌之一。品牌通过 Dogma 系列以及长期的顶级车队合作，建立了极强的冠军品牌心智。在现代公路车市场，Pinarello 把竞赛性能、意大利设计语言和品牌荣誉感紧密绑定。',
        'mission': 'Pinarello 长期通过顶级竞赛平台、意大利设计与高端产品体验传递速度、荣耀与品牌传统。',
        'core_values': 'Racing heritage; Prestige; Italian design; Championship validation; High-end brand identity',
        'core_technologies': 'Asymmetric frame concepts; aerodynamic race integration; high-end carbon race chassis; handling-focused pro-level tuning',
        'r_and_d_capabilities': 'Pinarello 在顶级竞赛车架开发、职业赛事反馈转化、空气动力学外形设计和高端品牌化表达方面具备深厚积累。其研发和品牌叙事高度依赖顶级赛事成绩与高端整车体验。',
        'flagship_platforms': 'Dogma; F-Series; X-Series',
        'employee_count_range': 'Premium heritage brand scale',
        'annual_revenue_range': 'Private premium brand; exact public figures limited',
        'product_lines': 'Road bikes; Gravel bikes; TT bikes; High-end framesets; Accessories',
        'road_product_lines': 'Dogma; F-Series; X-Series',
        'data_sources': 'Official Pinarello history and product pages; public cycling media summaries; widely documented industry information',
        'notes': 'Pinarello 的最大优势在于极强的竞赛品牌资产和外观辨识度。对很多消费者而言，它不仅是公路车平台，也是高端职业竞赛文化的象征。',
    },
    'brand_007': {
        'country_region': 'Switzerland',
        'market_positioning': 'High-end Performance and Innovation Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Givisiez, Switzerland',
        'founded_year': '1958',
        'founder': 'Ed Scott',
        'parent_company': 'Scott Sports SA',
        'company_type': 'Performance Sports Equipment Company',
        'ownership_type': 'Private Company',
        'road_cycling_positioning': 'Scott 在公路车领域定位为兼具轻量竞赛、空气动力和综合运动科技基因的高性能品牌。其公路平台长期强调轻量、效率和整车现代感，在顶级公路与综合运动市场都有较强存在感。',
        'target_audience': '希望获得现代高性能竞赛平台、轻量化体验与品牌科技感的公路车用户，包括竞赛骑手、进阶用户与偏好综合性能品牌的消费者。',
        'price_tier': 'Mid-High to Premium',
        'brand_slogan': 'No Shortcuts',
        'brand_story': 'Scott 起源于 1958 年，最早在滑雪领域建立品牌，随后扩展到自行车与综合运动装备。品牌在公路车方向通过 Addict RC、Foil、Speedster 等平台覆盖顶级轻量竞赛、空气动力竞赛与入门性能市场，并在现代整车设计中持续强化综合性能表达。',
        'mission': 'Scott 长期强调通过技术、创新和对性能细节的追求，为运动用户提供更高效、更直接的产品体验。',
        'core_values': 'Innovation; Lightweight performance; Multi-sport engineering mindset; Modern design; Competitive efficiency',
        'core_technologies': 'HMX carbon platform development; aerodynamic race frame integration; lightweight chassis tuning; syncros cockpit integration',
        'r_and_d_capabilities': 'Scott 在轻量竞赛平台、整车一体化、空气动力学优化与多运动品类研发协同方面具备成熟能力。品牌在公路车上强调轻量和效率，并通过配件系统增强整车一体化体验。',
        'flagship_platforms': 'Addict RC; Foil; Speedster',
        'employee_count_range': 'Global sports equipment company scale',
        'annual_revenue_range': 'Private company; public exact figures limited',
        'product_lines': 'Road bikes; Gravel bikes; Mountain bikes; Triathlon bikes; E-bikes; Apparel; Helmets; Components via accessory ecosystem',
        'road_product_lines': 'Addict RC; Foil; Speedster',
        'data_sources': 'Official Scott brand and product pages; public brand summaries; widely documented industry information',
        'notes': 'Scott 在公路车市场中的核心优势是轻量竞赛平台和现代整车集成表达。对用户而言，它往往意味着更鲜明的运动科技感和整车一体化体验。',
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
            WHERE brand_id IN ('brand_004','brand_005','brand_007','brand_008','brand_011')
            ORDER BY brand_id
        """)).fetchall()
        for row in rows:
            print('\t'.join('' if v is None else str(v) for v in row))


if __name__ == '__main__':
    main()
