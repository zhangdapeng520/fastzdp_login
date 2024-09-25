from sqlmodel import create_engine,SQLModel
import fastzdp_login

# 创建数据库引擎
db_url = "mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/fastzdp_login?charset=utf8mb4"
engine = create_engine(db_url, echo=True)

# 确保表存在
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
