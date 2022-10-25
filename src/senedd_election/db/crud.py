from logging import getLogger

from sqlalchemy.exc import DBAPIError

from .. import schema
from . import model
from .connect import get_db


def create_constituencies(input: list[schema.Constituency]) -> None:
    db = get_db(read_only=False)

    records_to_add = [model.Constituency(**x.dict()) for x in input]
    db.add_all(records_to_add)

    try:
        db.commit()
    except DBAPIError as err:
        getLogger(__name__).warning("create_constituencies: integrity error %s", err)
        return


def create_results(input: list[schema.ConstituencyResult]) -> None:
    db = get_db(read_only=False)

    records_to_add = [model.ConstituencyResult(**x.dict()) for x in input]
    db.add_all(records_to_add)

    try:
        db.commit()
    except DBAPIError as err:
        getLogger(__name__).warning("create_results: integrity error %s", err)
        return


def create_summary(input: schema.ConstituencySummary) -> None:
    db = get_db(read_only=False)

    db.add(model.ConstituencySummary(**input.dict()))

    try:
        db.commit()
    except DBAPIError as err:
        getLogger(__name__).warning("create_results: integrity error %s", err)
        return


# def export_db(output_file: str):
#     settings = get_settings()
#     con = sqlite3.connect(settings.db_path)

#     with open(output_file, "w") as outfile:
#         outcsv = csv.writer(outfile)

#         cursor = con.execute(f"select * from {Model.__tablename__}")

#         # dump column titles
#         outcsv.writerow(x[0] for x in cursor.description)

#         # dump rows
#         outcsv.writerows(cursor.fetchall())
