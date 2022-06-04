######################       Dragon's Den       ###############################


print('')
print('-----------------------------------------------------------------------')
print("---------------------- Welcome To Dragon's Den ------------------------")
print('-----------------------------------------------------------------------')
print('')

#FRAMEWORK FUNCTION TO CALL OTHER APPLICATIONS
def main():   
    
    print('')
    stud = input("--- Are you a new to the Dragon's Den? (Yes or No) ")
    
    if stud == 'No' or stud == 'no':
        print('')
        print('---', 'Great, opening main menu')
        doWhat()
    
    if stud == 'Yes' or stud == 'yes':
        secondDoor()
        
def secondDoor():
    
    setup = input("\n -- Would you like to join the Dragon's Den? (Yes or No) ")
    
    if setup == 'Yes' or setup == 'yes':
        print('')
        print('---', "Great, lets get you signed up!")
        register()
    
    if setup == 'No' or setup =='no':
        print ('')
        print ('---', "Bye now!")
            
def doWhat():
    
    print('')
    print('---', "What do you want to do? ")
    print('')
    print('---', "Your choices are DragonsDenConnect or BlazerPath: ")
    var = input("")
    
    if var == "DragonsDenConnect" or var == "dragonsdenconnect":
        DragonsDenConnect()
    
    if var == "BlazerPath" or var == "blazerpath":
        blazerpath()
    
    else:
        print('')
        print('---','Please make an appropriate selection!')
        doWhat()

def register():
    
    f = open('userPass.txt','a')
    print('')
    
    nam = input('--- Enter your desired username: ')
    print('')
    
    pas = input('--- Enter your desired password: ')
    f.write("\n")
    f.write(nam+","+pas)
    
    print("\n *** You have been added to the server!", nam, '***')
    doWhat()
    f.close()

###############################################################################

#DICTIONARIES FOR DRAGONSDEN CONNECT
#LISTINGS (CAN ALWAYS ADD MORE)
Hobbies =  ['Gaming', 'Concerts', 'Outdoors', 'Fitness', 'Paintball']
Schools =  ['UAB', 'Auburn', 'Jeff State', 'University of Alabama', 'Online']
Fields  =  ['Medical', 'CS', 'Engineering', 'Sociology', 'Biology']
Years   =  ['Freshman', 'Sophmore', 'Junior', 'Senior', 'Graduate']

#OTHER STUDENTS #IRL WOULD PULL FROM DATABASE OF STUDENTS SIGNED INTO D.D.
Zach    =  {
'School': Schools[0], 'Field': Fields[1], 'Year': Years[1], 'Hobby': Hobbies[3]}
Edward  =  {
'School': Schools[0], 'Field': Fields[1], 'Year': Years[2], 'Hobby': Hobbies[4]}
Ragan   =  {
'School': Schools[0], 'Field': Fields[3], 'Year': Years[3], 'Hobby': Hobbies[2]}
Samuel  =  {
'School': Schools[2], 'Field': Fields[2], 'Year': Years[1], 'Hobby': Hobbies[2]}
Alosia  =  {
'School': Schools[4], 'Field': Fields[4], 'Year': Years[4], 'Hobby': Hobbies[0]}
Evelyn  =  {
'School': Schools[1], 'Field': Fields[3], 'Year': Years[0], 'Hobby': Hobbies[2]}
James   =  {
'School': Schools[1], 'Field': Fields[1], 'Year': Years[2], 'Hobby': Hobbies[3]}
Liam    =  {
'School': Schools[3], 'Field': Fields[1], 'Year': Years[4], 'Hobby': Hobbies[1]}
Emma    =  {
'School': Schools[3], 'Field': Fields[0], 'Year': Years[2], 'Hobby': Hobbies[0]}
Noah    =  {
'School': Schools[2], 'Field': Fields[0], 'Year': Years[0], 'Hobby': Hobbies[1]}

StudentList = [
Zach, Edward, Ragan, Samuel, Alosia, Evelyn, James, Liam, Emma, Noah]

MyStudentsList = []

###############################################################################

#FUNCTIONS TO TAKE INPUT FROM USER AND STORE FOR USE IN MAIN FUNCTION
def SchoolsFunction():
    
    print('')
    print('---', Schools)
    Stest = input('--- Choose from list: Which school do you attend? ')
    
    if Stest not in Schools:
        SchoolsFunction()
    
    else:
        School = Stest 
        MyStudentsList.append(School)

def FieldsFunction():
    
    print('')
    print('---', Fields)
    Ftest = input('--- Choose from list: What are you studying? ')
    
    if Ftest not in Fields:
        FieldsFunction()
    
    else:
        Field = Ftest
        MyStudentsList.append(Field)

def YearsFunction(): 
    
    print('')
    print('---', Years)
    Ytest = input('--- Choose from list: What year student are you? ')
    
    if Ytest not in Years:
        YearsFunction()
    
    else:
        Year = Ytest
        MyStudentsList.append(Year)

def HobbiesFunction(): 
    
    print('')
    print('---', Hobbies)
    Htest = input('--- Choose from list: What do you enjoy doing? ')
    
    if Htest not in Hobbies:
        HobbiesFunction()
    
    else:
        Hobby = Htest
        MyStudentsList.append(Hobby)


######################  Dragon's Den Connect    ###############################


#MAIN FUNCTION FOR CONNECT
def DragonsDenConnect():
    
    print('')
    print('-----------------------------------------------------------------------')
    print('----------------- Dragons Den Connection Application ------------------')
    print('-----------------------------------------------------------------------')
    print('')
    
    #MATCHES (STORES COUNTER FOR COMMON INTERESTS)
    SC1, SC2  = 0, 0
    SC3, SC4  = 0, 0
    SC5, SC6  = 0, 0
    SC7, SC8  = 0, 0
    SC9, SC10 = 0, 0

###############################################################################
    
    #TAKE INPUTS FROM USER AND ADD TO DICTIONARY
    SchoolsFunction()
    FieldsFunction()
    YearsFunction()
    HobbiesFunction()
    
    School = MyStudentsList[0]
    Field  = MyStudentsList[1]       
    Year   = MyStudentsList[2]
    Hobby  = MyStudentsList[3]
    
    StudentDictionary = {
    'School': School, 'Field': Field, 'Year': Year, 'Hobby': Hobby }
   
###############################################################################    
    
    if StudentList[0]['School'] == StudentDictionary['School']:
        SC1 += 1
    if StudentList[1]['School'] == StudentDictionary['School']:
        SC2 += 1
    if StudentList[2]['School'] == StudentDictionary['School']:
        SC3 += 1
    if StudentList[3]['School'] == StudentDictionary['School']:
        SC4 += 1
    if StudentList[4]['School'] == StudentDictionary['School']:
        SC5 += 1
    if StudentList[5]['School'] == StudentDictionary['School']:
        SC6 += 1
    if StudentList[6]['School'] == StudentDictionary['School']:
        SC7 += 1
    if StudentList[7]['School'] == StudentDictionary['School']:
        SC8 += 1
    if StudentList[8]['School'] == StudentDictionary['School']:
        SC9 += 1
    if StudentList[9]['School'] == StudentDictionary['School']:
        SC10 += 1

###############################################################################    

    if StudentList[0]['Field'] == StudentDictionary['Field']:
        SC1 += 1
    if StudentList[1]['Field'] == StudentDictionary['Field']:
        SC2 += 1
    if StudentList[2]['Field'] == StudentDictionary['Field']:
        SC3 += 1
    if StudentList[3]['Field'] == StudentDictionary['Field']:
        SC4 += 1
    if StudentList[4]['Field'] == StudentDictionary['Field']:
        SC5 += 1
    if StudentList[5]['Field'] == StudentDictionary['Field']:
        SC6 += 1
    if StudentList[6]['Field'] == StudentDictionary['Field']:
        SC7 += 1
    if StudentList[7]['Field'] == StudentDictionary['Field']:
        SC8 += 1
    if StudentList[8]['Field'] == StudentDictionary['Field']:
        SC9 += 1
    if StudentList[9]['Field'] == StudentDictionary['Field']:
        SC10 += 1

###############################################################################

    if StudentList[0]['Year'] == StudentDictionary['Year']:
        SC1 += 1
    if StudentList[1]['Year'] == StudentDictionary['Year']:
        SC2 += 1
    if StudentList[2]['Year'] == StudentDictionary['Year']:
        SC3 += 1
    if StudentList[3]['Year'] == StudentDictionary['Year']:
        SC4 += 1
    if StudentList[4]['Year'] == StudentDictionary['Year']:
        SC5 += 1
    if StudentList[5]['Year'] == StudentDictionary['Year']:
        SC6 += 1
    if StudentList[6]['Year'] == StudentDictionary['Year']:
        SC7 += 1
    if StudentList[7]['Year'] == StudentDictionary['Year']:
        SC8 += 1
    if StudentList[8]['Year'] == StudentDictionary['Year']:
        SC9 += 1
    if StudentList[9]['Year'] == StudentDictionary['Year']:
        SC10 += 1

###############################################################################
    
    if StudentList[0]['Hobby'] == StudentDictionary['Hobby']:
        SC1 += 1
    if StudentList[1]['Hobby'] == StudentDictionary['Hobby']:
        SC2 += 1
    if StudentList[2]['Hobby'] == StudentDictionary['Hobby']:
        SC3 += 1
    if StudentList[3]['Hobby'] == StudentDictionary['Hobby']:
        SC4 += 1
    if StudentList[4]['Hobby'] == StudentDictionary['Hobby']:
        SC5 += 1
    if StudentList[5]['Hobby'] == StudentDictionary['Hobby']:
        SC6 += 1
    if StudentList[6]['Hobby'] == StudentDictionary['Hobby']:
        SC7 += 1
    if StudentList[7]['Hobby'] == StudentDictionary['Hobby']:
        SC8 += 1
    if StudentList[8]['Hobby'] == StudentDictionary['Hobby']:
        SC9 += 1
    if StudentList[9]['Hobby'] == StudentDictionary['Hobby']:
        SC10 += 1
    
###############################################################################    
    
    CounterDictionary = {
    'Zach': SC1, 'Edward': SC2, 'Ragan': SC3,
    'Samuel': SC4, 'Alosia': SC5, 'Evelyn': SC6, 'James': SC7,
    'Liam': SC8, 'Emma': SC9, 'Noah': SC10 }
    
    MaxInterest = max(CounterDictionary, key = CounterDictionary.get)
    
    print('')
    print('--- Your Dragon Connect is: ', MaxInterest)    
    print('')
    print('*** Returning to Main Menu ***')
    doWhat()

######################  BlazerPath Application  ###############################


import os.path

###############################################################################

def blazerpath():
    
    print('')
    print('-----------------------------------------------------------------------')
    print('----------------------- BlazerPath Application ------------------------')
    print('-----------------------------------------------------------------------')
    print('')
    
    blazerpath = []
    counter = 0
    
###############################################################################    
    
    #Check for required student files
    for items in range(1):
        
        for FinancialAid in range(1):
            
            if os.path.exists("fafsa.txt"):
                blazerpath.append(1)
            
            else:
                blazerpath.append(2)
                print('')
                print("---", "Please submit FAFSA to receive award letter.")
        
        for Transcript in range(1):
            
            if os.path.exists("transcript.txt"):
                blazerpath.append(1)
            
            else:
                blazerpath.append(2)
                print('')
                print("---", "Please submit transcript to continue.")
        
        for Immunizations in range(1):
            
            if os.path.exists("immune.txt"):
                blazerpath.append(1)
            
            else:
                blazerpath.append(2)
                print('')
                print("---", "Please submit immunizations to continue.")
        
        for Orientation in range(1):
            attended=input(
            "--- Did student attend orientation? Enter, Yes or No: ")
            
            if attended == "Yes" or "yes":
                blazerpath.append(1)
            
            else:
                blazerpath.append(2)
                print('')
                print("---", 
                "Must attend orientation before registering for classes.")
            
            for Registration in range(1):
               
                if os.path.exists("registration.txt"):
                    blazerpath.append(1)
                
                else:
                    blazerpath.append(2)
                    print('')
                    print("---", "Increase your knowledge and choose a class.")    
        
###############################################################################        
        
        #Add up until the number = the required items
        for i in blazerpath:
            
            if i == 1:
                counter += 1

###############################################################################  
    
    #checking what you have to see if you've met the requirements
    if counter == len(blazerpath):
        print('')
        print('---', "You have completed all necessary requirements!")
        print('')
        print("---", "Welcome to the Dragons Den! <ARRRRGGGHHHHH!!!!")
        print('')
        print('*** Returning to Main Menu ***')
        doWhat()
    
    elif counter == 0:
        print('')
        print('---', "You are missing all necessary requirements")
        print('')
        print("---", "Time to start your path to being a blazer.")
        print('')
        print('*** Returning to Main Menu ***')
        doWhat()
    
    else:
        print('')
        print('---', 'You have met some of the necessary requirements.')
        print('')
        print("---", "You're almost a blazer, don't give up!")
        print('')
        print('*** Returning to Main Menu ***')
        doWhat()

###############################################################################

#Framework (main) Function Call
main()              

    
            

    

