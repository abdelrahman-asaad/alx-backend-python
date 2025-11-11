def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]
    return nested_map

#ex
nested_map = {"a":1}
path = ("a",)

print(access_nested_map(nested_map, path))  # should return nested_map["a"] which is 1
# output: 1

print(access_nested_map({"a": {"b": 2}}, ("a",)))  
# output: {'b': 2}


print(access_nested_map({"a": {"b": 2},"b":3 }, ("a","b"))) 
# output: 2 
#         nested_map["a"] is {"b": 2} >> so the nested_map becomes {"b": 2} 
#         then in second iteration key is "b" >> so nested_map["b"] is 2

print(access_nested_map({"a": {"b": 2}}, ("a", "b"))) #should return nested_map["b"] which is 2
# output: 2

#explanation:
# in first iteration key is "a", so nested_map becomes 1 >> then in second iteration there is no second 
# iteration as path has only one element.



#________
def access_nested_mapp(nested_map, path):
    for key in path:
        nested_mapp = nested_map[key]
        print(nested_mapp)
    


access_nested_mapp({"a": {"b": 2},"b":3 }, ("a","b"))
# output: {'b': 2}
#          3