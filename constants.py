import os
raw_data_url = r'C:\Users\jupol\Desktop\TensorTut\covid\legacyCovidMexico'
file_names = [file for file in os.listdir(raw_data_url) if file.endswith('MEXICO.csv')]
data_base_url = r'C:\Users\jupol\Desktop\TensorTut\covid\CovidAnimations\database'
data_files = os.listdir(data_base_url)



patients_codes = {
        'origin': {
            1: 'viral respiratory disease monitor unit - USMER',
            2: 'outside USMER',
            99: 'no specified'
        },
        'sector':{
            1 : 'red cross',
            2 : 'DIF',
            3 : 'state',
            4 : 'IMSS',
            5 : 'IMSS-BIENESTAR',
            6 : 'ISSSTE',
            7 : 'county',
            8 : 'PEMEX',
            9 : 'Private',
            10 : 'SEDENA',
            11 : 'SEMAR',
            12 : 'SSA',
            13 : 'University',
            99 : 'no specified'
        },
        'sex': {
            1: 'women',
            2: 'man',
            99: 'no specified'
        },
        'patient_type': {
            1: 'outpatient',
            2: 'hospitalized',
            99: 'no specified'
        },
        'is_mexican': {
            1: 'mexican',
            2: 'alien',
            99: 'no specified'
        },
        'result': {
            1: 'Positive for SARS-CoV-2',
            2: 'Negative for SARS-CoV-2',
            3: 'Result Pending'
        },
        'states':{
            1:  'AGUASCALIENTES',
            2:  'BAJA CALIFORNIA',
            3:  'BAJA CALIFORNIA SUR',
            4:  'CAMPECHE',
            5:  'COAHUILA',
            6:  'COLIMA',
            7:  'CHIAPAS',
            8:  'CHIHUAHUA',
            9:  'DISTRITO FEDERAL',
            10: 'DURANGO',
            11: 'GUANAJUATO',
            12: 'GUERRERO',
            13: 'HIDALGO',
            14: 'JALISCO',
            15: 'MEXICO',
            16: 'MICHOACAN',
            17: 'MORELOS',
            18: 'NAYARIT',
            19: 'NUEVO LEON',
            20: 'OAXACA',
            21: 'PUEBLA',
            22: 'QUERETARO',
            23: 'QUINTANA ROO',
            24: 'SAN LUIS POTOSI',
            25: 'SINALOA',
            26: 'SONORA',
            27: 'TABASCO',
            28: 'TAMAULIPAS',
            29: 'TLAXCALA',
            30: 'VERACRUZ',
            31: 'YUCATAN',
            32: 'ZACATECAS',
            36: 'Nacional',
            97: 'not apply',
            98: 'unknown',
            99: 'not specified',

        },
        'boolean':{
            1: 'yes',
            2: 'no',
            97: 'not apply',
            98: 'unknown',
            99: 'no specified'
        }
    }
inverse_dict_for_name_states = {patients_codes['states'][i]: i for i in patients_codes['states'].keys()}
inverse_dict_for_sector_states = {patients_codes['sector'][i]: i for i in patients_codes['sector'].keys()}
cdns_states = ['AGUASCALIENTES',
                'BAJA CALIFORNIA',
                'BAJA CALIFORNIA SUR',
                'CAMPECHE',
                'CHIAPAS',
                'CHIHUAHUA',
                'DISTRITO FEDERAL',
                'COAHUILA',
                'COLIMA',
                'DURANGO',
                'GUANAJUATO',
                'GUERRERO',
                'HIDALGO',
                'JALISCO',
                'MEXICO',
                'MICHOACAN',
                'MORELOS',
                'NAYARIT',
                'NUEVO LEON',
                'OAXACA',
                'PUEBLA',
                'QUERETARO',
                'QUINTANA ROO',
                'SAN LUIS POTOSI',
                'SINALOA',
                'SONORA',
                'TABASCO',
                'TAMAULIPAS',
                'TLAXCALA',
                'VERACRUZ',
                'YUCATAN',
                'ZACATECAS',
                'Nacional']

