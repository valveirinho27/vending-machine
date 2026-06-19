def pence_to_string(pence: int) -> str:
    """Convert a pence integer value to a human-readable string (e.g. 150 -> '£1.50')."""
    if pence <= 0:
        return "0p"
    if pence >= 100:
        pounds = pence // 100
        remaining_pence = pence % 100
        if remaining_pence == 0:
            return f"£{pounds}"
        return f"£{pounds}.{remaining_pence:02d}"
    return f"{pence}p"

