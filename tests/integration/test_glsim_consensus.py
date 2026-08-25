from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Compare one gift proposal"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"fit": "FIT", "concern_note": "NONE"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_gift_selection():
    organizer_account, proposer_account, recipient_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "gift_brief_match.py")
    deployed = factory.deploy_contract_tx(args=[recipient_account.address, "A small graduation gathering", "The recipient enjoys practical desk accessories, muted blue or gray colors, durable materials, and easy maintenance.", "Avoid scented goods, clothing, personalization, and anything requiring a subscription."], account=organizer_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    contract_address = extract_contract_address(deployed)
    organizer = factory.build_contract(contract_address, account=organizer_account)
    proposer = factory.build_contract(contract_address, account=proposer_account)
    recipient = factory.build_contract(contract_address, account=recipient_account)
    ok(organizer.propose_gift(args=["desk", "Blue metal desk tray", "A durable muted-blue tray for organizing notebooks, pens, and charging cables on a desk.", "No scent, subscription, clothing, personalization, or recurring service; wipe-clean metal."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(proposer.propose_gift(args=["stand", "Gray wooden book stand", "A compact gray-stained stand that holds a book or tablet at an adjustable reading angle.", "No scent, subscription, clothing, personalization, or disposable components."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(organizer.lock_proposals(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(organizer.assess_gift(args=["desk"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(organizer.assess_gift(args=["stand"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(organizer.shortlist_gift(args=["desk"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(recipient.choose_gift(args=["desk", "This desk organizer matches the public color, durability, and maintenance preferences."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert organizer.get_state(args=[]).call()["selected_proposal"] == "desk"
