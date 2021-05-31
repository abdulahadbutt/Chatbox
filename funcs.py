import csv


def csv_reader(fname: str):
# * @param fname The name of the file 

    usernames = []
    passwords = []
    with open(fname) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            usernames.append(row[0])
            passwords.append(row[1])

    return (usernames, passwords)