from dataclasses import dataclass, field
from typing import Optional, List

from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import registry, Session, relationship

DB_URL = 'postgresql://localhost:5432/sqlalchemy_list_removal_test'
mapper_registry = registry()


def drop_tables(engine):
    engine.execute('''
DROP TABLE IF EXISTS foo_bar;
DROP TABLE IF EXISTS foo;
DROP TABLE IF EXISTS bar;    
    ''')


def create_tables(engine):
    engine.execute('''
CREATE TABLE foo
(
    id          SERIAL
        CONSTRAINT foo_pk
            PRIMARY KEY,
    some_column TEXT
);

CREATE TABLE bar
(
    id             SERIAL
        CONSTRAINT bar_pk
            PRIMARY KEY,
    another_column TEXT
);

CREATE TABLE foo_bar
(
    foo_id INT
        CONSTRAINT foo_bar_foo_id_fk
            REFERENCES foo,
    bar_id INT
        CONSTRAINT foo_bar_bar_id_fk
            REFERENCES bar
);

    ''')


@mapper_registry.mapped
@dataclass
class Foo:
    __tablename__ = 'foo'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(
        init=False,
        metadata={
            'sa': Column(Integer, primary_key=True, nullable=False),
        },
    )

    some_column: Optional[str] = field(
        default=None,
        metadata={
            'sa': Column(Text, nullable=True),
        },
    )

    bars: List['Bar'] = field(
        default_factory=list,
        metadata={
            'sa': relationship(
                'Bar',
                secondary='foo_bar',
                uselist=True,
                back_populates='foos',
            )
        },
    )


@mapper_registry.mapped
@dataclass
class Bar:
    __tablename__ = 'bar'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(
        init=False,
        metadata={
            'sa': Column(Integer, primary_key=True, nullable=False),
        },
    )

    another_column: Optional[str] = field(
        default=None,
        metadata={
            'sa': Column(Text, nullable=True),
        },
    )

    foos: List['Foo'] = field(
        default_factory=list,
        metadata={
            'sa': relationship(
                'Foo',
                secondary='foo_bar',
                uselist=True,
                back_populates='bars',
            )
        },
    )


@mapper_registry.mapped
@dataclass
class FooBar:
    __tablename__ = 'foo_bar'
    __sa_dataclass_metadata_key__ = 'sa'

    foo_id: int = field(metadata={'sa': Column(ForeignKey('foo.id'), primary_key=True)})
    bar_id: int = field(metadata={'sa': Column(ForeignKey('bar.id'), primary_key=True)})


def populate_tables(engine):
    with Session(engine) as session:
        foo = Foo(some_column='foo_1')
        bar_1 = Bar(another_column='bar_1')
        bar_2 = Bar(another_column='bar_2')

        foo.bars.append(bar_1)
        foo.bars.append(bar_2)

        session.add(foo)
        session.commit()


def remove_second_item(engine):
    with Session(engine) as session:
        foo = session.query(Foo).first()
        bar_2 = session.query(Bar).filter(Bar.another_column == 'bar_2').first()

        foo.bars.remove(bar_2)
        session.commit()


def remove_first_item(engine):
    with Session(engine) as session:
        foo = session.query(Foo).first()
        bar_1 = session.query(Bar).filter(Bar.another_column == 'bar_1').first()

        foo.bars.remove(bar_1)
        session.commit()


def main():
    engine = create_engine(DB_URL, echo=True)
    drop_tables(engine)
    create_tables(engine)

    # Populating tables with sample data and checking the amount of `bar` items associated with `foo` object
    populate_tables(engine)
    with Session(engine) as session:
        foo = session.query(Foo).first()
        assert len(foo.bars) == 2
        assert session.query(FooBar).count() == 2
        assert session.query(Bar).count() == 2

    # Removing the second item from the list of bars, item was not removed from DB
    remove_second_item(engine)
    with Session(engine) as session:
        foo = session.query(Foo).first()
        assert len(foo.bars) == 2
        assert session.query(FooBar).count() == 2
        assert session.query(Bar).count() == 2

    # Removing the first item from the list of bars, item was removed from db
    remove_first_item(engine)
    with Session(engine) as session:
        foo = session.query(Foo).first()
        assert len(foo.bars) == 1
        assert session.query(FooBar).count() == 1
        assert session.query(Bar).count() == 2


if __name__ == '__main__':
    main()
