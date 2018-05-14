import pandas as pd


def data_processing(data):
    services = []
    for i in data['Услуги']:
        i = i.strip()
        us = i.split(';')
        services.append(us)

    data['Услуги'] = services

    return data


def new_files():

    data_yur = pd.read_excel('yur_litsa.xlsx')
    data_fiz = pd.read_excel('Fiz_litsa.xlsx')

    data_fiz = data_processing(data_fiz)
    data_yur = data_processing(data_yur)

    # Created a new files
    writer1 = pd.ExcelWriter('fiz.xlsx')
    writer2 = pd.ExcelWriter('yur.xlsx')

    data_fiz.to_excel(writer1)
    data_yur.to_excel(writer2)
    writer1.save()
    writer2.save()


def choose_bank(data, services, security, price, support):
    rec_banks = []
    check_ser = False
    for index, row in data.iterrows():
        for ser in services:
            if ser in row['Услуги']:
                check_ser = True

        if check_ser is True:
            if row['Поддержка'] == support:
                if security == 'да':
                    if row['Безопасность'] == 'сильная':

                        if price <= row['Цена']:
                            rec_banks.append(row['Название банка'])

                else:
                    if price <= row['Цена']:
                        rec_banks.append(row['Название банка'])
    return rec_banks


def main():

    data_fiz = pd.read_excel('fiz.xlsx')
    data_yur = pd.read_excel('yur.xlsx')

    person = input('Who are you?: ')

    services = input('Which services do you prefer?: ').split()
    security = input('Does security important?: ').lower()
    price = int(input('How much would you like to spend on maintenance?: '))
    support = input('Do you need a 24/7 supporting?').lower()

    if person == 'физическое лицо':

        banks = choose_bank(data_fiz, services, security, price, support)

    else:

        banks = choose_bank(data_yur, services, security, price, support)

    print('We are reccomending:', ', '.join(banks))


if __name__ == '__main__':
    main()









