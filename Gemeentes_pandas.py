import pandas as pd

#Lezen juiste CSV met separator ";" (met Python engine omdat het anders mislukt) en komma als decimal separator.
Gem_df = pd.read_csv('Data_gemeentes.csv', sep=';', engine='python', decimal=',')

#Unpivot 'Jaar' voor 'Netto gemeenteschuld per inwoner'.
Gem_df_unpivot_1 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Netto gemeenteschuld per inwoner|2015', 'Netto gemeenteschuld per inwoner|2016', 'Netto gemeenteschuld per inwoner|2017'], 
    var_name='Jaar', value_name='Netto gemeenteschuld per inwoner')
Gem_df_unpivot_1_correct = Gem_df_unpivot_1
Gem_df_unpivot_1_correct['Jaar'] = Gem_df_unpivot_1['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Overlast zwervers'.
Gem_df_unpivot_2 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Overlast zwervers|2015', 'Overlast zwervers|2016', 'Overlast zwervers|2017'], 
    var_name='Jaar', value_name='Overlast zwervers')
Gem_df_unpivot_2_correct = Gem_df_unpivot_2
Gem_df_unpivot_2_correct['Jaar'] = Gem_df_unpivot_2['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Banen'.
Gem_df_unpivot_3 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Banen|2015', 'Banen|2016', 'Banen|2017'], 
    var_name='Jaar', value_name='Banen')
Gem_df_unpivot_3_correct = Gem_df_unpivot_3
Gem_df_unpivot_3_correct['Jaar'] = Gem_df_unpivot_3['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Vestigingen'.
Gem_df_unpivot_4 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Vestigingen|2015', 'Vestigingen|2016', 'Vestigingen|2017'], 
    var_name='Jaar', value_name='Vestigingen')
Gem_df_unpivot_4_correct = Gem_df_unpivot_4
Gem_df_unpivot_4_correct['Jaar'] = Gem_df_unpivot_4['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Faillissementen van bedrijven en instellingen inclusief eenmanszaken'.
Gem_df_unpivot_5 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Faillissementen van bedrijven en instellingen inclusief eenmanszaken|2015', 'Faillissementen van bedrijven en instellingen inclusief eenmanszaken|2016', 'Faillissementen van bedrijven en instellingen inclusief eenmanszaken|2017'], 
    var_name='Jaar', value_name='Faillissementen van bedrijven en instellingen inclusief eenmanszaken')
Gem_df_unpivot_5_correct = Gem_df_unpivot_5
Gem_df_unpivot_5_correct['Jaar'] = Gem_df_unpivot_5['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Vestigingen Landbouw'.
Gem_df_unpivot_6 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Vestigingen Landbouw|2015', 'Vestigingen Landbouw|2016', 'Vestigingen Landbouw|2017'], 
    var_name='Jaar', value_name='Vestigingen Landbouw')
Gem_df_unpivot_6_correct = Gem_df_unpivot_6
Gem_df_unpivot_6_correct['Jaar'] = Gem_df_unpivot_6['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Banen Vrouwen'.
Gem_df_unpivot_7 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Banen Vrouwen|2015', 'Banen Vrouwen|2016', 'Banen Vrouwen|2017'], 
    var_name='Jaar', value_name='Banen Vrouwen')
Gem_df_unpivot_7_correct = Gem_df_unpivot_7
Gem_df_unpivot_7_correct['Jaar'] = Gem_df_unpivot_7['Jaar'].str[-4:]

#Unpivot 'Jaar' voor 'Personen met bijstand en bijstand gerelateerde uitkering'.
Gem_df_unpivot_8 = pd.melt(
    Gem_df, id_vars='Gemeente', value_vars=['Personen met bijstand en bijstand gerelateerde uitkering|2015', 'Personen met bijstand en bijstand gerelateerde uitkering|2016', 'Personen met bijstand en bijstand gerelateerde uitkering|2017'], 
    var_name='Jaar', value_name='Personen met bijstand en bijstand gerelateerde uitkering')
Gem_df_unpivot_8_correct = Gem_df_unpivot_8
Gem_df_unpivot_8_correct['Jaar'] = Gem_df_unpivot_8['Jaar'].str[-4:]

#Join de unpivotted data met 'Jaar' als column
Gem_df_unpivot_all = Gem_df_unpivot_1_correct.merge(
    Gem_df_unpivot_2_correct.merge(
        Gem_df_unpivot_3_correct.merge(
            Gem_df_unpivot_4_correct.merge(
                Gem_df_unpivot_5_correct.merge(
                    Gem_df_unpivot_6_correct.merge(
                        Gem_df_unpivot_7_correct.merge(
                            Gem_df_unpivot_8_correct, on=['Gemeente', 'Jaar'])
                        , on=['Gemeente', 'Jaar'])
                        , on=['Gemeente', 'Jaar'])
                    , on=['Gemeente', 'Jaar'])
                , on=['Gemeente', 'Jaar'])
        , on=['Gemeente', 'Jaar'])
    , on=['Gemeente', 'Jaar'])

#Verander de column namen
Gem_df_unpivot_all.columns = ['Gemeente', 'Jaar', 'Gemeenteschuld', 'Overlast zwervers', 'Banen', 'Vestigingen', 'Faillisementen', '%Landbouw van vestigingen', '%Vrouw van banen', 'Aantal bijstandsuitkeringen']

#Exporteer de getransformeerde data naar CSV
Gem_df_unpivot_all.to_csv('Data_gemeentes_getransformeerd.csv', sep=";", decimal=",")