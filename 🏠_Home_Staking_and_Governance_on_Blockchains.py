#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[9]:


st.title('Staking and Governance on different Blockchain Ecosystems')


# In[10]:

st.markdown("In recent years, blockchain technology has emerged as a transformative force, revolutionizing various industries and introducing novel decentralized systems. At the heart of this technological breakthrough lies the concept of governance and staking activity, which empowers participants and promotes the smooth operation of blockchain networks.")

st.subheader("Governance: Empowering the Community")
st.markdown("Blockchain governance refers to the processes and mechanisms that enable decision-making and coordination among network participants. Unlike traditional centralized systems where a central authority holds power, blockchain governance embraces decentralization and seeks to distribute decision-making authority among its stakeholders.")

st.markdown("Governance Tokens: Many blockchain networks utilize governance tokens to facilitate decentralized decision-making. These tokens grant holders the right to vote on proposals, suggest improvements, and shape the future development of the network. By owning governance tokens, participants gain a voice in determining the network's rules, policies, and upgrades.")

st.markdown("Decentralized Autonomous Organizations (DAOs): A key component of blockchain governance, DAOs are self-governing entities that operate on smart contracts. DAOs enable participants to contribute funds, propose ideas, and vote on important matters in a transparent and democratic manner. Through DAOs, blockchain networks can achieve decentralized decision-making, fostering community engagement and collective ownership.")

st.subheader("Staking Activity: Securing the Network")
st.markdown("Staking is a fundamental activity in many blockchain networks that leverages participants' economic incentives to secure and maintain the integrity of the system. Staking involves holding and "staking" a certain amount of native cryptocurrency tokens as collateral to perform specific network functions.")

st.markdown("Proof-of-Stake (PoS): Unlike the traditional Proof-of-Work (PoW) consensus mechanism used by networks like Bitcoin, PoS blockchains rely on staking to achieve consensus. Participants lock up a certain amount of tokens as collateral and, in return, have the opportunity to validate transactions, create new blocks, and earn rewards. By staking their tokens, participants actively contribute to the security and efficiency of the network.")

st.markdown("Staking Rewards: In addition to securing the network, staking provides participants with an economic incentive. Stakers are typically rewarded with additional tokens for their contribution to the network's operations. These rewards can vary based on factors such as the amount of tokens staked, the duration of the stake, and the network's specific rules.")

st.markdown("Staking Pools: To make staking more accessible to a wider audience, staking pools have emerged. Staking pools allow multiple participants to combine their resources and stake together, increasing their chances of earning rewards. By pooling their tokens, participants with smaller holdings can still actively participate in staking and benefit from the associated rewards.")

st.markdown("In summary, governance and staking activity on the blockchain empower participants by giving them a say in decision-making processes and rewarding them for securing the network. By embracing decentralization and incorporating these mechanisms, blockchain networks strive to create transparent, inclusive, and community-driven ecosystems.")

st.markdown("So, the question is... How active and engaged are users? How many unique voters are there on each chain? How is voting power distributed? What chain has been the most active in proposals?")

# In[11]:
st.markdown("The main idea of this app is to show an overview of how the staking and governance is being used and developed on each different blockchains to see each performance and activity. You can find information about each different chain by navigating on the sidebar pages.")


# In[12]:


st.markdown("These includes:") 
st.markdown("1. **_Near Governance activity_**")
st.markdown("2. **_Cosmos Governance activity_**")
st.markdown("3. **_Terra Governance activity_**")
st.markdown("4. **_Axelar Governance activity_**")
st.markdown("5. **_Osmosis Governance activity_**") 


# In[ ]:




