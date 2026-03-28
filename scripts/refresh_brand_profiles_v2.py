from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.brand import Brand

# V2 strategy:
# - refresh existing brands with curated richer defaults
# - detect sparse brands and backfill key fields from local knowledge map
# - auto-insert high-confidence road-bike brands missing from DB
# - keep candidate list for the next wave

CURATED_UPDATES: dict[str, dict[str, str]] = {
    '3T': {
        'country_region': 'Italy',
        'market_positioning': 'Boutique Performance and Gravel-forward Brand',
        'sales_model': 'Global Dealer Network + Select Direct Channels',
        'headquarters': 'Presezzo, Italy',
        'founded_year': '1961',
        'price_tier': 'Premium',
        'notes': '3T 以零部件起家，在现代公路和 gravel 平台中强调空气动力与系统整合。',
    },
    'Basso': {
        'country_region': 'Italy',
        'market_positioning': 'Boutique Heritage Premium Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Dueville, Italy',
        'founded_year': '1977',
        'price_tier': 'Premium to Luxury',
        'notes': 'Basso 兼具意大利工艺传统与现代高端竞赛平台表达。',
    },
    'Boardman': {
        'country_region': 'United Kingdom',
        'market_positioning': 'Mainstream Performance Value Brand',
        'sales_model': 'Retail + Dealer Network',
        'headquarters': 'United Kingdom',
        'founded_year': '2007',
        'price_tier': 'Entry-Mid to Mid-High',
        'notes': 'Boardman 更偏大众性能和高性价比市场。',
    },
    'Cube': {
        'country_region': 'Germany',
        'market_positioning': 'Mainstream to High-end European Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Waldershof, Germany',
        'founded_year': '1993',
        'price_tier': 'Entry-Mid to High',
        'notes': 'Cube 覆盖广价格带，公路车定位偏欧洲主流综合品牌。',
    },
    'Felt': {
        'country_region': 'United States',
        'market_positioning': 'Performance and Triathlon-oriented Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'United States',
        'founded_year': '1991',
        'price_tier': 'Mid-High to Premium',
        'notes': 'Felt 在公路和铁三领域具有长期品牌认知。',
    },
    'Van Rysel': {
        'country_region': 'France',
        'market_positioning': 'Performance Value Brand',
        'sales_model': 'Retail-led',
        'headquarters': 'Lille, France',
        'founded_year': '2019',
        'price_tier': 'Entry-Mid to Mid-High',
        'notes': 'Van Rysel 是 Decathlon 体系下更聚焦竞赛和性能市场的品牌。',
    },
    'Winspace': {
        'country_region': 'China',
        'market_positioning': 'Direct High-performance Value Brand',
        'sales_model': 'Direct-to-Consumer + Distributor',
        'headquarters': 'Xiamen, China',
        'founded_year': '2010s',
        'price_tier': 'Mid-High',
        'notes': 'Winspace 在碳架、轮组和直面全球市场方面增长很快。',
    },
    'XDS': {
        'country_region': 'China',
        'market_positioning': 'Mainstream Manufacturing-backed Brand',
        'sales_model': 'Dealer + Brand Retail',
        'headquarters': 'Shenzhen, China',
        'founded_year': '1995',
        'price_tier': 'Entry-Mid to Mid-High',
        'notes': 'XDS 依托大规模制造背景，在大众和进阶公路市场持续扩张。',
    },
}

NEW_BRANDS = [
    {
        'brand_name_en': 'Simplon',
        'brand_name_cn': 'Simplon',
        'country_region': 'Austria',
        'brand_type': 'complete_bike',
        'market_positioning': 'Premium European Performance Brand',
        'sales_model': 'Dealer Network',
        'main_road_categories': 'race; aero; endurance; all-road',
        'official_website': 'https://www.simplon.com',
        'notes': '奥地利高端品牌，强调工程与定制化。',
    },
    {
        'brand_name_en': 'Storck',
        'brand_name_cn': 'Storck',
        'country_region': 'Germany',
        'brand_type': 'complete_bike',
        'market_positioning': 'Boutique Premium Performance Brand',
        'sales_model': 'Dealer Network',
        'main_road_categories': 'race; aero; all-round',
        'official_website': 'https://www.storck-bikes.com',
        'notes': '德系精品高端品牌，强调轻量与高端整车完成度。',
    },
    {
        'brand_name_en': 'Kuota',
        'brand_name_cn': 'Kuota',
        'country_region': 'Italy',
        'brand_type': 'complete_bike',
        'market_positioning': 'Boutique Performance Brand',
        'sales_model': 'Dealer Network',
        'main_road_categories': 'race; aero; triathlon',
        'official_website': 'https://www.kuota.com',
        'notes': '意大利小众性能品牌，公路和铁三基因明显。',
    },
    {
        'brand_name_en': 'Guerciotti',
        'brand_name_cn': 'Guerciotti',
        'country_region': 'Italy',
        'brand_type': 'complete_bike',
        'market_positioning': 'Heritage Boutique Racing Brand',
        'sales_model': 'Dealer Network',
        'main_road_categories': 'race; cyclocross; gravel',
        'official_website': 'https://www.guerciotti.it',
        'notes': '意大利传统赛事品牌，兼具公路和越野传统。',
    },
]

LOG_DIR = Path(__file__).resolve().parents[1] / 'var'
LOG_DIR.mkdir(exist_ok=True)
CANDIDATE_PATH = LOG_DIR / 'brand_candidates_v2.json'
REFRESH_LOG = LOG_DIR / 'brand_refresh_v2.log'


def choose_value(current: str | None, incoming: str) -> str:
    if not current or not current.strip():
        return incoming
    current_clean = current.strip()
    incoming_clean = incoming.strip()
    if len(incoming_clean) > len(current_clean) * 1.35:
        return incoming_clean
    return current


def collect_used_brand_numbers(session: Session) -> set[int]:
    rows = session.execute(text("SELECT brand_id FROM brands WHERE brand_id LIKE 'brand_%'" )).fetchall()
    used = set()
    for (brand_id,) in rows:
        try:
            used.add(int(brand_id.split('_')[1]))
        except Exception:
            continue
    return used


def next_brand_id(used: set[int]) -> str:
    candidate = 1
    while candidate in used:
        candidate += 1
    used.add(candidate)
    return f'brand_{candidate:03d}'


def resolve_database_url() -> str:
    mysql_host = os.getenv('MYSQL_HOST', '127.0.0.1')
    mysql_port = os.getenv('MYSQL_PORT', '3306')
    mysql_user = os.getenv('MYSQL_USER', 'root')
    mysql_password = os.getenv('MYSQL_PASSWORD', 'test123456')
    mysql_database = os.getenv('MYSQL_DATABASE', 'road_bike_db')
    return f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4"


def main() -> None:
    _ = get_settings()
    engine = create_engine(resolve_database_url())
    now = datetime.now(timezone.utc).isoformat()

    updated = 0
    inserted = 0
    with Session(engine) as session:
        brands = session.scalars(select(Brand)).all()
        existing_names = {brand.brand_name_en for brand in brands}

        for brand in brands:
            patch = CURATED_UPDATES.get(brand.brand_name_en)
            if not patch:
                continue
            dirty = False
            for field, incoming in patch.items():
                current = getattr(brand, field)
                chosen = choose_value(current, incoming)
                if chosen != current:
                    setattr(brand, field, chosen)
                    dirty = True
            source_note = f'curated-refresh-v2:{now}'
            if not brand.data_sources:
                brand.data_sources = source_note
                dirty = True
            elif source_note not in brand.data_sources:
                brand.data_sources = f"{brand.data_sources}; {source_note}"
                dirty = True
            if dirty:
                session.add(brand)
                updated += 1

        used_brand_numbers = collect_used_brand_numbers(session)
        for payload in NEW_BRANDS:
            if payload['brand_name_en'] in existing_names:
                continue
            brand = Brand(
                brand_id=next_brand_id(used_brand_numbers),
                brand_name_en=payload['brand_name_en'],
                brand_name_cn=payload['brand_name_cn'],
                country_region=payload['country_region'],
                brand_type=payload['brand_type'],
                market_positioning=payload['market_positioning'],
                sales_model=payload['sales_model'],
                main_road_categories=payload['main_road_categories'],
                official_website=payload['official_website'],
                notes=payload['notes'],
                data_sources=f'auto-insert-v2:{now}',
            )
            session.add(brand)
            existing_names.add(payload['brand_name_en'])
            inserted += 1

        session.commit()

    candidate_payload = {
        'generated_at': now,
        'inserted_defaults': [item['brand_name_en'] for item in NEW_BRANDS],
        'next_candidates': ['Lee Cougan', 'Cervelo Aspero-family expansion', 'Berria', 'Moots', 'Parlee'],
    }
    CANDIDATE_PATH.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2), encoding='utf-8')
    with REFRESH_LOG.open('a', encoding='utf-8') as fh:
        fh.write(f"{now}\tupdated={updated}\tinserted={inserted}\n")
    print(f'updated={updated}')
    print(f'inserted={inserted}')
    print(f'candidate_file={CANDIDATE_PATH}')


if __name__ == '__main__':
    main()
