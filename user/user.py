from models import User, SessionLocal

session = SessionLocal()


new_user = User(login="dontafraid121@icloud.com", password="Allornothing12", account_url='https://www.vinted.pl/member/228609071')
session.add(new_user)
session.commit()