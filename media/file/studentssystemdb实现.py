# _*_ coding:utf-8   _*_
# 文件名称：studentsystem.py
# 开发工具：PyCharm
import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='user1', password='123456', db='students_lc')
mycursor = conn.cursor()

def menu():
    # 输出菜单
    print('''
    ╔———————学生成绩管理系统————————╗
    │                                              │
    │   =============== 功能菜单 ===============   │
    │                                              │
    │   1 录入学生成绩                            │
    │   2 查找学生成绩                             │
    │   3 删除学生成绩                             │
    │   4 修改学生成绩                             │
    │   5 排序                                     │
    │   6 统计学生总人数                           │
    │   7 显示所有学生成绩                         │
    │   0 退出系统                                 │
    │  ==========================================  │
    │  说明：通过数字选择菜单          │
    ╚———————————————————————╝
    ''')


def main():
    ctrl = True  # 标记是否退出系统
    while (ctrl):
        menu()  # 显示菜单
        option = int(input("请选择："))  # 选择菜单项
        if option == 0:  # 退出系统
            print('您已退出学生成绩管理系统！')
            ctrl = False
        elif option == 1:  # 录入学生成绩信息
            insert()
        elif option == 2:  # 查找学生成绩信息
            search()
        elif option== 3:  # 删除学生成绩信息
            delete()
        elif option == 4:  # 修改学生成绩信息
            modify()
        elif option == 5:  # 排序
            sort()
        elif option == 6:  # 统计学生总数
            total()
        elif option == 7:  # 显示所有学生信息
            show()


'''1 录入学生成绩信息'''
def insert():
    mark = True  # 是否继续添加
    while mark:

        id = int(input("请输入ID（如 1001）："))
        if not id:  # ID为空，跳出循环
            continue
        name = input("请输入名字：")
        if not name:  # 名字为空，跳出循环
            continue
        try:
            english = int(input("请输入英语成绩："))
            python = int(input("请输入Python成绩："))
            c = int(input("请输入C语言成绩："))
        except:
            print("输入无效，不是整型数值．．．．重新录入信息")
            continue
        studentset = (id,name,english,python,c)# 将学生信息添加到集合中
        sql_i = '''insert into students_score (id,name,english,python,c) values (%s,%s,%s,%s,%s)'''
        try:
            mycursor.execute(sql_i, studentset)
            conn.commit()
            print('添加成功')
        except Exception:
            print(Exception,'添加失败')
        inputMark = input("是否继续添加？（y/n）:")
        if inputMark == "y":  # 继续添加
            mark = True
        else:  # 不继续添加
            mark = False
    print("学生信息录入完毕！！！")


'''2 查找学生成绩信息'''
def search():
    mark = True
    while mark:
        mode = input("按ID查输入1；按姓名查输入2：")
        if mode == "1":
            id = input("请输入学生ID：")
            sql_q = "select * from students_score where id = '%s'" % id
            mycursor.execute(sql_q)
        elif mode == "2":
            name = input("请输入学生姓名：")
            sql_q = "select * from students_score where name = '%s'" % name
            mycursor.execute(sql_q)
        else:
            print("您的输入有误，请重新输入！")
            continue
        my = mycursor.fetchall()[0]
        if my != ():
            print(my)
        else:
            print('无此学生')
        inputMark = input("是否继续查询？（y/n）:")
        if inputMark == "y":
            mark = True
        else:
            mark = False

'''3 删除学生成绩信息'''
def delete():
    mark = True  # 标记是否循环
    while mark:
        studentId = input("请输入要删除的学生ID：")
        sql_d = "delete from students_score where id='%s'" % studentId #删除
        try:
            flag=mycursor.execute(sql_d)
            conn.commit()
            if flag == 0:
                print('没有此学生')
            else:
                print('删除成功')
        except:
            conn.rollback()
        show()  # 显示全部学生信息
        inputMark = input("是否继续删除？（y/n）:")
        if inputMark == "y":
            mark = True  # 继续删除
        else:
            mark = False  # 退出删除学生信息功能

'''4 修改学生成绩信息'''
def modify():
    mark = True
    while mark:
        show()  # 显示全部学生信息
        studentid = input("请输入要修改的学生ID：")
        sql_q = "select * from students_score where id = '%s'" % studentid
        mycursor.execute(sql_q)
        my = mycursor.fetchall()
        if my !=():
            my = my[0]
            name,english,python,c = my[1],my[2],my[3],my[4]
        else:
            print('输入学生ID错误,请重新输入')
            continue
        while True:
            field = input("请输入要修改的学生信息对应序号（name[1]，english[2],python[3],c[4],结束修改其他信息[其他]）：")
            if field == '1':
                name = input('name=')
            elif field =='2':
                english = input('english=')
            elif field == '3':
                python = input('python=')
            elif field == '4':
                c = input('c=')
            else:
                break
        print(name,english,python,c)
        sql_m = "update students_score set id = '%s',`name` = '%s',english = '%s',python = '%s', `c` = '%s' where id = '%s'" % (studentid,name,english,python,c,studentid)
        try:
            mycursor.execute(sql_m)
            conn.commit()
        except:
            conn.rollback()
        inputMark = input("是否继续修改其他学生信息？（y/n）：")
        if inputMark == "y":
            mark = True  # 继续修改
        else:
            mark = False  # 退出修改学生信息功能


'''5 排序'''
def sort():
    show()  # 显示全部学生信息
    ascORdesc = input("请选择（0升序；1降序）：")
    mode = input("请选择排序方式（1按英语成绩排序；2按Python成绩排序；3按C语言成绩排序；0按总成绩排序）：")
    if mode == "1":  # 按英语成绩排序
        if ascORdesc =='1':
            sql_s = "select * from students_score order by english desc"
        else:
            sql_s = "select * from students_score order by english asc"
    elif mode == "2":  # 按Python成绩排序
        if ascORdesc =='1':
            sql_s = "select * from students_score order by python desc"
        else:
            sql_s = "select * from students_score order by python asc"
    elif mode == "3":  # 按C语言成绩排序
        if ascORdesc =='1':
            sql_s = "select * from students_score order by `c` desc"
        else:
            sql_s = "select * from students_score order by `c` asc"
    elif mode == "0":  # 按总成绩排序
        if ascORdesc == '1':
            sql_s = """select id,`name`,english,python,`c` from (select id,`name`,python,english,`c`,(python+english+`c`) as sum_score from students_score) as sum_tables order by sum_score desc """
        else:
            sql_s = """select id,`name`,english,python,`c` from (select id,`name`,python,english,`c`,(python+english+`c`) as sum_score from students_score) as sum_tables order by sum_score asc """
    else:
        print("您的输入有误，请重新输入！")
    try:
        mycursor.execute(sql_s)
    except:
        print(Exception)
    my_s = mycursor.fetchall()
    for i in my_s:
        print(i)

''' 6 统计学生总数'''
def total():
    sql_t = "select count(*) from students_score"
    mycursor.execute(sql_t)
    try:
        m = mycursor.fetchall()[0][0]
    except Exception:
        m = 0
    print(m)


''' 7 显示所有学生信息 '''
def show():
    sql_s = "select * from students_score"
    mycursor.execute(sql_s)
    my_s = mycursor.fetchall()
    if my_s == ():
        print('查无学生')
    else:
        for i in my_s:
            print(i)


if __name__ == "__main__":
    main()


mycursor.close()
conn.close()

