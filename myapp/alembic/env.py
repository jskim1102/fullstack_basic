import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# 현재 디렉터리의 상위 두 단계 디렉터리 (practice 디렉터리)를 sys.path에 추가하여 myapp 모듈을 찾도록 설정
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# 환경 변수 로드
load_dotenv()

# Alembic 설정 파일 불러오기
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# 로깅 설정
fileConfig(config.config_file_name)

# 모델을 임포트하여 target_metadata 설정
from myapp.models import Base  # myapp.models 모듈에서 Base를 가져옴
target_metadata = Base.metadata  # Alembic이 사용할 메타데이터를 Base.metadata로 설정

def run_migrations_offline():
    """Offline 모드에서의 마이그레이션 실행"""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Online 모드에서의 마이그레이션 실행"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()