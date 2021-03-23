from unittest.case import skip
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from . import vars
from random import randint
import os
import csv
import ftplib



class Csv(models.Model):
    file = models.FileField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File id: {self.id}'


class Simple(models.Model):

    azienda = models.CharField(max_length=18)
    email = models.EmailField(max_length=18)
    telefono = PhoneNumberField()
    importunato = models.BooleanField(default=False)

    def importFromCsv(self, csv_file_path):
        
        raw2=open(csv_file_path, mode='r')
        with raw2 as raw_csv:
            dict_csv = csv.DictReader(raw_csv, delimiter='|')
            only_old_info = True
            
            for row in dict_csv:
                try:
                    obj, created = self.objects.get_or_create(email = row['EMAIL'])
                    obj.azienda = row['AZIENDA']
                    obj.email = row['EMAIL']
                    obj.telefono = row['TELEFONO']
                    obj.importunato = row['IMPORTUNATO']
                    obj.save()
                except Exception as e:
                    print(e)
                    os.remove(csv_file_path)
                    raise
                if created:
                    only_old_info = False
        raw2.close()

        if only_old_info:
            os.remove(csv_file_path)

        return 0


class RemoteSimple(models.Model):
    nome = models.CharField(max_length=18)
    caricato = models.IntegerField()

    def sync(self):
        ftp_s=vars.FTP_SERVER
        ftp_u=vars.FTP_USER
        ftp_p=vars.FTP_PASSWD
        ftp = ftplib.FTP(ftp_s)

        #login and retrieve files+info
        try:
            ftp.login(user=ftp_u, passwd=ftp_p)
            gen_obj = ftp.mlsd()
            
        except Exception as e:
            print(e)
            raise

        #for each file check if it's new and in that case save it an pass it to the local csv reader method
        for each in gen_obj:
            gen_name = each[0]
            gen_dict = each[1]
            
            if str(gen_name).startswith('simple') and str(gen_name).endswith('.csv'):
                obj, created = self.objects.get_or_create(
                    nome = gen_name, 
                    caricato = gen_dict['modify'],
                )
            
                if created:
                    local_filename = 'simple' + '_' + str(randint(100000000,999999999)) + '.csv'
                    local_filepath = 'media/' + local_filename

                    with open(local_filepath, 'wb+') as local_file:
                        try:
                            file = ftp.retrbinary('RETR ' + gen_name, local_file.write)
                        except Exception as e:
                            print(e)
                            raise
                    try:
                        Simple.importFromCsv(Simple, local_filepath)

                    except Exception as e:
                        print(e)
                        obj.delete()
                        raise
                            
        ftp.quit()
        return 0