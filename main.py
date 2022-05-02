import random
import sqlite3
import requests
from requests.exceptions import ConnectionError
import threading
#from twilio.rest import Client
import time


from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
#from kivy.app import App
from kivy.clock import Clock
# from kivymd.uix.textinput import MDTextField
# from kivymd.uix.button import MDFlat

from kivy.core.window import Window

Window.size = (370, 640)
# from unittest.mock import Mock


# cur.execute(''' INSERT INTO user_table(FirstName, LastName, Email, Password, PhoneNumber) VALUES (?, ?, ?, ?, ?)''', ('Divine','Bako-johnson','divine00329@gmail.com', '1234', 8164287435))
# cur.execute(''' INSERT INTO user_table(FirstName, LastName, Email, Password, PhoneNumber) VALUES (?, ?, ?, ?, ?)''', ('Justin','Benjamin','divine00329@gmail.com', '1234', 8164287435))
# conn.commit()
########### view database #######
# cur.execute(''' SELECT * FROM user_table ''')
# records = cur.fetchall()
# print(records)

# Define our different screensn 



class DemoProject(ScreenManager):

    conn = sqlite3.connect('pythonClass.db')
    cur = conn.cursor()


    cur.execute(''' CREATE TABLE IF NOT EXISTS user_table(
                        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        FirstName TEXT,
                        LastName TEXT,
                        Email VARCHAR,
                        PassWord VARCHAR,
                        PhoneNumber INTEGER
                    )
                ''')
    


    def sign_up(self, fn, ln, em, pas, pn, app):
        
        # -------------------------- SIGN UP FORM DATA VALIDATION ----------------------------#

        if(not(len(fn) == 0 or len(ln) == 0 or len(em) == 0 or len(pas) == 0 or len(pn) == 0)):
            if((any(a.isdigit() for a in fn)) == False):
                if((any(b.isdigit() for b in ln)) == False):
                    if(len(pas) >= 6):
                        if((pn[0] == '8' or pn[0] == '9' or pn[0] == '7') and len(pn) == 10):  
                            # print("signed up sucessfully!")
                            self.ids.sign_err.text = ""
                            self.cur.execute(''' INSERT INTO user_table (FirstName, LastName, Email, Password, PhoneNumber) VALUES (?, ?, ?, ?, ?)''', (fn, ln, em, pas, int(pn)))
                            self.conn.commit()

                            self.cur.execute(''' SELECT CustomerID FROM user_table WHERE FirstName=? AND LastName=? AND Password=?''', (fn, ln, pas)) 
                            self.persons_ID = self.cur.fetchone()[0]

                            app.show_signed_up_dialog(str(self.persons_ID))

                            self.ids.firstName.text = ""       
                            self.ids.lastName.text = ""   
                            self.ids.email.text = ""
                            self.ids.user_password.text = ""
                            self.ids.phoneNumber.text = ""    

                        else:
                            self.ids.sign_err.text = "Invalid Phone Number" 
                    elif(len(pas) < 6):
                        self.ids.sign_err.text = "Password should be atleast 6 characters"
                elif(any(b.isdigit() for b in ln)):
                    self.ids.sign_err.text = "First Name and Last Name must not\ncontain integers" 
            elif(any(a.isdigit() for a in fn)):
                self.ids.sign_err.text = "First Name and Last Name must not\ncontain integers"
        else:
            self.ids.sign_err.text = "All data must be filled"
        #     if(self.fn_val and self.ln_val)
            # err_msg = "Hello world!"

        # --------------------------------------------------------------------------------------#  

    


#           



    

    def cat_clicked(self, value, app, root):
#        self.ids.loading.active = True
        try:
                
            self.api_url = requests.get('https://the-trivia-api.com/questions?categories=' + str(value) + '&limit=10')
            self.data = self.api_url.json() 
            
            self.num1 = random.randint(1, 4)
            self.num2 = random.randint(1, 4)
            self.num3 = random.randint(1, 4)
            self.num4 = random.randint(1, 4)
            self.num5 = random.randint(1, 4)
            self.num6 = random.randint(1, 4)
            self.num7 = random.randint(1, 4)
            self.num8 = random.randint(1, 4)
            self.num9 = random.randint(1, 4)
            self.num10 = random.randint(1, 4)
            
            def set_imgs(cat):
                self.ids.img1.source = "icons/images/" + str(cat) + str(self.num1) + ".png"
                self.ids.img2.source = "icons/images/" + str(cat) + str(self.num2) + ".png"
                self.ids.img3.source = "icons/images/" + str(cat) + str(self.num3) + ".png"
                self.ids.img4.source = "icons/images/" + str(cat) + str(self.num4) + ".png"
                self.ids.img5.source = "icons/images/" + str(cat) + str(self.num5) + ".png"
                self.ids.img6.source = "icons/images/" + str(cat) + str(self.num6) + ".png"
                self.ids.img7.source = "icons/images/" + str(cat) + str(self.num7) + ".png"
                self.ids.img8.source = "icons/images/" + str(cat) + str(self.num8) + ".png"
                self.ids.img9.source = "icons/images/" + str(cat) + str(self.num9) + ".png"
                self.ids.img10.source = "icons/images/" + str(cat) + str(self.num10) + ".png"
                
            
            if(value == 'arts_and_literature'):
                set_imgs("art")
            if(value == 'film_and_tv'):
                set_imgs("film")
            if(value == 'food_and_drink'):
                set_imgs("food")
            if(value == 'general_knowledge'):
                set_imgs("general")
            if(value == 'geography'):
                set_imgs("geo")
            if(value == 'history'):
                set_imgs("history")
            if(value == 'music'):
                set_imgs("music")
            if(value == 'science'):
                set_imgs("science")
            if(value == 'sport_and_leisure'):
                set_imgs("sports")
            
            ######################################################################################################################
            # ---------------------------------------------- QUIZ STRUCTURE -----------------------------------------------------#
            # ------------ Question 1----------------------#
            self.ids.que1.text = self.data[0]["question"]
            self.pre1_opt = self.data[0]["incorrectAnswers"]
            self.que1_correct_answer = self.data[0]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre1_opt.append(self.data[0]["correctAnswer"])
            # print(self.pre1_opt)
            self.que1_opt = []
            for i in range(len(self.pre1_opt)):
                a = random.randint(0, len(self.pre1_opt) - 1)
#                print(a)
                self.que1_opt.append(self.pre1_opt[a])
                self.pre1_opt.remove(self.pre1_opt[a])
            
            # print(self.que1_opt)
            self.ids.que1_opt1.text = self.que1_opt[0]
            self.ids.que1_opt2.text = self.que1_opt[1]
            self.ids.que1_opt3.text = self.que1_opt[2]
            self.ids.que1_opt4.text = self.que1_opt[3]

            # ------------ Question 2----------------------#


            self.ids.que2.text = self.data[1]["question"]
            self.pre2_opt = self.data[1]["incorrectAnswers"]
            self.que2_correct_answer = self.data[1]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre2_opt.append(self.data[1]["correctAnswer"])
            # print(self.pre1_opt)
            self.que2_opt = []
            for i in range(len(self.pre2_opt)):
                a = random.randint(0, len(self.pre2_opt) - 1)
                # print(a)
                self.que2_opt.append(self.pre2_opt[a])
                self.pre2_opt.remove(self.pre2_opt[a])
            
            # print(self.que1_opt)
            self.ids.que2_opt1.text = self.que2_opt[0]
            self.ids.que2_opt2.text = self.que2_opt[1]
            self.ids.que2_opt3.text = self.que2_opt[2]
            self.ids.que2_opt4.text = self.que2_opt[3]


            # ------------ Question 3----------------------#


            self.ids.que3.text = self.data[2]["question"]
            self.pre3_opt = self.data[2]["incorrectAnswers"]
            self.que3_correct_answer = self.data[2]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre3_opt.append(self.data[2]["correctAnswer"])
            # print(self.pre1_opt)
            self.que3_opt = []
            for i in range(len(self.pre3_opt)):
                a = random.randint(0, len(self.pre3_opt) - 1)
                # print(a)
                self.que3_opt.append(self.pre3_opt[a])
                self.pre3_opt.remove(self.pre3_opt[a])
            
            # print(self.que1_opt)
            self.ids.que3_opt1.text = self.que3_opt[0]
            self.ids.que3_opt2.text = self.que3_opt[1]
            self.ids.que3_opt3.text = self.que3_opt[2]
            self.ids.que3_opt4.text = self.que3_opt[3]



            # ------------ Question 4----------------------#


            self.ids.que4.text = self.data[3]["question"]
            self.pre4_opt = self.data[3]["incorrectAnswers"]
            self.que4_correct_answer = self.data[3]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre4_opt.append(self.data[3]["correctAnswer"])
            # print(self.pre1_opt)
            self.que4_opt = []
            for i in range(len(self.pre4_opt)):
                a = random.randint(0, len(self.pre4_opt) - 1)
                # print(a)
                self.que4_opt.append(self.pre4_opt[a])
                self.pre4_opt.remove(self.pre4_opt[a])
            
            # print(self.que1_opt)
            self.ids.que4_opt1.text = self.que4_opt[0]
            self.ids.que4_opt2.text = self.que4_opt[1]
            self.ids.que4_opt3.text = self.que4_opt[2]
            self.ids.que4_opt4.text = self.que4_opt[3]


            # ------------ Question 5----------------------#


            self.ids.que5.text = self.data[4]["question"]
            self.pre5_opt = self.data[4]["incorrectAnswers"]
            self.que5_correct_answer = self.data[4]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre5_opt.append(self.data[4]["correctAnswer"])
            # print(self.pre1_opt)
            self.que5_opt = []
            for i in range(len(self.pre5_opt)):
                a = random.randint(0, len(self.pre5_opt) - 1)
                # print(a)
                self.que5_opt.append(self.pre5_opt[a])
                self.pre5_opt.remove(self.pre5_opt[a])
            
            # print(self.que1_opt)
            self.ids.que5_opt1.text = self.que5_opt[0]
            self.ids.que5_opt2.text = self.que5_opt[1]
            self.ids.que5_opt3.text = self.que5_opt[2]
            self.ids.que5_opt4.text = self.que5_opt[3]


            # ------------ Question 6----------------------#


            self.ids.que6.text = self.data[5]["question"]
            self.pre6_opt = self.data[5]["incorrectAnswers"]
            self.que6_correct_answer = self.data[5]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre6_opt.append(self.data[5]["correctAnswer"])
            # print(self.pre1_opt)
            self.que6_opt = []
            for i in range(len(self.pre6_opt)):
                a = random.randint(0, len(self.pre6_opt) - 1)
                # print(a)
                self.que6_opt.append(self.pre6_opt[a])
                self.pre6_opt.remove(self.pre6_opt[a])
            
            # print(self.que1_opt)
            self.ids.que6_opt1.text = self.que6_opt[0]
            self.ids.que6_opt2.text = self.que6_opt[1]
            self.ids.que6_opt3.text = self.que6_opt[2]
            self.ids.que6_opt4.text = self.que6_opt[3]



            # ------------ Question 7----------------------#


            self.ids.que7.text = self.data[6]["question"]
            self.pre7_opt = self.data[6]["incorrectAnswers"]
            self.que7_correct_answer = self.data[6]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre7_opt.append(self.data[6]["correctAnswer"])
            # print(self.pre1_opt)
            self.que7_opt = []
            for i in range(len(self.pre7_opt)):
                a = random.randint(0, len(self.pre7_opt) - 1)
                # print(a)
                self.que7_opt.append(self.pre7_opt[a])
                self.pre7_opt.remove(self.pre7_opt[a])
            
            # print(self.que1_opt)
            self.ids.que7_opt1.text = self.que7_opt[0]
            self.ids.que7_opt2.text = self.que7_opt[1]
            self.ids.que7_opt3.text = self.que7_opt[2]
            self.ids.que7_opt4.text = self.que7_opt[3]



            # ------------ Question 8----------------------#


            self.ids.que8.text = self.data[7]["question"]
            self.pre8_opt = self.data[7]["incorrectAnswers"]
            self.que8_correct_answer = self.data[7]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre8_opt.append(self.data[7]["correctAnswer"])
            # print(self.pre1_opt)
            self.que8_opt = []
            for i in range(len(self.pre8_opt)):
                a = random.randint(0, len(self.pre8_opt) - 1)
                # print(a)
                self.que8_opt.append(self.pre8_opt[a])
                self.pre8_opt.remove(self.pre8_opt[a])
            
            # print(self.que1_opt)
            self.ids.que8_opt1.text = self.que8_opt[0]
            self.ids.que8_opt2.text = self.que8_opt[1]
            self.ids.que8_opt3.text = self.que8_opt[2]
            self.ids.que8_opt4.text = self.que8_opt[3]




            # ------------ Question 9----------------------#


            self.ids.que9.text = self.data[8]["question"]
            self.pre9_opt = self.data[8]["incorrectAnswers"]
            self.que9_correct_answer = self.data[8]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre9_opt.append(self.data[8]["correctAnswer"])
            # print(self.pre1_opt)
            self.que9_opt = []
            for i in range(len(self.pre9_opt)):
                a = random.randint(0, len(self.pre9_opt) - 1)
                # print(a)
                self.que9_opt.append(self.pre9_opt[a])
                self.pre9_opt.remove(self.pre9_opt[a])
            
            # print(self.que1_opt)
            self.ids.que9_opt1.text = self.que9_opt[0]
            self.ids.que9_opt2.text = self.que9_opt[1]
            self.ids.que9_opt3.text = self.que9_opt[2]
            self.ids.que9_opt4.text = self.que9_opt[3]


            # ------------ Question 10----------------------#


            self.ids.que10.text = self.data[9]["question"]
            self.pre10_opt = self.data[9]["incorrectAnswers"]
            self.que10_correct_answer = self.data[9]["correctAnswer"]
            # print(self.data[0]["incorrectAnswers"])
            # print(self.data[0]["correctAnswer"])

            self.pre10_opt.append(self.data[9]["correctAnswer"])
            # print(self.pre1_opt)
            self.que10_opt = []
            for i in range(len(self.pre10_opt)):
                a = random.randint(0, len(self.pre10_opt) - 1)
                # print(a)
                self.que10_opt.append(self.pre10_opt[a])
                self.pre10_opt.remove(self.pre10_opt[a])
            
            # print(self.que1_opt)
            self.ids.que10_opt1.text = self.que10_opt[0]
            self.ids.que10_opt2.text = self.que10_opt[1]
            self.ids.que10_opt3.text = self.que10_opt[2]
            self.ids.que10_opt4.text = self.que10_opt[3]


            # self.ids.que2 = self.data[1]["question"]
            # self.ids.que3 = self.data[2]["question"]
            # self.ids.que4 = self.data[3]["question"]
            # self.ids.que5 = self.data[4]["question"]
            # self.ids.que6 = self.data[5]["question"]
            # self.ids.que7 = self.data[6]["question"]
        


            # for i in self.data:
            #     print(i)

            self.all_correct_answers = [self.que1_correct_answer, 
                                        self.que2_correct_answer, 
                                        self.que3_correct_answer,
                                        self.que4_correct_answer, 
                                        self.que5_correct_answer, 
                                        self.que6_correct_answer, 
                                        self.que7_correct_answer, 
                                        self.que8_correct_answer, 
                                        self.que9_correct_answer, 
                                        self.que10_correct_answer]

            # print(self.all_correct_answers)
            ##################################################################################################################
            #----------------------------------------------------------------------------------------------------------------#
            return True
        except ConnectionError as e:
            # print("No Connection :(")
            return False

        
    user_phone_number = ''
    user_first_name = ''

    def log_in(self, user_id, password):
        self.cur.execute(''' SELECT COUNT(CustomerID) FROM user_table ''')
        id_range = self.cur.fetchone()[0]

        if(len(user_id) > 0 and user_id.isnumeric()):
            if(int(user_id) <= id_range and not(int(user_id) == 0)):
                self.cur.execute(''' SELECT Password FROM user_table WHERE CustomerID = ''' + str(user_id))
                correct_password = self.cur.fetchone()[0]

                if(password == correct_password):
                    self.cur.execute(''' SELECT FirstName FROM user_table WHERE CustomerID = ''' + str(user_id))
                    self.user_first_name = self.cur.fetchone()[0]
                    self.cur.execute(''' SELECT PhoneNumber FROM user_table WHERE CustomerID = ''' + str(user_id))
                    self.user_phone_number = self.cur.fetchone()[0]
                    
                    self.ids.greets.text = "Welcome " + self.user_first_name
                    return True
        else:
            return False
    

    #-------------------- STORING USER'S ANSWERS ---------------------#
    users_answers = ['', '', '', '', '', '', '', '', '', '']

    def checkbox_click(self, instance, value, root, option):
        
        for i in range(len(self.users_answers) + 1):
            if(root.current == "question" + str(i) and value == True):
                self.users_answers[i - 1] = option
                # print(self.users_answers)

    #-----------------------------------------------------------------#   
    minutes = 9
    secs = 60
    
    final_score = ''
    
    def calculate_score(self, obj):
        
        self.ids.time1.text = '10:00'
        self.ids.time2.text = '10:00'
        self.ids.time3.text = '10:00'
        self.ids.time4.text = '10:00'
        self.ids.time5.text = '10:00'
        self.ids.time6.text = '10:00'
        self.ids.time7.text = '10:00'
        self.ids.time8.text = '10:00'
        self.ids.time9.text = '10:00'
        self.ids.time10.text = '10:00'
        
        self.sec_interval.cancel()
        self.minutes = 9
        self.secs = 60
        self.score = 0
        self.all_user_answers = self.users_answers

#        root.current = "submit"
        self.current = "submit"

        for i in self.all_correct_answers:
            for j in self.all_user_answers:
                # print(i, j)
                if(i == j):
                    self.score += 1
        
        self.submit_dialog.dismiss()
#        print(self.score)

        self.final_score = str((self.score/10) * 100)
        
        
        
    
#    def show_score(self):
#        
#        time.sleep(2)
        
        
    result_dialog = None
    def show_result_dialog(self):
        if not self.result_dialog:
            self.result_dialog = MDDialog(
                title = str(self.final_score),
                buttons = [
                   MDFillRoundFlatButton(
                        text = "OK",
                        on_release = self.close_result_dialog
                    )
                ],
            )
            
        self.result_dialog.open()
        
    
    def close_result_dialog(self, obj):
        self.result_dialog.dismiss()
            
    
        
        
        
        
        
        

    
    submit_dialog = None
    def show_submit_dialog(self):   
        if not self.submit_dialog:
            self.submit_dialog = MDDialog(
                title = "Are you sure you want to submit?",
                buttons = [
                    MDFillRoundFlatButton(
                        text = "YES",
                        on_release = self.calculate_score
                    ),
                    MDRoundFlatButton(
                        text = "NO",
                        on_release = self.close_submit_dialog
                    )
                ],
            )
    
        self.submit_dialog.open()
    
    
    def close_submit_dialog(self, obj):
        
        self.submit_dialog.dismiss()
        
    
    
            
    
        
    def submit(self):
        self.show_submit_dialog()
        
        
        

    
    def log_out(self, root):
        self.ids.userID.text = ""
        self.ids.password.text = ""
        root.current = "screen_1"
        root.transition.direction = "right"
#            if(self.x == (self.minute + 1) * 60):
#                break



    
    def start_timer(self):
#        print("Hello world!")
        self.sec_interval = Clock.schedule_interval(self.update_timer, 1)


    def update_timer(self, dt):
        if(not(self.minutes == 0 and self.secs == 0)):
    #        self.x += 1
    #        self.root.ids.time.text = str(int(self.root.ids.time.text) + 1)

            self.secs = self.secs - 1

            if(self.secs == 60):
                self.secs = 0

            if(self.secs == -1):
                self.secs = 59
                self.minutes -= 1

            
            if(self.minutes == 10 and not(self.secs < 10)):
                self.time_left = str(self.minutes) + ':' + str(self.secs)
            if(self.minutes < 10 and not(self.secs < 10)):
                self.time_left = '0' + str(self.minutes) + ':' + str(self.secs)
            if(self.secs < 10 and self.minutes == 10):
                self.time_left = str(self.minutes) + ':0' + str(self.secs)
            if(self.secs < 10 and self.minutes < 10):
                self.time_left = '0' + str(self.minutes) + ':0' + str(self.secs)
                
            self.ids.time1.text = self.time_left
            self.ids.time2.text = self.time_left
            self.ids.time3.text = self.time_left
            self.ids.time4.text = self.time_left
            self.ids.time5.text = self.time_left
            self.ids.time6.text = self.time_left
            self.ids.time7.text = self.time_left
            self.ids.time8.text = self.time_left
            self.ids.time9.text = self.time_left
            self.ids.time10.text = self.time_left
    #        print(self.time_left)
        else:
            self.sec_interval.cancel()
            self.current = "submit"
            self.calculate_score
            
    
                
class Main(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Blue"


        Builder.load_file("my.kv")
        return DemoProject()

    # ------------------- sign up dialog -----------------------------#
    dialog = None
    def show_signed_up_dialog(self, user_ID):
        if not self.dialog:
            self.dialog = MDDialog(
                text = "Signed up sucessfully! Your ID is:\n" + user_ID,
                # size_hint = (0.7, 1)
                buttons = [
                    MDRoundFlatButton(
                        text = "OK",
                        on_release = self.close_signed_up_dialog
                    )
                ],
            )

        self.dialog.open()
   

    def close_signed_up_dialog(self, obj):
        self.dialog.dismiss()
     #------------------------------------------------------------------#

    #---------------------- CONNECTION ERROR DIALOG --------------------#
    connection_dialog = None
    def show_connection_dialog(self):
        if not self.connection_dialog:
            self.connection_dialog = MDDialog(
                title = ":(",
                text = "No Connection",
                buttons = [
                    MDFillRoundFlatButton(
                        text = "OK",
                        on_release = self.close_connection_dialog
                    )
                ],
            )
        
        self.connection_dialog.open()

    def close_connection_dialog(self, obj):
        self.connection_dialog.dismiss()
    
    #-------------------------------------------------------------------#
    
#    x = 0    
    
    

Main().run()






