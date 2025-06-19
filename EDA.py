
import pandas as pd
import plotly.express as px 
import numpy as np
import streamlit as st

st.set_page_config(layout= 'wide', page_title= 'Productivity', page_icon= '👩🏽‍💻')
st.image('https://empmonitor.com/blog/wp-content/uploads/2024/10/8-ways-to-improve-employee-productivity-in-the-workplace.webp')
st.markdown("""<h1 style="color:orange;text-align:center;">  Employee Performance & Productivity Data Analysis Dashboard 📊</h1>""",
             unsafe_allow_html= True)


df = pd.read_csv('cleaned_data.csv', index_col= 0)
st.dataframe(df)

tab_info, tab_univariate, tab_bivariate, tab_multivariate, tab_advanced = st.tabs( ["📄 Info", "📊 Univariate Analysis", "📈 Bivariate Analysis", "📉 Multivariate Analysis", "🧠 Advanced Insights"])

with tab_info :

    st.markdown("""<h1 style="color:yellow;text-align:center;">  Some info to describe numrical data </h1>""", unsafe_allow_html= True)
    st.dataframe(df.describe().round(2))
    st.markdown("""<h1 style="color:yellow;text-align:center;">  Some info to describe catgorical data </h1>""", unsafe_allow_html= True)
    st.dataframe(df.describe(include= 'object').round(2))
    df_corr = df.corr(numeric_only= True)
    st.markdown("""<h1 style="color:yellow;text-align:center;">  Some info to describe relation between  numrical columns </h1>""", unsafe_allow_html= True)
    corr_fig = px.imshow(df_corr, text_auto= True, height= 800, width= 1200)
    st.plotly_chart(corr_fig)

    st.markdown("""<h1 style="color:yellow;text-align:center;">  Some fig to describe relation between  numrical columns </h1>""", unsafe_allow_html= True)
    num_col = df.select_dtypes(include= 'number').columns 
    for col in num_col:
        his_fig = px.histogram(data_frame= df , x = col, title = f'{col}')
        st.plotly_chart(his_fig)

with tab_univariate :

    st.markdown("""<h1 style="color:orange;text-align:center;">  Univariate Analysis </h1>""", unsafe_allow_html= True)
    num_col = df.select_dtypes(include= 'number').columns 
    cat_col = df.select_dtypes(include= 'object').columns 

    tab_1, tab_2 = st.tabs(['Numerical Univariate Analysis', 'Categorical Univariate Analysis'])

    with tab_1:
        col = st.selectbox('Select Column', num_col)
        
        chart = st.selectbox('Select Chart', ['Histogram', 'Box'])

        if chart == 'Histogram':
            st.plotly_chart(px.histogram(data_frame= df, x= col, color= col, title= col))

        elif chart == 'Box':
            st.plotly_chart(px.box(data_frame= df, x= col, title= col))

    with tab_2:
        col = st.selectbox('Select Column', cat_col)
        
        chart = st.selectbox('Select Chart', ['Pie', 'Histogram'])

        if chart == 'Histogram':
            st.plotly_chart(px.histogram(data_frame= df, x= col, color= col, title= col))

        elif chart == 'Pie':
            st.plotly_chart(px.pie(data_frame= df, names= col, title= col, hole = 0.5))

with tab_bivariate :

    st.markdown("""<h1 style="color:orange;text-align:center;">  Bivariate Analysis </h1>""", unsafe_allow_html= True)
    col_1, col_2 = st.columns(2, vertical_alignment= 'center')

    groupby_col = col_1.selectbox('Select groupby Column', ['Department', 'Gender', 'Job_Title', 'Education_Level',
       'salary_categorical','Age', 'Performance_Score', 'Team_Size', 'Promotions','Salary_Percentile',
       'Attrition_Risk_Score'])

    filterd_col = col_1.selectbox('by Column', ['Resigned', 'salary_categorical', 'Salary_Percentile', 'Attrition_Risk_Score', 'Department',
     'Gender', 'Age', 'Job_Title', 'Years_At_Company', 'Education_Level', 'Performance_Score', 'Monthly_Salary',
     'Work_Hours_Per_Week', 'Projects_Handled', 'Overtime_Hours', 'Sick_Days', 'Remote_Work_Frequency', 'Team_Size', 'Training_Hours',
    'Promotions', 'Employee_Satisfaction_Score'])

    agg_options = {'Sum': np.sum,'Count': 'count', 'Mean': np.mean}

    agg_choice = col_1.selectbox('Select aggregation function', options=list(agg_options.keys()))

    agg_func = agg_options[agg_choice]

    filtered_data = df.groupby(groupby_col)[filterd_col].agg(agg_func).sort_values(ascending=False).reset_index()

    available_columns = filtered_data.columns.tolist()

    chart = col_1.selectbox('Select Chart', ['bar', 'scatter', 'line', 'Box', 'strip', 'vision'])
    
    x_axis = col_1.selectbox('Select Column x', available_columns, index=0)
    
    y_axis = col_1.selectbox('Select Column y', available_columns, index=1 if len(available_columns) > 1 else 0)


    if chart == 'scatter':
        col_2.plotly_chart(px.scatter(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}"))

    elif chart == 'Box':
        col_2.plotly_chart(px.box(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}"))

    elif chart == 'line':
        col_2.plotly_chart(px.line(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}"))

    elif chart == 'bar':
        col_2.plotly_chart(px.bar(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}", text_auto= True))

    elif chart == 'vilion':
        col_2.plotly_chart(px.vilion(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}"))
    
    elif chart == 'strip':
        col_2.plotly_chart(px.strip(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}"))

with tab_multivariate:

    st.markdown("""<h1 style="color:orange;text-align:center;">Multivariate Analysis</h1>""", unsafe_allow_html=True)

    groupby_col = st.multiselect('Select groupby Column',
        ['Department', 'Gender', 'Job_Title', 'Education_Level', 'salary_categorical', 'Age',
         'Performance_Score', 'Team_Size', 'Promotions', 'Salary_Percentile', 'Attrition_Risk_Score'],
        key='groupby_col_multiselect')

    filterd_col = st.selectbox('by Column',
        ['Resigned', 'salary_categorical', 'Salary_Percentile', 'Attrition_Risk_Score', 'Department',
         'Gender', 'Age', 'Job_Title', 'Years_At_Company', 'Education_Level', 'Performance_Score',
         'Monthly_Salary', 'Work_Hours_Per_Week', 'Projects_Handled', 'Overtime_Hours', 'Sick_Days',
         'Remote_Work_Frequency', 'Team_Size', 'Training_Hours', 'Promotions', 'Employee_Satisfaction_Score'],
        key='filterd_col_selectbox')

    agg_options = {'Sum': np.sum, 'Count': 'count', 'Mean': np.mean}

    agg_choice = st.selectbox('Select aggregation function', options=list(agg_options.keys()), key='agg_choice_selectbox')

    agg_func = agg_options[agg_choice]

    if groupby_col: 
        filtered_data = df.groupby(groupby_col)[filterd_col].agg(agg_func).sort_values(ascending=False).reset_index()

        available_columns = filtered_data.columns.tolist()

        hue_col = st.selectbox('Color Grouping Column (Optional)', ['None'] + groupby_col, key="hue_col")
        
        color_opt = hue_col if hue_col != 'None' and hue_col in filtered_data.columns else None


        chart = st.selectbox('Select Chart',
            ['bar', 'scatter', 'line', 'Box', 'strip', 'vision'], key='chart_type_selectbox')

        x_axis = st.selectbox('Select Column x', available_columns,index=0, key='x_axis_selectbox')

        y_axis = st.selectbox('Select Column y', available_columns, index=1 if len(available_columns) > 1 else 0, key='y_axis_selectbox')

        if chart == 'scatter':
            st.plotly_chart(px.scatter(data_frame= filtered_data, x= x_axis, y = y_axis, color = color_opt, title= f"the {y_axis} with each {x_axis}", height = 800, width = 1200))

        elif chart == 'Box':
            st.plotly_chart(px.box(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}", height = 800, width = 1200))

        elif chart == 'line':
            st.plotly_chart(px.line(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}", height = 800, width = 1200))

        elif chart == 'bar':
            st.plotly_chart(px.bar(data_frame= filtered_data, x= x_axis, y = y_axis, color= color_opt, barmode= "group", text_auto= True, title= f"the {y_axis} with each {x_axis}", height = 800, width = 1200))

        elif chart == 'viloin':
            st.plotly_chart(px.viloin(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}", height = 800, width = 1200))
        
        elif chart == 'strip':
            st.plotly_chart(px.strip(data_frame= filtered_data, x= x_axis, y = y_axis, title= f"the {y_axis} with each {x_axis}", height = 800, width = 1200))
   
    else:
        st.warning("Please select at least one column to group by.")

with tab_advanced :

    st.markdown("""<h1 style="color:orange;text-align:center;">Advanced Analysis</h1>""", unsafe_allow_html=True)

    st.markdown("""<h2 style="color:yellow;text-align:center;">What is the most common category in gender?</h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.pie(data_frame= df, names= 'Gender', hole= 0.5))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Which department has the highest number of employees? </h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.pie(data_frame= df, names= 'Department', hole= 0.5))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Which education level is most represented among employees? </h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.pie(data_frame= df, names= 'Education_Level', hole= 0.5))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Which salary category most represented among employees?</h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.pie(data_frame= df, names= 'salary_categorical'))

    st.markdown("""<h2 style="color:yellow;text-align:center;">What is the ratio of employees who resigned to those who stayed?</h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.pie(data_frame= df, names= 'Resigned'))

    st.markdown("""<h2 style="color:yellow;text-align:center;">what the average of age most represented among employees? </h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.box(data_frame = df, x = 'Age'))

    st.markdown("""<h2 style="color:yellow;text-align:center;">What is the average salary per department? </h2>""", unsafe_allow_html=True)
    avg_salary_by_dep = df.groupby('Department')['Monthly_Salary'].mean().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame = avg_salary_by_dep, x = 'Department', y = 'Monthly_Salary', text_auto= True, color= 'Department',
        labels= {'Monthly_Salary':'avg_salary'}, height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;"> </h2>""", unsafe_allow_html=True)
    df1 = df.groupby('Department')['Performance_Score'].mean().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame = df1, x = 'Department', y = 'Performance_Score', text_auto= True, color= 'Department',
        labels= {'Performance_Score':'avg performance'}, height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">What is the average number of projects handled per job title? </h2>""", unsafe_allow_html=True)
    df2 = df.groupby('Job_Title')['Projects_Handled'].mean().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame = df2, x = 'Job_Title', y = 'Projects_Handled', text_auto= True, color= 'Job_Title',
        labels= {'Projects_Handled':'avg number of projects'}, height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Which team has the highest average overtime hours?</h2>""", unsafe_allow_html=True)
    df3 = df.groupby('Team_Size')['Overtime_Hours'].mean().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame = df3, x = 'Team_Size', y = 'Overtime_Hours', text_auto= True, color= 'Team_Size',
        labels= {'Overtime_Hours':'avg Overtime_Hours'}, height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">What is the resignation rate by department?</h2>""", unsafe_allow_html=True)
    df4 = df.groupby('Department')['Resigned'].sum().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame = df4, x = 'Department', y = 'Resigned', text_auto= True, color= 'Department',
     height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Which age group has the highest resignation rate?</h2>""", unsafe_allow_html=True)
    df5 = df.groupby('Age')['Resigned'].sum().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame = df5, x = 'Age', y = 'Resigned', text_auto= True, color= 'Resigned',
     height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Is there a correlation between salary percentile and resignation?</h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.box(data_frame = df, x = 'Salary_Percentile', y = 'Resigned', height= 600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Is there a correlation between salary percentile and Performance_Score?</h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.scatter(data_frame = df, x = 'Salary_Percentile', y = 'Performance_Score', height= 600, color= 'Resigned'))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Is there a correlation between Attrition_Risk_Score and Resigned?</h2>""", unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df , x = 'Attrition_Risk_Score', color= 'Resigned', barmode= 'group', width=1600))

    st.markdown("""<h2 style="color:yellow;text-align:center;">Is there a link between salary_categorical and Resigned by gender?</h2>""", unsafe_allow_html=True)
    new_df = df.groupby(['Gender', 'salary_categorical'])['Resigned'].sum().sort_values(ascending= False).reset_index()
    st.plotly_chart(px.bar(data_frame= new_df, x = 'salary_categorical', y = 'Resigned', color= 'Gender', barmode= "group"))

    st.markdown("""<h2 style="color:yellow;text-align:center;">what is the most department have resigned as salary?</h2>""", unsafe_allow_html=True)
    new_df1 = df.groupby(['Department', 'salary_categorical'])['Resigned'].sum().sort_values(ascending= False).reset_index()
    st.plotly_chart(px.bar(data_frame= new_df1, x = 'Department', y = 'Resigned', color= 'salary_categorical', barmode= 'group'))

    st.markdown("""<h2 style="color:yellow;text-align:center;">what is the Job_Title have resigned raito as salary category?</h2>""", unsafe_allow_html=True)
    new_df2 = df.groupby(['Job_Title', 'salary_categorical'])['Resigned'].sum().sort_values(ascending= False).reset_index()
    st.plotly_chart(px.bar(data_frame= new_df2, x = 'Job_Title', y = 'Resigned', color= 'salary_categorical', barmode= 'group'))

    st.markdown("""<h2 style="color:yellow;text-align:center;">How does training hours relate to performance score?</h2>""", unsafe_allow_html=True)
    new_df4 = df.groupby(['Department', 'Resigned'])['Overtime_Hours'].mean().sort_values(ascending= False).reset_index().round(2)
    st.plotly_chart(px.bar(data_frame= new_df4, x = 'Department', y = 'Overtime_Hours', color= 'Resigned', barmode= 'group', text_auto= True ))

    st.markdown("""<h1 style="color:orange;text-align:center;">  Summary of Key Insights </h1>""", unsafe_allow_html= True)
    st.text_area('', """
    1. The extracted features 'Salary Category' and 'Attrition Risk Score' were highly valuable in understanding the data.
    2. High attrition risk is strongly linked to low salary, high overtime, and low satisfaction.
    3. The 'Attrition_Risk_Score' column is positively correlated with the 'Resigned' column.
    4. Departments like Customer Support and Technical Support show high resignation rates, often due to lower salaries and higher workload.
    5. Engineering department shows zero resignations despite long working hours, suggesting high motivation or better benefits.
    6. 'Salary Percentile' was useful in identifying underpaid employees across job titles.
    7. Resignation rates varied significantly across different age and gender groups.
    8. Zero values in 'Training Hours' or 'Sick Days' might indicate underreporting or lack of employee engagement.
    9. The Legal department had high attrition despite high salary – showing that money alone doesn’t guarantee retention.
    10. Building a predictive model will help HR proactively detect and address employees at risk of resignation.
       It's end that the employees who most often resign aren't those with the lowest salaries or positions, but rather the opposite. 
   This makes us question and understand that the problem isn't simply salary, working hours, or promotion. These are contributing factors,
   and paying attention to them is extremely important. However, employees often need a more integrated environment that helps them 
   achieve their goals and aspirations. """, height=400 )

    st.markdown("""<h1 style="color:orange;text-align:center;"> Thank you for reaching here 😇 </h1>""",
             unsafe_allow_html= True)
