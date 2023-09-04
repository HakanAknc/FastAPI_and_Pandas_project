import pandas as pd           

def excel_to_csv(excel_file, csv_file):      # bu fonksiyon verilen bir Excel dosyasını okuyacak ve bir CSV dosyasına dönüştürecek.
        try:
                if len(csv_file) < 3:
                        raise Exception('{name} dosyasi adi hatalidir'.format(name=csv_file))
                # Excel dosyasını pandas kütüphanesi ile okuma
                df = pd.read_excel(excel_file + '.xlsx')
 
                # DataFrame'i CSV dosyasına yazdık
                df.to_csv(csv_file + '.csv', index=False)

                return {'status': True, 'desc' : 'CSV file is created'}
        except Exception as error:
                return {'status': False, 'desc': str(error)}