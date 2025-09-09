#!/bin/bash
set -e  # 중간에 에러나면 스크립트 종료

echo "Alembic DB Stamp..."
alembic stamp head

echo "Alembic Revision Autogenerate..."
alembic revision --autogenerate -m "update"

echo "Alembic DB Upgrade..."
alembic upgrade head

echo "Alembic migration steps completed."