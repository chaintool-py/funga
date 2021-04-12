ethereum_recid_modifier = 35

def chain_id_to_v(chain_id, signature):
    v = signature[64]
    return (chain_id * 2) + ethereum_recid_modifier + v
