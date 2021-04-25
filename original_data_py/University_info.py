#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

read_file = pd.read_excel (r'C:\Users\Administrator\Desktop\course\551\project\data\School_location.xlsx')
read_file.to_csv (r'C:\Users\Administrator\Desktop\course\551\project\data\School_location.csv', index = None, header=True)


# In[ ]:




