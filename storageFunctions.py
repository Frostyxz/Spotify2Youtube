import json

#Functions for storage

#Checks if file exists
def storage_checker(file_name):
    try:
        open(file_name)
    except IOError:
        print('NOTE: Previous storage file not found, another will be made if possible.')
        return False
    return True

#Reads a json file and appends the contents to the object
def storage_reader(file_name, storage):
    with open(file_name) as json_file:
        storageTemp = json.load(json_file)
        for s in storageTemp['Songs']:
            storage['Songs'].append(s)
            print('Song found:' , s['name'])
        return storage

#Appends a lists elements to the json object
def storage_append(storage, list):
    for ele in list:
        storage['Songs'].append({
            'name': ele,
        })
    return storage

#Checks if a list's content matches a json object's content
def storage_match(storage, list):
    for i, ele in enumerate(storage['Songs']):
        if ele['name'] in list:
            print("Song already found, removing:" , ele['name'])
            list.remove(ele['name'])
    return list

#Writes to the file
def storage_writer(file_name, storage):
    with open(file_name, 'w') as outfile:
        json.dump(storage, outfile, indent=2)