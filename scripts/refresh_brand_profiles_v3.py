from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.brand import Brand

CURATED_UPDATES: dict[str, dict[str, str]] = {
    '3T': {
        'country_region': 'Italy',
        'market_positioning': 'Boutique Performance and Gravel-forward Brand',
        'sales_model': 'Global Dealer Network + Select Direct Channels',
        'headquarters': 'Presezzo, Italy',
        'founded_year': '1961',
        'price_tier': 'Premium',
    },
    'Basso': {
        'country_region': 'Italy',
        'market_positioning': 'Boutique Heritage Premium Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Dueville, Italy',
        'founded_year': '1977',
        'price_tier': 'Premium to Luxury',
    },
    'Boardman': {
        'country_region': 'United Kingdom',
        'market_positioning': 'Mainstream Performance Value Brand',
        'sales_model': 'Retail + Dealer Network',
        'headquarters': 'United Kingdom',
        'founded_year': '2007',
        'price_tier': 'Entry-Mid to Mid-High',
    },
    'Cube': {
        'country_region': 'Germany',
        'market_positioning': 'Mainstream to High-end European Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'Waldershof, Germany',
        'founded_year': '1993',
        'price_tier': 'Entry-Mid to High',
    },
    'Felt': {
        'country_region': 'United States',
        'market_positioning': 'Performance and Triathlon-oriented Brand',
        'sales_model': 'Global Dealer Network',
        'headquarters': 'United States',
        'founded_year': '1991',
        'price_tier': 'Mid-High to Premium',
    },
    'Van Rysel': {
        'country_region': 'France',
        'market_positioning': 'Performance Value Brand',
        'sales_model': 'Retail-led',
        'headquarters': 'Lille, France',
        'founded_year': '2019',
        'price_tier': 'Entry-Mid to Mid-High',
    },
    'Winspace': {
        'country_region': 'China',
        'market_positioning': 'Direct High-performance Value Brand',
        'sales_model': 'Direct-to-Consumer + Distributor',
        'headquarters': 'Xiamen, China',
        'founded_year': '2010s',
        'price_tier': 'Mid-High',
    },
    'XDS': {
        'country_region': 'China',
        'market_positioning': 'Mainstream Manufacturing-backed Brand',
        'sales_model': 'Dealer + Brand Retail',
        'headquarters': 'Shenzhen, China',
        'founded_year': '1995',
        'price_tier': 'Entry-Mid to Mid-High',
    },
}

NEW_BRANDS = [
    {
        'brand_name_en': 'Parlee',
        'brand_name_cn': 'Parlee',
        'country_region': 'United States',
        'brand_type': 'complete_bike',
        'market_positioning': 'Boutique Premium Carbon Brand',
        'sales_model': 'Dealer Network',
        'main_road_categories': 'race; endurance; all-road',
        'official_website': 'https://www.parleecycles.com',
        'notes': '美国精品碳纤维品牌，强调高端骑感与定制传统。',
    },
    {
        'brand_name_en': 'Moots',
        'brand_name_cn': 'Moots',
        'country_region': 'United States',
        'brand_type': 'complete_bike',
        'market_positioning': 'Boutique Titanium Premium Brand',
        'sales_model': 'Dealer Network',
        'main_road_categories': 'all-road; endurance; gravel',
        'official_website': 'https://moots.com',
        'notes': '美国精品钛架品牌，强调工艺和长寿命骑行体验。',
    },
]

LOG_DIR = Path(__file__).resolve().parents[1] / 'var'
LOG_DIR.mkdir(exist_ok=True)
CANDIDATE_PATH = LOG_DIR / 'brand_candidates_v3.json'
REFRESH_LOG = LOG_DIR / 'brand_refresh_v3.log'


def choose_value(current: str | None, incoming: str) -> str:
    if not current or not current.strip():
        return incoming.strip()
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


def fetch_site_meta(url: str) -> tuple[str | None, str | None]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read(120000).decode('utf-8', errors='ignore')
        title_match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
        title = re.sub(r'\s+', ' ', title_match.group(1)).strip() if title_match else None
        desc = re.sub(r'\s+', ' ', desc_match.group(1)).strip() if desc_match else None
        return title, desc
    except Exception:
        return None, None


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    now = datetime.now(timezone.utc).isoformat()

    updated = 0
    inserted = 0
    meta_refreshed = 0
    with Session(engine) as session:
        brands = session.scalars(select(Brand)).all()
        existing_names = {brand.brand_name_en for brand in brands}

        for brand in brands[:16]:
            patch = CURATED_UPDATES.get(brand.brand_name_en)
            dirty = False
            if patch:
                for field, incoming in patch.items():
                    current = getattr(brand, field)
                    chosen = choose_value(current, incoming)
                    if chosen != current:
                        setattr(brand, field, chosen)
                        dirty = True

            if brand.official_website:
                title, desc = fetch_site_meta(brand.official_website)
                if desc:
                    chosen_notes = choose_value(brand.notes, desc)
                    if chosen_notes != brand.notes:
                        brand.notes = chosen_notes
                        dirty = True
                    meta_refreshed += 1
                if title and (not brand.brand_story or not brand.brand_story.strip()):
                    brand.brand_story = title
                    dirty = True

            source_note = f'brand-refresh-v3:{now}'
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
                data_sources=f'auto-insert-v3:{now}',
            )
            session.add(brand)
            existing_names.add(payload['brand_name_en'])
            inserted += 1

        session.commit()

    candidate_payload = {
        'generated_at': now,
        'inserted_defaults': [item['brand_name_en'] for item in NEW_BRANDS],
        'next_candidates': ['Berria', 'Lee Cougan', 'Ventum', 'Open', 'Standert'],
    }
    CANDIDATE_PATH.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2), encoding='utf-8')
    with REFRESH_LOG.open('a', encoding='utf-8') as fh:
        fh.write(f"{now}\tupdated={updated}\tinserted={inserted}\tmeta_refreshed={meta_refreshed}\n")
    print(f'updated={updated}')
    print(f'inserted={inserted}')
    print(f'meta_refreshed={meta_refreshed}')
    print(f'candidate_file={CANDIDATE_PATH}')


if __name__ == '__main__':
    main()
