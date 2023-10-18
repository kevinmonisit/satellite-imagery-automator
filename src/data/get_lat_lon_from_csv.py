import csv

with open('combined_wikimapia_osm_leb.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('output_lat_lon.txt', mode='w') as txt_file:
        for row in csv_reader:
            lat = row['lat']
            lon = row['lon']

            txt_file.write(f"{lat}, {lon}\n")

print("The latitude and longitude values have been written to output_lat_lon.txt")
