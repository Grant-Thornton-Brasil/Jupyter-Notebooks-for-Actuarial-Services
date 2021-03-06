#!/usr/bin/env python
# coding: utf-8

# In[1]:


from glob import glob
from shutil import copy2


# In[2]:


def make_list(qe):
    for original, new in zip(glob(f".\*\\*EST{qe}.txt"),
                             list(map(lambda x: x.replace(".\\", "").replace("\\", "_"),
                                      glob(f".\*\\*EST{qe}.txt")))):
        copy2(original, new)


# In[3]:


for i in [376, 377, 378]:
    try:
        make_list(i)
    except:
        pass

