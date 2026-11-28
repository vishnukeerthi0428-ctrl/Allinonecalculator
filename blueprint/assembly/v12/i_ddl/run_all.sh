#!/bin/bash
# Group I (Part 11.9) reproducible build: Appendix C + C2 + C3 on a scratch PostgreSQL 16, then V12 and C3 tests.
set -e
D=$(cd "$(dirname "$0")" && pwd); P="-h ${PGHOST:-/tmp/pgv12} -p ${PGPORT:-55432} -U postgres"
psql $P -q -c 'drop database if exists v12c3' -c 'create database v12c3' >/dev/null
for f in appendix_c.sql appendix_c2.sql c3_part1_manual.sql c3_part2_new_tables.sql; do psql $P -d v12c3 -v ON_ERROR_STOP=1 -q -f $D/$f 2>&1 | grep -v NOTICE || true; done
python3 -I $D/gen_c3.py $P -d v12c3
psql $P -d v12c3 -v ON_ERROR_STOP=1 -q -f $D/c3_part3_generated.sql 2>&1 | grep -v NOTICE || true
cat $D/c3_part1_manual.sql $D/c3_part2_new_tables.sql $D/c3_part3_generated.sql > $D/appendix_c3_group_i.sql
psql $P -d v12c3 -f $D/c3_tests.sql 2>&1 | grep -E 'PASS|FAIL|ERROR|EXECUTED' | sed 's/psql:[^:]*:[0-9]*: //' > $D/c3_tests.out
psql $P -d v12c3 -f $D/c3_v12_regression.sql 2>&1 | grep -v '^BEGIN\|^ROLLBACK\|^COMMIT\|^SET\|^INSERT\|^count$\|^(1 row)\|^?column?\|^t_ctx\|^$\|^|\|^set_config\|^Output' | sed 's/psql:[^:]*:[0-9]*: //' > $D/c3_v12_regression.out
grep -c PASS $D/c3_tests.out; grep -c FAIL $D/c3_tests.out || true
