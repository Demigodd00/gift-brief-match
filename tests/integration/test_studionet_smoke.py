import json
from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_gift_fit(default_account, secondary_account, tertiary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "gift_brief_match.py")
    deployed = ok(factory.deploy_contract_tx(args=[tertiary_account.address, "A small graduation gathering", "The recipient enjoys practical desk accessories, muted blue or gray colors, durable materials, and easy maintenance.", "Avoid scented goods, clothing, personalization, and anything requiring a subscription."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    organizer = factory.build_contract(address, account=default_account)
    proposer = factory.build_contract(address, account=secondary_account)
    ok(organizer.propose_gift(args=["desk", "Blue metal desk tray", "A durable muted-blue tray for organizing notebooks, pens, and charging cables on a desk.", "No scent, subscription, clothing, personalization, or recurring service; wipe-clean metal."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(proposer.propose_gift(args=["stand", "Gray wooden book stand", "A compact gray-stained stand that holds a book or tablet at an adjustable reading angle.", "No scent, subscription, clothing, personalization, or disposable components."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(organizer.lock_proposals(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(organizer.assess_gift(args=["desk"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    observed = organizer.get_proposal(args=["desk"]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)["fit"]
    assert observed in ("FIT", "RISKY", "NO_FIT")
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
