# string_list = ['a','b','c','d','e','f']

# yes = [i for i in string_list if 'f' in i]

# print(yes)

# users = [{"id": "limliht-asg", "name": "limliht-asg"}, {"id": "limliht2-asg", "name": "limliht2-asg"}, {"id": "limliht3-asg", "name": "limliht3-asg"}, {"id": "limliht4-asg", "name": "limliht4-asg"}]

# for user_dict in users:
#     for i, j in user_dict.items():
#         if j == 'limliht-asg':
#             print('yes')
#         else:
#             print('no')
            
            
            
names = [{'name':'Tom', 'age': 10}, {'name': 'Mark', 'age': 5}, {'name': 'Pam', 'age': 7}]
# resultlist = [d for d in names if d.get('name', '') == 'Pam']
# first_result = resultlist[0]
# print(first_result)
# print(resultlist)

result = next((item for item in names if item["name"] == "Sam"), False) #This return default value = False
print(result)

# lst = [{"id": "limliht-asg", "name": "limliht-asg"}, {"id": "limliht2-asg", "name": "limliht2-asg"}, {"id": "limliht3-asg", "name": "limliht3-asg"}, {"id": "limliht4-asg", "name": "limliht4-asg"}]

# if next(item for item in lst if item['id'] == 'limliht-asg') is not None:
#     print('yes')
# else:
#     print('no')