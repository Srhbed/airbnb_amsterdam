from django.shortcuts import render
import pandas as pd





def home_view(request):
    ##qs1
    
    df=pd.read_csv('/home/apprenant/Documents/django_rbnb/airbnb_app/amesterdam/listings.csv')

    question1=df.groupby('neighbourhood_cleansed').agg({"host_id": 'count', 'number_of_reviews' : 'sum'})


    # render dataframe as html
    html = question1.to_html()
    
    ##qs2
    mean_host_acceptance = df["host_acceptance_rate"].str.rstrip('%').astype(float).mean()
    
    mean_host_response = df["host_response_rate"].str.rstrip('%').astype(float).mean()
    ##qs3
    phone_verification = (df["host_verifications"].apply(lambda x: 1 if "phone" in x else 0).sum() / df.host_verifications.count()) * 100
    email_verification = (df["host_verifications"].apply(lambda x: 1 if "email" in x else 0).sum() / df.host_verifications.count()) * 100
    email_pro_verification = (df["host_verifications"].apply(lambda x: 1 if "work_email" in x else 0).sum() / df.host_verifications.count()) * 100
    ##qs4
    amenities = df[['room_type', 'amenities']]
    amenities['nb_amenities'] = amenities["amenities"].str.split(",").apply(len)
    nbr_amn=amenities.groupby('room_type')[['nb_amenities']].agg(["mean","std"])
    
    amt=nbr_amn.to_html()
    ##qs5
    df['price'] = df['price'].str.replace('$','').str.replace(',','').astype(float)
    df['price']
    df_median = df[df['price'] > 1][['room_type','price']].groupby('room_type').median()
    df_describe = df.groupby('room_type')[['room_type','price']].describe()
    df_inner = pd.merge(df_median, df_describe, on = 'room_type', how = 'inner')
    qst5=df_inner.to_html()
    ##qst6
    
 
        ##qst7
    df['length_description']= df["description"].str.len()
    df[['length_description','number_of_reviews']]
    cor=df[['length_description','number_of_reviews']].corr()
    qst7=cor.to_html()
    ##qst8
    reviews = pd.read_csv('/home/apprenant/Documents/django_rbnb/airbnb_app/amesterdam/reviews.csv')
    df_reviews = pd.merge(reviews[['listing_id', 'reviewer_name']], df[['id', 'host_name']], how = 'left', left_on ='listing_id', right_on ='id')
    
    faux_com=((df_reviews['host_name'] == df_reviews['reviewer_name']).sum() / len(df_reviews)) * 100






 
    
    context={
        'dt_html':html,
        'acceptation':mean_host_acceptance,
        'reponse':mean_host_response,
        'tel': phone_verification,
        'mail':email_verification,
        'pro':email_pro_verification ,
        'amenities':amt,
        'median':qst5,
        'correlation':qst7,
        'faux_com':faux_com,
        
        
    }
 
    
    
    return render(request ,'apps/rbnb_amsterdam.html',context=context)
def home_page(request):
    
    return render(request,'apps/home_page.html')
