import streamlit as st
import pandas as pd
import re
from pyETT import ett
from functools import reduce


st.title('ETT Monthly Tournament Qualifier')

#ids = [3831, 234850, 11002]

collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
numbers = st.text_input("Please enter players IDs:")
ids = (collect_numbers(numbers))

start_date = st.text_input("START DATE (YYYY-MM-DD)")
end_date  = st.text_input("END DATE (YYYY-MM-DD)")

ELO_THRESHOLD = 2000

players = [ett.Player(p_id) for p_id in ids]

players_elo = [p.get_elo_history().rename(columns={"elo":p.name}) for p in
               players if p.get_elo_history() is not None]

group_elo_df = reduce(lambda df1,df2: pd.merge(df1,df2,how='outer', left_index=True, right_index=True),
                      players_elo).ffill(axis = 0)

monthly_stats = group_elo_df.loc[(group_elo_df.index >= start_date)  & (group_elo_df.index <= end_date)].describe().filter(like='m', axis=0).transpose()
monthly_stats['qualified'] = monthly_stats['max'] >= ELO_THRESHOLD
st.write(monthly_stats)

st.write("By highlanderNJ - Powered by pyETT")


