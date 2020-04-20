from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from kivy.properties import NumericProperty

class BankerWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    players = dict()

    tcheckin = 0
    il = 0
    ob = 0
    cb = 0
    def StartGame(self):
        try:
            self.il = int(self.ids.initialload.text)
            self.ob = int(self.ids.openbal.text)
            self.cb = self.ob
            self.ids.currentamt.text = str(self.cb)
            self.ids.initialload.text = 'Player Initial Load: '+str(self.il)
            self.ids.openbal.text = 'Bank Opening Bal: ' + str(self.ob)
            self.ids.initialload.background_color = (1, 0, 0, .5)
            self.ids.openbal.background_color = (1, 0, 0, .5)
            self.ids.openbal.readonly = True
            self.ids.initialload.readonly = True
            self.ids.addplayerbtn.disabled = False
        except:
            content = Button(text='OK')
            popup = Popup(title='Enter Numbers for Amount',content=content, size_hint=(None, None),size=(450,450))
            popup.open()
            content.bind(on_press=popup.dismiss)

    def AddPlayer(self):
        if len(self.ids.player.text)>0:
            if self.ids.player.text not in self.players.keys():
                self.players[self.ids.player.text] = [[self.il],[],-self.il]
                self.cb = self.cb - self.il
                if self.cb>self.ob or self.cb<0:
                    self.ids.currentamt.color = (1, 0, 0, .5)
                else:
                    self.ids.currentamt.color = (1, 1, 1, 1)
                self.ids.currentamt.text = str(self.cb)
        self.Print()
        self.ids.amount.text = ''
        self.ids.splayerbtn.disabled = False

    def EndGame(self):
        diff=0
        for z in self.players:
            diff += self.players[z][2]
        if diff>0:
            self.ids.score.text += 'To compensate the difference:(+' + str(diff) + '),\neach player should pay: '+str(((diff)/len(self.players)))+'\n'
        elif diff<0:
            self.ids.score.text += 'To compensate the difference:(-' + str(diff) + '),\neach player should receive: '+str(((diff)/len(self.players))*-1)+'\n'
        else:
            self.ids.score.text += 'Well played guys! 3 cheers to Banker\n'


    def Print(self):
        self.ids.player.text = ''
        self.ids.score.text = 'Player : [CheckOut,CheckIn,Total]\n'
        for x in self.players:
            self.ids.score.text = self.ids.score.text + x + " : " + str(self.players[x]) + '\n'



    def CheckOut(self):
        if(len(self.ids.amount.text)>0 and self.ids.splayerbtn.text != 'Select the Player'):
            pvalue = self.players[self.ids.splayerbtn.text]
            try:
                pvalue[0].append(int(self.ids.amount.text))
                tcheckout = 0
                tcheckin = 0
                for i in pvalue[0]:
                    tcheckout = tcheckout + i
                for j in pvalue[1]:
                    tcheckin = tcheckin + j
                ptotal = tcheckin - tcheckout
                pvalue[2] = ptotal
                self.players[self.ids.splayerbtn.text] = pvalue
                self.Print()
                self.cb = self.cb - int(self.ids.amount.text)
                self.ids.currentamt.text = str(self.cb)
                if self.cb>self.ob or self.cb<0:
                    self.ids.currentamt.color = (1, 0, 0, .5)
                else:
                    self.ids.currentamt.color = (1, 1, 1, 1)
                self.ids.amount.text = ''
            except:
                content = Button(text='OK')
                popup = Popup(title='Enter Numbers for Amount',content=content, size_hint=(None, None),size=(450,450))
                popup.open()
                content.bind(on_press=popup.dismiss)


    def CheckIn(self):
        if(len(self.ids.amount.text)>0 and self.ids.splayerbtn.text != 'Select the Player'):
            print("text on button", self.ids.splayerbtn.text)
            pvalue = self.players[self.ids.splayerbtn.text]
            try:
                pvalue[1].append(int(self.ids.amount.text))
                tcheckout = 0
                tcheckin = 0
                for a in pvalue[0]:
                    tcheckout = tcheckout + a
                for b in pvalue[1]:
                    tcheckin = tcheckin + b
                ptotal = tcheckin - tcheckout
                pvalue[2] = ptotal
                self.players[self.ids.splayerbtn.text] = pvalue
                self.Print()
                self.cb = self.cb + int(self.ids.amount.text)
                self.ids.currentamt.text = str(self.cb)
                if self.cb>self.ob or self.cb<0:
                    self.ids.currentamt.color = (1, 0, 0, .5)
                else:
                    self.ids.currentamt.color = (1, 1, 1, 1)
                self.ids.amount.text = ''
            except:
                content = Button(text='OK')
                popup = Popup(title='Enter Numbers for Amount',content=content, size_hint=(None, None),size=(450,450))
                popup.open()
                content.bind(on_press=popup.dismiss)


    def DropDown(self):
        dropdown = DropDown()
        for index in self.players:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.
            btn = Button(text='%s' % index, font_size=40, size_hint_y=None,height=60)
            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            # then add the button inside the dropdown
            dropdown.add_widget(btn)
        # create a big main button
        #mainbutton = Button(text='Hello', size_hint_y= None, height=44)
        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        #self.ids.addplayerbtn.bind(on_release=dropdown.open)
        dropdown.open(self.ids.splayerbtn)
        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        dropdown.bind(on_select=lambda instance, x: setattr(self.ids.splayerbtn, 'text', x))
        #print(mainbutton.text)
        #runTouchApp(mainbutton)
        self.ids.checkoutbtn.disabled = False
        self.ids.checkinbtn.disabled = False


class BankerApp(App):
    def build(self):
        #self.title = Banker
        self.icon = 'museum.png'
        return BankerWidget()



if __name__=="__main__":
    BankerApp(title="Banker-3patti").run()
