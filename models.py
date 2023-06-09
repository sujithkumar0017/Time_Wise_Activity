from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class user(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    phone = Column(Integer,nullable=True)
    password = Column(String,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class post(Base):

    __tablename__ = "post"
    id= Column(Integer,primary_key=True,nullable=False)
    post_name = Column(String,nullable=False)
    content = Column(String,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("user")

class activity(Base):

    __tablename__ = "user_activity"
    id= Column(Integer,primary_key=True,nullable=False)
    entity_id = Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),nullable=False)
    entity_type = Column(String(255), default='Post')
    raw_data = Column(String)
    actor = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    action = Column(String(255), default='Created')



