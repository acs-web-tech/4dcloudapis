def GenerateUniqueId():
    import secrets
    return secrets.token_hex(16)