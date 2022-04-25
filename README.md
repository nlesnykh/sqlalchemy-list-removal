Program output:
```
2022-04-25 17:40:09,291 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2022-04-25 17:40:09,291 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-04-25 17:40:09,292 INFO sqlalchemy.engine.Engine select current_schema()
2022-04-25 17:40:09,292 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-04-25 17:40:09,292 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2022-04-25 17:40:09,292 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-04-25 17:40:09,293 INFO sqlalchemy.engine.Engine 
DROP TABLE IF EXISTS foo_bar;
DROP TABLE IF EXISTS foo;
DROP TABLE IF EXISTS bar;    
    
2022-04-25 17:40:09,293 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-04-25 17:40:09,295 INFO sqlalchemy.engine.Engine COMMIT
2022-04-25 17:40:09,297 INFO sqlalchemy.engine.Engine 
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

    
2022-04-25 17:40:09,297 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-04-25 17:40:09,305 INFO sqlalchemy.engine.Engine COMMIT
2022-04-25 17:40:09,310 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-04-25 17:40:09,311 INFO sqlalchemy.engine.Engine INSERT INTO bar (another_column) VALUES (%(another_column)s) RETURNING bar.id
2022-04-25 17:40:09,311 INFO sqlalchemy.engine.Engine [generated in 0.00015s] ({'another_column': 'bar_1'}, {'another_column': 'bar_2'})
2022-04-25 17:40:09,314 INFO sqlalchemy.engine.Engine INSERT INTO foo (some_column) VALUES (%(some_column)s) RETURNING foo.id
2022-04-25 17:40:09,314 INFO sqlalchemy.engine.Engine [generated in 0.00012s] {'some_column': 'foo_1'}
2022-04-25 17:40:09,315 INFO sqlalchemy.engine.Engine INSERT INTO foo_bar (foo_id, bar_id) VALUES (%(foo_id)s, %(bar_id)s)
2022-04-25 17:40:09,315 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ({'foo_id': 1, 'bar_id': 2}, {'foo_id': 1, 'bar_id': 1})
2022-04-25 17:40:09,316 INFO sqlalchemy.engine.Engine COMMIT
2022-04-25 17:40:09,317 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-04-25 17:40:09,318 INFO sqlalchemy.engine.Engine SELECT foo.id AS foo_id, foo.some_column AS foo_some_column 
FROM foo 
 LIMIT %(param_1)s
2022-04-25 17:40:09,318 INFO sqlalchemy.engine.Engine [generated in 0.00012s] {'param_1': 1}
2022-04-25 17:40:09,320 INFO sqlalchemy.engine.Engine SELECT bar.id AS bar_id, bar.another_column AS bar_another_column 
FROM bar 
WHERE bar.another_column = %(another_column_1)s 
 LIMIT %(param_1)s
2022-04-25 17:40:09,320 INFO sqlalchemy.engine.Engine [generated in 0.00011s] {'another_column_1': 'bar_2', 'param_1': 1}
2022-04-25 17:40:09,322 INFO sqlalchemy.engine.Engine SELECT bar.id AS bar_id, bar.another_column AS bar_another_column 
FROM bar, foo_bar 
WHERE %(param_1)s = foo_bar.foo_id AND bar.id = foo_bar.bar_id
2022-04-25 17:40:09,322 INFO sqlalchemy.engine.Engine [generated in 0.00014s] {'param_1': 1}
2022-04-25 17:40:09,324 INFO sqlalchemy.engine.Engine SELECT foo.id AS foo_id, foo.some_column AS foo_some_column 
FROM foo, foo_bar 
WHERE %(param_1)s = foo_bar.bar_id AND foo.id = foo_bar.foo_id
2022-04-25 17:40:09,324 INFO sqlalchemy.engine.Engine [generated in 0.00012s] {'param_1': 1}
2022-04-25 17:40:09,325 INFO sqlalchemy.engine.Engine SELECT foo.id AS foo_id, foo.some_column AS foo_some_column 
FROM foo, foo_bar 
WHERE %(param_1)s = foo_bar.bar_id AND foo.id = foo_bar.foo_id
2022-04-25 17:40:09,325 INFO sqlalchemy.engine.Engine [cached since 0.000912s ago] {'param_1': 2}
2022-04-25 17:40:09,326 INFO sqlalchemy.engine.Engine COMMIT
2022-04-25 17:40:09,326 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-04-25 17:40:09,326 INFO sqlalchemy.engine.Engine SELECT foo.id AS foo_id, foo.some_column AS foo_some_column 
FROM foo 
 LIMIT %(param_1)s
2022-04-25 17:40:09,326 INFO sqlalchemy.engine.Engine [cached since 0.008456s ago] {'param_1': 1}
2022-04-25 17:40:09,327 INFO sqlalchemy.engine.Engine SELECT bar.id AS bar_id, bar.another_column AS bar_another_column 
FROM bar 
WHERE bar.another_column = %(another_column_1)s 
 LIMIT %(param_1)s
2022-04-25 17:40:09,327 INFO sqlalchemy.engine.Engine [cached since 0.007373s ago] {'another_column_1': 'bar_1', 'param_1': 1}
2022-04-25 17:40:09,328 INFO sqlalchemy.engine.Engine SELECT bar.id AS bar_id, bar.another_column AS bar_another_column 
FROM bar, foo_bar 
WHERE %(param_1)s = foo_bar.foo_id AND bar.id = foo_bar.bar_id
2022-04-25 17:40:09,328 INFO sqlalchemy.engine.Engine [cached since 0.00566s ago] {'param_1': 1}
2022-04-25 17:40:09,329 INFO sqlalchemy.engine.Engine DELETE FROM foo_bar WHERE foo_bar.foo_id = %(foo_id)s AND foo_bar.bar_id = %(bar_id)s
2022-04-25 17:40:09,329 INFO sqlalchemy.engine.Engine [generated in 0.00011s] {'foo_id': 1, 'bar_id': 1}
2022-04-25 17:40:09,330 INFO sqlalchemy.engine.Engine COMMIT
2022-04-25 17:40:09,330 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-04-25 17:40:09,330 INFO sqlalchemy.engine.Engine SELECT foo.id AS foo_id, foo.some_column AS foo_some_column 
FROM foo 
 LIMIT %(param_1)s
2022-04-25 17:40:09,330 INFO sqlalchemy.engine.Engine [cached since 0.01258s ago] {'param_1': 1}
2022-04-25 17:40:09,331 INFO sqlalchemy.engine.Engine SELECT bar.id AS bar_id, bar.another_column AS bar_another_column 
FROM bar, foo_bar 
WHERE %(param_1)s = foo_bar.foo_id AND bar.id = foo_bar.bar_id
2022-04-25 17:40:09,331 INFO sqlalchemy.engine.Engine [cached since 0.009099s ago] {'param_1': 1}
bar_2
2022-04-25 17:40:09,332 INFO sqlalchemy.engine.Engine ROLLBACK
```