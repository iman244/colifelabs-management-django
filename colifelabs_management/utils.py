def accounting_display(v: int):
    return f"{v:,}" if v > 0 else f"({abs(v):,})"