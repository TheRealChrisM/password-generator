import random
from fpdf import FPDF

#GLOBAL VARIBALES
PDF_FONT_SIZE = 13
PDF_FONT = "helvetica"
PDF_COLUMN_WIDTH = 0
PDF_COLUMN_HEIGHT = 0

def main():
    #Determine how the user would like their passwords generated.
    passwordsToGenerate = int(input("How many passwords would you like to generate: "))
    passwordWordAmount = int(input("How many words would you like in the password: "))
    passwordPrefix = input("Would you like a password prefix [Press Enter for No Prefix]: ")
    passwordSuffix = input("Would you like a password suffix [Press Enter for No Suffix]: ")
    passwordWordSeparator = input("Would you like a word separator for the password [Press Enter for No Word Separator]: ")
    passwordListName = input("What would you like to call this password list: ")
    outputFileName = input("What would you like the output file to be named: ")

    #Generate passwords and store them in an array.
    passwordList = generatePasswords(passwordsToGenerate, passwordWordAmount, passwordPrefix, passwordSuffix, passwordWordSeparator)

    #Build actual password list PDF utilizing the passwords contained in the passwordList array.
    buildPDF(passwordList, passwordListName, outputFileName)

#Load words from selected wordlist into a array to use for password generation.
#TODO: Allow user to select which wordlist to use at runtime.
def loadWordList():
    words = []
    wordlistInput = open("wordlist.txt", "r")
    for word in wordlistInput:
        parsedWord = word.replace("\n", "")
        words.append(parsedWord)
    wordlistInput.close()
    return words


#Begin generating passwords which are based on the user's preferences from earlier.
def generatePasswords(passwordsToGenerate, passwordWordAmount, passwordPrefix, passwordSuffix, passwordWordSeparator):
    #Load wordlist into array.
    words = loadWordList()

    #Begin password generation algorithm.
    passwordsGenerated = 0
    generatedPasswordsList = []
    while passwordsGenerated < passwordsToGenerate:
        newPassword = passwordPrefix
        for i in range(0,passwordWordAmount-1):
            newPassword += random.choice(words).capitalize() + passwordWordSeparator
        newPassword += random.choice(words).capitalize()
        newPassword += passwordSuffix
        generatedPasswordsList.append(newPassword)
        passwordsGenerated +=1
    return generatedPasswordsList

#Creates the header of each page for the PDF.
def renderTableHeader(pdfInput, passwordListName, pageNumber, columnWidth, lineHeight):
    pdfInput.cell(columnWidth*2, lineHeight, fill=True)
    pdfInput.ln(lineHeight)
    pdfInput.set_font(style="B")
    pdfInput.cell((columnWidth*2*(1/40)), lineHeight, fill=True)
    titleString = passwordListName + " - Page " + str(pageNumber)
    pdfInput.cell((columnWidth*2*(38/40)), lineHeight, titleString, border=1, align="C")
    pdfInput.cell((columnWidth*2*(1/40)), lineHeight, fill=True)
    pdfInput.ln(lineHeight)
    pdfInput.cell(columnWidth*2, lineHeight/2, fill=True)
    pdfInput.ln(lineHeight/2)
    pdfInput.set_font(style="")  # disabling bold text
    return

#Builds the PDF containing all the passwords.
#TODO: Allow for easier customizing of various settings: font, size, lineheight, 3rd column width, presence of header on each page, etc.
def buildPDF(passwordList, passwordListName, outputFileName):
    pdf = FPDF()
    pdf.add_page()
    pageNumber = 1
    pdf.set_font(PDF_FONT, size=PDF_FONT_SIZE)
    lineHeight = (pdf.font_size * 1.60)
    columnWidth = pdf.epw / 2
    renderTableHeader(pdf, passwordListName, pageNumber, columnWidth, lineHeight)
    currentPasswordNum = 1
    currentFillLevel = 255
    pdf.set_fill_color(currentFillLevel)
    for password in passwordList:  # repeat data rows
        if pdf.will_page_break(lineHeight*2):
            pdf.cell(columnWidth*2, lineHeight, fill=True)
            pdf.ln(lineHeight)
            pageNumber = pageNumber + 1
            renderTableHeader(pdf, passwordListName, pageNumber, columnWidth, lineHeight)
        pdf.set_fill_color(0)
        pdf.cell((columnWidth*(1/20)), lineHeight, fill=True)
        pdf.set_fill_color(currentFillLevel)
        pdf.cell((columnWidth*(1/10)), lineHeight, str(currentPasswordNum), border=1, align="R", fill=True)
        pdf.cell((columnWidth*(12/20)), lineHeight, password, border=1, fill=True)
        pdf.set_fill_color(0)
        pdf.cell((columnWidth*(1/20)), lineHeight, fill=True)
        pdf.set_fill_color(currentFillLevel)
        pdf.cell((columnWidth*(23/20)), lineHeight, border=1, fill=True)
        pdf.set_fill_color(0)
        pdf.cell((columnWidth*(1/20)), lineHeight, fill=True)
        pdf.ln(lineHeight)
        currentPasswordNum=currentPasswordNum+1
        if currentFillLevel == 255:
            currentFillLevel=215
        else:
            currentFillLevel=255
    pdf.cell(columnWidth*2, lineHeight, fill=True)
    pdf.ln(lineHeight)
    pdfFileName = outputFileName + ".pdf"
    pdf.output(pdfFileName)

main()
