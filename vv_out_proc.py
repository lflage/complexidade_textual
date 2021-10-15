
import pandas as pd
import re
import sys

ftrs, msqe = [], []

with open(sys.argv[1]) as file:
    for line in file.readlines():
        i = re.split(r',(?=\d)',line)
        ftrs.append(i[0])
        msqe.append(float(i[1].replace('\n','')))

df = pd.DataFrame(zip(ftrs, msqe), columns = ['Features','Mean_square_error'])

#print(df.head())
row = df[df['Mean_square_error'] == df['Mean_square_error'].min()].index

print(sys.argv[1])
print(df.iloc[row]['Features'].values)
print(df['Mean_square_error'].min())
