import ftplib
import os
import csv
from . import settings
from .models import Cliente




def importCsv(origin_list, destination_obj):
    
    for origin in origin_list:
        with open(origin, mode='r') as raw_csv:
            dict_csv = csv.DictReader(raw_csv, delimiter='|')
            only_old_info = True

            for row in dict_csv:
                try:
                    obj, created = destination_obj.objects.get_or_create(email = row['EMAIL'])
                    obj.azienda = row['AZIENDA']
                    obj.email = row['EMAIL']
                    obj.telefono = row['TELEFONO']
                    obj.importunato = row['IMPORTUNATO']
                    obj.save()
                except Exception as e:
                    print(e)
                    os.remove(origin)
                    raise

            if created:
                only_old_info = False

        if only_old_info:
            os.remove(origin)

    return 0




def ftpPull():
    pulled_path_list = []

    ftp = ftplib.FTP(settings.FTP_SERVER)

    ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWD)
    gen_obj = ftp.mlsd()

    for generator in gen_obj:
        gen_name = generator[0]
        gen_dict = generator[1]

        if str(gen_name).startswith('table') and str(gen_name).endswith('.csv'):
            obj, created = self.objects.get_or_create(
                nome = gen_name,
                caricato = gen_dict['modify'],
            )

            if created:
                local_filename = 'table' + '_' + str(randint(100000000,999999999)) + '.csv'
                local_filepath = 'media/' + local_filename
                pulled_path_list.append(local_filepath) 

                with open(local_filepath, 'wb+') as local_file:
                    file = ftp.retrbinary('RETR ' + gen_name, local_file.write)
    
    ftp.quit()
    return pulled_path_list



def localImport(origin_list):
    destination_obj = Cliente
    importCsv(origin_list, destination_obj)



def remoteImport():
    destination_obj = Cliente
    origin_list = ftpPull()
    importCsv(origin_list, destination_obj)


