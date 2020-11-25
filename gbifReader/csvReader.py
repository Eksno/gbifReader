import csv


def csv_to_list(csv_file):
    print(f"\nConverting {csv_file} to list...")

    print(f" - Opening {csv_file}...")
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)

        print(" - Creating list of contents...")

        val = []
        for row in reader:
            val.append(row)

    print(f" / {csv_file} has been converted.")

    return val
