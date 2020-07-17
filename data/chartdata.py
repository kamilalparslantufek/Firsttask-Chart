from evds import evdsAPI
import pandas as pd
import numpy as np
import json

class Data:
    tvaluelist = []
    def get_data(self):
        """
        Gets data from EVDS with API_KEY.
        Transforms data, making every year's start 0%, subtracting value from other weeks from data. 
        Weekly Data, 5 Years.
        """
        f = open("data/api.txt", "r")
        api_key = f.read()
        evds = evdsAPI(api_key, lang="ENG")
    
        weekly_raw = evds.get_data(['TP.KKHARTUT.KT1'], startdate="01-01-2016", enddate="31-12-2020", frequency=3, formulas=[1,0])
        
        np_weekly = weekly_raw.to_numpy()
        tvalue = 0
        tvaluelist = []
        """
        i[0] is date
        i[1] is YEARWEEK
        i[2] is our value also im appending 
        i[3] is NaN, this column is made because of formula im using to get percentage values. I think of dropping this column.
        Also im appending year's beginning values to a different list. I may use them.
        """
        for i in np_weekly:
            if i[1] == '2016-1':
                tvalue = i[2]
                tvaluelist.append((i[2]))
            elif i[1] == '2017-1':
                tvalue = i[2]
                tvaluelist.append((i[2]))
            elif i[1] == '2018-1':
                tvalue = i[2]
                tvaluelist.append((i[2]))
            elif i[1] == '2019-1':
                tvalue = i[2]
                tvaluelist.append((i[2]))
            elif i[1] == '2020-1':
                tvalue = i[2]
                tvaluelist.append((i[2]))
            i[2] = i[2] - tvalue
        self.tvaluelist = tvaluelist    
        #I need to transform data back to DF. numpy array is not really serializable as JSON, so i send it back. Also drop last column.
        #tvalue list is only 5 tuples so its easier to send them as JSON.
        transformed_df = pd.DataFrame(np_weekly, columns=weekly_raw.columns)
        transformed_df = transformed_df.drop(columns="TP_KKHARTUT_KT1")
        transformed_df = transformed_df.rename(columns={'TP_KKHARTUT_KT1-1' : 'Values'})

        return transformed_df.to_dict()
    
    def get_transform_values(self):
        """[summary]
        Makes a dictionary from year values and transformation values.
        Returns:
            [dict]: [dict of tvals for years]
        """
        dates = ["2016","2017","2018","2019","2020"]
        
        return dict(zip(dates, self.tvaluelist))