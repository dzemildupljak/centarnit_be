"""Init migration

Revision ID: 623c06223e56
Revises: 
Create Date: 2021-05-21 17:04:16.753186

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

Session = sessionmaker()


# revision identifiers, used by Alembic.
revision = '623c06223e56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('role', sa.String(), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('blogs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('body', sa.String(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_blogs_id'), 'blogs', ['id'], unique=False)
    #################
    bind = op.get_bind()
    session = Session(bind=bind)
    hs_password = pwd_cxt.hash('sysadmin')
    insert_sysadmin_sql = "INSERT INTO USERS (NAME,EMAIL,ROLE,USERNAME,PASSWORD) VALUES ('sysadmin','sysadmin@mail.com', 'sysadmin','sysadmin','{var_password}')"
    session.execute(insert_sysadmin_sql.format(var_password=hs_password))
    #################
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blogs_id'), table_name='blogs')
    op.drop_table('blogs')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
