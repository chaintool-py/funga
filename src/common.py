def strip_hex_prefix(hx):
    if hx[:2] == '0x':
        return hx[2:]
    return hx

