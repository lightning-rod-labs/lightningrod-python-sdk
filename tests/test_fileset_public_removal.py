from datetime import datetime

from lightningrod._generated.api.file_sets import list_file_sets_filesets_get
from lightningrod._generated.models.file_set import FileSet


def test_list_file_sets_request_has_no_public_filter() -> None:
    kwargs = list_file_sets_filesets_get._get_kwargs()

    assert kwargs == {
        "method": "get",
        "url": "/filesets/",
    }


def test_file_set_model_has_no_public_field() -> None:
    file_set = FileSet(
        id="fs-1",
        name="Reports",
        description=None,
        created_at=datetime(2026, 1, 1),
        updated_at=datetime(2026, 1, 2),
    )

    assert not hasattr(file_set, "is_public")
    assert "is_public" not in file_set.to_dict()
