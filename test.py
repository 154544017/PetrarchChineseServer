import pandas as pd

df = pd.read_excel("D:\\Document\\python_projects\\PetrarchChineseServer\\article\\1_1.xlsx")
data = df.loc[:, ["co4"]].values[0][0]
ddt = pd.Timestamp(data,tz=None).to_pydatetime()
print(type(ddt))
print(ddt)