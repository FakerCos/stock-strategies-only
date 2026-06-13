import pandas as pd
from stock_strategies import datasources as ds


def _raw():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-02-01", "2024-03-01"]),  # 所屬月
        "revenue_year": [2024, 2024],
        "revenue_month": [2, 3],
        "revenue": [100_000, 120_000],
    })


def test_revenue_avail_date_blocks_lookahead(monkeypatch):
    monkeypatch.setattr(ds, "fetch_finmind_cached", lambda *a, **k: _raw())
    # 3 月營收 avail_date = 2024-04-10；as_of=2024-04-05 不應看到 3 月
    out = ds.get_month_revenue("2330", "2024-01-01", as_of="2024-04-05")
    assert out["revenue_month"].max() == 2  # 只到 2 月（avail=2024-03-10）
    # as_of=2024-04-10 才看得到 3 月
    out2 = ds.get_month_revenue("2330", "2024-01-01", as_of="2024-04-10")
    assert 3 in out2["revenue_month"].values


def test_revenue_mom_yoy_columns(monkeypatch):
    monkeypatch.setattr(ds, "fetch_finmind_cached", lambda *a, **k: _raw())
    out = ds.get_month_revenue("2330", "2024-01-01")
    assert {"avail_date", "mom", "yoy", "revenue"}.issubset(out.columns)
