from datetime import datetime
str = "Hello World"

#print("String is %d bytes long" % len(str))

#print(str.upper())

#print(str.lower())

str2 = 'Please review the following information: \n\
here'

#print(str2)


#list = [1,2,3,4,5]


#print(*list, sep='\n')

#print(datetime.strptime('2012-05-29T19:30:03Z', '%Y-%m-%dT%H:%M:%SZ'))

list = [{"groupId": "sg-76717505"}, {"groupId": "sg-c1b666b5"}]
value = [i['groupId'] for i in list if 'groupId' in i]
#print(value)

mylist = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'f': 6}]
myvalues = [i['d'] for i in mylist if 'd' in i]
#print(myvalues)


accountpf_sg_list = [{'sg-A' : 'sg-fbde2f8c'},{'sg-B' : 'sg-9ba7c2ec'},{'sg-C': 'sg-352d1542'}]
#accountpf_sg_list = ['sg-fbde2f8c','sg-9ba7c2ec','sg-352d1542']

seach_value = 'sg-fbde2f8c'

xlist = {'george':16,'amber':19}
for name, age in xlist.items():    # for name, age in list.items():  (for Python 3.x)
    if age == 16:
        print(name)
        


li = [1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 6, 7, 7]   
print(dict(zip(li,li)))

lib = ['sg-A','sg-fbde2f8c','sg-B','sg-9ba7c2ec','sg-C','sg-352d1542']
lib2 = ['sg-fbde2f8c','sg-9ba7c2ec','sg-352d1542']
print(dict(zip(lib,lib2)))
combine_list = dict(zip(lib,lib2))
print(combine_list)

for name, sg_id in  combine_list.items():
    if sg_id == 'sg-fbde2f8c':
        print(name)

    


accountpf_sg_list = ['sg-fbde2f8c','sg-9ba7c2ec','sg-352d1542']
accountpf_sg_name = ['Prod_sg_mante','Monitor','Stag_account']
combine_sg_list = dict(zip(accountpf_sg_name,accountpf_sg_list))

print(combine_sg_list)

        



# for sg_list in accountpf_sg_list:
#     print(sg_list)






import re

s = 'asdf=5;iwantthis123jasd'
start = 'asdf=5;'
end = '123jasd'

result = re.search('%s(.*)%s' % (start, end), s).group(1)
print(result)