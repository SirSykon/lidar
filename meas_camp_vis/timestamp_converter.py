import gnss_utils
import lidar_utils
import datetime
import pandas as pd
import numpy as np
import csv

#gnss_file_path = r'C:\Users\hoes_lu\Documents\Diplomarbeit\20211105_Aurora_ZiekerSee\BOW_CSRS_PPP'
#gnss_file_path = r'C:\Users\hoes_lu\Documents\Diplomarbeit\20211105_Aurora_ZiekerSee\ROOF_CSRS_PPP'
#gnss_file_path = r'H:\data\20211110_Solution\BOW_CSRS_PPP'
gnss_file_path = r'H:\data\20211110_Solution\ROOF_CSRS_PPP'
#gnss_file_name = 'BOW000DEU_R_20213091011_03H_02Z_MO.csv'
#gnss_file_name = 'ROOF00DEU_R_20213091011_03H_02Z_MO.csv'
#gnss_file_name = 'BOW000DEU_R_20213141001_03H_02Z_MO.csv'
gnss_file_name = 'ROOF00DEU_R_20213141001_03H_02Z_MO.csv'
gnss_dataframe = gnss_utils.load_position_data(gnss_file_path+'/'+gnss_file_name)

storage_path_new_gnss = r'C:\Users\hoes_lu\Documents\Diplomarbeit\my_playground\data'
new_gnss_file_name = 'processed'+gnss_file_name

lidar_csv_name = 'C:/Users/hoes_lu/Documents/Diplomarbeit/my_playground/point_cloud_aurora_zirkerSee_20211105.csv'
lidar_dataframe = lidar_utils.read_file(lidar_csv_name)

lidar_start = round(lidar_dataframe.iloc[0]['unix timestamp']/1e9)
lidar_start = datetime.datetime.fromtimestamp(lidar_start)
print(lidar_start)

start_time = datetime.datetime(2021,11,10,11,5,0)
#start_time = lidar_start.hour + lidar_start.minute/60 + lidar_start.second/3600
start_time = start_time.hour*3600 + start_time.minute*60 + start_time.second
print(start_time)
print(gnss_dataframe['decimal_hour']*3600)

my_timestamp = 0
header = ['unix timestamp', 'latitude_decimal_degree', 'longitude_decimal_degree', 'ellipsoidal_height_m', 'rcvr_clk_ns']
with open(storage_path_new_gnss+'/'+new_gnss_file_name, mode='w') as f:
        w = csv.writer(f)
        w.writerow(header)

for i in np.arange(0,len(gnss_dataframe)):
    # get timestamp from gnss csv
    base = datetime.datetime(1970,1,1)
    day_of_year = str(gnss_dataframe.iloc[i]['day_of_year']).strip()
    year = int(gnss_dataframe.iloc[i]['year'])
    start_date_of_year = datetime.date(year,1,1)
    res_date = start_date_of_year+datetime.timedelta(days=float(day_of_year)-1)
    # generate datetime object
    hour = int(gnss_dataframe.iloc[i]['decimal_hour'])
    minute = int((gnss_dataframe.iloc[i]['decimal_hour']*60) % 60)
    second = int((gnss_dataframe.iloc[i]['decimal_hour']*3600) % 60)
    microsencond = int((gnss_dataframe.iloc[i]['decimal_hour']*3600) % 60 % 1 * 1e6)
    current_datetime = datetime.datetime(res_date.year, res_date.month, res_date.day, hour, minute, second, microsencond)
    # convert it to unix
    current_unix = int((current_datetime-base).total_seconds()*1000)

    #select only 1 timestamp per second and store it as unix
    if round(current_unix/1000) != my_timestamp:
        print('selected timestamp '+str(round(current_unix/1000)))
        # generate dataframe to store the data there
        #cloud_size = len(current_gnss_data)
        this_data = {header[0]: np.zeros(1), header[1]: np.zeros(1), header[2]: np.zeros(1), header[3]: np.zeros(1), header[4]: np.zeros(1)}
        this_data_frame = pd.DataFrame(this_data)
        # store data in the generated dataframe
        this_data_frame[header[0]] = current_unix
        this_data_frame[header[1]] = gnss_dataframe.iloc[i]['latitude_decimal_degree']
        this_data_frame[header[2]] = gnss_dataframe.iloc[i]['longitude_decimal_degree']
        this_data_frame[header[3]] = gnss_dataframe.iloc[i]['ellipsoidal_height_m']
        this_data_frame[header[4]] = gnss_dataframe.iloc[i]['rcvr_clk_ns']
        # append it to a csv file
        this_data_frame.to_csv(storage_path_new_gnss+'/'+new_gnss_file_name, header=False, mode='a', index=False)

    my_timestamp = round(current_unix/1000)
    print('timestamp '+str(i)+' : '+str(current_unix))

# with open(storage_path_new_gnss+'/'+new_gnss_file_name) as in_file:
#     with open(storage_path_new_gnss+'/'+new_gnss_file_name, 'w') as out_file:
#         writer = csv.writer(out_file)
#         for row in csv.reader(in_file):
#             if any(field.strip() for field in row):
#                 writer.writerow(row)