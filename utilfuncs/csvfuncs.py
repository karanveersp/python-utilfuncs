import csv

def get_rows(csvpath):
    with open(csvpath, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row


def write_rows(csvpath, list_of_rows):
    with open(csvpath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_of_rows)


def append_row(csvpath, row):
    with open(csvpath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


def append_rows(csvpath, rows):
    for row in rows:
        append_row(csvpath, row)
