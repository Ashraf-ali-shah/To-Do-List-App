from datetime import  datetime,date,timedelta
import re
import os
import json
class Task:
    def __init__(self,title,description,dueDate,priority,category,completed=False):
        self.title=title
        self.description=description
        self.dueDate=dueDate
        self.completed=completed
        self.priority=priority
        self.category=category
    def __str__(self):
        return f"Task Title: {self.title}   Description : {self.description}  DueDate : {self.dueDate}    Completed : {'Yes' if self.completed else 'NO'}"
# task class completed
class User:
    def __init__(self,name,password):
        self.name=name
        self.password=password
    def __str__(self):
        return self.name
# user class close      
class user_manger:
    def __init__(self,filename='user.json'):
        self.filename=filename
        self.users=[]
        self.load_user()
    def add_user(self,user):
        self.users.append(user)
        print("Thank you for joining us")
        self.update_user()
    def load_user(self):
        try:
            with open(self.filename,"r") as file:
                if os.path.getsize(self.filename)==0:
                    self.users=[]
                    return 
                data=json.load(file)
                for user in data:
                    self.users.append(User(**user))
        except FileExistsError:
            print("file does not exist")
        except FileNotFoundError:
            print("file not found")
        except Exception as e:
            print(f"{e} issue encountered")
    def update_user(self):
        try:
            data=[user.__dict__ for user in self.users]
            with open(self.filename,'w') as file:
                json.dump(data,file,indent=4)
        except FileExistsError:
            print("file does not exist")
        except FileNotFoundError:
            print("file not found")
        except Exception as e:
            print(f"{e} issue encountered")
    def remove_user(self,name):
        ruser=None
        for i in range(len(self.users)):
            if self.users[i].name==name:
                ruser=self.users[i]
                del self.users[i]
                break
        if not ruser:
            print("no user found please check spelling or else")
            return
        try:
            os.remove(f"{name}.json")
            self.update_user()
            print("Goodbye")
        except Exception as e:
            print(f"{e} issue encountered")
    def search_user(self,name,password):
        for user in self.users:
            if user.name==name and user.password==password:
                return True
        return False
# user_manger class end
class todoApp:
    def __init__(self,filename,currentUser):
        print(f"{currentUser}___________________________",end="")
        self.filename=filename
        self.tasks=[]
        self.upload_data()
        self.progress()
    def upload_data(self):
        try:
            with open(self.filename,"r") as file:
                if os.path.getsize(self.filename)==0:
                    self.tasks=[]
                    return 
                else:
                    data=json.load(file)
                    for item in data:
                        self.tasks.append(Task(**item))
        except FileExistsError:
            print("file does not exist")
        except FileNotFoundError:
            data={}
            with open(self.filename,"w") as file:
                json.dump(data,file,indent=4)
        except Exception as e:
            print(f"{e} issue encountered")
    def add_task(self,task):
        self.tasks.append(task)
        print("Task Successfully Added")
        self.update_data()
    def update_data(self):
        try:
            data=[tsk.__dict__ for tsk in self.tasks]
            with open(self.filename,'w') as file:
                json.dump(data,file,indent=4)
        except FileExistsError:
            print("file does not exist")
        except FileNotFoundError:
            print("file not found")
        except Exception as e:
            print(f"{e} issue encountered")
    def filter(self):
        task_periority={"high":0,"medium":1,"low":2}
        filter_tsk=sorted(self.tasks,key=lambda task:task_periority[task.priority])
        for tsk in filter_tsk:
            print(tsk)
    def progress(self):
        comp=[tsk for tsk in self.tasks if tsk.completed==True]
        print(f"your progress is {len(comp)}/{len(self.tasks)}")
        del comp
    def show_all(self):
        i=1
        for task in self.tasks:
            print(f"{i} {task}")
            i+=1
        del i
    def filter_time(self):
        near_task=[task for task in self.tasks if abs(datetime.strptime(task.dueDate,"%Y-%m-%d").date()-datetime.today().date())<=timedelta(days=8)]
        if len(near_task)==0:
            print("no task found")
            return
        for task in near_task:
            print(task)
        del near_task
    def show_completed_tasks(self):
        completed=[tsk for tsk in self.tasks if tsk.completed==True]
        if len(completed)==0:
            print("No completed task found")
            return
        for tsk in completed:
            print(tsk)
        del completed
    def show_uncompleted_tasks(self):
        uncompleted=[tsk for tsk in self.tasks if tsk.completed==False]
        if len(uncompleted)==0:
            print("No uncompleted task found")
            return
        for tsk in uncompleted:
            print(tsk)
        del uncompleted
    def show_single(self,stitle):
        obj=None
        for tsk in self.tasks:
            if tsk.title==stitle:
                obj=tsk
                break
        if obj:
            print(obj)
        else:
            print("task not found please check spelling or else")
    def mark_task(self,title):
        find=True
        for task in self.tasks:
            if task.title==title:
                task.completed=True
                print("Task marked completed Successfully")
                self.update_data()
                find=False
                break
        if find:
            print("No task found")
    def remove_task(self,title):
        if len(self.tasks)==0:
            print("No task found list is empty")
            return
        for i in range(len(self.tasks)):
            if self.tasks[i].title==title:
                obj=self.tasks[i]
                idx=i
                break
        if obj:
            print(obj)
            choice=input("Are you sure to delete this task yes/no    ").strip().lower()
            if re.match(r"^(yes|no)$",choice):
                if choice=="yes":
                    del self.tasks[idx]
                    print("Successfully Deleted")
                    self.update_data()
                    return
                elif choice=='no':
                    return
            else:
                print("wrong input")
        else :
            print("Task not found")
            return
# manager class closed
def main():
    print("_________Welcome To To-Do-List Application_________")
    print()
    print("1: Sign up")
    print("2: Log in")
    print("3: Exit")
    access=int(input())
    userManager=user_manger()
    user_name=None
    controller=True
    while controller:
        if access==1:
            user_name=str(input("Enter Username    ")).strip().capitalize()
            if not re.match(r"^[A-Za-z0-9 ]{3,}$",user_name):
                print("User name must be atleast three characters")
                continue
            else:
                if any(user.name==user_name for user in userManager.users):
                    print("user name already exist")
                    continue
            password=str(input("Enter password   ")).strip()
            if not re.match(r"^[A-Za-z0-9]{6,}$",password):
                print("password must be greater then 6 characters")
                continue
            user=User(name=user_name,password=password)
            userManager.add_user(user=user)
        elif access==2:
            user_name=str(input("Enter username    ")).strip().capitalize()
            password=str(input("Enter password    ")).strip()
            if not userManager.search_user(name=user_name,password=password):
                print("Incorrect username or password")
                break
        elif access==3:
            controller=False
            break
# User authentication End
        list_manger=todoApp(filename=f"{user_name}.json",currentUser=user_name)
        while True:
            print("1: add Task")
            print("2: remove Task")
            print("3: show Task")
            print("4: search task")
            print("5: Filter task")
            print("6: Mark task completed")
            print("7: Delete account")
            print("8: Exit")
            choice=int(input())
            if choice==1:
                title=str(input("Enter Title of the task    ")).strip().capitalize()
                description=str(input("Enter description of the task    ")).strip().lower()
                dudate=str(input("Enter Due Date (yy-mm-dd)    "))
                try: 
                    dudate=datetime.strptime(dudate,'%Y-%m-%d').date()
                except ValueError:
                    print("invalid formate yy-mm-dd expected")
                    continue
                priority=str(input("Enter priority of the task (high,medium,low)    ")).strip().lower()
                if not re.match(r"^(high|medium|low)",priority):
                    print("invalid input please check the spelling")
                    continue
                category=str(input("Enter category of the task    ")).strip().lower()
                task=Task(title=title,description=description,dueDate=dudate.isoformat(),priority=priority,category=category)
                list_manger.add_task(task=task)
            elif choice==2:
                title=str(input("Enter title of the task    ")).strip().capitalize()
                list_manger.remove_task(title=title)
            elif choice==3:
                print("choose any option")
                print("1: show all tasks")
                print("2: show completed tasks")
                print("3: show uncompleted tasks")
                show_choice=int(input())
                if show_choice==1:
                    list_manger.show_all()
                elif show_choice==2:
                    list_manger.show_completed_tasks()
                elif show_choice==3:
                    list_manger.show_uncompleted_tasks()
            elif choice==4:
                stitle=str(input("Enter title of the task    ")).strip().capitalize()
                list_manger.show_single(stitle)
            elif choice==5:
                print("1: Filter by priority")
                print("2: Filter by nearest due date")
                fchoice=int(input())
                if fchoice==1:
                    list_manger.filter()
                elif fchoice==2:
                    list_manger.filter_time()
            elif choice==6:
                mtitle=str(input("Enter title of the task    ")).strip().capitalize()
                list_manger.mark_task(mtitle)
            elif choice==7:
                userManager.remove_user(user_name)
                controller=False
                break
            elif choice==8:
                print("saving data......\nprocess completed")
                controller=False
                break
            else:
                print("invalid input")
                continue
# program execution
if __name__=="__main__":
    main()
# end of the journey
            

        



        


        