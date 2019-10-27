import os
import json
import pandas as pd
import numpy as np
import scipy

import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-whitegrid')

from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore")





# ============================= EXTRACT DATA FROM CSV =========================
def get_csv(filepath):   
    """
    Function which extracts data from the train.csv and test.csv file. 
    Input is a path to the file (string type)
    """
    # read .csv file
    DF = pd.read_csv(os.getcwd() + filepath)
    
    return DF


# ============================= SHOW DATA STATISTICS =============================
def show_df_stats(df):
    """
    Present DataFrame basic statistics
    Input is a DataFrame object
    """
    stats = df.select_dtypes(['float64', 'int']).describe()
    stats = stats.transpose()
    stats = stats[['count','std','min','25%','50%','75%','max','mean']]
    return stats



# ============================= SHOW DATA SUMMARY =============================
def show_df_summary(df):
    """
    Explore DataFrame getting basic information.
    Input is a DataFrame object.
    """
    summary = pd.DataFrame(df.dtypes, columns=['Dtype'])
    summary['Nulls'] = pd.DataFrame(df.isnull().any())
    summary['Sum_of_nulls'] = pd.DataFrame(df.isnull().sum())
    summary['Per_of_nulls'] = round((df.apply(pd.isnull).mean()*100),2)
    summary["Dtype"] = summary.Dtype.astype(str)
    
    uniq_num = []
    uniq_val = []
    for x in list(df.columns.values):
        uniq_num.append(len(set(list(df[x].unique()))))
        column_values = df[x].unique()
        uniq_val.append(list(column_values)[:9])
    summary["Num_Unique_values"] = uniq_num
    summary["Unique_val_example"] = uniq_val
    
    return pd.DataFrame(summary)



# ============================ PLOT NUMERICAL VARIABLE ===========================
def plot_num_variable(df, variable):
    """
    Get three plots: histogram, density plot and box plot of the one variable.
    Input is DataFrame and the variable / column name (string type)
    """
    
    figsize=(25,6)
    plt.figure(figsize=figsize)
    sns.set(font_scale=1.1)
    color = '#eb6c6a'

    # --------------- HISTOGRAM ---------------
    plt.subplot(1,3,1)
    #plt.figure(figsize=figsize)
    title = f"Histogram ({variable})"
    xlabel = variable
    ylabel = ''
    sns.distplot(df[variable],
                 kde = False, 
                 bins = 30, 
                 color = color).set(title = title, 
                                        xlabel = xlabel, 
                                        ylabel = ylabel)
    #plt.show()

    # --------------- DENSITY ---------------
    plt.subplot(1,3,2)
    #plt.figure(figsize=figsize)
    title = f"Density plot ({variable})"
    xlabel = xlabel
    ylabel = ylabel
    sns.kdeplot(df[variable], 
                shade = True, 
                color = color).set(title = title,
                                   xlabel = xlabel,
                                   ylabel = ylabel)
    #plt.show()

    # --------------- BOXPLOT ---------------
    plt.subplot(1,3,3)
    #plt.figure(figsize=figsize)
    title = f"Boxplot ({variable})"
    xlabel = xlabel
    ylabel = ylabel
    sns.boxplot(df[variable], 
                color = color).set(title = title, 
                                   xlabel = xlabel,
                                   ylabel = ylabel)
    plt.show()
    
    
    
# ========================== PLOT CATEGORICAL VARIABLE ===========================
def plot_cat_variable(df, variable):
    """
    Get Frequency graph for the categorical variable
    Input is DataFrame and the variable / column name (string type)
    """
    
    plt.figure(figsize=(10,5))
    title = f"Frequency graph ({variable})"
    xlabel = variable
    ylabel = 'normalized count [%]'    
    sns.countplot(df[variable], 
                  palette = ['#eb6c6a', '#f0918f', '#f2a3a2', '#f5b5b4', '#f7c8c7'], 
                  order = df[variable].value_counts().index).set(title = title,
                                                                 xlabel = xlabel,
                                                                 ylabel = ylabel)
    plt.xticks(rotation=45)
    plt.show()
    
    
    
# ============================= HYPOTHESIS TESTING =============================
def check_hypothesis(df, column, alpha=0.05):
    """
    Test for the normal distribution
    We assume Significance Level alfa = 0.05.
    Input is a DataFrame object and one variable
    """
    if(scipy.stats.normaltest(df[column])[1] < 0.05):
        print('We reject zero hypothesis so we accept the alternative hypothesis: variable does not come from the normal distribution')
    else:
        print('We accept zero hypothesis. Variable come from normal distribution')
        

        
# ============================= NUMERICAL CORRELATION ==========================
def plot_num_correlation(df, columns):
    
    plt.figure(figsize=(15,5))
    title = "Heatmap Spearman's rank correlation coefficient"

    corr_num = pd.DataFrame(scipy.stats.spearmanr(df[columns])[0],
                            columns = df[columns].columns,
                            index = df[columns].columns)

    sns.set(font_scale=1.2)
    sns.heatmap(corr_num.abs(), cmap="Reds", linewidths=.5).set(title=title)
    plt.yticks(rotation=0)
    plt.xticks(rotation=30)
    plt.show()
        
        
        
# ============================= CATEGORICAL DEPENDECY ===========================
def plot_cat_dependency(df, columns):
    def CramersV(tab):
        a = scipy.stats.chi2_contingency(tab)[0]/sum(tab.sum())
        b = min(tab.shape[0]-1, tab.shape[1]-1,)
        return(np.sqrt(a/b))

    def CalculateCrammersV(tab):
        ret = []
        for m in tab:
            row = []
            for n in tab:
                cross_tab = pd.crosstab(tab[m].values,tab[n].values)
                row.append(CramersV(cross_tab))
            ret.append(row)
        return pd.DataFrame(ret, columns=tab.columns, index=tab.columns)
    crammer = CalculateCrammersV(df.select_dtypes(include = ['object']))
    
    title = "Heatmap-a V-Crammer dependency coefficient"
    plt.figure(figsize=(15,6))
    sns.set(font_scale=1.2)
    sns.heatmap(crammer, cmap="Reds", linewidths=.5).set(title=title)
    plt.yticks(rotation=0)
    plt.xticks(rotation=30)
    plt.show()


    
# ========================== CONVERT DATE TO NUMBER ===============================
def date_to_number(df, column_list):
    """
    Function which converts date to number. Function takes as zero min date
    """
    
    # get min date
    min_date = 0
    for column in column_list:
        date = df[column].min()
        if min_date == 0:
            min_date = df[column].min()
        elif date < min_date:
            min_date = df[column].min()
        else:
            pass

    # convert dates to numbers
    for column in column_list:
        print('column')
        date_column = []
        for i in range(len(df)):
            date = df.loc[i, column]
            date_column.append((date - min_date).days)
            if i%1000 == 0:
                print(i)
        df[f"num_{column}"] = date_column

    return df


# ============================== MODIFY OUTLIERS ====================================
def modify_outliers(DF, columns):
    for column_name in columns:
        DF.loc[DF[column_name] <= DF[column_name].quantile(0.05), column_name] = DF[column_name].quantile(0.05)
        DF.loc[DF[column_name] >= DF[column_name].quantile(0.95), column_name] = DF[column_name].quantile(0.95)
    return DF
    

# ========================= SCALE NUMERICAL VALUES ==================================
def scale_num_variables(DF, columns):
    scaler = StandardScaler(with_mean=True, with_std=True)
    for column_name in columns:
        column_modified = scaler.fit_transform(DF[column_name].values.reshape(-1, 1))
        DF.loc[:, column_name] = pd.Series(column_modified[:, 0])
    return DF