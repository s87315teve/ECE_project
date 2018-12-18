from sklearn.externals import joblib 
import pandas as pd
import numpy as np
import sys
# df_test = pd.read_csv('./data_test.csv', header=0)
# array_test = df_test.values
# X_tmp1 = array_test[:,:3]
# X = X_tmp1
# clf = joblib.load('RVMresult_test19050.pkl')
# print(clf.predict(X[0:1]))

df_apcols=['STA_ID', \
         'STA_generate_time', \
         '_', \
         'ap_name', \
         'agg_start', \
         'agg_end(send)', \
         'sended_to_server_time']

df_stacols=['STA_ID', \
            'STA_generate_time', \
            'sended_to_ap_time']

df_logcols=['STA_ID', \
            'STA_generate_time', \
            'delay', \
            'server_catch_time']

df_outputs=['D_total', \
			'D_aggregation', \
			'D_block', \
      'ap_name']

# STATION_NAME = 'sta11'

if len(sys.argv) < 3:
   print "Usage:", sys.argv[0] , "arrival factorsize" 

df_apfile = pd.read_csv(sys.argv[1], header=0, names=df_apcols)
df_logfile = pd.read_csv(sys.argv[2], header=0, names=df_logcols)

df_total = pd.DataFrame(columns=df_outputs)

df_combine = df_logfile.merge(df_apfile, left_on='STA_generate_time' , right_on='STA_generate_time', how='inner')

df_total['D_total'] = df_combine['delay']
df_total['D_aggregation'] = (df_combine['agg_end(send)'] - df_combine['agg_start'])/df_combine['delay']/100
df_total['D_block'] = (df_combine['agg_start'] - df_combine['STA_generate_time'])/df_combine['delay']/100
df_total['D_total'] = df_combine['delay']/df_combine['delay']


df_total = df_total[df_total['D_block'] > 0]
df_total = df_total[df_total['D_total'] < 3000]

df_total = df_total.astype(np.float64)


df_total = df_total.groupby(np.arange(len(df_total))//20).mean()

df_total['ap_name'] = df_combine['ap_name']
print(df_total)

# df_apfile = df_apfile[df_apfile['STA_ID'] == STATION_NAME]
# df_stafile = df_stafile[df_stafile['STA_ID'] == STATION_NAME]
# df_logfile = df_logfile[df_logfile['STA_ID'] == STATION_NAME]

# df_apfile.reset_index(inplace=True)
# df_stafile.reset_index(inplace=True)
# df_logfile.reset_index(inplace=True)

# print(df_apfile.size)
# print(df_stafile.size)
# print(df_logfile.size)

# first_ap = df_apfile \
#            .index[df_apfile['STA generate time'] == df_logfile['STA generate time']].get_values()
# df_apfile = df_apfile.drop(df_apfile.index[range(first_ap[0])]) #

# print(df_apfile['STA generate time'] == df_logfile['STA generate time'])

# df_apfile.reset_index(inplace=True)

# first_log = df_logfile \
#            .index[df_logfile['STA generate time'] == df_apfile['STA generate time'][0]].get_values()
# df_logfile = df_logfile.drop(df_logfile.index[range(first_log[0])]) # 
# df_logfile.reset_index(inplace=True)

# first_sta = df_stafile \
#            .index[df_stafile['STA generate time'] == df_apfile['STA generate time'][0]].get_values()
# df_stafile = df_stafile.drop(df_stafile.index[range(first_sta[0])]) # 
# df_stafile.reset_index(inplace=True)

# df_total['D_total'] = df_logfile['delay']
# df_total['D_aggregation'] = (df_apfile['agg end(send)'] - df_apfile['agg start'])/100
# df_total['D_block'] = (df_apfile['agg start'] - df_apfile['STA generate time'])/100

# print(df_total)

df_total.to_csv('out.csv', sep=',')


