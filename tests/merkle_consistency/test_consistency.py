"""
run with
$ pytest -v -s test_consistency
"""

from tqdm import tqdm
import pytest
from consistency import (
    log2_ceiling,
    closest_pow_of_2,
    merkle_tree_hash,
    path,
    root_from_path,
    cons_proof_sub,
    root_0_from_const_proof,
    root_1_from_const_proof,
)


log2 = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 3, 8: 4}
closest = {0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 4, 6: 4, 7: 4, 8: 4, 9: 8, 10: 8}


@pytest.fixture
def init_environment():
    """
    This runs before every test
    """
    global data
    global start
    global step
    size = 33
    start = 1
    step = 1
    data = []
    for i in range(size):
        data.append(int(i).to_bytes(32, "big"))


def test_log2_ceiling(init_environment):

    for l in tqdm(log2.keys()):
        assert log2_ceiling(l)["result"] == log2[l]


def test_closest_pow_of_2(init_environment):

    for c in tqdm(closest.keys()):
        assert closest_pow_of_2(c)["result"] == closest[c]


def test_merkle_tree_hash(init_environment):

    root = merkle_tree_hash(data)["result"]
    for index in tqdm(range(start, len(data), step), desc="Testing paths"):
        merkle_proof, siblings = path(data, index)["result"]
        _root = root_from_path(index, merkle_proof, siblings)["result"]
        assert root == _root


def test_consistency_proof(init_environment):

    for m in tqdm(
        range(start, len(data), step), desc="Testing consistency for 0"
    ):
        root = merkle_tree_hash(data[:m])["result"]
        consistency_proof = cons_proof_sub(data, m)["result"]
        _root = root_0_from_const_proof(consistency_proof, m, len(data))[
            "result"
        ]
        assert root == _root

    root = merkle_tree_hash(data)["result"]
    for m in tqdm(
        range(start, len(data), step), desc="Testing consistency for 1"
    ):
        consistency_proof = cons_proof_sub(data, m)["result"]
        _root = root_1_from_const_proof(consistency_proof, m, len(data))[
            "result"
        ]
        assert root == _root
