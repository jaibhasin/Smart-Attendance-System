"""added changes

Revision ID: e5859ca3bed2
Revises: dafdec4c6372
Create Date: 2025-05-18 21:49:44.544035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5859ca3bed2'
down_revision = 'dafdec4c6372'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classroom', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_classroom_course', 'course', ['course_id'], ['course_id'])

    with op.batch_alter_table('parent', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('professor', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('professor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=100), nullable=True))

    with op.batch_alter_table('parent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=100), nullable=True))

    with op.batch_alter_table('classroom', schema=None) as batch_op:
        batch_op.drop_constraint('fk_classroom_course', type_='foreignkey')
        batch_op.drop_column('course_id')

    # ### end Alembic commands ###
