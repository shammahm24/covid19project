import dbconnect as db

db.createAdminTable()
db.createQueryTable()

#db.addQuery("Country=='Austria'")
ad=db.allAdmin()
#for a in ad:
#    print(a)
#db.addAdmin("Admin3","pass3")
g=db.authenticate("Admin2","pass2")
print(g)
db.deleteQuery("Country='US'")

db.deleteQuery("Country='Austria'")

q=db.getQueries()

for q1 in q:
    print(q1[0])