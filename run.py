import pymysql

base = pymysql.connect("192.168.32.10","tihon","123","Bank" )
 
cursor = base.cursor()


class Client():
    def __init__(self):
        self.name =""
        self.login=""
        self.password=""
        self.id=""

    def Add(self):
        print("имя:")
        self.name=str(input())
        print("логин:")
        self.login=str(input())
        print("пароль:")
        self.password=str(input())
        print("Имя:" +self.name+ " логин:" +self.login+ " пароль:"+self.password)
        cursor.execute('INSERT INTO Clients( names, login, pasword)  VALUES("{0}", "{1}", "{2}");'.format(self.name, self.login,self.password))
        base.commit()

    def Login(self):
        print("Введите ваш логин")
        self.login=input()
        print("Введите ваш пароль")
        self.password=input()
        cursor.execute('SELECT names FROM Clients WHERE login="{0}" AND pasword="{1}" LIMIT 1'.format(self.login,self.password))
        tmp=cursor.fetchall()
        #print(cursor.fetchall())
        if(len(tmp)==0 ):
            print("ОШИБКА")
        else:
            cursor.execute('SELECT user_id FROM Clients WHERE login="{0}" AND pasword="{1}" LIMIT 1'.format(self.login,self.password))
            self.id=cursor.fetchall()
            print(str(tmp[0][0])+"  " + str(self.id[0][0]))

class Category():
    def __init__(self):
        self.id=0
        self.currency=""
        self.interest=0
        self.periodicity=0
        self.name=""
    def Creat(self):
        print("Создание нового вида вклада")
        print("Название вклада:")
        self.name=input()
        print("Валюта:")
        self.currency=input()
        print("Количество процентов годовых")
        self.interest=input()
        try:
            self.interest=int(self.interest)
        except:
            print("Ошибка")
            return 0
        print("Переодичность выплат:")
        self.periodicity=input()
        try:
            self.periodicity=int(self.periodicity)
        except:
            print("Ошибка")
            return 0
        cursor.execute('INSERT INTO Category( currency, interest, periodicity, name)  VALUES("{0}", {1}, {2} , "{3}");'.format(self.currency, self.interest,self.periodicity,self.name))
        base.commit()

    def Delite(self):
        print("Удаление вида вклада")
        print("Название вклада:")
        self.name=input()
        print("Валюта:")
        self.currency=input()
        print("Количество процентов годовых")
        self.interest=input()
        try:
            self.interest=int(self.interest)
        except:
            print("Ошибка")
            return 0
        print("Переодичность выплат:")
        self.periodicity=input()
        try:
            self.periodicity=int(self.periodicity)
        except:
            print("Ошибка")
            return 0
        
        cursor.execute('DELETE FROM Category WHERE currency="{0}" AND interest={1} AND periodicity={2} AND name="{3}";'.format(self.currency, self.interest,self.periodicity,self.name))
        if(str(cursor.fetchall())=="()"):
            print("Ошибка")
            return 0
        
        cursor.execute('DELETE FROM Category WHERE currency="{0}" AND interest={1} AND periodicity={2} AND name="{3}";'.format(self.currency, self.interest,self.periodicity,self.name))
        
        base.commit()
        return 1


class Depozit():
    def __init__(self,id):
        self.id_user=id
        self.id_category=0
        self.sum=0
        self.date=""
    def  Creatе(self,date):
        print("Создание нового депозита")
        print("Сумма:")
        self.sum=input()
        try:
            sum=int(self.sum)
        except:
            print("Ошибка")
            return 0
        print("Выберите Вид депозита:(название,валюта,проценты,переодичность выплат)")
        cursor.execute('SELECT name ,currency, interest, periodicity FROM Category')
        tmp=cursor.fetchall()
        for i in range(len(tmp)):
            for j in range(len(tmp[0])):
                print(tmp[i][j], end =" ")
            print("")

        name=input()
        
        cursor.execute('SELECT id_category FROM Category WHERE name = "{0}"'.format(name))
        tmp=cursor.fetchall()
        print(tmp)
        if(str(tmp)=="()"):
            print("Ошибка")
            return 0
            
        print('INSERT INTO Deposits( user_id, type_depozit_id, sum, date_payment)  VALUES({0}, {1}, {2} , "{3}");'.format(self.id_user, tmp[0][0],int(self.sum),date))
        cursor.execute('INSERT INTO Deposits( user_id, type_depozit_id, summ, date_payment)  VALUES({0}, {1}, {2} , "{3}");'.format(int(self.id_user[0][0]), tmp[0][0],int(self.sum),date))
        base.commit()
        return 1



    def Replenish(self):
        print("Какую сумму вы хотите положить в банк?")
        sum=input()
        try:
            sum=int(sum)
        except:
            print("Ошибка")
            return 0
        print("Счёт какого депозита вы хотите пополнить?")
        cursor.execute('SELECT Deposits.id_deposits, Category.name, Category.currency,Category.interest,Category.periodicity,Deposits.summ,Deposits.date_payment FROM Category INNER JOIN Deposits ON Category.id_category = Deposits.type_depozit_id WHERE user_id="{0}";'.format(int(self.id_user[0][0])))
        tmp=cursor.fetchall()
        for i in range(len(tmp)):
            for j in range(len(tmp[0])):
                print(tmp[i][j], end =" ")
            print("")
        name=int(input())
        tmp2=""
        for j in range(len(tmp)):
            if(tmp[j][0]==name):
                tmp2=j
                break
        print("Вы хотите пополнить или уменьшить счёт?(+|-)")
        plus=input()
        if(plus!="+" or plus!="-"):
            print("Ошибка")
            return 0
        if(tmp2==""):
            print("Ошибка")
        else:
            if(plus=="+"):
                cursor.execute('UPDATE Deposits SET summ={0} WHERE user_id={1} AND id_deposits={2};'.format((sum+tmp[tmp2][5]),int(self.id_user[0][0]),name))
            else:
                cursor.execute('UPDATE Deposits SET summ={0} WHERE user_id={1} AND id_deposits={2};'.format((tmp[tmp2][5]-sum),int(self.id_user[0][0]),name))
        
        
        base.commit()
        return 0

        
        
        
        

c=Client()
cat=Category()
c.Add()
c.Login()
cat.Creat()
cat.Delite()
dep=Depozit(c.id)
dep.Creatе('2010-11-13')
dep.Replenish()


#cursor = base.cursor()
#cursor.execute("SELECT ip,NAME FROM hosts")-+
#cursor.execute("UPDATE hosts SET ONLINE = '{0}' WHERE ip='{1}';".format(ONLINE_or_OFFLINE(status), i))
#cursor.execute("INSERT INTO ping(ip, polling_date, polling_time, status) VALUES ('{0}', '{1}', '{2}', '{3}')".format(i, now.strftime("%d-%m-%Y"), now.strftime("%H:%M"), ONLINE_or_OFFLINE(status)))
#base.commit()
#base.close()