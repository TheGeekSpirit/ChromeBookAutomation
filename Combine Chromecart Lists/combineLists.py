import csv
import os

directory = input("Enter the path to the folder with the Chromecart lists:")

with open("allSerials.csv", mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    for file in os.listdir(directory):
        filePath = os.path.join(directory, file)
        fileData = csv.reader(open(filePath))

        for serial in fileData:
            csv_writer.writerow(serial)