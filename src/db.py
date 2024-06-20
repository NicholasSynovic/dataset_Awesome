from sqlalchemy import (
    Column,
    Engine,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
)


class DB:
    def __init__(self, dbConn: Engine) -> None:
        self.dbConn: Engine = dbConn

        metadata: MetaData = MetaData()

        listTableSchema: Table = Table(
            "lists",
            metadata,
            Column("id", Integer),
            Column("author", String),
            Column("name", String),
            Column("url", String),
            PrimaryKeyConstraint("id"),
        )
