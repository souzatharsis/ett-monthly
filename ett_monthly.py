import streamlit as st
import pandas as pd
import re
import base64
from pyETT import ett
from functools import reduce

ELO_THRESHOLD = 2000

st.title('ETT Monthly Tournament Qualifier')

# Input data
collect_numbers = lambda x: [int(i) for i in re.split("[^0-9]", x) if i != ""]
form = st.form(key='my-form')
numbers = form.text_input("Please enter players IDs:")
ids = (collect_numbers(numbers))
start_date = form.text_input("START DATE (YYYY-MM-DD)")
end_date = form.text_input("END DATE (YYYY-MM-DD)")
submit = form.form_submit_button('Submit')

if submit:
    players = [ett.Player(p_id) for p_id in ids]
    player_none_index = [i for i, e in enumerate(players) if e is None]
    
    # Handle invalid ids
    if len(player_none_index) > 0:
        st.write(f'The following players have invalid ids: ')
        [ids[k] for k in player_none_index]

    players = list(filter(None, players))

    ids = [p.id for p in players]
    if len(ids) > 0:
        monthly_stats = ett.ETT().Tournament(players).qualify(elo_min=ELO_THRESHOLD, start=start_date, end=end_date)

        pd.options.display.float_format = '{:,.1f}'.format

        csv = monthly_stats.to_csv().encode()
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
        st.markdown(href, unsafe_allow_html=True)

        monthly_stats

'''
By [highlanderNJ](https://www.elevenvr.net/eleven/348353) - Powered by [pyETT](https://github.com/souzatharsis/pyETT)
'''
