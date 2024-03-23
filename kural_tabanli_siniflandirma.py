
#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
from io import StringIO
df = pd.read_csv("persona.csv")
df.info()
df.head()

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
source_counts = df['SOURCE'].value_counts()
source_counts

# Soru 3: Kaç unique PRICE vardır?
unique_prices_count = df['PRICE'].nunique()
unique_prices_count

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
sales_per_price = df['PRICE'].value_counts()
sales_per_price

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
sales_per_country = df['COUNTRY'].value_counts()
sales_per_country

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
total_revenue_per_country = df.groupby('COUNTRY')['PRICE'].sum()
total_revenue_per_country

# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?
sales_per_source = df['SOURCE'].value_counts()
sales_per_source

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
average_price_per_country = df.groupby('COUNTRY')['PRICE'].mean()
average_price_per_country = df.groupby('COUNTRY')['PRICE'].mean()

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
average_price_per_source = df.groupby('SOURCE')['PRICE'].mean()

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
average_price_per_country_source = df.groupby(['COUNTRY', 'SOURCE'])['PRICE'].mean()
average_price_per_country_source

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
average_earnings = df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE'])['PRICE'].mean().reset_index()
average_earnings

#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.
agg_df = average_earnings.sort_values('PRICE', ascending=False).reset_index(drop=True)
agg_df


#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()
# agg_df.reset_index(inplace=True)
agg_df_index = agg_df.reset_index(inplace=True)
agg_df

#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'
age_bins = [0, 18, 23, 30, 40, 70]
age_labels = ['0_18', '19_23', '24_30', '31_40', '41_70']
agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], bins=age_bins, labels=age_labels, right=False)



#############################################
# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# Dikkat!
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.
agg_df['customers_level_based'] = agg_df.apply(lambda row: f"{row['COUNTRY'].upper()}_{row['SOURCE'].upper()}_{row['SEX'].upper()}_{row['AGE_CAT']}", axis=1)
level_based_avg_price = agg_df.groupby('customers_level_based')['PRICE'].mean().reset_index()
level_based_avg_price.head()


#############################################
# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
# PRICE'a göre segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz,
# segmentleri betimleyiniz,
quantiles = level_based_avg_price['PRICE'].quantile([0.33, 0.66]).to_list()
def segment_assigner(price):
    if price <= quantiles[0]:
        return 'C'
    elif price <= quantiles[1]:
        return 'B'
    else:
        return 'A'
level_based_avg_price['SEGMENT'] = level_based_avg_price['PRICE'].apply(segment_assigner)


#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
turkish_woman_category = "TUR_ANDROID_FEMALE_31_40"
french_woman_category = "FRA_IOS_FEMALE_31_40"
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
expected_revenue_turkish_woman = level_based_avg_price[level_based_avg_price['customers_level_based'] == turkish_woman_category]
expected_revenue_turkish_woman

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
expected_revenue_french_woman = level_based_avg_price[level_based_avg_price['customers_level_based'] == french_woman_category]
expected_revenue_french_woman
