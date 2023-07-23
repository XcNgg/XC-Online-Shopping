"""empty message

Revision ID: 4af076465ebf
Revises: 6a9ac1c9c1af
Create Date: 2023-07-23 10:53:45.702681

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4af076465ebf'
down_revision = '6a9ac1c9c1af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('XcOS_order_detail', schema=None) as batch_op:
        batch_op.drop_constraint('XcOS_order_detail_ibfk_1', type_='foreignkey')
        batch_op.drop_column('address_id')
        batch_op.drop_column('total_amount')
        batch_op.drop_column('quantity')

    with op.batch_alter_table('XcOS_product', schema=None) as batch_op:
        batch_op.alter_column('simple_description',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=25),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('XcOS_product', schema=None) as batch_op:
        batch_op.alter_column('simple_description',
               existing_type=sa.Text(length=25),
               type_=mysql.TINYTEXT(),
               existing_nullable=True)

    with op.batch_alter_table('XcOS_order_detail', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('total_amount', mysql.DECIMAL(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('address_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('XcOS_order_detail_ibfk_1', 'XcOS_address', ['address_id'], ['id'])

    # ### end Alembic commands ###
