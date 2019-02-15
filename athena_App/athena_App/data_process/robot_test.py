import aiml
import os

class AiRobot():
    def __init__(self):
        mybot_path='./'
        self.mybot=aiml.Kernel()
        pathZ=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        print(pathZ)

        self.mybot.learn(pathZ+'/COMM_robot/std-startup.xml')
        self.mybot.learn(pathZ+'/COMM_robot/Common_conversation.aiml')

    def start(self):
        while True:
            question=input()
            print(self.mybot.respond(question))

    def dataFinder(self):

    def textProcess(self):




bot=AiRobot()
bot.start()
