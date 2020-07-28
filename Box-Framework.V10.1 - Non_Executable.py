#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import time
t1 = time.time()


# In[19]:


data_1_sheet_kmg = pd.read_excel(r"C:\Users\samen\datasheet1.xlsx",sheet_name="GS-KS-MS data sheet 1")


# In[20]:


try:
    data_1_sheet_kmg.drop('Outlet tagging',axis=1,inplace=True)
except:
    pass


# In[21]:


data_1_sheet_kmg=pd.DataFrame(data_1_sheet_kmg)


# In[22]:


data_1_sheet_kmg.shape


# # KPI BEGIN

# In[23]:


#data_1_sheet_kmg.fillna(0,inplace=True)
#dropped one na  row
data_1_sheet_kmg.dropna(subset =['customer'],inplace=True)


# In[24]:


data_1_sheet_kmg


# In[25]:


city_category = list(data_1_sheet_kmg['city'].unique())
city_category
len_city_category = len(city_category)


# In[26]:


len_customer = len(data_1_sheet_kmg['customer'].unique())


# In[28]:


re = list(data_1_sheet_kmg['re'].unique())


# In[30]:


len_customer


# In[32]:


i=0
count=0
name="dataframe_new"


# In[39]:


d={}
for c in city_category:
    
    sheet_1_tvm = data_1_sheet_kmg[data_1_sheet_kmg['city']==c]
    for i in range(len(re)):
        #print("re=" + re[i]+ str(' running'))
        
        tvm_ks = sheet_1_tvm[sheet_1_tvm['re']==re[i]]
        tvm_ks_customer = list(tvm_ks['customer'].unique())
        month_cat = list(tvm_ks['mth'].unique())
        sum_df = []
        sum_ppg=[]
        call_sum = []
        cat = []
        #print(tvm_ks['mth'])
        #mth=[]
        m=[]
        m_df = pd.DataFrame(columns=month_cat)
        
        for k in tvm_ks_customer:
            sum_df.append(int(np.ceil(tvm_ks.loc[tvm_ks['customer']==k,'sales_value'].sum())))
            sum_ppg.append(tvm_ks.loc[tvm_ks['customer']==k,'uniq_npg'].sum())
            call_sum.append(tvm_ks.loc[tvm_ks['customer']==k,'invoices'].sum())
            for mt in month_cat:
                mth=tvm_ks.loc[(tvm_ks['mth']==mt) &(tvm_ks['customer']==k),'sales_value'].sum()
                #m["{}".format(mt)]=mth
                m.append(mth)
            m=pd.Series(m,index=m_df.columns)
            m_df = m_df.append(m,ignore_index=True)
            m=[]
            month_cat = list(tvm_ks['mth'].unique())
            #m_sum_t = 
            
                
                #print(mth)
                #quit()
                
        tvm_ks_final = pd.DataFrame()
        #print(c)
        tvm_ks_final['customer'] = tvm_ks_customer
        city = [str(c) for i in range(tvm_ks_final.shape[0])]
        tvm_ks_final['City'] = city
        print(str(c)+" "+str(re[i]))
        print(tvm_ks_final.shape[0])
        
        
        tvm_ks_final['sum_of_sales_value'] = sum_df
        #print("here")
        #print(i)
        tvm_ks_final['re'] = str(re[i])
        sum_ppg = [x/7 for x in sum_ppg ]
        tvm_ks_final['Total unique PPGs/7'] = sum_ppg
        call_sum = [x/7 for x in call_sum]
        tvm_ks_final['Total no. of calls/7'] = call_sum
        tvm_ks_final['Percentile_rank']=np.round(tvm_ks_final['sum_of_sales_value'].rank(pct=True),3)
        len_ = len(tvm_ks_final['customer'].unique())
        print("Total Unique Customers = "+str(len_))
        len_at = len_/10
        tvm_ks_final = tvm_ks_final.sort_values(by='sum_of_sales_value',ascending=False)
        tags = ['high','medium','low']
        #splitting for high = 3*len_at
        empt = [0.00 for n in range(len_)]
        #print("empt=",len(empt))
        
        new_len = round(3*len_at)
        for x in range(new_len):
            empt[x] = 'high'
        print("High = " +str(new_len))
        new_len = round(3*len_at)
        for x in range(new_len):
            empt[-x]='low'
        print("low = " +str(new_len))
        new_len = len_-((6*len_at))
        itee = int(round(3*len_at))
        #print(itee)
        #print(new_len)
        for x in range(int(new_len)):
            empt[itee]='medium'
            itee+=1
        print("new")
        print("a")
        print("Medium = " +str(int(new_len))
        #print("**************************************************")
        #tvm_ks_final['months']=mth
        #'''new_list = tvm_ks_final['Percentile_rank'].to_list()
        #for x in new_list:
        #    if x<=0.300:
        #       cat.append('low')
        #    elif x<=0.700 and x>0.300:
        #        cat.append('medium')
        #    else:
        #        cat.append('high')'''
        #print("empt="+str(len(empt)))
        
        tvm_ks_final['category'] = empt
        tvm_ks_final = pd.concat([tvm_ks_final,m_df],axis=1)
        d["{}_{}".format(c,re[i])]=pd.DataFrame(tvm_ks_final)
        count+=1
        d["{}_{}".format(c,re[i])].fillna(0,inplace=True)
        
        
            
            
            
            
        
        
        #pd.concat([df3, df4], axis='col')
        
        
        
    
    #pd.DataFrame(tvm_ks_final)
    
   
    
    
    

    


# In[4322]:


#tvm_ks_final.loc[tvm_ks_final['category']=='medium'].count()


# In[4323]:


month_cat = list(tvm_ks['mth'].unique())


# In[4326]:


test_df = pd.DataFrame()
for key in d.keys():
    temp = d[key]
    test_df = test_df.append(temp)


# In[4327]:


test_df.to_csv("newbasetest.csv")


# In[4328]:


#test_df.filter(['customer','Percentile_rank','category','sum_of_sales_value']).to_csv("test_init.csv")


# In[4329]:


keys_final= []
print("The Keys Are :- ")
print("use d[keyname to pick up  a dataframe]")
print("      ")
for key in d.keys():
    keys_final.append(key)
    print(key)


# # MONTH DONE

# # MONTH DICT + JOINING OF OUTLET TAGGING

# In[4330]:


month_dict = {8:'aug',
              9:'sep',
              10:'oct',
              11:'nov',
              12:'dec',
              1:'jan',
              2:'feb',
              3:'mar',
              4:'april',
              5:'may',
              6:'jun',
              7:'july'
}


# In[4331]:


#month_dict[8]


# In[4332]:


#k_d = d['TRIVANDRUM_KS'][['customer','category']]


# In[4333]:


cat_sheet =pd.DataFrame() #category of unique values ! 


# In[4334]:


for di in keys_final:
    new = d[di][['customer','category']]
    cat_sheet = cat_sheet.append(new)
# setting a dictionary !     


# In[ ]:





# In[4335]:


cat_sheet.shape[0]==len(data_1_sheet_kmg['customer'].unique()) #testing shapes of unqiue value ! 


# In[4339]:


cat_dict  = dict(zip(cat_sheet['customer'],cat_sheet['category'])) #creating Dict for values to apply to main dataset ! 


# In[4340]:


data_1_sheet_kmg['category'] = data_1_sheet_kmg['customer'].map(cat_dict)
#setting the values back to the table!!!


# In[4342]:


keys_final


# In[4343]:


#final_dict['TRIVANDRUM_MS']


# In[4344]:


final_dict={} #empty dict to create and store the needed tables , since we dont know how many might come in! 


# DIct and Adding Category Complete ! 
# 

# In[4345]:


#dfghjkl


# # Creating Final Set for DataSheet1

# In[4346]:


bon = ['avg_sale_value_per_retailer','no_of_outlets','median_sale_value_per_outlet','avg_npgs_per_retailer','median_npgs_per_outlet','avg_no_of_calls_per_outlet','median_no_of_calls_per_outlet']
# 7 value tables that are calculated


# In[4347]:


re


# In[4348]:



city_category


# In[4349]:


test = d['TRIVANDRUM_MS'].loc[d['TRIVANDRUM_MS']['category']=='low']


# In[4350]:


#test1 = test.loc[test[8]!=0]


# In[4351]:


#test1


# In[4352]:


#d


# No of Outlets 

# In[4353]:


from statistics import median
import numpy as np


# In[4354]:


category_valu = ['low','medium','high']


# In[4355]:


var_run=0


# In[4356]:


for c_name in city_category:
    bcount=0
    keys_final=[c_name+str("_")+str(i) for i in re]
    rows =[]
    new_1 = []
    final_df_1  = pd.DataFrame()
    category_valu=['low','medium','high']
       
    #Need 7 outputs ! 

    #avg sale value per retailer
    for x in re:
        column1='avg sale per retailer'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_1 = pd.DataFrame(columns = columns)
    final_df_1.insert(0,column1,rows)
    rows=[]
    print(final_df_1.shape)

    #no of outlets    
    for x in re:
        column1='number of outlets'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_2 = pd.DataFrame(columns = columns)
    final_df_2.insert(0,column1,rows)
    rows=[]

    print(final_df_2.shape)

    #median sale value per outlet
    for x in re:
        column1='median sale value per outlet'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_3 = pd.DataFrame(columns = columns)
    final_df_3.insert(0,column1,rows)
    rows=[]
    print(final_df_3.shape)


    #avg npgs per retailer
    for x in re:
        column1='avg npg per retailer'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_4 = pd.DataFrame(columns = columns)
    final_df_4.insert(0,column1,rows)
    rows=[]
    print(final_df_4.shape)




    #median npgs per outlet
    for x in re:
        column1='median npg per outlet'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_5 = pd.DataFrame(columns = columns)
    final_df_5.insert(0,column1,rows)
    rows=[]
    print(final_df_5.shape)





    #avg no of calls per outlet
    for x in re:
        column1='avg call per retailer'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_6 = pd.DataFrame(columns = columns)
    final_df_6.insert(0,column1,rows)
    rows=[]
    print(final_df_6.shape)




    #median no of calls per outlet
    for x in re:
        column1='median call per outlet'
        columns = [month_dict[m] for m in month_cat]
        new_1.append(str(x)+"_"+'low')
        new_1.append(str(x)+"_"+'mid')
        new_1.append(str(x)+"_"+'high')
        #new_1.append(str(x)+"_"+'overall')
        rows.append(new_1)
        new_1=[]
    rows = [item for sublist in rows for item in sublist] #flattening the list of list
    #df.insert(0,'name_of_column',value)   
    final_df_7 = pd.DataFrame(columns = columns)
    final_df_7.insert(0,column1,rows)
    rows=[]
    print(final_df_7.shape)
    print("empty Cells Created")
#***************************    
    ##########################OUTPUT SECTION#########################################
    #print(c)
    #avg sale value per retailer
    i=0
    for k in keys_final:
        #print(k)
        for c in category_valu:
            #print(c)
            test = d[k].loc[d[k]['category']==c]
            #print(test)

            for m in month_cat:
                #print(m)
                len_ = len(test.loc[test[m]==0]) #finidng unadded values
                nval = test[m].sum()/(test.shape[0]-len_)
                #print(nval)
                final_df_1[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_1.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_1)
    bcount+=1
    
#CHECKED
    
    
    #no of outlets
    i=0
    for k in keys_final:
        #print(k)
        for c in category_valu:
            #print(c)
            test = d[k].loc[d[k]['category']==c]
            #print(test)

            for m in month_cat:
                #print(m)
                #len_ = len(test.loc[test[m]==0])
                #print(len_)#finidng unadded values
                nval = len(test.loc[test[m]!=0])
                #print(nval)
                final_df_2[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_2.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_2)
    bcount+=1
#CHECKED    
    
    #median sale value per outlet
    i=0
    for k in keys_final:
        #print(k)
        for c in category_valu:
            #print(c)
            test = d[k].loc[d[k]['category']==c]
            #print(test)

            for m in month_cat:
               # print(m)
                #len_ = len(test.loc[test[m]==0])
                #print(len_)#finidng unadded values
                new = test.loc[test[m]!=0]
                nval =median(new[m])



                #print(nval)
                final_df_3[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_3.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_3)
    bcount+=1
#CHECKED 
    ########################################################33modifying#####################################
    #avg npgs per retailer
    import numpy as np
    i=0
    for r in re:
        #print(r)
        for j in keys_final:
            if j.find('{}_{}'.format(c_name,r))!=-1:
                k = j
                break
            else:
                pass
                
        #print(k)
        for c in category_valu:
            #print(c)
            #print(c)
            #temp = d[k].loc[d[k]['category']==c]
            #to find the key

            test = data_1_sheet_kmg.loc[(data_1_sheet_kmg['city']==c_name) &(data_1_sheet_kmg['re']==r)]
                    
            #print(test)

            for m in month_cat:
                #print(m)
                #len_ = len(test.loc[test[m]==0])
                #temp1 = temp.loc[temp[m]!=0]
                #print(len_)#finidng unadded values
                test1 = test.loc[test['mth']==m]
                test2 = test1.loc[(test1['uniq_npg']>0) & (test1['category']==c)]
                sum__ = test2['uniq_npg']>0
                nval = round(test2['uniq_npg'].sum()/sum__.shape[0])
                #print(nval)
                #print(nval)
                final_df_4[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_4.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_4)
    bcount+=1
    
#CHECKED

    #median npgs per outlet
    i=0
    for k in keys_final:
        #print(k)
        for c in category_valu:
            #print(c)
            test = d[k].loc[d[k]['category']==c]
            #print(test)

            for m in month_cat:
                #print(m)
                #len_ = len(test.loc[test[m]==0])
                #print(len_)#finidng unadded values
                test1 = test.loc[test[m]!=0]
                nval = np.ceil(median(test1['Total unique PPGs/7']))
                

                #print(nval)
                final_df_5[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_5.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_5)
    bcount+=1
#CHECKED
    
    #avg calls per retailer
    import numpy as np
    i=0
    for k in keys_final:
        #print(k)
        for c in category_valu:
            #print(c)
            test = d[k].loc[d[k]['category']==c]
            #print(test)

            for m in month_cat:
                #print(m)
                #len_ = len(test.loc[test[m]==0])
                #print(len_)#finidng unadded values
                test1 = test.loc[test[m]!=0]
                nval = np.ceil(test1['Total no. of calls/7'].sum()/test1.shape[0])
                #print(nval)
                final_df_6[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_6.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_6)
    bcount+=1
#CHECKED

    #median calls per outlet
    import numpy as np
    i=0
    for k in keys_final:
        #print(k)
        for c in category_valu:
            #print(c)
            test = d[k].loc[d[k]['category']==c]
            #print(test)

            for m in month_cat:
                #print(m)
                #len_ = len(test.loc[test[m]==0])
                #print(len_)#finidng unadded values
                test1 = test.loc[test[m]!=0]
                nval = np.ceil(median(test1['Total no. of calls/7']))

                #print(nval)
                final_df_7[month_dict[m]][i]=nval
                #print(i)
                #i+=1
            i+=1
    final_df_7.fillna(method='bfill',inplace=True)
    final_dict["{}_{}".format(c_name,bon[bcount])]=pd.DataFrame(final_df_7)
    bcount+=1
  


# In[4357]:


#Creating a list of keys for the firts one ! 

sheet1_dict =[]
sheet1_dict = [x for x in final_dict.keys()]


# # Sheet 1 Finished  - KPI !
# Note: - Slight Variations 

#  

#  

#  

#  

#  

#  

#  

# # SHEET 2 STARTS !

# In[4360]:


data_2_sheet_kmg = pd.read_excel(r"C:\Users\samen\datasheet2.xlsx",sheet_name="Data sheet 2")


# In[4361]:


data_2_sheet_kmg=pd.DataFrame(data_2_sheet_kmg)


# In[4362]:


data_2_sheet_kmg.shape


# In[4363]:


data_2_sheet_kmg.dropna(subset=['npg_code'],inplace=True)
#shows each and every row has an "na" Value


# In[4367]:


print("total Categorized Customers = "+ str(data_2_sheet_kmg.loc[data_2_sheet_kmg['Outlet tagging']=='High','customer'].count()+
                                           data_2_sheet_kmg.loc[data_2_sheet_kmg['Outlet tagging']=='Medium','customer'].count()+
                                           data_2_sheet_kmg.loc[data_2_sheet_kmg['Outlet tagging']=='Low','customer'].count()))


# In[4368]:


try:
    data_2_sheet_kmg.drop('Outlet tagging',axis=1,inplace=True)
    data_2_sheet_kmg.drop(['TRIVANDRUM|GS PPG flag','TRIVANDRUM|KS PPG flag','TRIVANDRUM|MS PPG flag','TRISSUR|GS PPG flag','TRISSUR|KS PPG flag','TRISSUR|MS PPG flag'],axis=1,inplace=True)
except:
    pass


# In[4374]:


len(data_2_sheet_kmg['customer'].unique())


# In[4375]:


product_dict = {}
product_dict_inverse = {}


# In[4376]:


product_dict  = dict(zip(data_2_sheet_kmg['npg_code'],data_2_sheet_kmg['npg_desc'])) #product Dictionary


# In[4377]:


len(product_dict)


# In[4378]:


product_dict_inverse  = dict(zip(data_2_sheet_kmg['npg_desc'],data_2_sheet_kmg['npg_code'])) #product Dictionary


# In[4379]:


npg_list= [x for x in product_dict.keys()]


# In[4380]:


len(npg_list)


# In[4381]:


data_2_sheet_kmg['category'] = data_2_sheet_kmg['customer'].map(cat_dict) # applying outlet tagging ! 


# In[ ]:





# TESTING and Comparing Values

# In[4382]:


#Values from Excel Sheet
print("High = " + str(data_2_sheet_kmg.loc[data_2_sheet_kmg['category']=='high','customer'].count()))


# In[4383]:


#Values from Excel Sheet
print("Medium = " + str(data_2_sheet_kmg.loc[data_2_sheet_kmg['category']=='medium','customer'].count()))


# In[4384]:


#Values from Excel Sheet
print("Low = " + str(data_2_sheet_kmg.loc[data_2_sheet_kmg['category']=='low','customer'].count()))


# In[4385]:


print("total Categorized Customers = "+ str(data_2_sheet_kmg.loc[data_2_sheet_kmg['category']=='high','customer'].count()+
                                           data_2_sheet_kmg.loc[data_2_sheet_kmg['category']=='medium','customer'].count()+
                                           data_2_sheet_kmg.loc[data_2_sheet_kmg['category']=='low','customer'].count()))


# In[4387]:


re_cust_dict  = dict(zip(data_2_sheet_kmg['customer'],data_2_sheet_kmg['category'])) #Re(high,low,medium)  Dictionary


# In[4388]:


city_cat_2 = list(data_2_sheet_kmg['city'].unique())


# In[4389]:


re_2 = list(data_2_sheet_kmg['re'].unique())


# In[4390]:


re_2 = list(set(re).intersection(set(re_2)))


# In[4391]:


re_2


# Initial splits on first tree of city's then on the basis of different Re's for each and adding them to a dictionary

# In[4392]:


re_2_dict = {}
for city in city_cat_2:
    for r in re_2:
        daf_2 = pd.DataFrame(data_2_sheet_kmg.loc[(data_2_sheet_kmg['re']==r)& (data_2_sheet_kmg['city']==city)])
        re_2_dict['{}_{}'.format(city,r)]=pd.DataFrame(daf_2)
#Dictionary basedd on city+re splits with entire data!         


# In[4393]:


re_2_keys=[]


# In[4394]:


for key in re_2_dict.keys():
    re_2_keys.append(key)
re_2_keys


# In[4395]:


re = re_2


# # After extracting the keys using it to fetch [Sales value, Participation, quantity for each]

# Extraction process for sales value

# In[4396]:


#creating a unique list of npg_codes


# In[4397]:


len(npg_list)


# In[4398]:


sale_dict = {}

for rk in re_2_keys:
    temp =re_2_dict[rk]
    temp = temp.dropna()
    #npg_list = list(temp['npg_code'].values)
    rows = npg_list
    columns = [str(rk)+"sale"+'01',str(rk)+"sale"+'02',str(rk)+"sale"+'03',str(rk)+"sale"+'04',str(rk)+"sale"+'05',str(rk)+"sale"+'06',str(rk)+"sale"+'07']
    column1 = 'sale_dict-npg'
    model = pd.DataFrame(columns=columns)
    model.insert(0,column1,rows)
    i=0
    for ni in npg_list:

        temp1 = temp.loc[temp['npg_code']==ni]
        model[str(rk)+"sale"+'01'][i]=temp1.loc[temp['SV_01']!=0,'SV_01'].sum()
        model[str(rk)+"sale"+'02'][i]=temp1.loc[temp['SV_02']!=0,'SV_02'].sum()
        model[str(rk)+"sale"+'03'][i]=temp1.loc[temp['SV_03']!=0,'SV_03'].sum()
        model[str(rk)+"sale"+'04'][i]=temp1.loc[temp['SV_04']!=0,'SV_04'].sum()
        model[str(rk)+"sale"+'05'][i]=temp1.loc[temp['SV_05']!=0,'SV_05'].sum()
        model[str(rk)+"sale"+'06'][i]=temp1.loc[temp['SV_06']!=0,'SV_06'].sum()
        model[str(rk)+"sale"+'07'][i]=temp1.loc[temp['SV_07']!=0,'SV_07'].sum()
        i+=1
    sale_dict["{}".format(rk)]=pd.DataFrame(model)
    i=0


# In[4399]:


sale_dict.keys()


# Verfied and cross- Checked With Values

#     

#                         
# 

# Extraction process for Quantity

# In[4407]:


quant_dict = {}


# In[4408]:


for rk in re_2_keys:
    temp =re_2_dict[rk]
    temp = temp.dropna()
    #npg_list = list(temp['npg_code'].unique())
    rows = npg_list
    columns = [str(rk)+'quant'+'01',str(rk)+'quant'+'02',str(rk)+'quant'+'03',str(rk)+'quant'+'04',str(rk)+'quant'+'05',str(rk)+'quant'+'06',str(rk)+'quant'+'07']
    column1 = 'quant_dict-npg'
    model = pd.DataFrame(columns=columns)
    model.insert(0,column1,rows)
    i=0
    for ni in npg_list:

        temp1 = temp.loc[temp['npg_code']==ni]
        model[str(rk)+'quant'+'01'][i]=round(temp1.loc[temp['QY_01']!=0,'QY_01'].sum())
        model[str(rk)+'quant'+'02'][i]=round(temp1.loc[temp['QY_02']!=0,'QY_02'].sum())
        model[str(rk)+'quant'+'03'][i]=round(temp1.loc[temp['QY_03']!=0,'QY_03'].sum())
        model[str(rk)+'quant'+'04'][i]=round(temp1.loc[temp['QY_04']!=0,'QY_04'].sum())
        model[str(rk)+'quant'+'05'][i]=round(temp1.loc[temp['QY_05']!=0,'QY_05'].sum())
        model[str(rk)+'quant'+'06'][i]=round(temp1.loc[temp['QY_06']!=0,'QY_06'].sum())
        model[str(rk)+'quant'+'07'][i]=round(temp1.loc[temp['QY_07']!=0,'QY_07'].sum())
        i+=1
    quant_dict["{}".format(rk)]=pd.DataFrame(model)
    i=0


# In[4409]:


quant_dict.keys()


# Verfied and cross- Checked With Values

#      

#           

#                

# In[4411]:


#re_2_dict['TRIVANDRUM_KS']


# Extraction process for Participation

# In[4412]:


re_2_keys


# In[4413]:


#product_dict


# In[4414]:


#part_dict = {}


# In[4415]:


len(re_2_dict['TRIVANDRUM_KS']['customer'].unique())


# In[4416]:


part_dict= {}
for rk in re_2_keys:
    temp =re_2_dict[rk]
    temp = temp.dropna()
    cust_count = len(temp['customer'].unique())
    #npg_list = list(temp['npg_code'].unique())
    rows = npg_list
    columns = [str(rk)+"part"+'01%',str(rk)+"part"+'02%',str(rk)+"part"+'03%',str(rk)+"part"+'04%',str(rk)+"part"+'05%',str(rk)+"part"+'06%',str(rk)+"part"+'07%']
    column1 = 'part_dict-npg'
    model = pd.DataFrame(columns=columns)
    model.insert(0,column1,rows)
    i=0
    for ni in npg_list:

        temp1 = temp.loc[temp['npg_code']==ni]
        model[str(rk)+"part"+'01%'][i]=(temp1.loc[temp['M_01']=='Y','M_01'].count()/cust_count)*100
        model[str(rk)+"part"+'02%'][i]=(temp1.loc[temp['M_02']=='Y','M_02'].count()/cust_count)*100
        model[str(rk)+"part"+'03%'][i]=(temp1.loc[temp['M_03']=='Y','M_03'].count()/cust_count)*100
        model[str(rk)+"part"+'04%'][i]=(temp1.loc[temp['M_04']=='Y','M_04'].count()/cust_count)*100
        model[str(rk)+"part"+'05%'][i]=(temp1.loc[temp['M_05']=='Y','M_05'].count()/cust_count)*100
        model[str(rk)+"part"+'06%'][i]=(temp1.loc[temp['M_06']=='Y','M_06'].count()/cust_count)*100
        model[str(rk)+"part"+'07%'][i]=(temp1.loc[temp['M_07']=='Y','M_07'].count()/cust_count)*100
        i+=1
    part_dict["{}".format(rk)]=pd.DataFrame(model)
    i=0
#SV_01


# In[4417]:


part_dict.keys()


# Verfied and cross- Checked With Values

# In[4421]:


#dicts are :- quant_dict ,sale_dict,part_dict


#  

#  

#  

#  

# # Fetching of [Sales value, Participation, quantity for each] and stored in respective dicts

#  

# # Getting the Top 20 from each of the above - sales,quant,part

# # Creating average sheet - 7 Months

# In[4422]:


sale_dict.keys()


# 1) for sales values/

# In[4424]:


final_sale_df = pd.DataFrame()


# In[4425]:


for key in list(sale_dict.keys()):
    temp =sale_dict[key]
    temp = temp.drop('sale_dict-npg',axis=1)
    model_new = pd.DataFrame()
    model_new[key+"-Sale"+'-average'] = temp.sum(axis=1)/7
    final_sale_df = pd.concat([final_sale_df,model_new],axis=1)
final_sale_df.insert(0,'Npg',npg_list)


# Verified 

# 2) Quantity 

# In[4427]:


final_quant_df = pd.DataFrame()


# In[4428]:


for key in list(quant_dict.keys()):
    temp =quant_dict[key]
    temp = temp.drop('quant_dict-npg',axis=1)
    model_new = pd.DataFrame()
    model_new[key+"-Quantity"+'-average'] = temp.sum(axis=1)/7
    final_quant_df = pd.concat([final_quant_df,model_new],axis=1)
final_quant_df.insert(0,'Npg',npg_list)


# Verified

# 3) Participation

# In[4430]:



final_part_df = pd.DataFrame()


# In[4431]:


part_dict.keys()


# In[4432]:


for key in list(part_dict.keys()):
    temp =part_dict[key]
    temp = temp.drop('part_dict-npg',axis=1)
    model_new = pd.DataFrame()
    model_new[key+"-Participation"+'-average'] = temp.sum(axis=1)/7
    final_part_df = pd.concat([final_part_df,model_new],axis=1)
final_part_df.insert(0,'Npg',npg_list)


# In[4433]:


temp = final_part_df


# Verified

# # Joining the final 3 Datasheets for picking the tops

# In[4441]:


final_3_df = pd.DataFrame()


# In[4442]:


final_3_df = pd.concat([final_sale_df,final_part_df,final_quant_df],axis=1)


# In[4444]:


prod_list = product_dict.values()
#npg_list


# In[4446]:


final_3_df =final_3_df.drop(['Npg'],axis=1)


# In[4447]:


final_3_df.insert(0,'Product',prod_list)


# # Obtained Consolidation
# Noticed Almost Nill Variations

#  

#  

#  

# # obtaining top 20 for all re's - 7 Months

# In[4451]:


top_20_list = {}
df_list  = list(final_3_df.columns)
df_list = df_list[1:]


# In[4452]:


df_list


# In[4453]:


for dl in df_list:
    temp = final_3_df.sort_values(dl,ascending=False)
    temp_list = temp['Product'].to_list()
    temp_list = temp_list[:20]
    top_20_list["{}".format(dl)] = pd.DataFrame(temp_list)
    


# In[4454]:


top_20_7M_keys = list(top_20_list.keys())


# In[4455]:


top_20_7M_df = pd.DataFrame(columns = top_20_7M_keys)


# In[4456]:


for key in top_20_7M_keys:
    temp = list(top_20_list[key][0])
    top_20_7M_df[key] = temp


# In[ ]:





# In[4459]:


sale_dict.keys()


# In[4460]:


top_20_7M_df.keys()


# In[4461]:


temp = list(top_20_7M_df.keys())
temp1 = list(sale_dict.keys())
top207m={}
lister = []
iter_ = 0
for iter_ in temp1:
    lister=[]
    for key in temp:

        
        if key.find(iter_)!=-1:
            print(key)
            print("inside")
            
            n_temp = top_20_7M_df[key].tolist()
            lister.append(n_temp)
        else:
            pass
    top207m["{}".format(iter_)] = lister
    
        
        
        
        
    
    


# In[4462]:


top207m.keys()


# In[4463]:


#top207m['TRIVANDRUM_GS']


# In[4464]:


temp = top207m['TRISSUR_GS']
temp1 = [y for x in temp for y in x]


# In[4468]:


len_list = []
for key in top207m.keys():
    temp = top207m[key]
    temp1 = [y for x in temp for y in x]
    temp_set = list(set(temp1))
    len_list.append(len(temp_set))
m_l = max(len_list)


# In[4470]:


top207m.keys()
top20_7m = pd.DataFrame()
i=0
top20_7m['null'] = [0 for x in range(m_l)]
for key in top207m.keys():
    temp = top207m[key]
    temp1 = [y for x in temp for y in x]
    temp_set = list(set(temp1))
    top20_7m[key] = pd.Series(temp_set)
top20_7m.drop('null',inplace=True,axis=1)  


# In[4471]:


top20_7m.keys()


# # Creating Averages for 3 months

# 1) Sales Value

# In[4476]:


final_sale_df3 = pd.DataFrame()


# In[4477]:


sale_dict.keys()


# In[4478]:


for key in list(sale_dict.keys()):
    temp =sale_dict[key].iloc[:,-3:,]
    #temp = temp.drop('sale_dict-npg',axis=1)
    model_new = pd.DataFrame()
    model_new[key+"-Sale"+'-average'] = temp.sum(axis=1)/3
    final_sale_df3 = pd.concat([final_sale_df3,model_new],axis=1)
final_sale_df3.insert(0,'Npg',npg_list)


# 2) Quantity

# In[4481]:


final_quant_df3 = pd.DataFrame()


# In[4482]:


for key in list(quant_dict.keys()):
    temp =quant_dict[key].iloc[:,-3:,]
    #temp = temp.drop('sale_dict-npg',axis=1)
    model_new = pd.DataFrame()
    model_new[key+"-Quantity"+'-average'] = temp.sum(axis=1)/3
    final_quant_df3 = pd.concat([final_quant_df3,model_new],axis=1)
final_quant_df3.insert(0,'Npg',npg_list)


# 3) Participation

# In[4483]:


final_part_df3 = pd.DataFrame()


# In[4484]:


for key in list(part_dict.keys()):
    temp =part_dict[key].iloc[:,-3:,]
    #temp = temp.drop('sale_dict-npg',axis=1)
    model_new = pd.DataFrame()
    model_new[key+"-Participation"+'-average'] = temp.sum(axis=1)/3
    final_part_df3 = pd.concat([final_part_df3,model_new],axis=1)
final_part_df3.insert(0,'Npg',npg_list)


# In[4485]:


final_3_df3 = pd.DataFrame()


# In[4486]:


final_3_df3 = pd.concat([final_sale_df3,final_part_df3,final_quant_df3],axis=1)


# In[4487]:


final_3_df3 =final_3_df3.drop(['Npg'],axis=1)


# In[4488]:


final_3_df3.insert(0,'Product',prod_list)


# In[4489]:


final_3_df3


# # Consolidation - 3 months obtained
# - values checked , error Correction Made properly 

#  

#  

#  

# # obtaining top 20 for the last 3 months

# In[4491]:


top_20_list3 = {}
df_list3  = list(final_3_df3.columns)
df_list3 = df_list3[1:]


# In[4492]:


for dl in df_list3:
    temp = final_3_df3.sort_values(dl,ascending=False)
    temp_list = temp['Product'].to_list()
    temp_list = temp_list[:20]
    top_20_list3["{}".format(dl)] = pd.DataFrame(temp_list)
    


# In[4493]:


top_20_list3.keys()


# In[4494]:


top_20_3M_keys = list(top_20_list3.keys())


# In[4495]:


top_20_3M_df = pd.DataFrame(columns = top_20_3M_keys)


# In[4496]:


for key in top_20_3M_keys:
    temp = list(top_20_list3[key][0])
    top_20_3M_df[key] = temp


# In[4497]:


#top_20_3M_df


# In[4498]:


temp = list(top_20_3M_df.keys())
temp1 = list(sale_dict.keys())
top203m={}
lister = []
iter_ = 0
for iter_ in temp1:
    lister=[]
    for key in temp:

        
        if key.find(iter_)!=-1:
            print(key)
            print("inside")
            
            n_temp = top_20_3M_df[key].tolist()
            lister.append(n_temp)
        else:
            pass
    top203m["{}".format(iter_)] = lister
    
        
        
        
        
    
    


# In[4499]:


len_list = []
for key in top203m.keys():
    temp = top203m[key]
    temp1 = [y for x in temp for y in x]
    temp_set = list(set(temp1))
    len_list.append(len(temp_set))
m_l = max(len_list)


# In[ ]:





# In[4500]:


top203m.keys()
top20_3m = pd.DataFrame()
i=0
top20_3m['null'] = [0 for x in range(m_l)]
for key in top203m.keys():
    temp = top203m[key]
    temp1 = [y for x in temp for y in x]
    temp_set = list(set(temp1))
    top20_3m[key] = pd.Series(temp_set)
top20_3m.drop('null',inplace =True , axis=1)


# # Done With top 20 (7,last3) Months - Validated and matches! 
# 

# Top 20 From 7 Months

# Top 20 From Last 3 Months

# In[4505]:


t_list = list(top20_3m.keys())


# In[4506]:


t_list


# In[4507]:


final_top20 = {}


# In[4508]:


for key1 in top20_7m.keys():
    for key2 in top20_3m.keys():
        if(key1==key2):
            lister_t1 = top20_3m[key2].tolist()
            lister_t2 = top20_7m[key1].tolist()
            final_t = list(set(lister_t1+lister_t2))
    final_top20["{}".format(key1)] = final_t


# In[4509]:


list_ = list(final_top20.keys())


# In[4510]:


list_


# In[4511]:


finaltop20 = {}
for key in list_:
    temp = final_top20[key]
    temp1 = [incom for incom in temp if str(incom) != 'nan']
    finaltop20["{}".format(key)] = temp1


# In[4512]:


max_ = list_[0]
for key in list_:
    if(len(finaltop20[key])>len(finaltop20[max_])):            #for pd.Series to start fetching from the highest value !
        max_ = key
    else:
        pass
in_ = list_.index(max_)
if(max_==list_[0]):
    pass
else:
    list_[0],list_[in_]=list_[in_],list_[0]


# In[4513]:


finaltop20_df = pd.DataFrame()
for key in list_:
    temp = finaltop20[key]
    #temp1 = [y for x in temp for y in x]
    temp_set = temp
    finaltop20_df[key] = pd.Series(temp_set)


# In[4515]:


final_order = list(top20_3m.keys())


# In[4516]:


final_order


# In[4517]:


finaltop20_df = finaltop20_df.reindex(final_order,axis=1)


# In[4524]:


pr_df = []
for d in list(finaltop20_df.keys()):
    temp = list(finaltop20_df[d])
    pr_df = pr_df+temp
    


# In[4525]:


pr_df_temp = [x for x in pr_df if str(x)!='nan']


# In[4526]:


len(pr_df_temp)


# In[4528]:


Y = ['Y' for x in range(len(pr_df_temp))]


# In[4529]:


pr_y_dict  = dict(zip(pr_df_temp,Y))


# In[4530]:


data_2_sheet_kmg['present'] = data_2_sheet_kmg['npg_desc'].map(pr_y_dict)


# Error Correction and Validation Done

# # Sheet 2 Finished - Values Verified
# - errors corrected , modified , values inplace [slight errors still remian] 

#  

#  

#   

#  

#  

# # Sheet 3 Starts !  

# # Crafting for 3 Kinds of Boxes - [ high , low ,medium]

# # Low

# In[4533]:


re = re_2


# In[4534]:


re


# In[4535]:


city_cat_2


# In[4536]:


finaltop20_df.shape


# In[4537]:


#types_class


# In[4538]:


finaltop20_df.columns


# In[4539]:


finaltop20_df.shape


# In[4540]:


finaltop20_df.keys()


# In[4543]:


#newWay
city_df = []
iter_=0
for key in finaltop20_df.keys():
    x = list(finaltop20_df.keys())[iter_]
    cit = x[:-3]
    temp = finaltop20_df[key].tolist()
    temp = [x for x in temp if str(x)!='nan']
    l_ = len(temp)
    for i in range(l_):
        
        city_df.append(cit)
    iter_+=1
    
    


# In[4544]:


len(city_df)


# pr_df = []
# for d in list(merged_df.columns):
#     temp = list(merged_df[d])
#     pr_df = pr_df+temp
#     

# Y = ['Y' for x in range(len(pr_df))]

# pr_y_dict  = dict(zip(pr_df,Y))

# data_2_sheet_kmg['present'] = data_2_sheet_kmg['npg_desc'].map(pr_y_dict)

# In[4547]:


re


# In[4551]:


re_df = []
iter_=0
for key in finaltop20_df.keys():
    x = list(finaltop20_df.keys())[iter_]
    re = x[-2:]
    temp = finaltop20_df[key].tolist()
    temp = [x for x in temp if str(x)!='nan']
    l_ = len(temp)
    for i in range(l_):
        
        re_df.append(re)
    iter_+=1


# In[4554]:


outlet_type = ["low" for l in range(len(re_df))]


# In[4555]:


len(outlet_type)


# In[4556]:


low_part_df = pd.DataFrame()
low_part_df['NPG'] = pr_df_temp
low_part_df['City'] = city_df
low_part_df['RE'] = re_df


# In[4557]:


tags = list(filter(lambda x: str(x)!='nan',data_2_sheet_kmg['category'].unique()))


# In[4558]:


tags


# In[4559]:


low_part_df


# In[4560]:


#number of outlets unique
tag_dict_low = {}
for cit in city_cat_2:
    for r in re_2:
        temp = data_2_sheet_kmg.loc[(data_2_sheet_kmg['re']==r) & (data_2_sheet_kmg['category']=='low') &(data_2_sheet_kmg['city']==cit)]
        temp1 = len(temp.loc[temp['present']=='Y','customer'].unique())
        tag_dict_low["{}_{}_low".format(cit,r)]=temp1


# In[4561]:


tag_dict_low.keys()


# temp = data_2_sheet_kmg.loc[(data_2_sheet_kmg['re']=='MS') & (data_2_sheet_kmg['category']=='high') &(data_2_sheet_kmg['city']=='TRIVANDRUM')]

# temp1 = temp.loc[temp['present']=='Y','customer'].unique()

# In[4565]:


finaltop20_df.shape


# In[4568]:


outlets_df = []
iter_=0
for key in list(tag_dict_low.keys()):
    #x = list(finaltop20_df.keys())[iter_]
    #re = x[-2:]
    temp = finaltop20_df[key[:-4]].tolist()
    temp = [x for x in temp if str(x)!='nan']
    l_ = len(temp)
    for i in range(l_):
        
        outlets_df.append(tag_dict_low[key])
    iter_+=1


# In[4569]:


tag_dict_low.keys()


# In[4570]:


len(outlets_df)


# In[4571]:


low_part_df['Active Outlets'] = outlets_df


# In[4573]:


low_part_df['npg_code'] = low_part_df['NPG'].map(product_dict_inverse)


# # Analysed and Debugged Code 
# - Slight Variations

# # P1

# In[4577]:


merged_df = finaltop20_df


# 
# 
# MONTH  DIVISION

# In[4579]:


npg_low_list = low_part_df['npg_code'].to_list()


# In[4582]:


model = pd.DataFrame()


# In[4583]:


city_cat_2


# In[4585]:


loc=0
kk=0
#empx = finaltop20_df[finaltop20_df.keys()[0]].tolist()
#empx = [x for x in tempx if str(x)!='nan']
#_ = len(tempx)
shape_end=0


temp_dict = {}
#print("Loc = "+str(loc))
#print("Shape_end = "+str(shape_end))



iter_ = 0
#comp = len(npg_low_list)//finaltop20_df.shape[0]

for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        #print(cit)
        #iter_ = 0
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        print("LOC="+str(loc))
        print("shapened="+str(shape_end))#print(r)
        #if(iter_<comp//len(city_cat_2)):
        set_ = npg_low_list[loc:shape_end]
        rows = set_
        columns = [str(r)+"outlet"+'01',str(r)+"outlet"+'02',str(r)+"outlet"+'03',str(r)+"outlet"+'04',str(r)+"outlet"+'05',str(r)+"outlet"+'06',str(r)+"outlet"+'07']
        column1 = 'npg_low_list'
        model = pd.DataFrame(columns=columns)
        model.insert(0,column1,rows)

        i=0
        for n in set_:



            temp = data_2_sheet_kmg.loc[data_2_sheet_kmg['re']==r]
            temp1 = temp.loc[temp['city']==cit]
            temp2 = temp1.loc[temp1['category']=='low']
            temp3 = temp2.loc[temp2['npg_code']==n]
            l = len(temp3.loc[temp3['M_01']=='Y'])
            model[str(r)+"outlet"+'01'][i]=l
            l = len(temp3.loc[temp3['M_02']=='Y'])
            model[str(r)+"outlet"+'02'][i]=l
            l = len(temp3.loc[temp3['M_03']=='Y'])
            model[str(r)+"outlet"+'03'][i]=l
            l = len(temp3.loc[temp3['M_04']=='Y'])
            model[str(r)+"outlet"+'04'][i]=l
            l = len(temp3.loc[temp3['M_05']=='Y'])
            model[str(r)+"outlet"+'05'][i]=l
            l = len(temp3.loc[temp3['M_06']=='Y'])
            model[str(r)+"outlet"+'06'][i]=l
            l = len(temp3.loc[temp3['M_07']=='Y'])
            model[str(r)+"outlet"+'07'][i]=l
            i+=1




        temp_dict["{}_{}".format(cit,r)]=pd.DataFrame(model)
        
        print(kk)
        kk+=1
        loc = loc+l_
        i=0
        
        #ter_+=1

            #if(kk>=len(finaltop20_df.keys())):
               # break


# In[4586]:


temp_dict.keys()


# In[4588]:


low_m_div = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_m_div['outlet_m01']=[0 for it in range(low_part_df.shape[0])]
low_m_div['outlet_m02']=[0 for it in range(low_part_df.shape[0])]
low_m_div['outlet_m03']=[0 for it in range(low_part_df.shape[0])]
low_m_div['outlet_m04']=[0 for it in range(low_part_df.shape[0])]
low_m_div['outlet_m05']=[0 for it in range(low_part_df.shape[0])]
low_m_div['outlet_m06']=[0 for it in range(low_part_df.shape[0])]
low_m_div['outlet_m07']=[0 for it in range(low_part_df.shape[0])]


# In[4590]:


loc=0
shape_end = 0
ite_ = 0
for key in list(temp_dict.keys()):
    for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
    for j in re_2:
        if key.find(j)!=-1:
            r = str(j)
        #print(cit)
        #iter_ = 0
    l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
    shape_end = l_+shape_end
    #print(key)
    ite_ = 0
    print("loc="+str(loc))
    print("shape_end="+str(shape_end))
    #print(cit)
    #print(r)
    for il in range(loc,shape_end):
        #print(ite_)
        temp = list(temp_dict[key].iloc[ite_])
        temp.pop(0)
        low_m_div.iloc[il]=temp
        ite_+=1
        #print(temp)
    #print("success")
    loc=loc+l_
    
        
    
    


# In[4591]:


low_m_div


# In[4592]:


low_part_df = pd.concat([low_part_df,low_m_div],axis=1)


# SALES DIVISION

# In[4595]:


model = pd.DataFrame()


# In[4596]:


loc=0
shape_end = 0
temp_dict_s = {}



for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        #print(cit)
        #iter_ = 0
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        print("LOC="+str(loc))
        print("shapened="+str(shape_end))#print(r)  
        set_ = npg_low_list[loc:shape_end]
        rows = set_
        columns = [str(r)+"sale"+'01',str(r)+"sale"+'02',str(r)+"sale"+'03',str(r)+"sale"+'04',str(r)+"sale"+'05',str(r)+"sale"+'06',str(r)+"sale"+'07']
        column1 = 'npg_low_list'
        model = pd.DataFrame(columns=columns)
        model.insert(0,column1,rows)

        i=0
        for n in set_:



            temp = data_2_sheet_kmg.loc[data_2_sheet_kmg['re']==r]
            temp1 = temp.loc[temp['city']==cit]
            temp2 = temp1.loc[temp1['category']=='low']
            temp3 = temp2.loc[temp2['npg_code']==n]
            l = temp3.loc[temp3['SV_01']!=0,'SV_01'].sum()
            model[str(r)+"sale"+'01'][i]=l
            l = temp3.loc[temp3['SV_02']!=0,'SV_02'].sum()
            model[str(r)+"sale"+'02'][i]=l
            l = temp3.loc[temp3['SV_03']!=0,'SV_03'].sum()
            model[str(r)+"sale"+'03'][i]=l
            l = temp3.loc[temp3['SV_04']!=0,'SV_04'].sum()
            model[str(r)+"sale"+'04'][i]=l
            l = temp3.loc[temp3['SV_05']!=0,'SV_05'].sum()
            model[str(r)+"sale"+'05'][i]=l
            l = temp3.loc[temp3['SV_06']!=0,'SV_06'].sum()
            model[str(r)+"sale"+'06'][i]=l
            l = temp3.loc[temp3['SV_07']!=0,'SV_07'].sum()
            model[str(r)+"sale"+'07'][i]=l
            i+=1





            
        temp_dict_s["{}_{}".format(cit,r)]=pd.DataFrame(model)
        #print(kk)
        kk+=1
        loc = loc+l_
        i=0
        


# In[4597]:


temp_dict_s.keys()


# In[4599]:


low_s_div = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_s_div['sale_01']=[0 for it in range(low_part_df.shape[0])]
low_s_div['sale_02']=[0 for it in range(low_part_df.shape[0])]
low_s_div['sale_03']=[0 for it in range(low_part_df.shape[0])]
low_s_div['sale_04']=[0 for it in range(low_part_df.shape[0])]
low_s_div['sale_05']=[0 for it in range(low_part_df.shape[0])]
low_s_div['sale_06']=[0 for it in range(low_part_df.shape[0])]
low_s_div['sale_07']=[0 for it in range(low_part_df.shape[0])]


# In[4601]:


loc=0
shape_end = 0
ite_ = 0
for key in list(temp_dict.keys()):
    for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
    for j in re_2:
        if key.find(j)!=-1:
            r = str(j)
        #print(cit)
        #iter_ = 0
    l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
    print(l_)
    shape_end = l_+shape_end
    #print(key)
    ite_ = 0
    print("loc="+str(loc))
    print("shape_end="+str(shape_end))
    #print(cit)
    #print(r)
    for il in range(loc,shape_end):
        #print(ite_)
        temp = list(temp_dict_s[key].iloc[ite_])
        temp.pop(0)
        low_s_div.iloc[il]=temp
        ite_+=1
        #print(temp)
    #print("success")
    loc=loc+l_
    
        
    
    


# In[4603]:


low_part_df = pd.concat([low_part_df,low_s_div],axis=1)


# In[4604]:


#low_part_df.to_csv("interlowBox.csv")


# #  Verfied with slight differences
# - outlet numbers and sales value
# 
# varying values observed, due to difference in outlet tagging ! /
# 

# QUANTITY DIVISION

# In[4606]:


model = pd.DataFrame()


# In[4609]:


loc=0
shape_end = finaltop20_df.shape[0]
temp_dict_q = {}
shape_end = 0
    

iter_ = 0
#comp = len(npg_low_list)//finaltop20_df.shape[0]


for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        #print(cit)
        #iter_ = 0
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        print("LOC="+str(loc))
        print("shapened="+str(shape_end))#print(r)
        set_ = npg_low_list[loc:shape_end]
        rows = set_
        columns = [str(r)+"quantity"+'01',str(r)+"quantity"+'02',str(r)+"quantity"+'03',str(r)+"quantity"+'04',str(r)+"quantity"+'05',str(r)+"quantity"+'06',str(r)+"quantity"+'07']
        column1 = 'npg_low_list'
        model = pd.DataFrame(columns=columns)
        model.insert(0,column1,rows)

        i=0
        for n in set_:



            temp = data_2_sheet_kmg.loc[data_2_sheet_kmg['re']==r]
            temp1 = temp.loc[temp['city']==cit]
            temp2 = temp1.loc[temp1['category']=='low']
            temp3 = temp2.loc[temp2['npg_code']==n]
            l = temp3.loc[temp3['QY_01']!=0,'QY_01'].sum()
            model[str(r)+"quantity"+'01'][i]=l
            l = temp3.loc[temp3['QY_02']!=0,'QY_02'].sum()
            model[str(r)+"quantity"+'02'][i]=l
            l = temp3.loc[temp3['QY_03']!=0,'QY_03'].sum()
            model[str(r)+"quantity"+'03'][i]=l
            l = temp3.loc[temp3['QY_04']!=0,'QY_04'].sum()
            model[str(r)+"quantity"+'04'][i]=l
            l = temp3.loc[temp3['QY_05']!=0,'QY_05'].sum()
            model[str(r)+"quantity"+'05'][i]=l
            l = temp3.loc[temp3['QY_06']!=0,'QY_06'].sum()
            model[str(r)+"quantity"+'06'][i]=l
            l = temp3.loc[temp3['QY_07']!=0,'QY_07'].sum()
            model[str(r)+"quantity"+'07'][i]=l






            i+=1
        temp_dict_q["{}_{}".format(cit,r)]=pd.DataFrame(model)
        #print(kk)
        kk+=1
        loc+=l_
        i=0
    


# In[4610]:


temp_dict_q.keys()


# In[4612]:


low_q_div = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_q_div['quantity_01']=[0 for it in range(low_part_df.shape[0])]
low_q_div['quantity_02']=[0 for it in range(low_part_df.shape[0])]
low_q_div['quantity_03']=[0 for it in range(low_part_df.shape[0])]
low_q_div['quantity_04']=[0 for it in range(low_part_df.shape[0])]
low_q_div['quantity_05']=[0 for it in range(low_part_df.shape[0])]
low_q_div['quantity_06']=[0 for it in range(low_part_df.shape[0])]
low_q_div['quantity_07']=[0 for it in range(low_part_df.shape[0])]


# In[4613]:


loc=0
shape_end = 0
ite_ = 0
for key in list(temp_dict_q.keys()):
    for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
    for j in re_2:
        if key.find(j)!=-1:
            r = str(j)
        #print(cit)
        #iter_ = 0
    l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
    print(l_)
    shape_end = l_+shape_end
    #print(key)
    ite_ = 0
    print("loc="+str(loc))
    print("shape_end="+str(shape_end))
    #print(cit)
    #print(r)
    for il in range(loc,shape_end):
        #print(ite_)
        temp = list(temp_dict_q[key].iloc[ite_])
        temp.pop(0)
        low_q_div.iloc[il]=temp
        ite_+=1
        #print(temp)
    #print("success")
    loc=loc+l_
    
        
    
    


# In[4615]:


low_part_df = pd.concat([low_part_df,low_q_div],axis=1)


# PARTICIPATION - FLooring has been done here in the main sheet ?

# In[4618]:


model = pd.DataFrame()
part_df_ne=pd.DataFrame()


# In[4619]:


part_df_new = low_part_df.filter(['NPG','outlet_m01','outlet_m02','outlet_m03','outlet_m04','outlet_m05','outlet_m06','outlet_m07','Active Outlets'],axis=1)


# In[4620]:


part_df_new


# In[4621]:


low_p_div = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_p_div['participation_01']=[0 for it in range(low_part_df.shape[0])]
low_p_div['participation_02']=[0 for it in range(low_part_df.shape[0])]
low_p_div['participation_03']=[0 for it in range(low_part_df.shape[0])]
low_p_div['participation_04']=[0 for it in range(low_part_df.shape[0])]
low_p_div['participation_05']=[0 for it in range(low_part_df.shape[0])]
low_p_div['participation_06']=[0 for it in range(low_part_df.shape[0])]
low_p_div['participation_07']=[0 for it in range(low_part_df.shape[0])]


# In[4622]:


for l in range(low_part_df.shape[0]):
    temp=(part_df_new['outlet_m01'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_01'][l]=temp
    temp=(part_df_new['outlet_m02'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_02'][l]=temp
    temp=(part_df_new['outlet_m03'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_03'][l]=temp
    temp=(part_df_new['outlet_m04'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_04'][l]=temp
    temp=(part_df_new['outlet_m05'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_05'][l]=temp
    temp=(part_df_new['outlet_m06'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_06'][l]=temp
    temp=(part_df_new['outlet_m07'][l]/part_df_new['Active Outlets'][l])*100
    low_p_div['participation_07'][l]=temp
    


# In[4624]:


low_part_df = pd.concat([low_part_df,low_p_div],axis=1)


# In[4626]:


low_part_df.columns


# Average Sales Value

# In[4631]:


low_avg_sale = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_avg_sale['AvgSValue01']=[0 for it in range(low_part_df.shape[0])]
low_avg_sale['AvgSValue02']=[0 for it in range(low_part_df.shape[0])]
low_avg_sale['AvgSValue03']=[0 for it in range(low_part_df.shape[0])]
low_avg_sale['AvgSValue04']=[0 for it in range(low_part_df.shape[0])]
low_avg_sale['AvgSValue05']=[0 for it in range(low_part_df.shape[0])]
low_avg_sale['AvgSValue06']=[0 for it in range(low_part_df.shape[0])]
low_avg_sale['AvgSValue07']=[0 for it in range(low_part_df.shape[0])]


# In[4632]:


for l in range(low_part_df.shape[0]):
    temp=low_part_df['sale_01'][l]/low_part_df['outlet_m01'][l]
    low_avg_sale['AvgSValue01'][l]=temp
    temp=low_part_df['sale_02'][l]/low_part_df['outlet_m02'][l]
    low_avg_sale['AvgSValue02'][l]=temp
    temp=low_part_df['sale_03'][l]/low_part_df['outlet_m03'][l]
    low_avg_sale['AvgSValue03'][l]=temp
    temp=low_part_df['sale_04'][l]/low_part_df['outlet_m04'][l]
    low_avg_sale['AvgSValue04'][l]=temp
    temp=low_part_df['sale_05'][l]/low_part_df['outlet_m05'][l]
    low_avg_sale['AvgSValue05'][l]=temp
    temp=low_part_df['sale_06'][l]/low_part_df['outlet_m06'][l]
    low_avg_sale['AvgSValue06'][l]=temp
    temp=low_part_df['sale_07'][l]/low_part_df['outlet_m07'][l]
    low_avg_sale['AvgSValue07'][l]=temp
    


# In[4634]:


low_part_df = pd.concat([low_part_df,low_avg_sale],axis=1)


# Average Quantity

# In[4637]:


low_avg_q = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_avg_q['AvgQty01']=[0 for it in range(low_part_df.shape[0])]
low_avg_q['AvgQty02']=[0 for it in range(low_part_df.shape[0])]
low_avg_q['AvgQty03']=[0 for it in range(low_part_df.shape[0])]
low_avg_q['AvgQty04']=[0 for it in range(low_part_df.shape[0])]
low_avg_q['AvgQty05']=[0 for it in range(low_part_df.shape[0])]
low_avg_q['AvgQty06']=[0 for it in range(low_part_df.shape[0])]
low_avg_q['AvgQty07']=[0 for it in range(low_part_df.shape[0])]


# In[4638]:


for l in range(low_part_df.shape[0]):
    temp=low_part_df['quantity_01'][l]/low_part_df['outlet_m01'][l]
    low_avg_q['AvgQty01'][l]=round(temp)
    temp=low_part_df['quantity_02'][l]/low_part_df['outlet_m02'][l]
    low_avg_q['AvgQty02'][l]=round(temp)
    temp=low_part_df['quantity_03'][l]/low_part_df['outlet_m03'][l]
    low_avg_q['AvgQty03'][l]=round(temp)
    temp=low_part_df['quantity_04'][l]/low_part_df['outlet_m04'][l]
    low_avg_q['AvgQty04'][l]=round(temp)
    temp=low_part_df['quantity_05'][l]/low_part_df['outlet_m05'][l]
    low_avg_q['AvgQty05'][l]=round(temp)
    temp=low_part_df['quantity_06'][l]/low_part_df['outlet_m06'][l]
    low_avg_q['AvgQty06'][l]=round(temp)
    temp=low_part_df['quantity_07'][l]/low_part_df['outlet_m07'][l]
    low_avg_q['AvgQty07'][l]=round(temp)
    


# In[4640]:


low_part_df = pd.concat([low_part_df,low_avg_q],axis=1)


# # Verfied and Values with Slight Changes Identified
# - NAN values present in Avg Sales & AVg Quantity
# - Values nearly tallying 

# Price Per Quantity 

# In[4642]:


low_ppq = pd.DataFrame()
#low_m_div['init_col'] = pr_df
low_ppq['PricePQty01']=[0 for it in range(low_part_df.shape[0])]
low_ppq['PricePQty02']=[0 for it in range(low_part_df.shape[0])]
low_ppq['PricePQty03']=[0 for it in range(low_part_df.shape[0])]
low_ppq['PricePQty04']=[0 for it in range(low_part_df.shape[0])]
low_ppq['PricePQty05']=[0 for it in range(low_part_df.shape[0])]
low_ppq['PricePQty06']=[0 for it in range(low_part_df.shape[0])]
low_ppq['PricePQty07']=[0 for it in range(low_part_df.shape[0])]


# In[4643]:


for l in range(low_part_df.shape[0]):
    try:
        temp=low_part_df['AvgSValue01'][l]/low_part_df['AvgQty01'][l]
        low_ppq['PricePQty01'][l]=temp
    except:
        temp = 0
        low_ppq['PricePQty01'][l]=temp
        
        
    try:
        temp=low_part_df['AvgSValue02'][l]/low_part_df['AvgQty02'][l]
    
        low_ppq['PricePQty02'][l]=temp
    except:
        temp=0
        low_ppq['PricePQty02'][l]=temp
        
        
    try:
        temp=low_part_df['AvgSValue03'][l]/low_part_df['AvgQty03'][l]
    
        low_ppq['PricePQty03'][l]=temp
    except:
        temp=0
        low_ppq['PricePQty03'][l]=temp
        
        
    try:
        temp=low_part_df['AvgSValue04'][l]/low_part_df['AvgQty04'][l]
    
        low_ppq['PricePQty04'][l]=temp
    except:
        temp=0
        low_ppq['PricePQty04'][l]=temp
        
    try:
        temp=low_part_df['AvgSValue05'][l]/low_part_df['AvgQty05'][l]
    
        low_ppq['PricePQty05'][l]=temp
    except:
        temp=0
        low_ppq['PricePQty05'][l]=temp
        
    try:
        temp=low_part_df['AvgSValue06'][l]/low_part_df['AvgQty06'][l]
    
        low_ppq['PricePQty06'][l]=temp
    except:
        temp=0
        low_ppq['PricePQty06'][l]=temp
        
    try:
        temp=low_part_df['AvgSValue07'][l]/low_part_df['AvgQty07'][l]
    
        low_ppq['PricePQty07'][l]=temp
    except:
        temp = 0
        low_ppq['PricePQty07'][l]=temp
    


# In[4644]:


low_part_df = pd.concat([low_part_df,low_ppq],axis=1)


# In[ ]:





# AverageRetailerPArticipation  -- list of averages ! 

# In[4646]:


ret_df = low_part_df.filter(['participation_01','participation_02','participation_03','participation_04','participation_05','participation_06','participation_07'],axis=1)


# In[4647]:


ret_avg = []


# In[4648]:


months = 7 


# In[4649]:


for l in range(low_part_df.shape[0]):
    ret_avg.append(round(ret_df.loc[l].sum()/months))
    


# In[4650]:


low_part_df['KPI-1 AvgRetPart'] = ret_avg


# AVERAGE SALES VALUE

# In[4652]:


avg_df_kpi= low_part_df.filter(['AvgSValue01','AvgSValue02', 'AvgSValue03','AvgSValue04', 'AvgSValue05', 'AvgSValue06', 'AvgSValue07'],axis=1)


# In[4653]:


avg_kpi_sl  = []


# In[4655]:


#conditional Average
for l in range(low_part_df.shape[0]):
    xtemp = list(avg_df_kpi.loc[l])
    k = len([j for j in xtemp if j!=0 and str(j)!='nan'])
    avg_kpi_sl.append(avg_df_kpi.loc[l].sum()/k)


# In[4656]:


low_part_df['KPI-2 AvgSales'] = avg_kpi_sl


# AVERAGE SALES QUANTITY

# In[4658]:


avg_df_kpi2 = low_part_df.filter(['AvgQty01','AvgQty02', 'AvgQty03', 'AvgQty04', 'AvgQty05', 'AvgQty06', 'AvgQty07'],axis=1)


# In[4659]:


avg_kpi_sl2  = []


# In[4660]:


for l in range(low_part_df.shape[0]):
    xtemp = list(avg_df_kpi.loc[l])
    k = len([j for j in xtemp if j!=0 and str(j)!='nan'])
    avg_kpi_sl2.append(round(avg_df_kpi2.loc[l].sum()/k))


# In[4661]:


low_part_df['KPI-3 AvgSlQty'] = avg_kpi_sl2


# AVERAGE PPQ 

# In[4664]:


avg_df_p1 = low_part_df.filter(['PricePQty01', 'PricePQty02', 'PricePQty03', 'PricePQty04','PricePQty05', 'PricePQty06', 'PricePQty07'],axis=1)


# In[ ]:





# In[4666]:


avg_kpi_p  = []


# In[4667]:


months


# In[4668]:


for l in range(low_part_df.shape[0]):
    xtemp = list(avg_df_kpi.loc[l])
    k = len([j for j in xtemp if j!=0 and str(j)!='nan'])
    avg_kpi_p.append(sum(avg_df_p1.loc[l])/k)


# In[4669]:


low_part_df['KPI- PPQAvg'] = avg_kpi_p


# In[4670]:


#low_part_df.replace(np.inf,0)


# In[4671]:


#'iuhiok[p;]p[]'


# In[4672]:


#currently Checking
#low_part_df.fillna(method='bfill',inplace=True)
low_part_df.replace(np.inf,0,inplace=True)


# In[ ]:





# In[4677]:


r_df = low_part_df.filter(['RE','KPI-1 AvgRetPart','KPI-2 AvgSales','KPI-3 AvgSlQty'],axis=1)


# In[4678]:


avg_list=[]
x_list = []


# In[4679]:


r_df.shape


# In[4680]:


merged_df.shape


# In[4682]:


finaltop20_df.keys()


# In[4683]:


loc=0
kk=0
shape_end=0
iter_ = 0
temp_dict = {}
avg_list=[]
x_list = []


for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        print(city,key)
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        #print("LOC="+str(loc))
        #print("shapened="+str(shape_end))
        temp=r_df['KPI-1 AvgRetPart']
        x_list=temp[loc:shape_end].rank(method = 'dense',ascending = False) 
        avg_list.append(x_list.values.tolist())
        print(shape_end-loc)
        
        loc = loc+l_
        i=0


# In[ ]:





# In[4684]:


flat_avg = [int(y) for x in avg_list for y in x] #flattening code


# In[4685]:


tag_list_ = []
point_list_=[]


# In[4686]:


for x in flat_avg:
    if x <5:
        tag_list_.append("Very_High")
        point_list_.append(5)
    elif x<10:
        tag_list_.append("High")
        point_list_.append(4)
    elif x<15:
        tag_list_.append("Medium_1")
        point_list_.append(3)
    elif x<20:
        tag_list_.append("Medium_2")
        point_list_.append(2)
    elif x>=20:
        tag_list_.append("Low")
        point_list_.append(1)
    else:
        tag_list_.append("nan")
        point_list_.append(0)
        


# In[ ]:





# In[4687]:


low_part_df['AvgRetPart_Tag'] = tag_list_


# In[4688]:


low_part_df['AvgRetPart_point'] = point_list_


# In[4689]:


low_part_df['Rank AvgRetPart'] = flat_avg


#  

#  

# In[4692]:


loc=0
kk=0
shape_end=0
iter_ = 0
temp_dict = {}
avg_list=[]
x_list = []


for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        print("LOC="+str(loc))
        print("shapened="+str(shape_end))
        temp=r_df['KPI-2 AvgSales']
        x_list=temp[loc:shape_end].rank(method = 'dense',ascending = False) 
        avg_list.append(x_list.values.tolist())
        
        
        loc = loc+l_
        i=0


# In[4693]:


flat_avg = [int(y) for x in avg_list for y in x]


# In[4694]:


tag_list_ = []
point_list_=[]


# In[4695]:


for x in flat_avg:
    if x <5:
        tag_list_.append("Very_High")
        point_list_.append(5)
    elif x<10:
        tag_list_.append("High")
        point_list_.append(4)
    elif x<15:
        tag_list_.append("Medium_1")
        point_list_.append(3)
    elif x<20:
        tag_list_.append("Medium_2")
        point_list_.append(2)
    elif x>=20:
        tag_list_.append("Low")
        point_list_.append(1)
    else:
        tag_list_.append("nan")
        point_list_.append(0)
        


# In[ ]:





# In[4696]:


low_part_df['AvgSales_Tag'] = tag_list_


# In[4697]:


low_part_df['AvgSales_point'] = point_list_


# In[4698]:


low_part_df['Rank AvgSales'] = flat_avg


#  

#  

# In[4700]:


loc=0
kk=0
shape_end=0
iter_ = 0
temp_dict = {}
avg_list=[]
x_list = []


for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        print("LOC="+str(loc))
        print("shapened="+str(shape_end))
        temp=r_df['KPI-3 AvgSlQty']
        x_list=temp[loc:shape_end].rank(method = 'dense',ascending = False) 
        avg_list.append(x_list.values.tolist())
        
        
        loc = loc+l_
        i=0


# In[4701]:


flat_avg = [int(y) for x in avg_list for y in x]


# In[4702]:


tag_list_ = []
point_list_=[]


# In[4703]:


for x in flat_avg:
    if x <5:
        tag_list_.append("Very_High")
        point_list_.append(5)
    elif x<10:
        tag_list_.append("High")
        point_list_.append(4)
    elif x<15:
        tag_list_.append("Medium_1")
        point_list_.append(3)
    elif x<20:
        tag_list_.append("Medium_2")
        point_list_.append(2)
    elif x>=20:
        tag_list_.append("Low")
        point_list_.append(1)
    else:
        tag_list_.append("nan")
        point_list_.append(0)
        


# In[ ]:





# In[4704]:


low_part_df['AvgSlQty_Tag'] = tag_list_


# In[4705]:


low_part_df['AvgSlQty_point'] = point_list_


# In[4706]:


low_part_df['Rank AvgSlQty'] = flat_avg


#  

#  

# In[4708]:


low_part_df.to_csv("New_fileCheck1.csv")


# In[ ]:





# Points Extraction for ranking index

# In[4709]:


in_df = low_part_df.filter(['AvgRetPart_point','AvgSales_point','AvgSlQty_point'])


# In[4712]:


index = []


# In[4713]:


for il in range(in_df.shape[0]):
    temp = (in_df['AvgRetPart_point'][il]*0.6)+(in_df['AvgSales_point'][il]*0.2)+(in_df['AvgSlQty_point'][il]*0.2)
    index.append(temp)


# In[4714]:


len(index)


# In[4715]:


low_part_df['Index'] = index


# In[4716]:


low_part_df


# Index Ranking

# In[4717]:


avg_list=[]
x_list = []
loc = 0
st_end = merged_df.shape[0]


# In[4721]:


loc=0
kk=0
shape_end=0
iter_ = 0
temp_dict = {}
avg_list=[]
x_list = []
for key in finaltop20_df.keys():
        for h in city_cat_2:
            if key.find(h)!=-1:
                cit=str(h)
        for j in re_2:
            if key.find(j)!=-1:
                r = str(j)
        l_ = low_part_df.loc[(low_part_df['City']==cit)&(low_part_df['RE']==r),'NPG'].count()
        shape_end = shape_end+l_
        print("LOC="+str(loc))
        print("shapened="+str(shape_end))
        temp=low_part_df['Index']
        x_list=round(temp[loc:shape_end].rank(ascending = False))
        avg_list.append(x_list.values.tolist())
        
        
        loc = loc+l_
        i=0


# In[4722]:


flat_avg = [int(y) for x in avg_list for y in x]


# In[4723]:


low_part_df['Ranked Index'] = flat_avg


# In[4724]:


#splitting for checking


# In[4725]:


low_part_df.to_csv("newtagtest.csv")


#  

#  

#  

#  

# # Building Box - LOW

# In[ ]:


final_dict.keys()


# In[ ]:


final_dict['TRIVANDRUM_avg_npgs_per_retailer']


# In[ ]:


dd = []
for cit in city_cat_2:
    
    for key in final_dict.keys():
        if key.find("{}_median_sale_value_per_outlet".format(cit))!=-1:
            dd.append(key)
        if key.find("{}_avg_npgs_per_outlet".format(cit))!=-1:
            dd.append(key)


# In[ ]:


dd


# In[ ]:


city_cat_2


# In[ ]:


tags = ['Low','Medium','High']


# In[ ]:


row_count_final = len(re_2)*len(tags)


# In[ ]:


#npg Count
main_key = []
key = dd[0]
for cit in city_cat_2:
    for wrd in dd:
        if wrd.find("{}_avg_npgs_per_retailer".format(cit))!=-1:
            key = "{}_avg_npgs_per_retailer".format(cit)
        else:
            pass
    typ_list = final_dict[key].iloc[:,0:1]
    typ_list1 = typ_list.values.tolist()
    rows = [item for x in typ_list1 for item in x]
    for x in rows:
        if x.find('low')!=-1:

            main_key.append(x)
        else:
            pass
npg_dict={}
for cit in city_cat_2:
    for key in main_key:
        temp_ = final_dict["{}_avg_npgs_per_retailer".format(cit)]
        temp1 = temp_.loc[temp_['avg npg per retailer']==key]
        temp1List = temp1.iloc[0].values.tolist()
        temp1List.pop(0)
        av = np.ceil(sum(temp1List)/7)
        if av==1:
            av+=1
        npg_dict["{}_{}".format(cit,key)]=av


# In[ ]:


npg_dict


# In[ ]:


#npg Count
main_key2 = []
key2 = dd[0]
for cit in city_cat_2:
    for wrd in dd:
        if wrd.find("{}_median_sale_value_per_outlet".format(cit))!=-1:
            key = "{}_median_sale_value_per_outlet".format(cit)
        else:
            pass
    typ_list = final_dict[key].iloc[:,0:1]
    typ_list1 = typ_list.values.tolist()
    rows = [item for x in typ_list1 for item in x]
    for x in rows:
        if x.find('low')!=-1:

            main_key.append(x)
        else:
            pass
med_val_dict={}
for cit in city_cat_2:
    for key in main_key:
        temp_ = final_dict["{}_median_sale_value_per_outlet".format(cit)]
        temp1 = temp_.loc[temp_['median sale value per outlet']==key]
        temp1List = temp1.iloc[0].values.tolist()
        temp1List.pop(0)
        av = np.ceil(sum(temp1List)/7)
        if av==1:
            av+=1
        med_val_dict["{}_{}".format(cit,key)]=av


# In[ ]:


med_val_dict


# In[ ]:


box_dict = {}
i=0


# In[ ]:


low_part_df.isna().any()


# In[ ]:





# In[ ]:


loc=0
st_end = merged_df.shape[0]
low_dict_2={}
for cit in city_cat_2:
    for r in re_2:
        temp = low_part_df[loc:st_end]
        low_dict_2["{}_{}".format(cit,r)]=temp
        loc+=merged_df.shape[0]
        st_end+=merged_df.shape[0]
        
        


# In[ ]:


low_dict_2.keys()


# In[ ]:


npg_dict


# In[ ]:


med_val_dict


# #slicing boxes 

# In[ ]:


low_dict_3={}
for key in low_dict_2.keys():
    #df = low_dict_2[key]
    temp = low_dict_2[key].sort_values('Ranked Index')
    print(key)
    l =list(npg_dict.keys())
    for e in l:
        if e.find(key)!=-1:
            new_val = int(npg_dict[e])
            break
        else:
            pass
    tempn= temp[:new_val]
    low_dict_3["{}".format(key)]=tempn
    print(new_val)


# In[ ]:


low_dict_3.keys()


# In[ ]:


low_dict_3['TRIVANDRUM_MS'].columns


# In[ ]:


low_dict_4 = {}
for key in low_dict_3.keys():
    
    temp = low_dict_3[key]
    temp1 = temp.filter(['NPG', 'City', 'RE','Index','Ranked Index','KPI-1 AvgRetPart','KPI-2 AvgSales','KPI-3 AvgSlQty','KPI- PPQAvg'])
    temp1.reset_index(inplace=True)
    temp1 = temp1.drop(['index'],axis=1)
    act_val = []
    for iter_ in range(temp1.shape[0]):
        xtmp = (temp1['KPI-1 AvgRetPart'][iter_]*temp1['KPI-2 AvgSales'][iter_])/100
        act_val.append(xtmp)
    temp1['Actual_value'] = act_val
    act_sum = sum(temp1['Actual_value'].values)
    val_con = []
    for iter_ in range(temp1.shape[0]):
        vtmp = (temp1['Actual_value'][iter_]/act_sum)*100
        val_con.append(vtmp)
    temp1['SalesPartPerc%'] = val_con
    low_dict_4["{}".format(key)]= temp1
    
    
        
    


# In[ ]:


low_dict_4.keys()


# In[ ]:


low_dict_4['TRISSUR_GS'].isna()


# In[ ]:


med_val_dict


# In[ ]:


low_dict_5={}
iter_ = 0
for key in low_dict_4.keys():
    print(key)
    temp = low_dict_4[key]
    contribution = []
    ll = list(med_val_dict.keys())
    for k in ll:
        if k.find(key)!=-1:
            new_val = med_val_dict[k]
            break
        else:
            pass
    
    print(new_val)
    for i in range(temp.shape[0]):
        ctmp = (temp['SalesPartPerc%'][i]*new_val)/100
        contribution.append(ctmp)
    temp['normalisedSale'] = contribution
    low_dict_5["{}".format(key)]= temp
    iter_ +=1
        
    
    


# In[ ]:


import math


# In[ ]:


low_dict_6={}
iter_ = 0
for key in low_dict_5.keys():
    low_dict_5[key].fillna(method='bfill',inplace=True)
    temp = low_dict_5[key]
    ct1 = []
    print(key)
    for i in range(temp.shape[0]):
        ctmp = np.ceil(temp['normalisedSale'][i]/temp['KPI- PPQAvg'][i])
        #print(ctmp)
        if(ctmp%3!=0 and ctmp>1):
            val=ctmp%3
            ctmp=ctmp-val
        if ctmp==0:
            ctmp+=1
            
        ct1.append(ctmp)
    
    temp['Quantity'] = ct1
    print(ct1)
    low_dict_6["{}".format(key)]= temp
    iter_ +=1

        
    
    


# In[ ]:





# In[ ]:


low_dict_6.keys()


# In[ ]:


low_dict_6['TRIVANDRUM_MS']


# Sale Value calculation
# 

# Sales Amount

# In[ ]:


low_dict_7={}
iter_ = 0
for key in low_dict_6.keys():
    temp = low_dict_6[key]
    ct = []
    for i in range(temp.shape[0]):
        ctmp = np.ceil(temp['Quantity'][i]*temp['KPI- PPQAvg'][i])
        ct.append(ctmp)
    temp['SaleVAmt'] = ct
    iter_ +=1
    low_dict_7["{}".format(key)]= temp
    iter_ +=1   
    
    


# In[ ]:


low_dict_7['TRIVANDRUM_MS']


# In[ ]:


ll = list(med_val_dict.keys())
for key in low_dict_7.keys():
    temp = low_dict_7[key]
    for l in ll:
        if l.find(key)!=-1:
            new_val = med_val_dict[l]
    sum_ = temp['SaleVAmt'].sum()
    if sum_ - new_val >0:
        pass
    else:
        print(new_val)
        print(new_val -sum_)
        templ = list(temp['KPI-1 AvgRetPart'])
        ind = templ.index(max(templ))
        diff = new_val-sum_
        needed = 15*(new_val)/100
        num = np.ceil(needed/temp['KPI- PPQAvg'][ind])
        num = np.ceil(num/3)*3
        print(num)
        low_dict_7[key]['Quantity'][ind]=int(low_dict_7[key]['Quantity'][ind])+num
    
    
        
    
    


# In[ ]:


low_dict_8={}
iter_ = 0
for key in low_dict_7.keys():
    temp = low_dict_7[key]
    ct = []
    for i in range(temp.shape[0]):
        ctmp = np.ceil(temp['Quantity'][i]*temp['KPI- PPQAvg'][i])
        ct.append(ctmp)
    temp['SaleVAmt'] = ct
    iter_ +=1
    low_dict_8["{}".format(key)]= temp
    iter_ +=1   
    
    


# Sale Contribution

# In[ ]:



low_dict_9={}
iter_ = 0
for key in low_dict_8.keys():
    temp = low_dict_8[key]
    sum_ = temp['SaleVAmt'].values.sum()
    print(sum_)
    ct = []
    for i in range(temp.shape[0]):
        ctmp = (temp['SaleVAmt'][i]/sum_)*100
        ct.append(ctmp)
    temp['SaleContribution'] = ct
    low_dict_9["{}".format(key)]= temp
    iter_ +=1
        
    
    


# In[ ]:


low_dict_8.keys()


# In[ ]:


low_dict_8['TRIVANDRUM_MS']


# In[ ]:


med_val_dict


# In[ ]:


final_low_box = pd.DataFrame()


# In[ ]:


for key in low_dict_8.keys():
    final_low_box = final_low_box.append(low_dict_8[key])
    


# In[ ]:


final_low_box.fillna(0,inplace=True)


# In[ ]:


final_low_box = final_low_box.filter(['NPG','City','RE','Quantity','SaleVAmt','KPI- PPQAvg','SaleContribution'])


# In[ ]:


final_low_box

