from shopee_affiliate.auth import generate_signature, build_authorization_header


def test_generate_signature_is_deterministic():
    sig1 = generate_signature("1", "secret", '{"query":"x"}', 123)
    sig2 = generate_signature("1", "secret", '{"query":"x"}', 123)
    assert sig1 == sig2


def test_build_authorization_header_contains_parts():
    header = build_authorization_header("123", "sec", "{}", timestamp=1)
    assert header.startswith("SHA256 Credential=123")
    assert "Timestamp=1" in header
    assert "Signature=" in header
