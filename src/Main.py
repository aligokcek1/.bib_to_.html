# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
bib_file = open("in.bib", "r")
html_file  = open("out.html", "w")
line_list = []
items_list = []
article_names = []
field_names = []
strippeditemslist = []

def findindexofbracelets(list):
    indexofbracelets = []
    a = 0
    for findindex in list:
        if findindex != "}":
            a += 1
        else:
            indexofbracelets.append(a)
            a += 1
    return indexofbracelets
def error():
    html_file.write("Input file in.bib is not a valid .bib file!")
def fieldcontentfinder(fieldname, itemnum):
    index = 0
    for field in items_list[itemnum]:
        if field.find(fieldname) == -1:
            index += 1
            continue
        else:
            sentence = items_list[itemnum][index]
            if sentence.find("{") != -1:
                startingindex = int(sentence.find("{") + 1)
                endingindex = int(sentence.find("}"))
            elif sentence.find("\"") != -1:
                startingindex = int(sentence.find("\"") + 1)
                endingindex = int(sentence.find("\"", startingindex))
            return sentence[startingindex:endingindex]
def indexfinder(fieldname, itemnum):
    index = 0
    for field in items_list[itemnum]:
        if field.find(fieldname) == -1:
            index += 1
            continue
        else:
            sentence = items_list[itemnum][index]
            a = sentence.split(" ")
            stripsen = ""
            for i in a:
                stripsen += i
        if len(items_list[itemnum]) - 1 == index:
            firstindex = int((stripsen.find("=")) + 1)
            secindex = int(len(stripsen) - 1)
            commaindex = None
        else:
            firstindex = int((stripsen.find("=")) + 1)
            secindex = int(len(stripsen) - 2)
            commaindex = int(len(stripsen) - 1)
        return firstindex, secindex, commaindex

x = 1
while x == 1:
    # appending every line
    for line in bib_file:
        if line == " " or line == "\n":
            continue
        else: line_list.append(line[:-1])

    # creating item list
    b = 0
    for j in findindexofbracelets(line_list):
        item = []
        for i in line_list[b:j]:
            item.append(i)
        b = j
        if item[0] == "}":
            items_list.append(item[1:])
        else:
            items_list.append(item)

    # creating stripped item list:
    for i in items_list:
        dummy = []
        for j in i:
            string = ""
            dummylist = j.split(" ")
            for k in dummylist:
                string += k
            dummy.append(string)
        strippeditemslist.append(dummy)


    # article name list and checking
    y = 1
    while y == 1:
        for i in range(len(items_list)):
            name = items_list[i][0][9:-1]
            if name.isalnum():
                article_names.append(name)
            else:
                error()
                x = 0
                y = 0
                break
        if y == 0:
            break
        countlist = []
        for i in article_names:
            countlist.append(article_names.count(i))


        for i in countlist:
            if i == 1:
                pass
            else:
                error()
                x = 0
                y = 0
            break
        break
    if x == 0:
        break


    # fields are single and must line or not:
    z = 1
    allpossiblelabels = ["author", "title", "journal", "year", "volume", "number", "pages", "doi"]
    mustlabels = ["author", "title", "journal", "year", "volume"]
    while z == 1:
        for items in items_list:
            checklist = []
            for contents in items:
                if contents[0] == "@":
                    continue
                mysentence = contents.split(" ")
                strippedsentence = ""
                for i in mysentence:
                    strippedsentence += i
                ind = strippedsentence.find("=")
                label = strippedsentence[:ind]
                checklist.append(label)
            field_names.append(checklist)
            for label in mustlabels:
                if label in checklist:
                    continue
                else:
                    error()
                    x = 0
                    z = 0
                    break
            if z == 0: break
            for checklabel in checklist:
                if checklabel not in allpossiblelabels:
                    error()
                    x = 0
                    z = 0
                    break
                else: continue
            if z == 0:
                break
        break
    if x == 0:
        break

    # checking fieldnames:
    for item in field_names:
        for fieldname in item:
            if fieldname != fieldname.lower():
                error()
                x = 0
                break
        if x == 0:
            break
    if x == 0:
        break

    # fieldcontents are enclosed "" or {} and check commas:
    j = 1
    while j == 1:
        l = 0
        for item in field_names:
            m = 1
            for fieldname in item:
                a1 = 0
                c1 = 0
                if (strippeditemslist[l][m][indexfinder(fieldname, l)[0]] == "\"") and (strippeditemslist[l][m][indexfinder(fieldname, l)[1]] == "\""):
                    a1 = 1
                if (strippeditemslist[l][m][indexfinder(fieldname, l)[0]] == "{") and (strippeditemslist[l][m][indexfinder(fieldname, l)[1]] == "}"):
                    a1 = 1
                if indexfinder(fieldname, l)[2] == None:
                    c1 = 1
                elif strippeditemslist[l][m][indexfinder(fieldname, l)[2]] == ",":
                    c1 = 1
                if (a1 != 1) or (c1 != 1):
                    x = 0
                    error()
                    j = 0
                    break
                m += 1
                if m == len(items_list[l]):
                    break
            if j == 0:
                break
            l += 1
            if l == len(items_list):
                break
        break
    if x == 0:
        break

    # fieldcontents non-empty:
    for item in field_names:
        for fieldname in item:
            indexofitem = field_names.index(item)
            if fieldcontentfinder(fieldname, indexofitem) == "":
                error()
                x = 0
                break
        if x == 0:
            break
    if x == 0:
        break

    # field checkers:
    def authorchecker(author):
        if author.find(" and ") == -1:
            if author.find(",") == -1:
                return "invalid form"
            names = author.split(",")
            for name in names:
                for word in name:
                    if word.isalpha():
                        continue
                    elif word == " ":
                        continue
                    elif word == ".":
                        continue
                    else:
                        return "invalid form"
        else:
            people = author.split(" and ")
            for person in people:
                if person.find(",") == -1:
                    return "invalid form"
                names2 = person.split(",")
                for name2 in names2:
                    for word2 in name2:
                        if word2.isalpha():
                            continue
                        elif word2 == " ":
                            continue
                        elif word2 == ".":
                            continue
                        else:
                            return "invalid form"
        return "correct form"

    def titlechecker(title):
        for word in title:
            if word.isalnum():
                continue
            elif word == " ":
                continue
            elif word == ",":
                continue
            elif word == ".":
                continue
            elif word == "_":
                continue
            elif word == "-":
                continue
            elif word == "*":
                continue
            elif word == "=":
                continue
            elif word == ":":
                continue
            else: return "invalid form"
        return "correct form"

    def journalchecker(journal):
        for word in journal:
            if word.isalnum():
                continue
            elif word == " ":
                continue
            elif word == ",":
                continue
            elif word == ".":
                continue
            elif word == "_":
                continue
            else: return "invalid form"
        return "correct form"

    def yearchecher(year):
        if len(year) != 4:
            return "invalid form"
        if (ord(year[0]) == ord("1")) or (ord(year[0]) == ord("2")):
            pass
        else:
            return "invalid form"
        for num in year[1:]:
            if ord("0") <= ord(num) <= ord("9"):
                continue
            else: return "invalid form"
        return "correct form"

    def volumechecker(volume):
        if (volume.isnumeric()) and (volume != "0"):
            return "correct form"
        else: return "invalid form"

    def numberchecker(number):
        if (number.isnumeric()) and (number != "0"):
            return "correct form"
        else: return "invalid form"

    def pageschecker(pages):
        if pages.find("--") == -1:
            return "invalid form"
        else:
            startindex = pages.find("--")
            start = pages[:startindex]
            end = pages[startindex + 2:]
            if (start.isnumeric()) and (start != "0"):
                pass
            else:
                return "invalid form"
            if (end.isnumeric()) and (end != "0"):
                pass
            else:
                return "invalid form"
        return "correct form"

    def doichecker(doi):
        if doi.find("/") == -1:
            return "invalid form"
        else:
            presuf = doi.split("/")
            for i in presuf:
                if i == "":
                    return "invalid form"
                for word in i:
                    if word.isalnum():
                        continue
                    elif word == ".":
                        continue
                    else: return "invalid form"
        return "correct form"

    # checking every form:
    def checker(items_list):
        for itemnum in range(len(items_list)):
            for fieldname in field_names[itemnum]:
                if fieldname == "author":
                    if authorchecker(fieldcontentfinder("author", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "title":
                    if titlechecker(fieldcontentfinder("title", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "journal":
                    if journalchecker(fieldcontentfinder("journal", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "year":
                    if yearchecher(fieldcontentfinder("year", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "volume":
                    if volumechecker(fieldcontentfinder("volume", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "number":
                    if numberchecker(fieldcontentfinder("number", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "pages":
                    if pageschecker(fieldcontentfinder("pages", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
                elif fieldname == "doi":
                    if doichecker(fieldcontentfinder("doi", itemnum)) == "correct form":
                        continue
                    else:
                        return "error"
        return "ok"

    def pagesnameconverter(fpagesfinder, itemnum):
        pages = fieldcontentfinder("pages", itemnum)
        return pages.replace("--", "-")

    def authornameconverter(fauthorfinder, itemnum):
        firstr = fieldcontentfinder("author", itemnum)
        if firstr.count("and") == 0:
            dumlist = firstr.split(",")
            dumlist.reverse()
            secstr =""
            convertedstring = ""
            for i in dumlist:
                j = i.strip(" ")
                secstr += j +" "
                convertedstring = secstr[:-1] + ","
            return convertedstring
        else:
            convertedstring = ""
            dumlist = firstr.split(" and ")
            a = 1
            for i in dumlist:
                namestr = ""
                dumlist2 = i.split(",")
                dumlist3 = []
                for j in dumlist2:
                    l = j.strip(" ")
                    dumlist3.append(l)
                dumlist3.reverse()
                for k in dumlist3:
                    namestr += k + " "
                namestr = namestr[:-1]
                if a == len(dumlist) - 1:
                    convertedstring += namestr +" and "
                elif a == len(dumlist):
                    convertedstring += namestr +","
                else:
                    convertedstring += namestr + ", "
                a+=1
            return convertedstring

    #form checker:
    if checker((items_list)) == "error":
        x = 0
        error()
        break


    # checking same year or not:
    def checksameyears(sorted_list):
        yearlist = []
        for item in sorted_list:
            if item[0] not in yearlist:
                yearlist.append(item[0])
            else:
                return "same"
        return "no same"

    # sorting items:
    not_sorted_list = []* len(items_list)
    for itemnum in range(len(items_list)):
        exlist = []
        exlist.append(3000 - int(fieldcontentfinder("year", itemnum)))
        exlist.append(fieldcontentfinder("title", itemnum))
        exlist.append(itemnum)
        not_sorted_list.append(exlist)
    sorted_list = sorted(not_sorted_list)


    # creating write string:
    if checksameyears(sorted_list) == "no same":
        string = ""
        string += "<html>" + "\n"
        for itemnum in range(len(items_list)):
            string += "<br> <center> <b> "+ str(3000 - sorted_list[itemnum][0])+" </b> </center>"+"\n"+"<br>"+"\n"
            string += "[J"+ str(len(items_list)-itemnum) +"] "
            itemindex = sorted_list[itemnum][2]
            string += authornameconverter(fieldcontentfinder("author", itemindex), itemindex)+ " "
            string += "<b>" + fieldcontentfinder("title", itemindex) +"</b>, <i>" + fieldcontentfinder("journal", itemindex) + "</i>, " + fieldcontentfinder("volume", itemindex)
            if "number" in field_names[itemindex]:
                string += ":" + fieldcontentfinder("number", itemindex)
            if "pages" in field_names[itemindex]:
                string += ", pp. " + pagesnameconverter(fieldcontentfinder("pages", itemindex), itemindex)
            string += ", " + fieldcontentfinder("year", itemindex) +"."
            if "doi" in field_names[itemindex]:
                string += " <a href=\"https://doi.org/" + fieldcontentfinder("doi", itemindex) + "\">link</a>"
            string += " <br>\n"
        string += "</html>"
    else:
        used_year_list = []
        string = ""
        string += "<html>\n"
        for itemnum in range(len(items_list)):
            itemindex = sorted_list[itemnum][2]
            if fieldcontentfinder("year", itemindex) not in used_year_list:
                used_year_list.append(fieldcontentfinder("year", itemindex))
                string += "<br> <center> <b> "+ str(3000 - sorted_list[itemnum][0])+" </b> </center>"+"\n"+"<br>"+"\n"
                string += "[J"+ str(len(items_list)-itemnum) +"] "
                string += authornameconverter(fieldcontentfinder("author", itemindex), itemindex)+ " "
                string += "<b>" + fieldcontentfinder("title", itemindex) +"</b>, <i>" + fieldcontentfinder("journal", itemindex) + "</i>, " + fieldcontentfinder("volume", itemindex)
                if "number" in field_names[itemindex]:
                    string += ":" + fieldcontentfinder("number", itemindex)
                if "pages" in field_names[itemindex]:
                    string += ", pp. " + pagesnameconverter(fieldcontentfinder("pages", itemindex), itemindex)
                string += ", " + fieldcontentfinder("year", itemindex) +"."
                if "doi" in field_names[itemindex]:
                    string += " <a href=\"https://doi.org/" + fieldcontentfinder("doi", itemindex) + "\">link</a>"
                string += " <br>\n"
            else:
                used_year_list.append(fieldcontentfinder("year", itemindex))
                string += "<br>" + "\n"
                string += "[J" + str(len(items_list) - itemnum) + "] "
                string += authornameconverter(fieldcontentfinder("author", itemindex), itemindex) + " "
                string += "<b>" + fieldcontentfinder("title", itemindex) + "</b>, <i>" + fieldcontentfinder("journal", itemindex) + "</i>, " + fieldcontentfinder("volume", itemindex)
                if "number" in field_names[itemindex]:
                    string += ":" + fieldcontentfinder("number", itemindex)
                if "pages" in field_names[itemindex]:
                    string += ", pp. " + pagesnameconverter(fieldcontentfinder("pages", itemindex), itemindex)
                string += ", " + fieldcontentfinder("year", itemindex) + "."
                if "doi" in field_names[itemindex]:
                    string += " <a href=\"https://doi.org/" + fieldcontentfinder("doi", itemindex) + "\">link</a>"
                string += " <br>\n"
        string += "</html>"

    html_file.write(string)

    break

bib_file.close()
html_file.close()
# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE