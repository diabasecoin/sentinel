import pytest
import sys
import os
import time

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../lib"))
)
import misc
import config
from models import GovernanceObject, Proposal, Superblock, Vote
from conftest import MockDiabaseDaemon


# clear DB tables before each execution
def setup():
    # clear tables first...
    Vote.delete().execute()
    Proposal.delete().execute()
    Superblock.delete().execute()
    GovernanceObject.delete().execute()


def teardown():
    pass


# list of proposal govobjs to import for testing
@pytest.fixture
def go_list_proposals():
    items = [
        {
            "AbsoluteYesCount": 1000,
            "AbstainCount": 7,
            "CollateralHash": "acb67ec3f3566c9b94a26b70b36c1f74a010a37c0950c22d683cc50da324fdca",
            "DataHex": "5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20323132323532303430302c20226e616d65223a20226465616e2d6d696c6c65722d35343933222c20227061796d656e745f61646472657373223a2022795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e74223a2032352e37352c202273746172745f65706f6368223a20313437343236313038362c202274797065223a20312c202275726c223a2022687474703a2f2f6461736863656e7472616c2e6f72672f6465616e2d6d696c6c65722d35343933227d5d5d",
            "DataString": '[["proposal", {"end_epoch": 2122520400, "name": "dean-miller-5493", "payment_address": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amount": 25.75, "start_epoch": 1474261086, "type": 1, "url": "http://diabasecentral.org/dean-miller-5493"}]]',
            "Hash": "dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c",
            "IsValidReason": "",
            "NoCount": 25,
            "YesCount": 1025,
            "fBlockchainValidity": True,
            "fCachedDelete": False,
            "fCachedEndorsed": False,
            "fCachedFunding": False,
            "fCachedValid": True,
        },
        {
            "AbsoluteYesCount": 1000,
            "AbstainCount": 29,
            "CollateralHash": "3efd23283aa98c2c33f80e4d9ed6f277d195b72547b6491f43280380f6aac810",
            "DataHex": "5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20323132323532303430302c20226e616d65223a20226665726e616e64657a2d37363235222c20227061796d656e745f61646472657373223a2022795443363268755234595145506e39414a486a6e517878726548536267416f617456222c20227061796d656e745f616d6f756e74223a2033322e30312c202273746172745f65706f6368223a20313437343236313038362c202274797065223a20312c202275726c223a2022687474703a2f2f6461736863656e7472616c2e6f72672f6665726e616e64657a2d37363235227d5d5d",
            "DataString": '[["proposal", {"end_epoch": 2122520400, "name": "fernandez-7625", "payment_address": "yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV", "payment_amount": 32.01, "start_epoch": 1474261086, "type": 1, "url": "http://diabasecentral.org/fernandez-7625"}]]',
            "Hash": "0523445762025b2e01a2cd34f1d10f4816cf26ee1796167e5b029901e5873630",
            "IsValidReason": "",
            "NoCount": 56,
            "YesCount": 1056,
            "fBlockchainValidity": True,
            "fCachedDelete": False,
            "fCachedEndorsed": False,
            "fCachedFunding": False,
            "fCachedValid": True,
        },
    ]

    return items


# list of superblock govobjs to import for testing
@pytest.fixture
def go_list_superblocks():
    items = [
        {
            "AbsoluteYesCount": 1,
            "AbstainCount": 0,
            "CollateralHash": "0000000000000000000000000000000000000000000000000000000000000000",
            "DataHex": "5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d",
            "DataString": '[["trigger", {"event_block_height": 72696, "payment_addresses": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amounts": "25.75000000|25.7575000000", "type": 2}]]',
            "Hash": "667c4a53eb81ba14d02860fdb4779e830eb8e98306f9145f3789d347cbeb0721",
            "IsValidReason": "",
            "NoCount": 0,
            "YesCount": 1,
            "fBlockchainValidity": True,
            "fCachedDelete": False,
            "fCachedEndorsed": False,
            "fCachedFunding": False,
            "fCachedValid": True,
        },
        {
            "AbsoluteYesCount": 1,
            "AbstainCount": 0,
            "CollateralHash": "0000000000000000000000000000000000000000000000000000000000000000",
            "DataHex": "5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d",
            "DataString": '[["trigger", {"event_block_height": 72696, "payment_addresses": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
            "Hash": "8f91ffb105739ec7d5b6c0b12000210fcfcc0837d3bb8ca6333ba93ab5fc0bdf",
            "IsValidReason": "",
            "NoCount": 0,
            "YesCount": 1,
            "fBlockchainValidity": True,
            "fCachedDelete": False,
            "fCachedEndorsed": False,
            "fCachedFunding": False,
            "fCachedValid": True,
        },
        {
            "AbsoluteYesCount": 1,
            "AbstainCount": 0,
            "CollateralHash": "0000000000000000000000000000000000000000000000000000000000000000",
            "DataHex": "5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d",
            "DataString": '[["trigger", {"event_block_height": 72696, "payment_addresses": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
            "Hash": "bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36",
            "IsValidReason": "",
            "NoCount": 0,
            "YesCount": 1,
            "fBlockchainValidity": True,
            "fCachedDelete": False,
            "fCachedEndorsed": False,
            "fCachedFunding": False,
            "fCachedValid": True,
        },
    ]

    return items


@pytest.fixture
def superblock():
    sb = Superblock(
        event_block_height=62500,
        payment_addresses="yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|8j3GDpppVGTcWtEBuHAZSwcv33tWXey89M",
        payment_amounts="5|3",
        proposal_hashes="e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e",
    )
    return sb


def test_superblock_is_valid(superblock):
    diabased = MockDiabaseDaemon.initialize(None)

    orig = Superblock(**superblock.get_dict())  # make a copy

    # original as-is should be valid
    assert orig.is_valid(diabased) is True

    # mess with payment amounts
    superblock.payment_amounts = "7|yyzx"
    assert superblock.is_valid(diabased) is False

    superblock.payment_amounts = "7,|yzx"
    assert superblock.is_valid(diabased) is False

    superblock.payment_amounts = "7|8"
    assert superblock.is_valid(diabased) is True

    superblock.payment_amounts = " 7|8"
    assert superblock.is_valid(diabased) is False

    superblock.payment_amounts = "7|8 "
    assert superblock.is_valid(diabased) is False

    superblock.payment_amounts = " 7|8 "
    assert superblock.is_valid(diabased) is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid(diabased) is True

    # mess with payment addresses
    superblock.payment_addresses = (
        "yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV|1234 Anywhere ST, Chicago, USA"
    )
    assert superblock.is_valid(diabased) is False

    # leading spaces in payment addresses
    superblock.payment_addresses = " yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV"
    superblock.payment_amounts = "5.00"
    assert superblock.is_valid(diabased) is False

    # trailing spaces in payment addresses
    superblock.payment_addresses = "yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV "
    superblock.payment_amounts = "5.00"
    assert superblock.is_valid(diabased) is False

    # leading & trailing spaces in payment addresses
    superblock.payment_addresses = " yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV "
    superblock.payment_amounts = "5.00"
    assert superblock.is_valid(diabased) is False

    # single payment addr/amt is ok
    superblock.payment_addresses = "yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV"
    superblock.payment_amounts = "5.00"
    assert superblock.is_valid(diabased) is True

    # ensure number of payment addresses matches number of payments
    superblock.payment_addresses = "yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV"
    superblock.payment_amounts = "37.00|23.24"
    assert superblock.is_valid(diabased) is False

    superblock.payment_addresses = (
        "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV"
    )
    superblock.payment_amounts = "37.00"
    assert superblock.is_valid(diabased) is False

    # ensure amounts greater than zero
    superblock.payment_addresses = "yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV"
    superblock.payment_amounts = "-37.00"
    assert superblock.is_valid(diabased) is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid(diabased) is True

    # mess with proposal hashes
    superblock.proposal_hashes = "7|yyzx"
    assert superblock.is_valid(diabased) is False

    superblock.proposal_hashes = "7,|yyzx"
    assert superblock.is_valid(diabased) is False

    superblock.proposal_hashes = "0|1"
    assert superblock.is_valid(diabased) is False

    superblock.proposal_hashes = "0000000000000000000000000000000000000000000000000000000000000000|1111111111111111111111111111111111111111111111111111111111111111"
    assert superblock.is_valid(diabased) is True

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid(diabased) is True


def test_serialisable_fields():
    s1 = [
        "event_block_height",
        "payment_addresses",
        "payment_amounts",
        "proposal_hashes",
    ]
    s2 = Superblock.serialisable_fields()

    s1.sort()
    s2.sort()

    assert s2 == s1


def test_deterministic_superblock_creation(go_list_proposals):
    import diabaselib
    import misc

    diabased = MockDiabaseDaemon.initialize(None)

    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_diabased(diabased, item)

    max_budget = 60
    prop_list = Proposal.approved_and_ranked(
        proposal_quorum=1, next_superblock_max_budget=max_budget
    )

    sb = diabaselib.create_superblock(prop_list, 72000, max_budget, misc.now())

    assert sb.event_block_height == 72000
    assert (
        sb.payment_addresses
        == "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV"
    )
    assert sb.payment_amounts == "25.75000000|32.01000000"
    assert (
        sb.proposal_hashes
        == "dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c|0523445762025b2e01a2cd34f1d10f4816cf26ee1796167e5b029901e5873630"
    )

    assert (
        sb.hex_hash()
        == "bb3f33ccf95415c396bd09d35325dbcbc7b067010d51c7ccf772a9e839c1e414"
    )


def test_deterministic_superblock_selection(go_list_superblocks):
    diabased = MockDiabaseDaemon.initialize(None)

    for item in go_list_superblocks:
        (go, subobj) = GovernanceObject.import_gobject_from_diabased(diabased, item)

    # highest hash wins if same -- so just order by hash
    sb = Superblock.find_highest_deterministic(
        "542f4433e438bdd64697b8381fda1a7a9b7a111c3a4e32fad524d1821d820394"
    )
    assert (
        sb.object_hash
        == "bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36"
    )
