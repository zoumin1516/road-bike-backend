from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.brand import Brand

# Default strategy:
# - refresh existing brands from local curated brand knowledge map
# - only fill empty fields unless the new value is clearly richer
# - append/update data_sources with refresh timestamp
# - record candidate brands for manual review before insertion logic is expanded

CURATED_UPDATES: dict[str, dict[str, str]] = {
    'Specialized': {
        'country_region': 'United States',
        'sales_model': 'Dealer Network + DTC',
    },
    'Trek': {
        'country_region': 'United States',
        'sales_model': 'Global Dealer Network + Trek Retail',
    },
    'Giant': {
        'country_region': 'Taiwan',
    },
    'Merida': {
        'country_region': 'Taiwan',
    },
    'Colnago': {
        'country_region': 'Italy',
    },
    'Cannondale': {
        'country_region': 'United States',
    },
    'Cervelo': {
        'country_region': 'Canada',
    },
    'Scott': {
        'country_region': 'Switzerland',
    },
    'BMC': {
        'country_region': 'Switzerland',
    },
    'Pinarello': {
        'country_region': 'Italy',
    },
    'Canyon': {
        'country_region': 'Germany',
        'sales_model': 'Direct-to-Consumer',
    },
    'Orbea': {
        'country_region': 'Spain',
    },
    'Look': {
        'country_region': 'France',
    },
    'Factor': {
        'country_region': 'United Kingdom',
    },
    'Wilier Triestina': {
        'country_region': 'Italy',
    },
    'Ridley': {
        'country_region': 'Belgium',
    },
    'Argon 18': {
        'country_region': 'Canada',
    },
    'Time': {
        'country_region': 'France',
    },
    'Lapierre': {
        'country_region': 'France',
    },
    'De Rosa': {
        'country_region': 'Italy',
    },
    'Bianchi': {
        'country_region': 'Italy',
    },
    'Rose': {
        'country_region': 'Germany',
        'sales_model': 'Direct-to-Consumer',
    },
    'Fuji': {
        'country_region': 'Japan',
    },
    'BH': {
        'country_region': 'Spain',
    },
    'Chapter2': {
        'country_region': 'New Zealand',
    },
}

CANDIDATE_BRANDS = [
    'Simplon',
    'Storck',
    'Kuota',
    'Guerciotti',
    'Lee Cougan',
]

LOG_DIR = Path(__file__).resolve().parents[1] / 'var'
LOG_DIR.mkdir(exist_ok=True)
CANDIDATE_PATH = LOG_DIR / 'brand_candidates.json'
REFRESH_LOG = LOG_DIR / 'brand_refresh.log'


def choose_value(current: str | None, incoming: str) -> str:
    if not current or not current.strip():
        return incoming
    if len(incoming.strip()) > len(current.strip()) * 1.35:
        return incoming
    return current


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    now = datetime.now(timezone.utc).isoformat()

    updated = 0
    with Session(engine) as session:
        brands = session.scalars(select(Brand)).all()
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
            source_note = f'curated-refresh:{now}'
            if not brand.data_sources:
                brand.data_sources = source_note
                dirty = True
            elif source_note not in brand.data_sources:
                brand.data_sources = f"{brand.data_sources}; {source_note}"
                dirty = True
            if dirty:
                session.add(brand)
                updated += 1
        session.commit()

    candidate_payload = {
        'generated_at': now,
        'candidates': CANDIDATE_BRANDS,
    }
    CANDIDATE_PATH.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2), encoding='utf-8')
    REFRESH_LOG.write_text(f"{now}\tupdated={updated}\tcandidates={len(CANDIDATE_BRANDS)}\n", encoding='utf-8')
    print(f'updated={updated}')
    print(f'candidates={len(CANDIDATE_BRANDS)}')
    print(f'candidate_file={CANDIDATE_PATH}')


if __name__ == '__main__':
    main()
