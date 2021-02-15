
from vendoasg.vendoasg import Vendo
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('setings.ini')

# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))

with open('Uwagi_do_operatora.xlsx','rb')as tabela_do_wgrania:
    df = pd.read_excel(tabela_do_wgrania)

with open('Nazwy_wd_tech.xls','rb') as tabela_nazw_wd:
    df_WD_technologii = pd.read_excel(tabela_nazw_wd)
    df_WD_technologii = df_WD_technologii.fillna('wolna')
    
# tworzenie dictionary z nazwami WD
wd_dict = dict()
for index, row in df_WD_technologii.iterrows():
    if row['Nazwa'] == 'wolna' or row['Zmienna'] == 'wolna':
        continue
    wd_dict[row['Nazwa']] = row['Zmienna']
lista_kolumn = list(df)
for index, row in df.iterrows():
    idTechnologii = row['ID']
    for nazwa_kolumny in lista_kolumn:
        try:
            nazwaWD = wd_dict[nazwa_kolumny]            
        except:
            continue
        wartoscWD = str(row[nazwa_kolumny])
        if wartoscWD == 'nan':
            continue
    
        wartoscWD = wartoscWD.replace(' ','\u00A0')
        
        print(wartoscWD)
        wd_query = vendoApi.getJson ('/json/reply/DB_UstawWartoscDowolna', {"Token":vendoApi.USER_TOKEN,"Model":{"ObiektTypDanych":"Technologia","ObiektID":idTechnologii,"Typ":"Tekst","Wartosci":wartoscWD,"Nazwa":"uv_konstr_rodzaj"}})
        wartosci = wd_query["Wynik"]
        try:
            print(wartosci)
            print(wd_query["ResponseStatus"])
        except:
            print(wartosci)