import pandas as pd

df = pd.read_csv('./Hotel_Reviews.csv', sep=',')
# tags_list = set()
# for i, row in df.iterrows():
#   t = []
#   exec("t = %s" % (row["Tags"],))
#   df.at[i, "Tags"] = t
#   tags_list.update(set(t))
# tags_list = list(tags_list)
hotels_list = sorted(df['Hotel_Name'].unique())
countries_list = sorted(df['Hotel_Country'].unique())
nationalities_list = sorted(df['Reviewer_Nationality'].unique())
years_list = sorted(df['Review_Year'].unique())
