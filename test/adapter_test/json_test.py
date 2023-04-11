data_list = [1, 2, 3, 4, 5, 6]
data_dict = {"a": [1], "b": [2], "c": [3]}

# Path: test/adapter_test/json_test.py

from adapter import JsonAdapter

li = JsonAdapter(data=data_list)
li_data = li.to_df()
print(li_data)

di = JsonAdapter(data=data_dict)
di_data = di.to_df()
print(di_data)
