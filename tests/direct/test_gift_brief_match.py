from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "gift_brief_match.py"
SDK = "v0.2.16"
PROMPT = "Compare one gift proposal"
BRIEF = "The recipient enjoys practical desk accessories, prefers muted blue or gray, and values items that are durable and easy to maintain."
CONSTRAINTS = "Avoid scented products, novelty clothing, personalized names, and items that require a subscription."


def address(account):
    return "0x" + account.hex()


def deploy(vm, direct_deploy, owner, recipient):
    vm.sender = owner
    return direct_deploy(str(CONTRACT), address(recipient), "A small graduation gathering", BRIEF, CONSTRAINTS, sdk_version=SDK)


def prepare(contract, vm, owner, proposer):
    contract.propose_gift("desk", "Blue metal desk tray", "A durable muted-blue powder-coated tray for organizing notebooks, pens, and charging cables on a desk.", "No scent, no subscription, no clothing, no printed personal name, and wipe-clean metal construction.")
    vm.sender = proposer
    contract.propose_gift("stand", "Gray wooden book stand", "A compact gray-stained wooden stand that holds a book or tablet at an adjustable reading angle.", "No scent, no subscription, no clothing, no personal name, and a reusable solid-wood frame.")
    vm.sender = owner
    contract.lock_proposals()


def test_match_shortlist_and_recipient_choice(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_charlie)
    prepare(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"fit_mask": "1111", "concern_note": "NONE"}))
    contract.assess_gift("desk")
    leader = direct_vm._captured_validators[-1][0]
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"fit_mask": "1111", "concern_note": "No declared exclusion or preference conflicts with the proposal."}))
    assert direct_vm.run_validator(leader_result=leader) is True
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"fit_mask": "1101", "concern_note": "This different hard-constraint assessment must be rejected by the validator."}))
    assert direct_vm.run_validator(leader_result=leader) is False
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"fit_mask": "1111", "concern_note": "NONE"}))
    contract.assess_gift("stand")
    contract.shortlist_gift("desk")
    direct_vm.sender = direct_charlie
    contract.choose_gift("desk", "This practical desk organizer matches the stated color and maintenance preferences.")
    assert contract.get_state()["phase"] == "COMPLETE"
    assert contract.get_state()["selected_proposal"] == "desk"
    assert contract.get_proposal("desk")["fit_mask"] == "1111"
    assert contract.get_proposal("desk")["fit"] == "FIT"


def test_one_proposal_per_address_and_only_organizer_locks(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_charlie)
    direct_vm.sender = direct_bob
    contract.propose_gift("first", "Gray cable pouch", "A reusable gray pouch that keeps charging cables and small desk adapters organized for travel.", "No scent, subscription, clothing, personalization, or disposable components are declared.")
    with direct_vm.expect_revert("one_proposal_per_address"):
        contract.propose_gift("second", "Blue pen cup", "A second proposal from the same address must not enter this public gift matching round.", "No scent, subscription, clothing, or personalization is declared for this second proposal.")
    with direct_vm.expect_revert("only_organizer"):
        contract.lock_proposals()


def test_flagged_proposer_revision_and_bad_output_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_charlie)
    prepare(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"fit_mask": "1101", "concern_note": "The original description declares a recurring subscription."}))
    contract.assess_gift("desk")
    contract.revise_gift("desk", "A durable muted-blue desk tray sold as a standalone item with no recurring service or account.", "No scent, subscription, clothing, personal name, or recurring service; wipe-clean metal construction.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"fit_mask": "11X1", "concern_note": "Outside the allowed schema."}))
    with direct_vm.expect_revert("invalid_fit_mask"):
        contract.assess_gift("desk")
    assert contract.get_proposal("desk")["state"] == "REVISED"
    assert contract.get_proposal("desk")["revision_used"] is True
