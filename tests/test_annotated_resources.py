import datetime
import json

from odin.codecs import json_codec
from odin.datetimeutil import utc
from odin.utils import getmeta

from tests.annotated_resources import Book, Publisher, Author, Library, IdentifiableBook


class TestAnnotatedResourceType:
    def test_fields_are_identified_in_correct_order(self):
        meta = getmeta(Book)

        assert [f.name for f in meta.fields] == [
            "title",
            "isbn",
            "num_pages",
            "rrp",
            "fiction",
            "genre",
            "published",
            "authors",
            "publisher",
        ]


class TestAnnotatedResource:
    def test_fields_are_inherited_from_parent_resources(self):
        meta = getmeta(IdentifiableBook)

        assert [f.name for f in meta.fields] == [
            "title",
            "isbn",
            "num_pages",
            "rrp",
            "fiction",
            "genre",
            "published",
            "authors",
            "publisher",
            "id",
            "purchased_from",
        ]


class TestAnnotatedKitchenSink:
    def test_dumps_with_valid_data(self):
        book = Book(
            title="Consider Phlebas",
            isbn="0-333-45430-8",
            num_pages=471,
            rrp=19.50,
            genre="sci-fi",
            fiction=True,
            published=[datetime.datetime(1987, 1, 1, tzinfo=utc)],
        )
        book.publisher = Publisher(name="Macmillan")
        book.authors.append(Author(name="Iain M. Banks"))

        library = Library(name="Public Library", books=[book])
        actual = json_codec.dumps(library)

        assert json.loads(actual) == json.loads(
            """
{
    "$": "new_library.Library",
    "name": "Public Library",
    "books": [
        {
            "$": "new_library.Book",
            "publisher": {
                "$": "Publisher",
                "name": "Macmillan"
            },
            "num_pages": 471,
            "isbn": "0-333-45430-8",
            "title": "Consider Phlebas",
            "authors": [
                {
                    "$": "Author",
                    "name": "Iain M. Banks"
                }
            ],
            "fiction": true,
            "published": ["1987-01-01T00:00:00+00:00"],
            "genre": "sci-fi",
            "rrp": 19.5
        }
    ],
    "subscribers": null,
    "book_count": 1
}
        """
        )
