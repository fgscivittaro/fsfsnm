import csv

def split_names(old_filename, new_filename):
    """
    Takes an existing file, splits the name column into first name and last
    name columns, and creates a new file with the new data.
    """

    oldfile = open(old_filename)
    newfile= open(new_filename, 'a')

    old_list = list(oldfile)
    headers = old_list.pop(0).split(",")

    del(headers[0])
    added_headers = ['LastName','FirstName']
    new_headers = added_headers + headers

    newfile.write(','.join(new_headers))

    for row in old_list:
        if row[:4] != "Name":
            data = row.split(',')
            player_name = data.pop(0)
            first_last = player_name.split()
            data.insert(0, first_last[1])
            data.insert(1, first_last[0])

            newfile.write(','.join(data))

    oldfile.close()
    newfile.close()