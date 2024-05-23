import flet 
import database_creator as dc
import qrcode as qr

def main(page:flet.Page):
    page.title = 'Название'
    page.theme_mode = 'Dark'
    #Таблички
    db = dc.Database('База')
    dc.Database.Table.create(db, 'Заявки', ['НомерЗаявки', 'ДатаЗаявки', 'Сотрудник', 'ДатаСдачи'], ['COUNTER', 'TEXT', 'INTEGER', 'TEXT'])
    dc.Database.Table.create(db, 'Сотрудники', ['НомерСотрудники', 'Квалификация', 'ФИО'], ['COUNTER', 'TEXT', 'TEXT'])
    dc.Database.Table.create(db, 'Оборудование', ['НомерОборудования', 'ДатаЗачисления', 'Фирма', 'Цена'], ['COUNTER', 'TEXT', 'TEXT', 'INTEGER'])
    #гр код
    img = qr.make('vk.com')
    img.save('QR.png')

    def get_columns(tablename):
        data = dc.Database.Info.getColumns(db, tablename)
        c_list = []
        for name in data:
            c_list.append(flet.DataColumn(flet.Text(name)))
        return c_list
    
    def get_rows(tablename):
        data = dc.Database.Table.get(db, tablename)
        r_list = []
        for row in data:
            c_list = []
            for cell in row:
                c_list.append(flet.DataCell(flet.Text(cell)))
            r_list.append(flet.DataRow(cells=c_list))
        return r_list
   
    def table(tablename):
        dt = flet.DataTable(
            columns=get_columns(tablename),
            rows=get_rows(tablename)
        )
        return dt
    
    #Для не просто просмотра
    #Для добавления данных в таблицу
    def add(tablename, *args):
        dc.Database.Table.write(db, tablename, *args)
        page.update()

    #Для кнопок но обновление через перезапуск
    #В общем это не надо если не нужны кнопки
    datazayavki = flet.TextField(hint_text='Дата заявки')
    sotrudnik = flet.TextField(hint_text= 'Сотрудник')
    datasdachi = flet.TextField(hint_text= 'Дата сдачи')
    
    kvalification = flet.TextField(hint_text= 'Квалификация')
    fio = flet.TextField(hint_text= '"ФИО" сотрудники')

    DataZach = flet.TextField(hint_text= 'Дата зачисления')
    Firma = flet.TextField(hint_text= 'Фирма')
    cena = flet.TextField(hint_text= 'Цена')

    page.add(
        flet.Column(
            horizontal_alignment='center',
            controls=[
                flet.Image('QR.png', width= 50, height= 50),
                flet.Tabs(
                    tabs=[
                        #В общем в нижнем комментарии написано как без кнопки сделать просто для просмотра
                        flet.Tab('Заявки', content=flet.Column(controls=[table('Заявки'), datazayavki, sotrudnik, datasdachi, 
                        flet.ElevatedButton('Добавить', on_click=lambda e: add('Заявки', datazayavki.value, sotrudnik.value, datasdachi.value))])),
                        flet.Tab('Сотрудники',content=flet.Column(controls=[table('Сотрудники'), kvalification, fio, 
                        flet.ElevatedButton('Добавить', on_click=lambda e: add('Сотрудники', kvalification.value, fio.value))])),
                        #flet.Tab('Сотрудники', content=table('Сотрудники')), простой вывод таблиц
                        #Не нужно писать def add(tablename, *args):
                        flet.Tab('Оборудование',content=flet.Column(controls=[table('Оборудование'), DataZach, Firma, cena, 
                        flet.ElevatedButton('Добавить', on_click=lambda e: add('Оборудование', DataZach.value, Firma.value, cena.value,))]))
                        ]
                    )
                ]
            )                  
        )   
  
flet.app(target=main)
#view=flet.AppView.WEB_BROWSER для отображения на странице