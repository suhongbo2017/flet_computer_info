from flet import *
from functools import partial 

import flet as ft
import mysql.connector

# CONECTION TO OB
mydb = mysql.connector.connect(
    host = '192.168.0.118',
    user = 'su',
    password = '123456',
    database = 'jhs',
    connect_timeout = 30,
)

cursor = mydb.cursor()


def main(page: Page):
    # page.width = 1800
    # page.height = 1000
    page.title ='电脑出入库录入'
    page.bgcolor = '#E6E6FA'
    page.scroll = 'auto'
    departxt = TextField(label='使用部门')
    codetxt = TextField(label='物料编码')
    midtxt = TextField(label='设备ID')
    remtxt = TextField(label='备注')

    # CREATE EDIT INPUT
    edit_departxt = TextField(label='部门')
    edit_codetxt = TextField(label='编码')
    edit_midtxt = TextField(label='设备ID')
    edit_remtxt = TextField(label='备注')
    edit_idtxt = Text()
    delete_id = Text()
    # 获取部门名称列表
    cursor.execute('select 名称,简称 from department_info')
    department_list = {name:simple_name for name,simple_name in cursor.fetchall()}
    departments = department_list.keys()
    
    
    # 下拉菜单列表
    depart_dropdown = Dropdown(
        label='使用部门',
        options=[dropdown.Option(d) for d in departments],
        # value= departments
    )
    def deletebtn(e):
        print('you selected id is ',delete_id.value)
        try:
            sql = 'DELETE FROM computer_info WHERE id = %s'
            val = (delete_id.value,)
            cursor.execute(sql,val)
            mydb.commit()
            delete_dialog.open = False
            page.update()
            mydt.rows.clear()
            load_data()

            # AND SHOW SNACBAR
            page.snack_bar = SnackBar(
                Text('数据删除成功',size= 30),
                bgcolor='red'
                )
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            print(e)
            print('error you code delete')
    # 删除确认页面
    def handle_close(e):
        page.close_dialog()
    
    # DELETE FUNCTION
    delete_dialog = AlertDialog(
        title= Text('确认删除'),
        content = Column([
            Text('是否确认删除该数据！！！'),
            Text('请谨慎操作！！！'),
            delete_id,
            Text(),
            ]),
        actions=[
            TextButton('确认',on_click= deletebtn       
                    ),            
            TextButton('再想想',on_click= handle_close              
                    )            
        ]
        )
    def delete_dia(e):
        delete_id.value = (e.control.data['id'])

        page.dialog = delete_dialog
        delete_dialog.open = True
        page.update()
        return delete_dialog
    def savedata(e):
        try:
            sql = 'UPDATE computer_info SET 部门 = %s , 编码 = %s ,设备id = %s, 备注 = %s WHERE id = %s'
            val = (edit_departxt.value,edit_codetxt.value,edit_midtxt.value,edit_remtxt.value,edit_idtxt.value)
            # print(sql,val)
            cursor.execute(sql,val)
            mydb.commit()
            print('you success edit data')
            dialog.open = False


            page.update()
            
            # CLEAR EDIT TEXTIFIELD
            edit_departxt.value = ''
            edit_codetxt.value = ''
            edit_midtxt.value = ''
            edit_remtxt.value = ''
            edit_idtxt.value = ''

            page.update()
            mydt.rows.clear()
            load_data()

            # AND SHOW SNACBAR
            page.snack_bar = SnackBar(
                Text('数据成功修改',size= 30),
                bgcolor='blue'
                )
            page.snack_bar.open = True
            page.update()
            
        except Exception as e:
            print(e)
            print('error you code edit')

    # CREATE DIALOG SHOW WHEN YOU CLICK EDIT BUTTON
    dialog = AlertDialog(
        title= Text('Edit data'),
        content = Column([
            edit_departxt,
            edit_codetxt,
            edit_midtxt,
            edit_remtxt

            
            ]),
        actions=[
            TextButton('save',
                       on_click= savedata
                       )            
        ]
        )
    # EDIT FUNCTION
    def editbtn(e):
        edit_departxt.value = e.control.data['部门']
        edit_codetxt.value = e.control.data['编码']
        edit_idtxt.value = e.control.data['id']
        edit_midtxt.value = e.control.data['设备id']
        edit_remtxt.value = e.control.data['备注']


        page.dialog = dialog
        dialog.open = True
        page.update()
        
    mydt = DataTable(
        bgcolor='#d6E6FB',
        border_radius = 10,
        width= 1000,
        
        
        
        
        columns = [
            DataColumn(Text('id')),
            DataColumn(Text('部门')),
            DataColumn(Text('编码')),
            DataColumn(Text('设备ID')),
            DataColumn(Text('时间')),
            DataColumn(Text('备注')),
            DataColumn(Text('删除      修改'))
        ]
    )
   
    
    def load_data():
        cursor.execute('select * from computer_info')
        result = cursor.fetchall()
        # print(result)
        # AND PUSH DATA TO DICT
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        # print(columns,rows)
        # LOOP AND PUSH
        # print(len(rows))
        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells= [
                        DataCell(Text(row['id'])),
                        DataCell(Text(row['部门'])),
                        DataCell(Text(str(row['编码']),selectable=True)),
                        DataCell(Text(row['设备id'])),
                        DataCell(Text(row['时间'].date())),
                        DataCell(Text(row['备注'],selectable = True)),
                        DataCell(
                            Row([
                                IconButton('delete',icon_color='red',
                                           data= row,
                                           on_click= delete_dia,disabled= False),
                                IconButton('create',icon_color='green',
                                           data= row,
                                           on_click= editbtn)
                            ],scroll=ScrollMode.AUTO)
                        )
                    ]
                )
            )
        page.update()
        # print(rows[-1]['id'])
        if rows:
            return rows[-1]['id']
        else:
            return 1
    # AND CALL FUNCTION WHEN YOU APP IS FIRST OPEN
    load_data()
    
   
    def addtodo(e):
        try:
            select_department = depart_dropdown.value
            simple_depart = department_list[select_department]
            midtxt.value = simple_depart + '-' + str(load_data() + 1)
            print(midtxt.value)
            sql = 'insert into computer_info (部门,编码,设备id,备注) values(%s,%s,%s,%s)'
            val = (select_department,codetxt.value,midtxt.value,remtxt.value)
            cursor.execute(sql,val)
            # print(sql,val)
            mydb.commit()
            
            print(cursor.rowcount,'YOU RECORD INSERT !!!')

            # AND CLEAR ROWS IN TABLE AND PUSH FROM DATABASE AGAIN

            mydt.rows.clear()
            load_data()

            # AND SHOW SNACBAR
            page.snack_bar = SnackBar(
                Text('数据成功添加',size= 30),
                bgcolor='green'
                )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(e)
            print('代码错误，请检查！！！')

        # AND AFTER YOU SUCCESS INPUT TO OB THEN CLEAR TEXTINPUT
        departxt.value = ''
        codetxt.value = ''
        midtxt.value = ''
        remtxt.value = ''
        page.update()
    def reflush(e):
        load_data()
    scroll_container = Column(
        spacing=10,
        height= 400,
        scroll=ScrollMode.AUTO,
        # on_scroll_interval=0

    )
    scroll_container.controls.append(mydt)
     
    page.add(
        
        Column([
            depart_dropdown,
            codetxt,
            remtxt,
            Row([

            ElevatedButton('添加数据',on_click= addtodo),
            ElevatedButton('刷新',on_click= reflush)
            ]

            ),
            # mydt,
            scroll_container,
        ]),
        
    )

ft.app(main)
