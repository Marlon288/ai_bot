
from shutil import move
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import ait
import tkinter as tk
import re
import random
import os
import math
from time import sleep

clear = lambda: os.system('cls')
clear()


def start(searchArtist):  
    def set_viewport_size(driver, width, height):
            window_size = driver.execute_script("""
                return [window.outerWidth - window.innerWidth + arguments[0],
                window.outerHeight - window.innerHeight + arguments[1]];
                """, width, height)
            driver.set_window_size(*window_size)

    def moveTo(currPos, element):
    
       
        location = element.location
        print(location)
        endX = location.get("x")
        endY = location.get("y")


        location = currPos.location
        currX = location.get("x")
        currY = location.get("y")
        absCurrX = lambda: currX + 15
        absCurrY = lambda: currY + 135

        n = 40

        c1 = 1.2
        c2 = 1.2
        fitnessX = lambda x : abs(x[0] - endX) 
        fitnessY = lambda x : abs(x[1] - endY)

        def globalBest(x):
            min = [[fitnessX(x[0][3]), 0],[fitnessY(x[0][3]), 0]]
            
            for index, item in enumerate(x):
                if(fitnessX(item[3]) < min[0][0]):
                    min[0][0] = fitnessX(item[3])
                    min[0][1] = index
                if(fitnessY(item[3]) < min[1][0]):
                    min[1][0] = fitnessY(item[3])
                    min[1][1] = index
            return [min[0][1], min[1][1]]


        #v = lambda x, best, pR1, pR2: weight*x[2]  +  c1 * pR1 * (x[3][0] + x[3][1] - (x[0] + x[1])) + c2 * pR2 * ((best[0] + best[1]) - (x[0] + x[1]))
    
        vX = lambda x, best, pR1, pR2, weightX: weightX*x[2][0]  +  c1 * pR1 * (x[3][0] - x[0]) + c2 * pR2 * (best[0] - x[0])
        vY = lambda x, best, pR1, pR2, weightY: weightY*x[2][1]  +  c1 * pR1 * (x[3][1] - x[1]) + c2 * pR2 * (best[1] - x[1])
        particles = [[random.uniform(currX - 2.5, currX + 2.5), random.uniform(currY - 2.5, currY + 2.5), [abs(currX - endX)*0.05,abs(currY - endY)*0.05] , [0,0]] for i in range(n)]
        for var in particles:
            var[3] = [var[0], var[1]]
        
        best = globalBest(particles)
        i = 0
        print(endX)
        print(endY)

        #weight = lambda x : -2.982815587859 * 10**-7 * x**2 + 0.00104466*x + 0.294669 # Good for close bad for far away elements
        #weight = lambda x : -7.854350840830 *10**-7 *x**2+0.00238708*x+0.339846 #Amazing for medium far away elements 
        #weight = lambda x : -1.7303264931989 *10**-7 * x**2+0.00106014*x+0.528749 #Good for medium far away, but when closer to element takes to long
        #weight = lambda x : -4.121133567736*10**-8*x**2+0.000738568*x+0.657843 #Good for medium far away, but when closer to element takes to long but shoerter than the above,
        #weight = lambda x : 8.328423506398*10**-10*x**2+0.000597812*x+0.768315 #Does not work good, nice start but overflew the goal and went into negative territory
        #weight = lambda x : -2.1710420994303*10**-7*x**2+0.00116544*x+0.48938 #Does not work good, closer objects dont work well
        #weight = lambda x : 0.110343 * math.log(64.4087*x-1661.65)-0.153561 #Worked alright but issue with negative number in log
        #weight = lambda x : -3.440860214531*10**-6*x**2+0.00245161*x+0.466667 #Did not work at all stuck at element which is far away
        weight = lambda x : 0.0719644*(x**0.30423)+0.468071 #Works very good 
        # weight = lambda x, i : 7.75723*(x**0.0169864) -7.59032 if(i < 15) else 0.7 #Worked very well, fast in close and fast in far away elements
        # weight = lambda x, i : 7.75723*(x**0.0169864) -7.59032 if(i < 10) elseif(x > 100) 1 else if(x > 50) 0.5

        
        
        
        
        xFound = False
        yFound = False

        while not xFound or not yFound:
            r1 = random.random()
            r2 = random.random()  
            xW = weight(abs(currX - endX))
            yW = weight(abs(currY - endY))
            print("Weight X = " + str(xW) + " Weight Y = " + str(yW))
            for var in particles:
                #fit = fitness(var)
                
                if not xFound:
                    fitX = fitnessX(var)
                    if fitX < fitnessX(var[3]):
                        var[3][0] = var[0]
                    vXValue = vX(var, particles[best[0]], r1, r2, xW)
                    
                
                    var[0] = var[0] + vXValue
                    var[2][0] = vXValue
                if not yFound:
                    fitY = fitnessY(var)
                    if fitY < fitnessY(var[3]):
                        var[3][1] = var[1]
                    vYValue = vY(var, particles[best[1]], r1, r2, yW)
                    var[1] = var[1] + vYValue
                    var[2][1] = vYValue  
                
                

            best = globalBest(particles)
            old = [currX, currY]
            currX = particles[best[0]][0]
            currY = particles[best[1]][1]

            print("OFFSET: "+ str(currX - old[0]) + " " + str(currY - old[1]))

            i += 1
            if(currX - endX < 2 and currX - endX > 0): xFound = True
            if(currX - endX < 2 and currX - endX > 0): yFound = True
            ait.move(absCurrX(), absCurrY())
            sleep(0.05)
      
        return element

    similarArtists = set([])
    
    def validateAndFitness(title):
        #Example valid song: 
        # TRETTMANN FEAT. ALLI NEUMANN - ZEIT STEHT - PROD. KITSCHKRIEG (OFFICIAL VIDEO)
        # TRETTMANN - GRAUER BETON (prod. KITSCHKRIEG) (OFFICIAL VIDEO)
        # Major Lazer & DJ Snake - Lean On (feat. MØ) (Official Music Video)
        # DJ Khaled - BODY IN MOTION (Official Lyric Video) ft. Bryson Tiller, Lil Baby, Roddy Ricch
        #Evaluation
        #   From searchArtist + 10
        #   SearchArtist that is in feature + 7
        #   produced from someone the artist was produced or someone the artist had a feature with +3,


        fitness = 0
        if "official" not in title.lower():
            return 0
        try:
            splitted = title.split("-")
            if len(splitted) != 2:
                return fitness
            artists = re.split('feat.|feature| x | & |ft.|, ', splitted[0].lower())
            
            sA = False
            
            names = re.split('feat.|feature|ft.|\(|prod.', splitted[1].lower(), maxsplit=1)
            
            artists = artists + re.split("feat.|feature| x | & |ft.|, |prod.|\(", names[1].lower())
            
            artists = [x for x in artists if "official" not in x]
            
            for count, item in enumerate(artists):
                artists[count] = re.sub('\)|\(', '', artists[count]).strip()
                if artists[count] in similarArtists and not sA:
                    fitness = 3
                if artists[count] == searchArtist.lower():
                    fitness = 7
                    sA = True

            if artists[0] == searchArtist.lower():
                fitness = 10
                sA = True
            
            if sA:
                for item in artists:
                    
                    if(item != "" and "lyric" not in item):
                        similarArtists.add(item)
        except:
            fitness = 0
        return fitness

    #Proccess time out of aria-label 
    #Example1 1 minute funny videos by MEMES HUB 1 year ago 1 minute 10 seconds 93,484 views
    #Example2 1 minute funny videos by MEMES HUB 1 year ago 10 seconds 93,484 views
    def getTime(label):
        try:
            split = label.split("ago") #split[-1] =  1 minute 10 seconds 93,484 views # 10 seconds 93,484 views # 10 minutes 93,434 views
            split[-1] = re.sub(",", "", split[-1])
            split = split[-1].split("second") #split = {1 minute 10 , s 93,484 views} # 10, s 93,484 views
        
            if len(split) > 1:
                split =  split[0].split("minute")
                if(len(split) == 1):       # {1 , 10}
                    seconds = split[0].strip()
                    minutes = 0
                else: 
                    split[0] = re.sub('s', '', split[0]).strip() # {1, 10}
                    split[1] = re.sub('s', '', split[1]).strip() # {1, 10}
                
                    minutes = split[0]
                    seconds = split[1]
            else:
                minutes = split[0].strip().split("minute")[0].strip()
                seconds = 0
            return int(minutes) * 60 + int(seconds) 
        except:
            return 0
            

            

        
    PATH = r"C:\Users\marlo\ai_bot\drivers\chromedriver.exe"
    URL = "https://www.youtube.com/"
    ADDBLPATH = r"C:\Users\marlo\ai_bot\drivers\4.46.0_0"

    queue = []
    allSongs = []
    
    #Setup for starting page
    chop = webdriver.ChromeOptions()
    chop.add_argument("--load-extension="+ADDBLPATH)
    

    driver = webdriver.Chrome(PATH, options=chop)

    driver.set_page_load_timeout(10)
    driver.get(URL)


    #set_viewport_size(driver, 1400, 900)
    driver.switch_to.window(driver.current_window_handle)
    driver.set_window_position(0, 0)
    actions = ActionChains(driver)
    

    currPos = driver.find_element_by_xpath("/html[1]/body[1]/ytd-app[1]/div[1]/div[1]/ytd-masthead[1]/div[3]/div[1]/ytd-topbar-logo-renderer[1]/a[1]/div[1]/ytd-logo[1]/yt-icon[1]")
    currPos = moveTo(currPos, driver.find_element_by_xpath("/html[1]/body[1]/ytd-app[1]/div[1]/div[1]/ytd-masthead[1]/div[3]/div[2]/ytd-searchbox[1]/form[1]/div[1]/div[1]/input[1]"))
    ait.click()
    sleep(0.9)
    ait.write(searchArtist)
    currPos = moveTo(currPos, driver.find_element_by_xpath("/html[1]/body[1]/ytd-app[1]/div[1]/div[1]/ytd-masthead[1]/div[3]/div[2]/ytd-searchbox[1]/button[1]/yt-icon[1]"))
    ait.click()
    print("click")
    driver.get(driver.current_url)
    elements = driver.find_elements_by_id("video-title")
    link = ""
    while(True):
        for el in elements:
            time = getTime(el.get_attribute("aria-label"))
            if time > 90 and time < 300:
                fitness = validateAndFitness(el.get_attribute("title"))
                if fitness > 0:
                    exists = False
                    for q in allSongs:
                        if q[3] == el.get_attribute("title"): exists = True
                    if not exists:
                        if link == "":
                            queue.append([fitness, el.get_attribute("href"), time, el.get_attribute("title")])
                            allSongs.append([fitness, el.get_attribute("href"), time, el.get_attribute("title")])
                        else:
                            grandParent = el.find_element_by_xpath("./..").find_element_by_xpath("./..")
                            queue.append([fitness,grandParent.get_attribute("href"), time,el.get_attribute("title")])
                            allSongs.append([fitness,grandParent.get_attribute("href"), time,el.get_attribute("title")])

        index = random.choices(population=range(len(queue)),k=1, weights=[x[0] for x in queue])[0]
        try:
            driver.get(str(queue[index][1]));
            if link == "" :
                link = queue[index][1]
        except:
            driver.get(link)
        sleep(2)
        ait.write("f")
        sleep(queue[index][2]-5) #Sleep as long as the video plays
        #sleep(15)
        ait.write("f")
        del queue[index]
        
        if len(queue) == 0:
            print("There were no more available songs found")
            break;
        elements = driver.find_elements_by_id("video-title")   
        print("Length of queue: " + str(len(queue)))
        print(similarArtists)
        for el in queue:
            print(el[3])
    
    ait.click();
    


    



root = tk.Tk()
root.title("AI Presentation")


#Elements for the GUI
canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

label1 = tk.Label(root, text='Stream an artist on youtube')
label1.config(font=('helvetica', 20))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Type your Artist:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root) 
canvas1.create_window(200, 140, window=entry1)


def getStarted():
        search = entry1.get()
        start(search)

        label3 = tk.Label(root, text= search + ' is playing right now',font=('helvetica', 10))
        canvas1.create_window(200, 210, window=label3)


button1 = tk.Button(text='Start radio', command=getStarted, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()


        





             

        
            
            