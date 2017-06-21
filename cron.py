import speedtest
import csv

from pushbullet import Pushbullet

# read pushbullet API token from pushbullet_token.txt
with open('pushbullet_token.txt') as token_txt:
    access_token = token_txt.readline()

# min download bandwith (bit/s)
download_min = 75000000

# min upload bandwith (bit/s)
upload_min = 25000000

# max ping in ms
ping_max = 30

# disable in production
test_run = True

servers = []
s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download()
s.upload()

share_url = s.results.share()[:-4]

if s.results.download < download_min or s.results.upload < upload_min or s.results.ping > ping_max or test_run:
    pb = Pushbullet(api_key=access_token)
    push = pb.push_link("Internet Bandwidth Warning",
                        share_url,
                        "down: %d Mb/s\nup: %d Mb/s\nping: %d ms\n" %
                        (s.results.download/1000000, s.results.upload/1000000, s.results.ping))

results_dict = s.results.dict()

with open('stats.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([results_dict['timestamp'],
                     results_dict['download'],
                     results_dict['upload'],
                     results_dict['ping'],
                     results_dict['bytes_sent'],
                     results_dict['bytes_received'],
                     results_dict['share'][:-4],
                     results_dict['server']['url'],
                     results_dict['server']['lat'],
                     results_dict['server']['lon'],
                     results_dict['server']['name'],
                     results_dict['server']['country'],
                     results_dict['server']['cc'],
                     results_dict['server']['sponsor'],
                     results_dict['server']['id'],
                     results_dict['server']['url2'],
                     results_dict['server']['host'],
                     results_dict['server']['d'],
                     results_dict['server']['latency']])
