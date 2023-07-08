# Saliha Billur Koca
import numpy as np
import pandas as pd
file = "Innova-Yapay-Zeka-Soru-2.xlsx"
data = pd.ExcelFile(file)

# ....oooOO0OOooo........oooOO0OOooo.... Data Frame Creation ....oooOO0OOooo........oooOO0OOooo....
given = data.parse('data_metrics')
desired = data.parse('beklenen')
# print(desired.columns[0]) # Get each name of the column

# I will make two dataframes which contains only Enter Gates and Exit Gates for minimum values of each column.
# So that, one can easily compare the exit gates of desired and given sheet for a specific column.
summary = pd.DataFrame(columns=["EnterGate","MinValue","ExitGate"])
pd.set_option('display.max_columns', None)
givenSum=pd.DataFrame(columns=["EnterGate","MinValue","ExitGate"])
pd.set_option('display.max_columns', None)

for i in range(0,25):
    new_row = pd.Series({"EnterGate":desired.columns[i], "MinValue":min(desired.loc[:,desired.columns[i]]),"ExitGate":desired[desired[str(desired.columns[i])]==min(desired.loc[:,desired.columns[i]])].index.to_numpy()[0]})
    summary = pd.concat([summary, new_row.to_frame().T], ignore_index=True)

for i in range(0,25):
    new_row = pd.Series({"EnterGate":given.columns[i], "MinValue":min(given.loc[:,given.columns[i]]),"ExitGate":given[given[str(given.columns[i])]==min(given.loc[:,given.columns[i]])].index.to_numpy()[0]})
    givenSum = pd.concat([givenSum, new_row.to_frame().T], ignore_index=True)

# ....oooOO0OOooo........oooOO0OOooo.... User Defined Functions ....oooOO0OOooo........oooOO0OOooo....
indices=[]
diffs=[]
def re(dfgivenSum,dfsummary,dfgiven):
    for i in range(1, 25):
        if ((dfgivenSum.loc[i]["ExitGate"] != dfsummary.loc[i]["ExitGate"]).any()):
            mustbe = dfgiven.loc[dfsummary.loc[i]["ExitGate"]][i]
            # summary.loc[i]["ExitGate"] gives the minimum value in the row of the desired exit gate.
            diff = abs(dfgivenSum.loc[i]["MinValue"] - mustbe) + 1
            # We also need to evaluate the index of the row of desired gate.
            index = np.where(dfgiven[str(dfgivenSum.loc[i]["EnterGate"])] == dfgivenSum.loc[i]["MinValue"])[0]
            # Bir [0] daha ekleyince error vermesinin sebebi givenSum'ın yenilenmemesi!
            indices.append(index)
            diffs.append(diff)
        else:
            index = dfgivenSum.loc[i]["ExitGate"]
            indices.append(index)
            diffs.append(0)
    s = []
    for i in range(0, 11):
        if i not in indices:
            s.append(i)
        else:
            a = [index for (index, item) in enumerate(indices) if item == i]
            sl = [diffs[a[j]] for j in range(len(a))]
            s.append(sum(sl))
    return s

def all(row,differences,dfgiven):
    for i in range(1,25):
        dfgiven.iloc[row,i]=dfgiven.iloc[row,i]+differences
    return dfgiven

s = re(givenSum,summary,given)

for l in range(0,len(s)):
    k=all(l,s[l],given)

# ....oooOO0OOooo........oooOO0OOooo.... Second Iteration ....oooOO0OOooo........oooOO0OOooo....

gs2=pd.DataFrame(columns=["EnterGate","MinValue","ExitGate"])
pd.set_option('display.max_columns', None)
for i in range(0,25):
    new_row = pd.Series({"EnterGate":k.columns[i], "MinValue":min(k.loc[:,k.columns[i]]),"ExitGate":k[k[str(k.columns[i])]==min(k.loc[:,k.columns[i]])].index.to_numpy()[0]})
    gs2 = pd.concat([gs2, new_row.to_frame().T], ignore_index=True)
s2 = re(gs2,summary,k)
for l in range(0,len(s2)):
    g=all(l,s2[l],k)
print("Metrics Values {}".format(s2))
