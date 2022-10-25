from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import get

from . import schema
from .db import create_constituencies, create_results, create_summary
from .settings import get_settings


def scrape():
    settings = get_settings()

    doc = get(settings.election_all_constituency_url).text

    soup = BeautifulSoup(doc, features="html.parser")

    table = soup.find(
        attrs={
            "class": "mgNonBulletTableList",
        }
    )

    constituency_map: dict[str, str] = {}
    if isinstance(table, Tag):
        for constituency in table.find_all("li"):
            constituency_map[constituency.a.get("href")] = constituency.text

    constituencies = [
        schema.Constituency(name=name) for name in constituency_map.values()
    ]
    create_constituencies(constituencies)

    _scrape_constituencies(constituency_map)


def _scrape_constituencies(map: dict[str, str]):
    settings = get_settings()

    for ref, constituency_name in map.items():
        doc = get(f"{settings.election_url}/{ref}").text
        soup = BeautifulSoup(doc, features="html.parser")
        tables = soup.find_all("table")

        for table in tables:
            if " - results" in table.caption.text:
                _parse_constituency_results(table, constituency_name)
            elif "Voting Summary" == table.caption.text:
                _parse_constituency_summary(table, constituency_name)


def _parse_constituency_results(table: Tag, constituency: str):
    rows = table.find_all("tr")

    # remove first element, as this is the header row
    rows.pop(0)

    # parse out fields only
    rows = [x.find_all("td") for x in rows]
    result_records: list[schema.ConstituencyResult] = []

    for row in rows:
        fields = [x.text for x in row]
        result_records.append(
            schema.ConstituencyResult(
                constituency=constituency,
                candidate=fields[0],
                party=fields[1],
                votes=int(fields[2]),
                elected=(fields[4] == "Elected"),
            )
        )
    create_results(result_records)


def _parse_constituency_summary(table: Tag, constituency: str):
    rows = table.find_all("tr")

    # remove header row and empty bottom row
    rows.pop(0)
    rows.pop(-1)

    fields_dict: dict[str, str] = {}
    for row in rows:
        fields = [str(x.text) for x in row.find_all("td")]

        fields_dict[fields[0]] = fields[1]

    rejected_ballots = fields_dict.get("Number of ballot papers rejected")

    record_to_add = schema.ConstituencySummary(
        constituency=constituency,
        seats=int(fields_dict["Seats"]),
        valid_votes=int(fields_dict["Valid votes cast"]),
        electorate=int(fields_dict["Electorate"]),
        rejected_ballots=(int(rejected_ballots) if rejected_ballots else None),
    )

    create_summary(record_to_add)
