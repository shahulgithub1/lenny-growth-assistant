"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Sessions table
    op.create_table(
        'sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_created_at'), 'sessions', ['created_at'], unique=False)

    # Messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('sources', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_session_id'), 'messages', ['session_id'], unique=False)
    op.create_index(op.f('ix_messages_created_at'), 'messages', ['created_at'], unique=False)

    # Artifacts table
    op.create_table(
        'artifacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('message_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artifacts_session_id'), 'artifacts', ['session_id'], unique=False)

    # Transcript chunks table
    op.create_table(
        'transcript_chunks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('episode_title', sa.String(length=500), nullable=True),
        sa.Column('guest', sa.String(length=255), nullable=True),
        sa.Column('source_file', sa.String(length=500), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transcript_chunks_source_file'), 'transcript_chunks', ['source_file'], unique=False)
    op.create_index(op.f('ix_transcript_chunks_episode_title'), 'transcript_chunks', ['episode_title'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_transcript_chunks_episode_title'), table_name='transcript_chunks')
    op.drop_index(op.f('ix_transcript_chunks_source_file'), table_name='transcript_chunks')
    op.drop_table('transcript_chunks')
    op.drop_index(op.f('ix_artifacts_session_id'), table_name='artifacts')
    op.drop_table('artifacts')
    op.drop_index(op.f('ix_messages_created_at'), table_name='messages')
    op.drop_index(op.f('ix_messages_session_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_sessions_created_at'), table_name='sessions')
    op.drop_table('sessions')
