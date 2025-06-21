import re
names = []
departures =  ('Youssef essaadouny, Said Hammouch, Elmokhtar Lazrak')  
# for l in departures:
#      names.append(l)
names = departures.split(',')
print(f'list is : {names}')
for name in names:

