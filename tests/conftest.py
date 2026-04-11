from typing import Any

import pytest
from syrupy.extensions.single_file import SingleFileSnapshotExtension, WriteMode
from syrupy.types import SerializedData


class MathMLExtension(SingleFileSnapshotExtension):
    # Use .html so snapshots open directly in a browser for visual verification.
    # All major browsers support MathML: https://caniuse.com/mathml
    file_extension = "html"
    _write_mode = WriteMode.TEXT

    def serialize(self, data: Any, **kwargs: Any) -> SerializedData:
        return str(data)


@pytest.fixture
def snapshot(snapshot: Any) -> Any:
    return snapshot.use_extension(MathMLExtension)
