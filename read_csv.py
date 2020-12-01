import csv
import pprint

with open('./resource/ngsl.csv', 'r') as f:
  render = csv.reader(f)
  l = [row for row in render]

pprint.pprint(l[1])