from subprocess import call
import datetime
import sqlite3



def gen_ws_id():
	import uuid
	return uuid.uuid1().hex

ws_name = gen_ws_id()

conn = sqlite3.connect("/Users/lincai/MaProject/website/db.sqlite3") #../website/db.sqlite3
# call(["mkdir", "../workspaces/" + gen_ws_id()])
# Copy ../class files to workspace
call(["sh","create_ws_content.sh",ws_name])

c = conn.cursor()
c.execute("INSERT INTO questions_question (question_text,workspace,pub_date) \
      VALUES ('Question From shell','" + ws_name +"','"+str(datetime.datetime.now())+"');")
# print("INSERT INTO questions_question (question_text,uuid,pub_date) \
#       VALUES ('Question From shell','" + ws_name +"','"+str(datetime.datetime.now())+"')")
conn.commit()

conn.close()
print("Workspace created: "+ws_name)


