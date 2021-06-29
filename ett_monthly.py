import streamlit as st
import pandas as pd
import re
import base64
from pyETT import ett
from functools import reduce


st.title('ETT Monthly Tournament Qualifier')

#ids = [3831, 234850, 11002]

collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]

form = st.form(key='my-form')


numbers = form.text_input("Please enter players IDs:")
ids = (collect_numbers(numbers))
start_date = form.text_input("START DATE (YYYY-MM-DD)")
end_date  = form .text_input("END DATE (YYYY-MM-DD)")
submit = form.form_submit_button('Submit')

ELO_THRESHOLD = 2000


if submit:
    players = [ett.Player(p_id) for p_id in ids]

    players_elo = [p.get_elo_history().rename(columns={"elo":p.name}) for p in
                   players if p.get_elo_history() is not None]

    group_elo_df = reduce(lambda df1,df2: pd.merge(df1,df2,how='outer', left_index=True, right_index=True),
                          players_elo).ffill(axis = 0)

    monthly_stats = group_elo_df.loc[(group_elo_df.index >= start_date)  & (group_elo_df.index <= end_date)].describe().filter(like='m', axis=0).transpose()
    monthly_stats['direct_entry'] = monthly_stats['max'] > ELO_THRESHOLD
    monthly_stats['can_qualify'] = monthly_stats['min'] <= ELO_THRESHOLD
    monthly_stats['id'] = ids
    pd.options.display.float_format = '{:,.1f}'.format

    csv = monthly_stats.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    st.markdown(href, unsafe_allow_html=True)

    monthly_stats




'''
By [highlanderNJ](https://www.elevenvr.net/eleven/348353) - Powered by [pyETT](https://github.com/souzatharsis/pyETT)
'''


