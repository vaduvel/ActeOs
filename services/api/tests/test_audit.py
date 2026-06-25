from wb_api.audit import AuditChain, GENESIS_HASH, verify_chain


def test_chain_links_and_verifies():
    chain = AuditChain()
    assert chain.head == GENESIS_HASH
    e1 = chain.append("user:1", "journey.created", {"journey_id": "j1"})
    e2 = chain.append("user:1", "route.resolved", {"route_hash": "sha256:abc"})
    assert e1["prev_hash"] == GENESIS_HASH
    assert e2["prev_hash"] == e1["entry_hash"]
    assert e1["seq"] == 1 and e2["seq"] == 2
    assert verify_chain(chain.entries) is True


def test_tampered_payload_detected():
    chain = AuditChain()
    chain.append("user:1", "a", {"v": 1})
    chain.append("user:1", "b", {"v": 2})
    entries = chain.entries
    entries[0]["payload"] = {"v": 999}
    assert verify_chain(entries) is False


def test_deleted_entry_detected():
    chain = AuditChain()
    chain.append("u", "a", {})
    chain.append("u", "b", {})
    chain.append("u", "c", {})
    entries = chain.entries
    del entries[1]  # break the chain by removing the middle entry
    assert verify_chain(entries) is False


def test_reordered_entries_detected():
    chain = AuditChain()
    chain.append("u", "a", {})
    chain.append("u", "b", {})
    entries = list(reversed(chain.entries))
    assert verify_chain(entries) is False
