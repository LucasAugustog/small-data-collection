import wx
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
import time
import datetime
from bs4 import BeautifulSoup, element
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlopen


#tips for connecting to a database
#https://docs.sqlalchemy.org/en/20/core/engines.html
#engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")


engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/base")
Base = declarative_base()
conn = engine.connect()
Session = sessionmaker(bind=engine)
Session = Session()


class Users(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.username}, {self.password}]"
    

class Games(Base):
    __tablename__ = "games" 

    team = Column(String, primary_key=True)
    points = Column(Integer, nullable=False)

   


class LoginDialog(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, None, title="Login", size=(250, 300))
        self.logged_in = False
        

        # user info
        front_user = wx.BoxSizer(wx.HORIZONTAL)
        user_label = wx.StaticText(self, label="Username:")
        front_user.Add(user_label, 0, wx.ALL|wx.CENTER, 5, )
        self.quest_user = wx.TextCtrl(self)
        front_user.Add(self.quest_user, 0, wx.ALL, 5|wx.CENTER, 5)

        # pass info
        front_pass = wx.BoxSizer(wx.HORIZONTAL)
        pass_label = wx.StaticText(self, label="Password:", pos = (20, 20))
        front_pass.Add(pass_label, 0, wx.ALL|wx.CENTER, 5)
        self.quest_password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.quest_password.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        front_pass.Add(self.quest_password, 0, wx.ALL, 5)
        
        front_main = wx.BoxSizer(wx.VERTICAL)
        front_main.Add(front_user, 0, wx.ALL, 5)
        front_main.Add(front_pass, 0, wx.ALL, 5)
        
        button = wx.Button(self, label="Login")
        button.Bind(wx.EVT_BUTTON, self.onLogin)
        front_main.Add(button, 0, wx.ALL|wx.CENTER, 10)
       
        self.SetSizer(front_main)
        
    def onLogin(self, event):
        
        user_password = self.quest_password.GetValue()
        user_pass = self.quest_user.GetValue()

        data = Session.query(Users).all()
        
        x = 0
        y = len(data)

        while x < y:
            correct_password = data[x].password
            correct_username = data[x].username

            correct_password = str(correct_password)
            correct_password = correct_password.replace(' ', '')
            correct_username = str(correct_username)
            correct_username = correct_username.replace(' ', '')

            if user_password == correct_password and user_pass == correct_username:
                self.logged_in = True
                self.Close()
                break   
            x += 1

        if(x == y):
            c = wx.BoxSizer(wx.HORIZONTAL)
            d = wx.StaticText(self, label="incorrect credentials!", pos=(60, 140))
            
           
class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        

    

class MainFrame(wx.Frame):
    def __init__(self, parent=None, title="Demonstration of small data collection"):
        super(MainFrame, self).__init__(parent, title=title, size = (600, 500))

        panel = MyPanel(self)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(self, label = "Status: Information Not Collected")
        

        sizer.Add(self.label, 1, wx.EXPAND)

        self.btn = wx.Button(self, label = "START")
        sizer.Add(self.btn, 0)
        self.btn.Bind(wx.EVT_BUTTON, self.onClickMe)

        self.SetSizer(sizer)
        

      
    
        
        dlg = LoginDialog()
        dlg.ShowModal()
        authenticated = dlg.logged_in
        if not authenticated:
            self.Close()
        
        self.Show()
        


    def onClickMe(self, event):
        self.label.SetLabelText("Status: Collecting Information")
        self.label.SetBackgroundColour( wx.Colour( 170, 237, 152 ) )
        
        html_content = "https://pt.global.nba.com/boxscore/0042200405/"
        
        option = Options()
        option.headless = True
        driver = webdriver.Firefox() 

        driver.get(html_content)
        time.sleep(1)

        act = ActionChains(driver)

        p = 1
        l = 0
        while l <= p:
            act.send_keys(Keys.PAGE_UP).perform()
            time.sleep(0.1)
            act.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.1)
            act.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.1)
            act.send_keys(Keys.PAGE_UP).perform()
            time.sleep(0.1)
            act.send_keys(Keys.PAGE_UP).perform()
            time.sleep(0.1)
            l += 1


        time.sleep(1)
        element = driver.find_element(By.XPATH, "/html/body")

        html_content = element.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')

        PointsA = soup.find_all('div', class_='GamesHeader_homeScore__Hvc6F')
        PointsA = str(PointsA)
        PointsA = PointsA.replace('[<div class="GamesHeader_homeScore__Hvc6F" data-cy="team-score"><span>','')
        PointsA = PointsA.replace('</span></div>]','')

        PointsB = soup.find_all('div', class_='GamesHeader_awayScore__mcVD_')
        PointsB = str(PointsB)
        PointsB = PointsB.replace('[<div class="GamesHeader_awayScore__mcVD_" data-cy="team-score"><span>','')
        PointsB = PointsB.replace('</span></div>]','')


        nameTeamA = soup.find_all('span', class_='GamesHeader_fullTeamName__y2m3P')
        nameTeamA = str(nameTeamA)
        nameTeamA = nameTeamA.replace('[<span class="GamesHeader_fullTeamName__y2m3P"><div data-cy="team-city">Miami</div><div data-cy="team-name">Heat (A)</div></span>, <span class="GamesHeader_fullTeamName__y2m3P"><div data-cy="team-city">','')
        nameTeamA = nameTeamA.replace('</div><div data-cy="team-name">','')
        nameTeamA = nameTeamA.replace('</div></span>]','')
       

        nameTeamB = soup.find_all('span', class_='GamesHeader_fullTeamName__y2m3P')
        nameTeamB = str(nameTeamB)
        nameTeamB = nameTeamB.replace('[<span class="GamesHeader_fullTeamName__y2m3P"><div data-cy="team-city">','')
        nameTeamB = nameTeamB.replace('</div><div data-cy="team-name">',' ')
        nameTeamB = nameTeamB.replace('</div></span>, <span class="GamesHeader_fullTeamName__y2m3P"><div data-cy="team-city">Denver Nuggets (H)</div></span>]','')


        driver.quit()

        self.label.SetLabelText("Status: Information Collected with success")
        self.label.SetBackgroundColour( wx.Colour( 170, 237, 152 ) )
        
        sizerInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.showInformations = wx.StaticText(self, label = "Show collected information", pos=(40, 120))
        self.showInformations.SetBackgroundColour( wx.Colour( 170, 237, 152 ) )

        sizerInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.showTeamA = wx.StaticText(self, label = "Team "+nameTeamA+" Points:"+PointsA, pos=(60, 140))
        self.showTeamA.SetBackgroundColour( wx.Colour( 170, 237, 152 ) )

        sizerInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.showTeamB = wx.StaticText(self, label = "Team "+nameTeamB+" Points:"+PointsB, pos=(60, 160))
        self.showTeamB.SetBackgroundColour( wx.Colour( 170, 237, 152 ) )
        
        data_insert = Games(team=nameTeamA, points=PointsA)
        Session.add(data_insert)
        Session.commit()

        data_insert = Games(team=nameTeamB, points=PointsB)
        Session.add(data_insert)
        Session.commit()

        sizerInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.DataBaseInfo = wx.StaticText(self, label = "Information added to database successfully", pos=(40, 200))
        self.DataBaseInfo.SetBackgroundColour( wx.Colour( 170, 237, 152 ) )
        


       






if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()