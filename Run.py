import persistqueue


Hotmail = persistqueue.SQLiteQueue('HotMailACC', auto_commit=True)
# if Hotmail.qsize() == 0:
#     with open('NewHotMail.txt', 'r') as f:
#         ACC = f.readlines()
#     for acc in ACC:
#         Hotmail.put(acc.strip("\n"))
# print(Hotmail.qsize())
for i in range(Hotmail.qsize()):
      print(Hotmail.get())
