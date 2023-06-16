#!/usr/bin/env python
# coding: utf-8

# In[5]:


#!/usr/bin/env python
# coding: utf-8

# In[18]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
import altair as alt

sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[19]:


st.title('Near Governance Activity')


# In[20]:


st.markdown('This page shows the basic governance activity trends on **Near** chain. It is intended to provide an overview of the current activity and usage since inception.')


# In[5]:


st.markdown('To do that, we are gonna track the basic activity metrics registered such as:') 


st.write('- How did the voting power of the top 66% of the active set validators change')
st.write('- Power share distribution by validators rank')
st.write('- How did the Nakamoto Coefficient change?')
st.write('- Validators and delegators activity')
st.write('')


# In[10]:


sql = f"""
 with
top10 as (
select 
date,
address as validator,
balance,
rank() over (partition by date order by balance desc) as ranks
from near.core.fact_staking_pool_daily_balances
),
final as (
SELECT 
   date,
   case when ranks <10 then 'Top 10'
when ranks between 10 and 50 then 'Top 10-50'
else 'Others' end as ranks,
   sum(balance) as total_near_delegated
FROM top10
group by 1,2
order by 1 asc
) select * from final where date>=current_date - INTERVAL '3 MONTHS'
"""

sql2 = f"""
 with
top10 as (
select 
date,
address as validator,
balance,
rank() over (partition by date order by balance desc) as ranks
from near.core.fact_staking_pool_daily_balances
),
final as (
SELECT 
   date,
   case when ranks <10 then 'Top 10'
when ranks between 10 and 50 then 'Top 10-50'
else 'Others' end as ranks,
   sum(balance) as total_near_delegated
FROM top10
group by 1,2
order by 1 asc 
 ) select * from final where date>=current_date - INTERVAL '3 MONTHS'


"""

sql3 = f"""
 WITH 
totals as (
SELECT 
   date as months,
    count(distinct address) as validators,
   sum(balance) as cumulative_near_delegated
FROM near.core.fact_staking_pool_daily_balances 
group by 1
),
ranking3 as (
   SELECT 
   date as month,
   address as validator,
   balance as total_near_delegated,
cumulative_near_delegated
FROM near.core.fact_staking_pool_daily_balances x
join totals y on date=y.months 
),
   stats as (
  SELECT
  month,
33 as bizantine_fault_tolerance,
cumulative_near_delegated,
(cumulative_near_delegated*bizantine_fault_tolerance)/100 as threshold--,
--sum(total_sol_delegated) over (partition by month order by validator_ranks asc) as total_sol_delegated_by_ranks,
--count(distinct vote_accounts) as validators
from ranking3
),
stats2 as (
   select *,
1 as numbering,
sum(numbering) over (partition by month order by total_near_delegated desc) as rank 
from ranking3
   ),
stats3 as (
SELECT
month,
validator,
  total_near_delegated,
rank,
sum(total_near_delegated) over (partition by month order by rank asc) as total_staked
--count(case when total_staked)
--sum(1) over (partition by month order by stake_rank) as nakamoto_coeff
  from stats2 where total_near_delegated is not null and total_near_delegated>0
order by rank asc), --select * from stats3
   final_nak as (
SELECT
a.month,
validator,
total_staked,
threshold,
count(case when total_staked <= threshold then 1 end) as counts,
validators as vals,
counts/vals as nakamoto_coeff
from stats3 a 
join stats b 
on a.month = b.month --where a.month >=CURRENT_DATE-INTERVAL '3 MONTHS'
join totals c on a.month=c.months
group by 1,2,3,4,6
order by 1 asc
   ) --select * from final_nak
SELECT
month,sum(nakamoto_coeff) as nakamoto_coeff
from final_nak where month>=current_date-INTERVAL '3 MONTHS'
group by 1 order by 1 asc 

"""

# In[11]:


@st.cache_data
def compute(a):
    data=sdk.query(a)
    return data

data = compute(sql)
df = pd.DataFrame(data.records)
df.info()

@st.cache_data
def compute2(a):
    data2=sdk.query(a)
    return data2

data2 = compute2(sql2)
df2 = pd.DataFrame(data2.records)
df2.info()

@st.cache_data
def compute3(a):
    data3=sdk.query(a)
    return data3
  
data3 = compute(sql3)
df3 = pd.DataFrame(data3.records)
df3.info()
#st.subheader('Near general activity metrics regarding Governance')


# In[22]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = px.area(df, x="days", y="voting_power")

fig.update_layout(
    title='Voting power of the top 66% of the active set validators change',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig.update_yaxes(title_text="Daily voting power", secondary_y=False)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


st.altair_chart(alt.Chart(df2)
        .mark_area()
        .encode(x="days:N", y=alt.Y("power_share:Q",stack="normalize"),color='ranks')
        .properties(title='Power share distribution per validators rank',width=600))

st.altair_chart(alt.Chart(df3)
        .mark_bar()
        .encode(x='days:N', y='nakamoto_coeff:Q',color='nakamoto_coeff')
        .properties(title='Nakamoto coefficient evolution',width=600))


# In[8]:


st.subheader('Validators and delegators activity')

sql="""

with
  t1 as (
    SELECT
      distinct x.tx_hash as proposal_id,
      x.block_timestamp as debut
    FROM
      near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 MONTHS'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
  )
select trunc(debut,'week') as weeks,
count(distinct proposal_id) as new_proposals,
sum(new_proposals) over (order by weeks) as cum_proposals
from t1 group by 1 order by 1 asc

"""

sql2 = f"""
 with
t0 as (
SELECT
distinct x.tx_signer as voter,
min(trunc(x.block_timestamp,'day')) as debut
from near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 months'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
group by 1
),
  t1 as (
    SELECT
      trunc(x.block_timestamp,'day') as date,
      x.tx_signer,
     x.tx_hash
    FROM
      near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 months'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
  )
    select
      date,
      case when date<debut+interval'30 days' then 'New voter' else 'Old voter' end as type,
      count(distinct tx_signer) as voters,
      count(distinct tx_hash) as votes
    from t1 join t0 on t1.tx_signer=t0.voter group by 1,2 order by 1 asc 
  """

sql3="""
   with
t0 as (
SELECT
distinct x.tx_signer as voter,
min(trunc(x.block_timestamp,'day')) as debut
from near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 months'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
group by 1
),
  t1 as (
    SELECT
      trunc(x.block_timestamp,'day') as date,
      x.tx_signer,
      x.tx_hash
    FROM
      near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 months'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
  ),
final as (
    select
      date,
      case when date<debut+interval'30 days' then 'New voter' else 'Old voter' end as type,
      tx_signer as voter,
      count(distinct tx_hash) as votes
    from t1 join t0 on t1.tx_signer=t0.voter group by 1,2,3 order by 1 asc 
)
SELECT
trunc(date,'day') as weeks, type,avg(votes) as avg_votes_per_voter
from final group by 1,2 order by 1 asc 
"""

data = compute(sql)
df = pd.DataFrame(data.records)
df.info()

data2 = compute2(sql2)
df2 = pd.DataFrame(data2.records)
df2.info()

data3 = compute3(sql3)
df3 = pd.DataFrame(data3.records)
df3.info()

#Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['weeks'],
                y=df['new_proposals'],
                name='# of proposals',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['weeks'],
                y=df['cum_proposals'],
                name='# of proposals',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Near proposals evolution',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly new proposals", secondary_y=False)
fig3.update_yaxes(title_text="Total new proposals", secondary_y=True)

st.plotly_chart(fig3, theme="streamlit", use_container_width=True)



# Create figure with secondary y-axis
st.altair_chart(alt.Chart(df2)
        .mark_bar()
        .encode(x='date:N', y='voters:Q',color='type')
        .properties(title='Active voters by type of validator over time',width=600))

st.altair_chart(alt.Chart(df2)
        .mark_line()
        .encode(x='date:N', y='votes:Q',color='type')
        .properties(title='Voting activity by type of validator over time',width=600))

# Create figure with secondary y-axis
st.altair_chart(alt.Chart(df3)
        .mark_line()
        .encode(x='weeks:N', y='avg_votes_per_voter:Q',color='type')
        .properties(title='Average weekly votes per voter per type of validator',width=600))


# In[12]:

sql2="""
WITH
  new_wallets as (
  select 
  distinct tx_signer as user,
  min(block_timestamp) as debut
  from near.core.fact_transactions
  group by 1
  ),
  votes as (
SELECT
distinct x.tx_signer as user,
min(trunc(x.block_timestamp,'day')) as governance_debut
from near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 months'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
group by 1
  ),
  final as (
SELECT
x.user,
debut,
governance_debut,
datediff('day',debut,governance_debut) as time_to_governance_participation
from new_wallets x
  join votes y on x.user=y.user 
  )
SELECT
avg(time_to_governance_participation) as avg_time_to_governance_participation
from final
"""

sql3="""
  WITH
  new_wallets as (
  select 
  distinct tx_signer as user,
  min(block_timestamp) as debut
  from near.core.fact_transactions
  group by 1
  ),
  votes as (
SELECT
distinct x.tx_signer as user,
min(trunc(x.block_timestamp,'day')) as governance_debut
from near.core.fact_transactions x
      LEFT JOIN near.core.dim_address_labels y ON y.address = x.tx_receiver
      LEFT JOIN near.core.fact_actions_events_function_call z on z.tx_hash = x.tx_hash
    WHERE
      label_type = 'dao'
      AND x.block_timestamp >= current_date-INTERVAL '3 months'
      AND tx_status = 'Success'
      AND method_name = 'add_proposal'
group by 1
  ),
  final as (
SELECT
x.user,
debut,
governance_debut,
datediff('day',debut,governance_debut) as time_to_governance_participation
from new_wallets x
  join votes y on x.user=y.user 
  )
SELECT
trunc(governance_debut,'day') as date,
avg(time_to_governance_participation) as avg_time_to_governance_participation,
count(distinct user) as participants
from final
group by 1
order by 1 asc
"""


data2 = compute(sql2)
df2 = pd.DataFrame(data2.records)
df2.info()

data3 = compute(sql3)
df3 = pd.DataFrame(data3.records)
df3.info()






col1,col2=st.columns(2)
with col1:
    st.metric('Average days before participating in governance',df2['avg_time_to_governance_participation'])
col2.altair_chart(alt.Chart(df3)
        .mark_line()
        .encode(x='date:N', y='avg_time_to_governance_participation:Q')
        .properties(title='Average time to governance participation',width=300))


