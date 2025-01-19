#!/bin/bash
set -e

PG_USER=${POSTGRES_USER:-postgres}
PG_DB=${POSTGRES_DB:-postgres}

pg_isready -U "$PG_USER" -d "$PG_DB"