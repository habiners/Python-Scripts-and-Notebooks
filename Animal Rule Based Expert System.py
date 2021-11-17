# Two classes
# A rule class
# A Knowledge base class which contains the rules

# Inference engine method/function, which is mainly a while loop for forward chaining
# Why Forward chaining? Because we are inferring based on the information on the animal

class Fact:
    def __init__(self, *facts):
        self.fact = list(facts)
        self.inferredFacts = dict()

    def addFact(self, fact):
        # MEH
        # obj = fact.split("=")[0]
        # val = fact.split("=")[1]
        # if(len(obj) and len(val)): 
        #     existingObj = False
        #     for item in self.fact:
        #         if(obj == item.split("=")[0]):
        #             existingObj = True
        #     if(not existingObj):
        #         self.fact.append(fact)
        if(fact not in self.fact):
            self.fact.append(fact)

    def addInferredFact(self, key, fact): 
        self.addFact(fact)
        # if(fact not in self.fact):
        #     self.fact.append(fact)
        if(key not in self.inferredFacts):
            self.inferredFacts[key] = list()
        if(fact not in self.inferredFacts[key]):
            self.inferredFacts[key].append(fact)
            for concs in self.inferredFacts[key]:
                print("Test: " + concs) # Sakto ra

    def printFacts(self):
        allFacts = "Facts: [ "
        for facts in self.fact:
            allFacts += facts + ", "
        print(allFacts + "]")

    def printInferredFacts(self): #dictionary
        allFacts = "Inferred Facts: [ "
        for inferredFactsInd in self.inferredFacts:
            for inferredFacts in self.inferredFacts[inferredFactsInd]:
                    allFacts += inferredFacts + ", "
        print(allFacts + "]")

    def printConclusion(self):
        highestLevel = 0
        for keys in self.inferredFacts:
            # print(keys)
            if(highestLevel < int(keys)):
                highestLevel = int(keys)
        # print(highestLevel)
        if(highestLevel > 0): # Inference was made
            if len(self.inferredFacts[str(highestLevel)]) == 1:
                print("Conclusion: " + self.inferredFacts[str(highestLevel)][0] + " ")
            else:
                conclusions = "Multiple inferences; Could be: "
                for inferences in self.inferredFacts[str(highestLevel)]:
                    conclusions += inferences + "; "
                print(conclusions)
        else:
            print("Inference could not be made: either no matches, or insufficient facts")

    def getConclusion(self):
        highestLevel = 0
        for keys in self.inferredFacts:
            # print(keys)
            if(highestLevel < int(keys)):
                highestLevel = int(keys)
        print(highestLevel)

        if(highestLevel == 0):
            return "Inference could not be made: either no matches, or insufficient facts"

        if len(self.inferredFacts[str(highestLevel)]) == 1:
            return self.inferredFacts[str(highestLevel)][0]
        else:
            conclusions = "Could be: "
            for inferences in self.inferredFacts[str(highestLevel)]:
                conclusions += inferences + "; "
            return conclusions
        
class Rule:
    def __init__(self, *condition, conclusion, level):
        self.condition = list(condition)
        self.conclusion = conclusion
        self.isFired = False # If true, means na gamit na
        self.level = level # Level or Priority of Inference, Higher means bigger
        self.asked = 0

    def print(self):
        print(self.condition)
        print(self.conclusion)

    def appendWithCondList(self, listConditions):
        self.condition = list()
        for conds in listConditions:
            # print(conds)
            self.condition.append(conds)

    def checkRule(self, facts): # Returns true if rule is fired
        for fact in facts.fact:
            print(fact + " " + self.condition)
            if(fact not in self.condition):
                return False

        return True

#Contains a list of rules
class KnowledgeBase: 
    def __init__(self):
        self.rules = list() 
        self.ruleWasFired = True # Is true if a rule was fired in a cycle

    def clearFired(self):
        for rule in self.rules:
            rule.isFired = False

    def clearAsked(self):
        for rule in self.rules:
            rule.asked = 0

    def updatePriority(self):
        for rule in self.rules:
            for condition in rule.condition:
                for otherRules in self.rules:
                    if(condition in otherRules.conclusion):
                        rule.level = int(otherRules.level) + 1

    def addRuleOld(self, *condition, conclusion, level):
        self.rules.append(Rule(*condition, conclusion=conclusion, level=level))    

    def addRule(self, *condition, conclusion):
        self.rules.append(Rule(*condition, conclusion=conclusion, level=1))
        self.updatePriority()
        self.rules.sort(key=lambda e: int(e.level), reverse=True)    

    def addRuleList(self, listConditions, conclusion):
        rule = Rule("", conclusion=conclusion, level=1)
        rule.appendWithCondList(listConditions)
        self.rules.append(rule)    
        self.updatePriority()
        self.rules.sort(key=lambda e: int(e.level), reverse=True)    

    def getRules(self):
        rules = ""
        cnt = 1
        for rule in self.rules:
            rules += "Rule #" + str(cnt) + ":  Condition(s): "
            for cond in rule.condition:
                rules += cond + ", "
            rules += "\n\tConclusion: " + rule.conclusion + "\n"
            cnt += 1
        return rules

    def printRules(self):
        print("Rules:")
        x = 1
        for ruleNode in self.rules:
            rl = "Condition(s):"
            for conds in ruleNode.condition:
                rl += " " + conds + ", "
            rl = "Rule: #{} [Priority: {}; " + rl + "; Conclusion: " + ruleNode.conclusion + "]"
            print(rl.format(x, ruleNode.level))
            x += 1                            

#Forward Chaining
def inferenceEngine(knowledgeBase, facts):
    knowledgeBase.ruleWasFired = True
    while knowledgeBase.ruleWasFired:
        knowledgeBase.ruleWasFired = False
        for rule in knowledgeBase.rules:
            allCondsInFacts = True
            ruleLevel = str(rule.level) # Key for dictionary
            for condition in rule.condition: # Checks if all the conditions inside the rule are in facts and if rule has not been fired
                if(condition in facts.fact and not rule.isFired):
                    pass
                    # print("Condition found in fact! Name: " + condition)
                else:
                    allCondsInFacts = False
                    # print("Condition not found in fact :( " + condition)
            if(allCondsInFacts):
                rule.isFired = True
                knowledgeBase.ruleWasFired = True
                # print("A rule was fired! Rule: " + listToString(rule.condition) + " " + rule.conclusion)
                facts.addFact(rule.conclusion)
                # if(ruleLevel in facts.inferredFacts):
                #     facts.inferredFacts[ruleLevel] += ", " + rule.conclusion                    
                # else:
                facts.addInferredFact(ruleLevel, rule.conclusion)

    # Debugging Purposes
    facts.printFacts()
    facts.printInferredFacts()
    facts.printConclusion()

    knowledgeBase.clearFired()
    knowledgeBase.clearAsked()
    return facts.getConclusion()

# Miscellaneous Functions
def listToString(list):
    result = "( "
    for item in list:
        result += item + ", "
    return result + " )"

import tkinter as tk

def generateGUI(kb, facts, mydb):
    def switchScreens(prevFrame, nextFrame):
        padding = 10
        prevFrame.grid_forget()
        nextFrame.grid(row=0, column=0, padx=padding, pady=padding, ipadx=padding, ipady=padding, sticky=tk.NSEW)

    def addFact(fact):
        cleanFact = fact.strip()
        if(cleanFact != "" and "=" in cleanFact):
            facts.addFact(cleanFact)
            message_facts = tk.Message(master=frame, text=listToString(facts.fact), width=360)
            message_facts.grid(row=3, column=0, padx=padding, pady=5, ipadx=padding, columnspan=7, rowspan=3, sticky=tk.NSEW)
        else:
            label_disp.config(text="Error: Invalid Input")

    def addRule(conditions, conclusion):
        tokenizedConditions = conditions.split(",")
        for i in range(len(tokenizedConditions)):
            tokenizedConditions[i] = tokenizedConditions[i].strip()
            if "=" not in tokenizedConditions[i]:
                message_rules.config(state="normal")
                message_rules.insert(tk.END, "Error: Invalid Input")
                message_rules.config(state="normal")
                return
        # print(tokenizedConditions)
        # print(conclusion)
        cleanConclusion = conclusion.strip()
        if "=" not in cleanConclusion:
            message_rules.config(state="normal")
            message_rules.insert(tk.END, "Error: Invalid Input")
            message_rules.config(state="normal")
            return

        if(len(tokenizedConditions) > 0 and tokenizedConditions[0] != "" and cleanConclusion != ""):
            print("Do it.")
            kb.addRuleList(tokenizedConditions, conclusion=cleanConclusion)
            ruleList = kb.getRules()
            message_rules.config(state="normal")
            message_rules.delete(1.0, tk.END)
            message_rules.insert(tk.END, ruleList)
            message_rules.config(state="disabled")
            if(mydb):
                mycursor = mydb.cursor()
                sql = "INSERT INTO CONSEQUENT (consequent, createdAt) VALUES ('"+ cleanConclusion +"', now());"
                mycursor.execute(sql)
                mydb.commit()
                print("Consequent inserted, ID:", mycursor.lastrowid)
                consequentID = mycursor.lastrowid

                for item in tokenizedConditions:
                    sql = "INSERT INTO ANTECEDENT (consequentID, antecedent, createdAt) VALUES (" + str(consequentID) + ", '" + item +"', now());"
                    mycursor.execute(sql)
                    mydb.commit()
                    print("Antecedent inserted, Consequent ID:", consequentID)

    def displayConclusion():
        if(len(facts.fact) > 0):
            conclusion = inferenceEngine(kb, facts)
            print(conclusion)
            # kb.printRules()
            label_disp.config(text=conclusion)
            label_question.config(text=getGuideQuestion())
        else:
            label_disp.config(text="Error: there are no facts")

    obj = ""
    val = ""
    foundQuestion = False

    def getGuideQuestion():
        global obj 
        global val
        global foundQuestion 
        foundQuestion = False
        for rule in kb.rules:
            # for
            if(rule.asked < len(rule.condition)): #If all questions weren't asked yet
                obj = rule.condition[rule.asked].split("=")[0]
                val = rule.condition[rule.asked].split("=")[1]
                foundQuestion = True
                rule.asked += 1
                fact = obj.strip() + "=" + val.strip()
                if fact in facts.fact: # Meaning ni exist na
                    return getGuideQuestion()
                break
        
        if foundQuestion:
            return "is the animal's <" + obj + "> = <" + val + ">?"
        return "There are no more questions."

    def guideQuestionYes():
        global obj 
        global val
        global foundQuestion
        # print(obj + "=" + val)
        if foundQuestion:
            fact = obj.strip() + "=" + val.strip()
            addFact(fact)
            label_question.config(text=getGuideQuestion())
            

        
    padding = 10
    window = tk.Tk(className=" Animal Classification Expert System")
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    # Main Frame
    frame = tk.Frame(master=window)
    frame.grid(row=0, column=0, padx=padding, pady=padding, ipadx=padding, ipady=padding, sticky=tk.NSEW)
    for i in range(7):
        frame.grid_columnconfigure(i, minsize=20, weight=1)
    for i in range(11):
        frame.grid_rowconfigure(i, minsize=20, weight=1)

    # Rule Frame
    rule_frame = tk.Frame(master=window)    
    for i in range(7):
        rule_frame.grid_columnconfigure(i, minsize=30, weight=1)
    for i in range(10):
        rule_frame.grid_rowconfigure(i, minsize=20, weight=1)

    # Main Frame Widgets
    label_addFact = tk.Label(master=frame, text="Add Fact [object=value]:")
    label_addFact.grid(row=0, column=0, sticky=tk.NSEW)
    input_fact = tk.Entry(master=frame)
    input_fact.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)
    button_addFact = tk.Button(master=frame, text="Add Fact", borderwidth=1, command=lambda: addFact(input_fact.get()))
    button_addFact.grid(row=0, column=5, columnspan=2, padx=padding, ipadx=padding, sticky=tk.NSEW)

    button_rules = tk.Button(master=frame, text="Add/View Rules", command=lambda: switchScreens(frame, rule_frame))
    button_rules.grid(row=1, column=5, columnspan=2, padx=padding, ipadx=padding, sticky=tk.NSEW)

    label_fact = tk.Label(master=frame, text="Facts:")
    label_fact.grid(row=2, column=0, sticky=tk.EW)

    message_facts = tk.Message(master=frame, text=listToString(facts.fact), width=360)
    message_facts.grid(row=3, column=0, padx=padding, pady=5, ipadx=padding, columnspan=7, rowspan=3, sticky=tk.NSEW)

    label_possiblefact = tk.Label(master=frame, text="Guide questions:", anchor="w")
    label_possiblefact.grid(row=7, column=0, sticky=tk.NSEW)
    label_question = tk.Label(master=frame, text=getGuideQuestion(), anchor="w")
    label_question.grid(row=7, column=1, columnspan=4, sticky=tk.NSEW)
    button_rules = tk.Button(master=frame, text="Yes", command=lambda: guideQuestionYes())
    button_rules.grid(row=7, column=5, padx=padding, ipadx=padding, sticky=tk.NSEW)
    button_rules = tk.Button(master=frame, text="No", command=lambda: label_question.config(text=getGuideQuestion()))
    button_rules.grid(row=7, column=6, padx=padding, ipadx=padding, sticky=tk.NSEW)

    button_start = tk.Button(master=frame, text="Start inference engine", command=lambda: displayConclusion())
    button_start.grid(row=9, column=1, padx=padding, pady=5, ipadx=padding, columnspan=5, sticky=tk.EW)


    label_result = tk.Label(master=frame, text="Conclusion: ")
    label_result.grid(row=10, column=0)
    label_disp = tk.Label(master=frame)
    label_disp.grid(row=10, column=1, columnspan=6)

    # Rule Frame Widgets
    button_back = tk.Button(master=rule_frame, text="Back", command=lambda: switchScreens(rule_frame, frame))
    button_back.grid(row=0, column=0, padx=padding, ipadx=padding, sticky=tk.NSEW)
    label_rules = tk.Label(master=rule_frame, text="Rules:")
    label_rules.grid(row=0, column=4, sticky=tk.NSEW)

    ruleList = kb.getRules()
    scrollbar = tk.Scrollbar(rule_frame)
    scrollbar.grid(row=1, column=7, rowspan=9, sticky=tk.NS)

    message_rules = tk.Text(rule_frame, background=label_rules.cget("background"), relief="flat", borderwidth=0, font=label_rules.cget("font"), yscrollcommand=scrollbar.set)
    message_rules.grid(row=1, column=4, padx=padding, pady=5, ipadx=padding, columnspan=3, rowspan=9, sticky=tk.NSEW)
    message_rules.config(state="normal", padx=padding)
    message_rules.insert(tk.END, ruleList)
    message_rules.config(state="disabled")

    label_addRule = tk.Label(master=rule_frame, text="Add Rule:", anchor="w")
    label_addRule.grid(row=2, column=0, sticky=tk.NSEW)

    label_addRule = tk.Label(master=rule_frame, text="Input Condition(s) [object=value]  [Separate by commas e.g. spine=vertebrate, habitat=land]:", anchor="w")
    label_addRule.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)

    input_conditions = tk.Entry(master=rule_frame)
    input_conditions.grid(row=4, column=0, columnspan=4, sticky=tk.EW)

    label_addInference = tk.Label(master=rule_frame, text="Input inference [object=value]:", anchor="w")
    label_addInference.grid(row=5, column=0, columnspan=4, sticky=tk.NSEW)

    input_inference = tk.Entry(master=rule_frame)
    input_inference.grid(row=6, column=0, columnspan=4, sticky=tk.EW)

    button_addRule = tk.Button(master=rule_frame, text="Add Rule", command=lambda: addRule(input_conditions.get(), input_inference.get()))
    button_addRule.grid(row=7, column=1, columnspan=2, sticky=tk.EW)

    # kb.printRules()
    window.mainloop()

import mysql.connector

def setUpMySQL(knowledgeBase):
    host = "localhost"
    user = "root"
    password = "1234"
    mydb = False
    try:
        mydb = mysql.connector.connect(
        host= host,
        user= user,
        password= password
        )
    except:
        print("Connection to MySQL failed.")

    if(mydb):
        print("MySQL Connection successful!")
        mycursor = mydb.cursor()
        # mycursor.execute("SHOW DATABASES")
        # for databases in mycursor:
        #     print(databases)        

        try:
            mycursor.execute("CREATE DATABASE aniexpsys")
        except:
            print("Database 'aniexpsys' already exists.")
        for tables in mycursor:
            print(tables)        

        mydb = mysql.connector.connect(
        host= host,
        user= user,
        password= password,
        database="aniexpsys"
        )
        mycursor = mydb.cursor(dictionary=True)
        try:
            mycursor.execute("CREATE TABLE CONSEQUENT( consequentID INT PRIMARY KEY AUTO_INCREMENT, consequent VARCHAR (50), createdAt TIMESTAMP );")
        except:
            print("Table CONSEQUENT already exists.")

        try:
            mycursor.execute("CREATE TABLE ANTECEDENT( consequentID INT, FOREIGN KEY (consequentID) REFERENCES CONSEQUENT (consequentID) ON DELETE SET NULL ON UPDATE CASCADE, antecedent VARCHAR(50), createdAt TIMESTAMP );")
        except:
            print("Table ANTECEDENT already exists.")


        # Select
        mycursor.execute("SELECT * FROM CONSEQUENT")
        selectResult = mycursor.fetchall()

        if(len(selectResult) == 0): #If not yet populated
            print("Empty")
            # Populate and insert rules
            for i in range(32): # NGANO WAY SWITCH ANG PYTHON
                if i == 0: # Level 1 Vertebrate
                    consequent = "class=reptile"
                    antecedents = ["spine=vertebrate", "habitat=land", "blood=cold-blooded", "skin=scaly"]
                elif i == 1:
                    consequent = "class=fish"
                    antecedents = ["spine=vertebrate", "habitat=water", "blood=cold-blooded"]
                elif i == 2:
                    consequent = "class=mammal"
                    antecedents = ["spine=vertebrate", "habitat=land", "blood=warm-blooded"]
                elif i == 3:
                    consequent = "class=bird"
                    antecedents = ["spine=vertebrate", "body=wings", "blood=warm-blooded"]
                elif i == 4:
                    consequent = "class=amphibian"
                    antecedents = ["spine=vertebrate", "habitat=land-water", "blood=cold-blooded"]
                elif i == 5: # Level 1 Invertebrate
                    consequent = "class=arthropods"
                    antecedents = ["spine=invertebrate", "external skeleton=yes"]
                elif i == 6: 
                    consequent = "class=protozoa"
                    antecedents = ["spine=invertebrate", "cell=single-cell"]
                elif i == 7:
                    consequent = "class=echinoderm"
                    antecedents = ["spine=invertebrate", "appearance=worm-like"]
                elif i == 8:
                    consequent = "class=annelida"
                    antecedents = ["spine=invertebrate", "appearance=radial symmetry"]
                elif i == 9:
                    consequent = "class=mollusks"
                    antecedents = ["spine=invertebrate", "appearance=mantle"]
                elif i == 10: # Level 2 Reptiles
                    consequent = "specie=turtle"
                    antecedents = ["class=reptile", "body=shell"]
                elif i == 11: 
                    consequent = "specie=snake"
                    antecedents = ["class=reptile", "body=elongated", "legs=none"]
                elif i == 12: 
                    consequent = "specie=lizards"
                    antecedents = ["class=reptile", "body=small"]
                elif i == 13: 
                    consequent = "specie=alligators"
                    antecedents = ["class=reptile", "snout=rounded"]
                elif i == 14: 
                    consequent = "specie=crocodiles"
                    antecedents = ["class=reptile", "snout=pointed"]
                elif i == 15: # Level 2 Amphibians
                    consequent = "specie=frogs"
                    antecedents = ["class=amphibians", "skin=slimy"]
                elif i == 16: 
                    consequent = "specie=toads"
                    antecedents = ["class=amphibians", "skin=dry"]
                elif i == 17: 
                    consequent = "specie=salamanders"
                    antecedents = ["class=amphibians", "adult-life=semi-aquatic"]
                elif i == 18: 
                    consequent = "specie=newts"
                    antecedents = ["class=amphibians", "adult-life=semi-terrestrial"]
                elif i == 19: # Level 2 Fish
                    consequent = "specie=shark"
                    antecedents = ["class=fish", "size=big"]
                elif i == 20: 
                    consequent = "specie=tuna"
                    antecedents = ["class=fish", "size=small"]
                elif i == 21: 
                    consequent = "specie=eel"
                    antecedents = ["class=fish", "shape=elongated"]
                elif i == 22: 
                    consequent = "specie=rays"
                    antecedents = ["class=fish", "shape=flattened"]
                elif i == 23: # Level 2 Bird
                    consequent = "specie=shark"
                    antecedents = ["class=bird", "weight=heavy", "habitat=land"]
                elif i == 24: 
                    consequent = "specie=tuna"
                    antecedents = ["class=bird", "weight=heavy", "habitat=land-water"]
                elif i == 25: 
                    consequent = "specie=eel"
                    antecedents = ["class=bird", "activity=nocturnal"]
                elif i == 26: 
                    consequent = "specie=rays"
                    antecedents = ["class=bird", "activity=diurnal"]
                elif i == 27: 
                    consequent = "specie=penguin"
                    antecedents = ["class=bird", "habitat=southern hemisphere"]
                elif i == 28: # Level 2 Mammals
                    consequent = "specie=canine"
                    antecedents = ["class=mammal", "claws=non-retractable"]
                elif i == 29: 
                    consequent = "specie=feline"
                    antecedents = ["class=mammal", "claws=retractable"]
                elif i == 30: 
                    consequent = "specie=rodents"
                    antecedents = ["class=mammal", "size=tiny"]
                elif i == 31: 
                    consequent = "specie=primates"
                    antecedents = ["class=mammal", "skin=hairy"]
                elif i == 32: 
                    consequent = "specie=marsupials"
                    antecedents = ["class=mammal", "body=pouch"]                
                else:
                    consequent = "class=mammal"
                    antecedents = ["spine=vertebrate", "habitat=land", "blood=warm-blooded"]

                sql = "INSERT INTO CONSEQUENT (consequent, createdAt) VALUES ('"+ consequent +"', now());"
                mycursor.execute(sql)
                mydb.commit()
                print("Consequent inserted, ID:", mycursor.lastrowid)
                consequentID = mycursor.lastrowid

                for item in antecedents:
                    sql = "INSERT INTO ANTECEDENT (consequentID, antecedent, createdAt) VALUES (" + str(consequentID) + ", '" + item +"', now());"
                    mycursor.execute(sql)
                    mydb.commit()
                    print("Antecedent inserted, Consequent ID:", consequentID)
        
        # Retrieving Rules
        mycursor.execute("SELECT CONSEQUENT.consequentID, antecedent, consequent FROM CONSEQUENT INNER JOIN ANTECEDENT ON CONSEQUENT.consequentID = ANTECEDENT.consequentID;")
        selectResult = mycursor.fetchall()
    
        consequentID = selectResult[0]["consequentID"]
        antecedents = list()
        for row in selectResult:
            if(row["consequentID"] != consequentID or row == selectResult[-1]):
                # rule = Rule("", conclusion=consequent, level=1)
                # rule.appendWithCondList(antecedents)
                # knowledgeBase.rules.append(rule)
                if(row == selectResult[-1]):
                    antecedents.append(row["antecedent"].strip())
                knowledgeBase.addRuleList(antecedents, consequent)
                consequentID = row["consequentID"]
                antecedents = list()
            antecedents.append(row["antecedent"].strip())
            consequent = row["consequent"]
        return mydb
    return False

def main(*args):
    facts = Fact()
    # facts = Fact("spine=vertebrate", "habitat=land", "blood=warm-blooded", "blood=cold-blooded")
    # facts.printFacts()

    kb = KnowledgeBase()
    connectedToMySQL = setUpMySQL(kb)
    if not connectedToMySQL:
        print("Populating rules locally... (because MySQL was unavailable)")

        # Level 1 Vertebrate
        kb.addRule("spine=vertebrate", "habitat=land", "blood=cold-blooded", "skin=scaly", conclusion="class=reptile")
        kb.addRule("spine=vertebrate", "habitat=water", "blood=cold-blooded", conclusion="class=fish")
        kb.addRule("spine=vertebrate", "habitat=land", "blood=warm-blooded", conclusion="class=mammal")
        kb.addRule("spine=vertebrate", "body=wings", "blood=warm-blooded", conclusion="class=bird")    
        kb.addRule("spine=vertebrate", "habitat=land-water", "blood=cold-blooded", conclusion="class=amphibian")    

        # Level 1 Invertebrate
        kb.addRule("spine=invertebrate", "external skeleton=yes", conclusion="class=arthropods")
        kb.addRule("spine=invertebrate", "cell=single-cell", conclusion="class=protoza")
        kb.addRule("spine=invertebrate", "appearance=worm-like", conclusion="class=annelida")
        kb.addRule("spine=invertebrate", "appearance=radial symmetry", conclusion="class=echinoderm")
        kb.addRule("spine=invertebrate", "appearance=mantle", conclusion="class=mollusks")

        # Level 2 Reptiles
        kb.addRule("class=reptile", "body=shell", conclusion="specie=turtle")
        kb.addRule("class=reptile", "body=elongated", "legs=none", conclusion="specie=snake")
        kb.addRule("class=reptile", "body=small", conclusion="specie=lizards")
        kb.addRule("class=reptile", "snout=rounded", conclusion="specie=alligators")
        kb.addRule("class=reptile", "snout=pointed", conclusion="specie=crocodiles")

        # Level 2 Amphibians
        kb.addRule("class=amphibians", "skin=slimy", conclusion="specie=frogs")
        kb.addRule("class=amphibians", "skin=dry", conclusion="specie=toads")
        kb.addRule("class=amphibians", "adult-life=semi-aquatic", conclusion="specie=salamanders")
        kb.addRule("class=amphibians", "adult-life=semi-terrestrial", conclusion="specie=newts")

        # Level 2 Fish
        kb.addRule("class=fish", "size=big", conclusion="specie=shark")
        kb.addRule("class=fish", "size=small", conclusion="specie=tuna")
        kb.addRule("class=fish", "shape=elongated", conclusion="specie=eel")
        kb.addRule("class=fish", "shape=flattened", conclusion="specie=rays")

        # Level 2 Bird
        kb.addRule("class=bird", "weight=heavy", "habitat=land", conclusion="specie=shark")
        kb.addRule("class=bird", "weight=heavy", "habitat=land-water", conclusion="specie=tuna")
        kb.addRule("class=bird", "activity=nocturnal", conclusion="specie=eel")
        kb.addRule("class=bird", "activity=diurnal", conclusion="specie=rays")
        kb.addRule("class=bird", "habitat=southern hemisphere", conclusion="specie=penguin")

        # Level 2 Mammals
        kb.addRule("class=mammal", "claws=non-retractable", conclusion="specie=canine")
        kb.addRule("class=mammal", "claws=retractable", conclusion="specie=feline")
        kb.addRule("class=mammal", "size=tiny", conclusion="specie=rodents")
        kb.addRule("class=mammal", "skin=hairy", conclusion="specie=primates")
        kb.addRule("class=mammal", "body=pouch", conclusion="specie=marsupials")
    return kb
    # generateGUI(kb, facts, connectedToMySQL)

main()

