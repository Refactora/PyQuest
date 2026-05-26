"""Initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-05-26
"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('username', sa.String(30), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('avatar_id', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('level', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('xp', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('xp_to_next', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('total_xp', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('hp_max', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('streak_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_active', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('locations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('slug', sa.String(50), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('topic', sa.String(100), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('boss_name', sa.String(100), nullable=False),
        sa.Column('boss_sprite_id', sa.String(50), nullable=False),
        sa.Column('background_id', sa.String(50), nullable=False),
        sa.Column('enemy_sprite_id', sa.String(50), nullable=False),
        sa.Column('color_theme', sa.String(7), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
        sa.UniqueConstraint('order_index'),
    )

    op.create_table('questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('code_snippet', sa.Text(), nullable=True),
        sa.Column('option_a', sa.Text(), nullable=False),
        sa.Column('option_b', sa.Text(), nullable=False),
        sa.Column('option_c', sa.Text(), nullable=False),
        sa.Column('option_d', sa.Text(), nullable=False),
        sa.Column('correct_option', sa.String(1), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.Integer(), server_default='1'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('boss_challenges',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('story_text', sa.Text(), nullable=False),
        sa.Column('task_text', sa.Text(), nullable=False),
        sa.Column('function_signature', sa.String(200), nullable=False),
        sa.Column('function_call_template', sa.String(300), nullable=False),
        sa.Column('starter_code', sa.Text(), nullable=False),
        sa.Column('test_cases', sa.JSON(), nullable=False),
        sa.Column('hints', sa.JSON(), nullable=False),
        sa.Column('boss_hp', sa.Integer(), server_default='100'),
        sa.Column('time_limit_sec', sa.Integer(), server_default='10'),
        sa.Column('memory_limit_mb', sa.Integer(), server_default='128'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('location_id'),
    )

    op.create_table('achievements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('slug', sa.String(50), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=False),
        sa.Column('icon_id', sa.String(50), nullable=False),
        sa.Column('xp_reward', sa.Integer(), server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )

    op.create_table('user_location_progress',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='locked'),
        sa.Column('quiz_completed', sa.Boolean(), server_default='false'),
        sa.Column('boss_defeated', sa.Boolean(), server_default='false'),
        sa.Column('best_quiz_score', sa.Integer(), server_default='0'),
        sa.Column('quiz_attempts', sa.Integer(), server_default='0'),
        sa.Column('boss_attempts', sa.Integer(), server_default='0'),
        sa.Column('hints_used', sa.Integer(), server_default='0'),
        sa.Column('first_try_boss', sa.Boolean(), server_default='false'),
        sa.Column('no_death_run', sa.Boolean(), server_default='false'),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'location_id'),
    )

    op.create_table('quiz_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('questions_order', sa.JSON(), nullable=False),
        sa.Column('current_index', sa.Integer(), server_default='0'),
        sa.Column('hero_hp', sa.Integer(), nullable=False),
        sa.Column('correct_answers', sa.Integer(), server_default='0'),
        sa.Column('wrong_answers', sa.Integer(), server_default='0'),
        sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('boss_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('challenge_id', sa.Integer(), nullable=False),
        sa.Column('hero_hp', sa.Integer(), nullable=False),
        sa.Column('boss_hp', sa.Integer(), server_default='100'),
        sa.Column('hints_used', sa.Integer(), server_default='0'),
        sa.Column('submissions', sa.JSON(), server_default='[]'),
        sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('is_won', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.ForeignKeyConstraint(['challenge_id'], ['boss_challenges.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('user_achievements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('achievement_id', sa.Integer(), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'achievement_id'),
    )

    op.create_table('daily_quests',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('quest_date', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE')),
        sa.Column('quest_type', sa.String(50), nullable=False),
        sa.Column('description', sa.String(300), nullable=False),
        sa.Column('target_value', sa.Integer(), nullable=False),
        sa.Column('current_value', sa.Integer(), server_default='0'),
        sa.Column('xp_reward', sa.Integer(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), server_default='false'),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'quest_date', 'quest_type'),
    )


def downgrade():
    for table in ['daily_quests','user_achievements','boss_sessions','quiz_sessions',
                  'user_location_progress','achievements','boss_challenges','questions','locations','users']:
        op.drop_table(table)
