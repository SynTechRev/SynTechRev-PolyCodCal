from __future__ import annotations

import numpy as np

from syntechrev_polycodcal.legal_generator.embedder import Embedder


def test_embedder_shapes_and_determinism():
    e = Embedder(dim=128)
    texts = ["alpha", "beta", "alpha"]
    vecs = e.encode_texts(texts)
    assert vecs.shape == (3, 128)
    # Deterministic: same input -> identical vector
    assert np.allclose(vecs[0], vecs[2])
    # Different inputs likely produce different vectors
    assert not np.allclose(vecs[0], vecs[1])
