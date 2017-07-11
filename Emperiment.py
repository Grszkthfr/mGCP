 #!/usr/bin/env python
#-*- coding: utf-8 -*- #

#(PsychoPy) Libraries I want to use
import os, csv, random, itertools, datetime
from psychopy import visual, core, event, gui #Verschiedene (5/20) Libraries von Psychopy


'''Set up'''
experimentName = "mGCP"

eveText = ""
welcomeText = u"Herzlich Willkommen!\n\nVielen Dank, dass Sie heute an unserem Versuch zur Aufmerksamkeitsverteilung teilnehmen.\nBitte bearbeiten Sie den Versuch so konzentriert und gewissenhaft wie möglich.\n\n\n\t\t\t\t\t\tWeiter mit der <Leertaste>"
instructionText1 = u"Der Versuch besteht aus mehreren Durchgängen. Zwischendurch gibt es kleine Pausen.\n\nZuerst legen Sie bitte den Zeigefinger und den Mittelfinger Ihrer dominanten Hand auf die makierten Tasten der Tastatur.\n\nLassen Sie die Finger für die Dauer des Versuchs dort.\n\n\n\t\t\t\t\t\tWeiter mit der <Leertaste>"
instructionText2 = u"Zu Beginn eines Durchganges fixieren Sie bitte das Fixationskreuz.\n\nKurz darauf werden Ihnen Gesichter präsentiert.\n\nAnschließend erscheint ein Buchstabe auf der rechten oder linken Bildschirmhälfte.\n\n\n\t\t\t\t\t\tWeiter mit der <Leertaste>"
instructionText3 = u"Erscheint ein \tE\t drücken Sie bitte die Taste, die mit dem \"E\" gekennzeichnet ist.\n\nErscheint ein \tF\t drücken Sie bitte die Taste, die mit dem \"F\" gekennzeichnet ist.\n______________________________________________________\n\nReagieren Sie bitte so schnell und so sorgfältig wie möglich.\n\nWenn Sie noch Fragen haben wenden Sie sich bitte jetzt an den Versuchsleiter.\n\nWenn Sie alles verstanden haben können Sie den Versuch mit der <Leertaste> starten.\n\nViel Spaß."
warningText = u"Bitte schneller reagieren."
pauseText = u"Pause!\n\n\nVersuch fortsetzen mit der <Leertaste>"
goodbyeText = u"Fast geschafft!\n\nBitte geben Sie dem Versuchsleiter ein leises Zeichen, dann erhalten Sie noch ein paar kurze Fragebögen.\n\n\nVielen Dank!"

cueDirectory = 'stimuli/cues/'
femaleList = [] #later liste with femaleFaces
maleList = [] #later List with maleFaces
trialList = [] #complete List of trials
trialCounter = 1 #für den Trialzähler
blockCounter = 1

#Nummer des Bildes aus dem RaFD, wichtig, damit nicht 2 Gesichter von einer Peron erscheinen
femaleFace1 = '090_' +'19'
femaleFace2 = '090_' + '26'
femaleFace3 = '090_' + '61'
maleFace1 = '090_' + '10'
maleFace2 = '090_' + '15'
maleFace3 = '090_' + '71'

#Experimentsettings
interStimuliIntervall = .500 #Interstimuli Intervall in seconds, time between appearance of cue and target
maxResponseTime = 1 #maximale time to respond to target in seconds
interTrialIntervall = (0.75, 1.25) #time in seconds between two trials, from ... to, jitter is generated
minReadingTime = 2 #mimimum time text will be presented


responseKeyE = 'u'
responseKeyF = 'n'
continueKey = "space"
quitKey = "q"


'''End of setup'''

#Creat a window
window = ""
myText = '' #required for showText-Funciton
expInfo={'Subject': ''}

########################################
############Functions###################
########################################

'''standard functions by Mario'''


def wait(seconds):
    try: number = float(seconds); core.wait(number, number) #Wait presentationTime seconds.  Maximum accuracy (2nd parameter) is used all the time (i.e. presentationTime seconds).
    except TypeError:
        jitter = random.random()*(seconds[1]-seconds[0]) + seconds[0]; core.wait(jitter, jitter)
        ##print "Jitter: %.3f sec" %(jitter); #to control for correctness



def getTimestamp(time, format='%Y-%m-%d %H:%M:%S'):
##def getTimestamp(time=core.getAbsTime(), format='%Y-%m-%d %H:%M:%S'): #doesn't work correctly because core.getAbsTime() is only called the first time
    timeNowString = datetime.datetime.fromtimestamp(time).strftime(format)
    ##print string
    return timeNowString

def getTimestampNow(format='%Y-%m-%d_%H:%M'):
    return getTimestamp(core.getAbsTime(), format)


'''my own functions'''


def prepare():
    global window
    while True:
        input = gui.DlgFromDict(dictionary=expInfo, title=experimentName)
        if input.OK==False: core.quit() #user pressed cancel
        if (expInfo['Subject'] != ''): break #if Subject field wasn't specified, display Input-Window again (i.e. don't break the loop)
    #if (expInfo['key Assignment'] != 1): keyAssignment = 0 #keyAssignment = 1: target category1 <=> responseKey1
    #if (keyAssignment == 1): instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key1>", responseKey1.upper()); instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key2>", responseKey2.upper())
    #else: instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key1>", responseKey2.upper()); instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key2>", responseKey1.upper())

    window = visual.Window([1920,1080], monitor="Office207", fullscr= True)
    event.Mouse(visible=False)



def fillList(faceList, path):
    for file in os.listdir(path):
        if file.lower().endswith(".jpg"): ##or file.lower().endswith(".png") or file.lower().endswith(".gif") or file.lower().endswith(".tif") or file.lower().endswith(".bmp"):
            faceList.append(os.path.join(path, file)) #If the file is an image file, add its relative path STARTING IN THE WORKING DIRECTORY to our list of targets
    return faceList



def writeTrialToFile(left_image, top_image, right_image, cued, left, female, target, targetPos, number_of_cues, correct, RT):
    # check if file and folder already exist
    if not os.path.isdir('data'):
        os.makedirs('data') #if this fails (e.g. permissions) you will get an error
    fileName = 'data' + os.path.sep + experimentName + '_' + expInfo['Subject'] + '.csv' #generate file name with name of the experiment and subject

    # open file
    with open(fileName, 'ab') as saveFile: #'a' = append; 'w' = writing; 'b' = in binary mode
        fileWriter = csv.writer(saveFile, delimiter=',') #generate fileWriter ... somewhat similar to java
        if os.stat(fileName).st_size == 0: #if file is empty, insert header
            fileWriter.writerow(('expName', 'subject', 'date', 'block', 'trial', 'left_face', 'top_face', 'right_face', 'cue_trial', 'left_cue', 'female_trial', 'target_E', 'target_left', 'number_of_cues', 'correct_response', 'rt'))

        #write trial
        fileWriter.writerow((experimentName, expInfo['Subject'], getTimestampNow(), blockCounter, trialCounter, left_image, top_image, right_image, cued, left, female, target, targetPos, number_of_cues, correct, RT))

        '''
        print experimentName
        print VP
        print block
        print trial
        print left_image
        print top_image
        print right_image
        print cued
        print left
        print female
        print target
        print targetPos
        print gazes
        print correct
        print RT
        '''



def showText (window, myText):
    message = visual.TextStim(window, text=myText, height=0.05)
    message.draw()
    window.flip()
    wait(minReadingTime)
    event.clearEvents()
    while True: #Participant decides when to proceed
        if event.getKeys(continueKey):
            break
        if event.getKeys(quitKey):
            core.quit()



def showTrial(left_face, top_face, right_face, cued, left, female, target, targetPos, number_of_cues): #cued, left, female & gazes not necessary for showTrial, but later to return to writeTrialToFile

        #Preparation
    FixationCross = visual.TextStim(window, text=u"+", font='Arial', pos=[0,0], height=30, units=u'pix', color='white')
    LeftImage = visual.ImageStim(window, units= 'cm', size = (75,100), pos = (-60.622, -35)) #size in mm
    #TopImage = visual.ImageStim(window, units= 'norm', size = (0.28125,0.5), pos = (0, 0.5))
    TopImage = visual.ImageStim(window, units= 'cm', size = (75,100), pos = (0, 70))
    RightImage = visual.ImageStim(window, units= 'cm', size = (75,100), pos = (60.622, -35))
    Warning = visual.TextStim(window, text=warningText, font='Arial', pos=[0,0], height=30, units=u'pix', color='white')
    reactionTime = core.Clock()


        #Target position
    if (target == '1'): #target T
        correctKey = responseKeyE
        wrongKey = responseKeyF
        if (targetPos == '1'): #target left
            Target = visual.TextStim(window, text = 'E', font = 'Arial', pos= [-.65,0])
            ##print '1'
        elif (targetPos == '0'): #target right
            Target = visual.TextStim(window, text = 'E', font = 'Arial', pos= [.65,0])
            ##print '2'
        else:
            print '>>> Error target E needs to be somewhere!!'
    elif (target == '0'): #target F
        correctKey = responseKeyF
        wrongKey = responseKeyE
        if (targetPos == '1'): #target left
            Target = visual.TextStim(window, text = 'F', font = 'Arial', pos= [-.65,0])
            ##print '3'
        elif (targetPos == '0'): #target right
            Target = visual.TextStim(window, text = 'F', font = 'Arial', pos= [.65,0])
            ##print '4'
        else:
            print '>>> Error target F needs to be somewhere!!'
    else:
        print '>>> Error, target needs to be something! ' + target

    #print 'Go!'
    FixationCross = visual.TextStim(window, text=u"+", font='Arial', pos=[0,0], height=30, units=u'pix', color='white')
    FixationCross.draw()
    window.flip()
    wait(interTrialIntervall) #1sec fixationCross prior to beginning



    LeftImage.setImage(left_face)
    LeftImage.draw()

    TopImage.setImage(top_face)
    TopImage.draw()

    RightImage.setImage(right_face)
    RightImage.draw()

    FixationCross.draw()

    window.flip()
    wait(interStimuliIntervall)

    Target.draw()
    #FixationCross.draw()
    window.flip()
    reactionTime.reset() #reactionTime starts right after Flip
    event.clearEvents()

    while (reactionTime.getTime() <= maxResponseTime): #Participant decides when to proceed, after onset of target!
        if event.getKeys(correctKey):
            correctResponse = 1
            RT = reactionTime.getTime()
            ##print 'correct'
            ##print reactionTime.getTime()
            break
        elif event.getKeys(wrongKey):
            correctResponse = 0
            RT = reactionTime.getTime()
            ##print 'NOT correct'
            ##print reactionTime.getTime()
            break
        if event.getKeys(quitKey):
            print 'quit'
            core.quit()

    while (reactionTime.getTime() > maxResponseTime): #after maxResponseTime runs out
        if (event.getKeys(correctKey)) or (event.getKeys(wrongKey)):
            correctResponse = 99
            RT = 99

            Warning.draw()
            window.flip()
            wait(1.5)

            break
        if event.getKeys(quitKey):
            print 'quit'
            core.quit()
    print blockCounter, ' ', trialCounter, ' ', str(correctResponse), ' ', str(RT)


    #print what is returned to writeTrialToFile-Function
    ##print left_face.split('\\')[-1], top_face.split('\\')[-1], right_face.split('\\')[-1], target, targetPos, correctResponse, RT)
    return writeTrialToFile(left_face.split('\\')[-1], top_face.split('\\')[-1], right_face.split('\\')[-1], cued, left, female, target, targetPos, number_of_cues, correctResponse, RT)



def TrialFromTrialListPicker(triallist, i):
    return showTrial(trialList[i][0], trialList[i][1], trialList[i][2], trialList[i][3], trialList[i][4], trialList[i][5], trialList[i][6], trialList[i][7], trialList[i][8]) #0=left_face,1=top_face,2=right_face,6=target,7=targetPosition



def Block(trials, randomize=True):
    global trialCounter, blockCounter

    if (randomize): random.shuffle(trials)
    #for i in [1,2,3,4,5,6,7,8]: #for testing
    for i in range(len(trials)): #for each trial, go to trialPicker, add +1 for Trialcounter
        TrialFromTrialListPicker(trials, i) # run trial i
        trialCounter += 1
        #print 'trialCounter: ', trialCounter

        if (trialCounter == 215) or (trialCounter == 431) or (trialCounter == 647): #Pause after mentioned trials, ewxcluding 0 it would be 224 and 448
            blockCounter += 1
            showText(window, pauseText)
            #print 'blockCounter: ', blockCounter



def run():

    prepare()

    showText (window, eveText)
    showText (window, welcomeText)
    showText (window, instructionText1)
    showText (window, instructionText2)
    showText (window, instructionText3)


    Block(trialList)

    showText (window, goodbyeText)

    #Closing Section
    window.close()
    core.quit()



############################################
############Here starts the script##########
############################################
###############Making Trials################
############################################


fillList(femaleList, cueDirectory + '/femaleFace') #stimuliListe mit femaleFace füllen
fillList(maleList, cueDirectory + '/maleFace') #stimuliliste mit maleFace füllen


temporaryTrialList = list(itertools.permutations(femaleList,3)) + list(itertools.permutations(maleList,3)) #komplette Trialliste aus den beiden (male&female) Listen mit permutation, !left-right trials sind drin + gleiche Gesichter in 1 trial!


for i in range(len(temporaryTrialList)):
    ##for j in range(len(temporaryTrialList[i])):
    x = ','.join(map(str,temporaryTrialList[i]))
    ##print x

#Ausschließen, dass in einem Trial beide Blickrichtungen drin sind, und dass gleiche Gesichter auftauchen!
    if not ('left' in x and 'right' in x) and (((femaleFace1 in x and femaleFace2 in x and femaleFace3 in x) or (maleFace1 in x and maleFace2 in x and maleFace3 in x))):

#Kodieren der Trials
        if 'female' in x and 'left' in x:

            #How many gaze cues?
            a = temporaryTrialList[i][0].count('left')
            a += temporaryTrialList[i][1].count('left')
            a += temporaryTrialList[i][2].count('left')

            x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '1', '1', '1', str(a) #cued, left, female trial, für target E, links, Anzahl an cues
            x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '1', '1', '0', str(a) #trial für target E rechts
            x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '1', '0', '1', str(a) #trial für target F links
            x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '1', '0', '0', str(a) #trial für target F rechts

            trialList.append(x1)
            trialList.append(x2)
            trialList.append(x3)
            trialList.append(x4)

            if a == 3: #without there would only 96 trials (against 288 in the other conditions)
                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)

                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)
            ##print 'female left, target left >>>>> '  + str(x1)

        elif 'female' in x and 'right' in x:

            #How many gaze cues?
            a = temporaryTrialList[i][0].count('right')
            a += temporaryTrialList[i][1].count('right')
            a += temporaryTrialList[i][2].count('right')

            x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '1', '1', '1', str(a)
            x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '1', '1', '0', str(a)
            x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '1', '0', '1', str(a)
            x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '1', '0', '0', str(a)

            trialList.append(x1)
            trialList.append(x2)
            trialList.append(x3)
            trialList.append(x4)

            if a == 3: #without there would only 96 trials (against 288 in the other conditions)
                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)

                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)
            ##print 'female right, target left >>>>> ' + str(x1)
        elif 'male' in x and 'left' in x:

            #How many gaze cues?
            a = temporaryTrialList[i][0].count('left')
            a += temporaryTrialList[i][1].count('left')
            a += temporaryTrialList[i][2].count('left')

            x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '0', '1', '1', str(a)
            x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '0', '1', '0', str(a)
            x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '0', '0', '1', str(a)
            x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '0', '0', '0', str(a)

            trialList.append(x1)
            trialList.append(x2)
            trialList.append(x3)
            trialList.append(x4)

            if a == 3: #without there would only 96 trials (against 288 in the other conditions)
                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)

                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)
            ##print 'male left, target left >>>>> ' + str(x1)
        elif 'male' in x and 'right' in x:

            #How many gaze cues?
            a = temporaryTrialList[i][0].count('right')
            a += temporaryTrialList[i][1].count('right')
            a += temporaryTrialList[i][2].count('right')

            x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '0', '1', '1', str(a)
            x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '0', '1', '0', str(a)
            x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '0', '0', '1', str(a)
            x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '0', '0', '0', str(a)

            trialList.append(x1)
            trialList.append(x2)
            trialList.append(x3)
            trialList.append(x4)

            if a == 3: #without there would only 96 trials (against 288 in the other conditions)
                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)

                trialList.append(x1)
                trialList.append(x2)
                trialList.append(x3)
                trialList.append(x4)
            ##print 'male right, target left >>>>> ' + str(x1)

        '''
        elif 'female' in x and not ('right' in x or 'left' in x):
            x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '1', '1', '1', '0'
            x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '1', '1', '0', '0'
            x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '1', '0', '1', '0'
            x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '1', '0', '0', '0'
            trialList.append(x1)
            trialList.append(x2)
            trialList.append(x3)
            trialList.append(x4)
            ##print 'female frontal, target left >>>>> ' + str(x1)
        elif 'male' in x and not ('right' in x or 'left' in x):
            x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '0', '1', '1', '0'
            x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '0', '1', '0', '0'
            x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '0', '0', '1', '0'
            x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', 'NA', '0', '0', '0', '0'
            trialList.append(x1)
            trialList.append(x2)
            trialList.append(x3)
            trialList.append(x4)
            ##print 'male frontal, target left >>>>> ' + str(x1)
        else:
            print 'Auch dieser Trial muss irgendwo hin! >>>>> ' + str(x)
        '''
    #print alle ausgeschlossenen Trials ,d.h.: left/right-Trials & mit identischen Gesichtern.
    ##else:
        ##print str(x)

print 'Amount of Trials: ', len(trialList)

c0=0
c1=0
c2=0
c3=0

for i in range(len(trialList)):
    if trialList[i][8]=='1':
        c1+=1
    elif trialList[i][8] =='2':
        c2 +=1
    elif trialList[i][8] =='3':
        c3+=1
    elif trialList[i][8] =='0':
        c0+=1
    else:
        print 'WTF?!'

print 'Trials with one gaze cue: ', c1
print 'Trials with two gaze cue: ', c2
print 'Trials with three gaze cue: ', c3
print 'Trials without gaze cue: ', c0

print 'Block', 'Trial', 'Correct', 'RT'
##j = 0 #print trial j
##print 'length of trial "' + str(j) + '" is: ' + str(len(trialList[j]))
##for i in range(len(trialList[j])):
  ##  print trialList[j][i]

############################################


run()


'''vermutlich nicht benötigt aka Resterampe

#angepasst, aber notwendig trialiste in .csv abzulegen?!?!
def writeTriallistToFile(listOfTrials):
    #if not os.path.isdir('triallist'): #exist the path?! if not...
    #    os.makedirs('triallist')
    fileName = 'triallist' + '.csv'

    with open(fileName, 'ab') as saveFile: #'a' = append; 'w' = writing; 'b' = in binary mode
        fileWriter = csv.writer(saveFile, delimiter=',')
        if os.stat(fileName).st_size == 0: #if file is empty, insert header
            fileWriter.writerow(('left_face', 'top_face', 'right_face', 'cue', 'left', 'femaleFace', 'targetT', 'targetLeft')) #1=ja
        for i in range(len(listOfTrials)):
            fileWriter.writerow(listOfTrials[i])
'''
