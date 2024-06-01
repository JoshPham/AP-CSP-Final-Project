from tkinter import *
from math import ceil
import gc

# Colors
BackgroundColor = "#c4b282"
TopbarColor = "#f5f5dc"
SidebarColor = "#9c8a59"
FrameBackground = "#85764c"
FrameBorder = "#d1c6a5"
ImageBackground = "#d6c698"
MainButtonColor = "#635736"

# Screen Initialization
screen = Tk()
screenwidth = 910
screenheight = 640
screen.minsize(screenwidth, screenheight)
screen.maxsize(screenwidth, screenheight)
screen.resizable(False, False)
screen.config(bg=BackgroundColor)

# Variables
Items = {}
FruitImages = {}
PageNum = 1
CartNum = 0
UserCart = []

# Functions
# Search Queries
def searchQuery():
    IncludedFruits = []
   
    user_search = Search.get()
   
    for fruit in FruitNameList:
        if user_search.lower() in str(fruit).lower():
            IncludedFruits.append(FruitNameList[fruit])
   
    return IncludedFruits

def continentQuery():
    IncludedContinents = []
    IncludedFruits = []
   
    for continent in Continents:
        if continent.get() == 1:
            IncludedContinents.append(continent.name)
   
    for fruit in FruitList:
        if fruit.continent in IncludedContinents:
            IncludedFruits.append(fruit)
   
    return IncludedFruits

def updateQuery():
    global PageNum
    
    Sidebar.grid(row=1, column=0, rowspan=5, sticky=NW)
    
    removeFrames()
    
    newlist = rearrangeFruits(list(set(searchQuery()).intersection(continentQuery())))
    newlistPages = ceil(len(newlist)/6)
    
    if PageNum > newlistPages:
        PageNum = newlistPages
        PageNumLabel.config(text=str(newlistPages))
        PageRight["state"] = DISABLED
    
    if newlistPages == 1 or newlistPages == 0:
        PageNum = 1
        PageNumLabel.config(text=str(PageNum))
        disablePages()
    else:
        if PageNum > 1:
            PageLeft["state"] = NORMAL
        if PageNum < newlistPages:
            PageRight["state"] = NORMAL
    
    loadFruits(newlist)

def rearrangeFruits(originallist):
    newlist = []
    finalnewList = []
    FruitGridOrder = ["Na", "Sa", "Asia", "Europe", "Africa", "Oceania"]
    AlphabetOrder = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
    for continent in FruitGridOrder:
        for fruit in originallist:
            if fruit.continent == continent:
                newlist.append(fruit)
                
    for letter in AlphabetOrder:
        for fruit in newlist:
            if fruit.name[0][0] == letter:
                finalnewList.append(fruit)
    
    return finalnewList

# Page Handlers
def nextPage():
    if pageBoundary(1):
        global PageNum
        PageNum += 1
        PageNumLabel.config(text=str(PageNum))
        updateQuery()

def lastPage():
    if pageBoundary(-1):
        global PageNum
        PageNum -= 1
        PageNumLabel.config(text=str(PageNum))
        updateQuery()

def pageBoundary(nextPg):
    global PageNum
    MaxPages = ceil(len((list(set(searchQuery()).intersection(continentQuery()))))/6)
    
    if PageNum+2 > MaxPages and nextPg == 1:
        PageRight["state"] = DISABLED
    else:
        PageRight["state"] = NORMAL
    
    if PageNum-2 < 1 and nextPg == -1:
        PageLeft["state"] = DISABLED
    else:
        PageLeft["state"] = NORMAL
    
    if PageNum + nextPg < 1 or PageNum + nextPg > MaxPages:
        return False
    return True

def disablePages():
    PageLeft["state"] = DISABLED
    PageRight["state"] = DISABLED

# Cart Functions
def CartList():
    UniqueOnlyCart = [*set(UserCart)]
    
    return rearrangeFruits(UniqueOnlyCart)

def AddToCart(fruit):
    UserCart.append(fruit)

# Extra Functions
def costHandler(price):
    NewPrice = round(price, 2)
    NewPriceText = f"${NewPrice}"
    
    if NewPrice == round(NewPrice, 1) and NewPrice:
        NewPriceText += "0"
    
    return NewPriceText

# GUIs
# Create Fruit Frames
def removeFrames():
    for key in Items.copy():
        Items[key].grid_remove()
        Items.pop(key)

def loadFruits(IncludedFruitList):
    global PageNum
    
    if IncludedFruitList:
        for index in range(0, len(IncludedFruitList)-((PageNum-1)*6)): # 0 to the max in that page
            FruitIndex = ((PageNum-1) * 6 + index) - 1
            
            if FruitIndex-((PageNum-1)*6)+1 < 6 and IncludedFruitList[FruitIndex]:
                fruit = IncludedFruitList[FruitIndex]
                
                FruitName = fruit.name[0] if not fruit.displayname else fruit.displayname
                FruitContinent = fruit.continent
            
                if fruit.continent == "Na":
                    FruitContinent = "North America"
                if fruit.continent == "Sa":
                    FruitContinent = "South America"

                Items["frame{0}".format(index)] = Frame(screen, bg=FrameBackground, highlightbackground=FrameBorder, highlightthickness=3)
                FruitFrame = Items["frame{0}".format(index)]
            
                FruitImages["image{0}".format(index)] = PhotoImage(file=fruit.picture).zoom(15).subsample(16)

                FruitImage = Canvas(FruitFrame, bg=ImageBackground, width=187.5, height=120, highlightthickness=5, highlightbackground=MainButtonColor)
                FruitImage.create_image(0, 0, image=FruitImages["image{0}".format(index)], anchor=NW)
                FruitImage.grid(row=1, column=0, columnspan=2)
            
                fontsize = 15
                PadY = (0, 0)
                if len(list(FruitName)) > 19:
                    fontsize = 12
                    PadY = (0, 5)
                elif len(list(FruitName)) > 13:
                    fontsize = 13
                    PadY = (0, 4)
                    
                FruitNameLabel = Label(FruitFrame, text=FruitName, font=("Century Gothic", fontsize, "bold"), bg=FrameBackground)
                FruitNameLabel.grid(row=2, column=0, pady=PadY, columnspan=2)
                
                FruitRegion = Label(FruitFrame, text=FruitContinent, font=("Century Gothic", 10), bg=FrameBackground)
                FruitRegion.grid(row=3, column=0, columnspan=2)
                
                FruitInfo = Button(FruitFrame, text="More Info", font=("Century Gothic", 10, "bold"), command=lambda fruit=fruit: moreInfo(fruit), bg=MainButtonColor)
                FruitInfo.grid(row=5, column=0, columnspan=2, pady=5)
                
                FruitPrice = Label(FruitFrame, text=f"${fruit.cost}", font=("Century Gothic", 12, "bold"), bg=FrameBackground)
                FruitPrice.grid(row=4, column=0, sticky=E)
            
                FruitAdd = Button(FruitFrame, text="Add to Cart", font=("Century Gothic", 10, "bold"), command=lambda fruit=fruit: AddToCart(fruit), bg="#7a6d2d")
                FruitAdd.grid(row=4, column=1)
            
                FramePadX = (10, 10)
                FramePadY = (15, 0)
            
                if index % 3 == 0:
                    FramePadX = (190, 10)
                if index % 3 == 2:
                    FramePadX = (10, 0)

                Items["frame{0}".format(index)].grid(row=(index//3)+1, column=(index%3), padx=FramePadX, pady=FramePadY, sticky=NW)
    else:
        Items["0Results"] = Label(text="No Results", font=("Century Gothic", 30, "bold"), bg=BackgroundColor)
        Items["0Results"].grid(row=1, column=1)

def moreInfo(fruit):
    removeFrames()
    disablePages()
    
    Items["frame0"] = Frame(screen, bg=BackgroundColor)
    MainInfoFrame = Items["frame0"]
    
    Items["frame1"] = Frame(MainInfoFrame, bg=FrameBackground, highlightbackground=FrameBorder, highlightthickness=3)
    FruitFrame = Items["frame1"]
    
    BackButton = Button(MainInfoFrame, text="Back", font=("Century Gothic", 15, "bold"), command=updateQuery, bg=MainButtonColor)
    BackButton.grid(row=0, column=0, padx=15, pady=(5, 10), sticky=W)
    
    FruitInfoFrame = Frame(FruitFrame, bg=FrameBackground)
    
    FruitImages["image"] = PhotoImage(file=fruit.picture).zoom(3).subsample(2)

    FruitImage = Canvas(FruitInfoFrame, bg=ImageBackground, width=300, height=200, highlightthickness=5, highlightbackground=MainButtonColor)
    FruitImage.create_image(0, 0, image=FruitImages["image"], anchor=NW)
    FruitImage.grid(row=1, column=0, rowspan=4)
    
    FruitName = Label(FruitInfoFrame, text=fruit.name[0] if not fruit.displayname else fruit.displayname, font=("Century Gothic", 20, "bold"), bg=FrameBackground)
    FruitName.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=NW)
    
    PriceText = Label(FruitInfoFrame, text=f"${fruit.cost}", font=("Century Gothic", 15, "bold"), bg=FrameBackground, justify=LEFT)
    PriceText.grid(row=2, column=1, padx=(10, 0), pady=(0, 40), sticky=NW)
    
    ColorsText = "Colors: " if len(fruit.info["Colors"])>1 else "Color: "
    for index, color in enumerate(fruit.info["Colors"]):
        if (index+1)%5 == 0:
            ColorsText += "\n"
            
        ColorsText += color
        
        if index != len(fruit.info["Colors"])-1:
            ColorsText += ", "
            
    FruitColors = Label(FruitInfoFrame, text=ColorsText, font=("Century Gothic", 12), bg=FrameBackground, justify=LEFT)
    FruitColors.grid(row=3, column=1, padx=(10, 0), pady=(10, 0), sticky=NW)
    
    RegionsText = "Regions: " if len(fruit.info["Regions"])>1 else "Region: "
    for index, Region in enumerate(fruit.info["Regions"]):
        if (index+1)%3 == 0:
            RegionsText += "\n"
            
        RegionsText += Region

        if index != len(fruit.info["Regions"])-1:
            RegionsText += ", "
            
    FruitRegions = Label(FruitInfoFrame, text=RegionsText, font=("Century Gothic", 12), bg=FrameBackground, justify=LEFT)
    FruitRegions.grid(row=4, column=1, padx=(10, 0), pady=(10, 0), sticky=NW)
    
    AddCart = Button(FruitInfoFrame, text="Add to Cart", font=("Century Gothic", 15, "bold"), command=lambda fruit=fruit: AddToCart(fruit), bg=MainButtonColor)
    AddCart.grid(row=5, column=1, padx=(249, 10), pady=(0, 10), sticky=NW)
    
    Items["frame2"] = Frame(MainInfoFrame, bg=FrameBackground, highlightbackground=FrameBorder, highlightthickness=3)
    DescFrame = Items["frame2"]
    
    DescriptionLabel = Label(DescFrame, text="Description:", font=("Century Gothic", 18, "bold"), bg=FrameBackground, justify=LEFT)
    DescriptionLabel.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=NW)
    
    infoText = ""
    
    for info in fruit.info["Description"]:
        infoText += " - " + info + "\n"
    
    infoLabel = Label(DescFrame, text=infoText, font=("Century Gothic", 12), bg=FrameBackground, justify=LEFT)
    infoLabel.grid(row=1, column=0, padx=10, sticky=NW)
    
    DescPadX = Label(DescFrame, text="", bg=FrameBackground)
    DescPadX.grid(row=2, column=0, padx=(688, 0), sticky=NW)
    
    DescPadY = Label(DescFrame, text="", bg=FrameBackground)
    DescPadY.grid(row=0, column=1, rowspan=3, pady=(166, 0), sticky=NW)
    
    FruitInfoFrame.grid(row=1, column=0)
    FruitFrame.grid(row=1, column=0, sticky=NW, pady=(10, 0))
    DescFrame.grid(row=2, column=0, sticky=NW)
    MainInfoFrame.grid(row=1, column=1)

# Cart GUI
def updateCart(event, initial=True):
    global CartNum
    
    if initial:
        CartNum = 0
    
    def handleQuantities(fruit, direction):
        if direction == 1:
            UserCart.append(fruit)
        if direction == -1:
            UserCart.remove(fruit)
           
        updateCart("<Button-1>", False)
    
    Sidebar.grid_remove()
    removeFrames()
    disablePages()
      
    Items["frame0"] = Frame(screen, bg=BackgroundColor)
    MainCartFrame = Items["frame0"]
    
    BackButton = Button(MainCartFrame, text="Back", font=("Century Gothic", 15, "bold"), command=updateQuery, bg=MainButtonColor)
    BackButton.grid(row=0, column=0, padx=15, pady=10, sticky=NW)
    
    FruitImages["frame1"] = Frame(MainCartFrame, bg=FrameBackground, highlightbackground=FrameBorder, highlightthickness=3)
    CartFrame = FruitImages["frame1"]
    
    CartTitle = Label(CartFrame, text="Your Cart", font=("Century Gothic", 25, "bold"), bg=FrameBackground, justify=LEFT)
    CartTitle.grid(row=0, column=0, sticky=NW)
    
    PadY = Label(CartFrame, text="", bg=FrameBackground)
    PadY.grid(row=0, column=3, pady=(440, 0), sticky=NW, rowspan=5)
    
    FruitFrames = Frame(CartFrame, bg=FrameBackground)
    
    Cart = CartList()
    
    def handleScroll(direction):
        global CartNum
        
        if direction:
            if direction == 1 and CartNum+3 < len(Cart):
                CartNum += 1
                
            if direction == -1 and CartNum > 0:
                CartNum -= 1

            if CartNum+3 == len(Cart):
                ScrollDown["state"] = DISABLED
            else:
                ScrollDown["state"] = NORMAL

            if CartNum == 0:
                ScrollUp["state"] = DISABLED
            else:
                ScrollUp["state"] = NORMAL
                    
            if len(Cart) <= 3:
                ScrollUp["state"] = DISABLED
                ScrollDown["state"] = DISABLED
            
            updateCart("<Button-1>", False)
        else:
            if len(Cart) <= 3:
                ScrollUp["state"] = DISABLED
                ScrollDown["state"] = DISABLED
    
    def updateFruits():
        i = 2
        Cart = CartList()
        
        for index in range(3):
            CartIndex = CartNum + index
            
            if CartIndex < len(Cart):
                fruit = Cart[CartIndex]
                quantity = UserCart.count(fruit)
                FruitName = fruit.name[0] if not fruit.displayname else fruit.displayname
                
                Items["frame{0}".format(i)] = Frame(FruitFrames, bg=FrameBackground, highlightbackground=FrameBorder, highlightthickness=3)
                FruitFrame = Items["frame{0}".format(i)]
                
                Items["quantity{0}".format(i)] = Frame(FruitFrame, bg=FrameBackground)
                QuantityFrame = Items["quantity{0}".format(i)]
                
                FruitImages["image{0}".format(i)] = PhotoImage(file=fruit.picture).zoom(3).subsample(4)

                FruitImage = Canvas(FruitFrame, bg=ImageBackground, width=157.5, height=101.25, highlightthickness=5, highlightbackground=MainButtonColor)
                FruitImage.create_image(0, 0, image=FruitImages["image{0}".format(i)], anchor=NW)
                FruitImage.grid(row=0, column=0, rowspan=3)
                
                FruitNameLabel = Label(FruitFrame, text=f"{FruitName}", font=("Century Gothic", 18, "bold"), bg=FrameBackground)
                FruitNameLabel.grid(row=0, column=1, sticky=NW, padx=(5, 0))
                
                PadX = Label(FruitFrame, text="", bg=FrameBackground)
                PadX.grid(row=1, column=1, padx=(400, 0), sticky=NW)
                
                RemoveFruit = Button(QuantityFrame, text="-", font=("Century Gothic", 12, "bold"), width=2, bg=MainButtonColor, command=lambda fruit=fruit: handleQuantities(fruit, -1))
                RemoveFruit.grid(row=0, column=0, sticky=NW)

                AddFruit = Button(QuantityFrame, text="+", font=("Century Gothic", 12, "bold"), width=2, bg=MainButtonColor, command=lambda fruit=fruit: handleQuantities(fruit, 1))
                AddFruit.grid(row=0, column=2, sticky=NE)
                
                FruitQuantity = Label(QuantityFrame, text=f"{quantity}", font=("Century Gothic", 15, "bold"), bg=FrameBackground)
                FruitQuantity.grid(row=0, column=1, padx=5, sticky=NE)

                PadYVal = 8
                if index == 2:
                    PadYVal = 29
                
                QuantityFrame.grid(row=2, column=1, sticky=SE)  
                FruitFrame.grid(row=i, column=0, sticky=NW, padx=(5, 0), pady=(0, PadYVal))
                
                i += 1
        
        TextExtra = 0
        
        if not Cart:
            Items["Empty"] = Label(FruitFrames, text="Cart is empty", font=("Century Gothic", 30, "bold"), bg=FrameBackground, fg="#524930")
            Items["Empty"].grid(row=1, column=0, pady=(70, 0))
            TextExtra = 123
        
        if len(Cart) < 3:
            Items["pad"] = Frame(FruitFrames, bg=FrameBackground)
            FruitFrame = Items["pad"]
            
            PadY = Label(FruitFrame, text="", bg=FrameBackground)
            PadY.grid(row=0, column=0, pady=((3-len(Cart))*125-TextExtra, 0), sticky=NW)
            
            FruitFrame.grid(row=i, column=0, sticky=NW)
            
        elif CartNum+3 > len(Cart):
            Items["pad"] = Frame(FruitFrames, bg=FrameBackground)
            FruitFrame = Items["pad"]
            
            PadY = Label(FruitFrame, text="", bg=FrameBackground)
            PadY.grid(row=0, column=0, pady=(((3-(len(Cart)-CartNum))*125, 0)), sticky=NW)
            
            FruitFrame.grid(row=i+1, column=0, sticky=NW)

    def updateTotal():
        TotalFrame = Frame(MainCartFrame, bg=FrameBackground, highlightbackground=FrameBorder, highlightthickness=3)
        
        TotalTitle = Label(TotalFrame, text="Your Cart Totals:", font=("Century Gothic", 20, "bold"), bg=FrameBackground)
        TotalTitle.grid(row=0, column=0)
        
        for index, fruit in enumerate(Cart):
            Items["text{0}".format(index)] = Frame(TotalFrame, bg=FrameBackground)
            FruitFrame = Items["text{0}".format(index)]
            
            FruitName = fruit.name[0] if not fruit.displayname else fruit.displayname
            FruitCost = costHandler(fruit.cost*UserCart.count(fruit))
    
            fontsize = 12
            if len(list(FruitName)) > 15:
                fontsize = 10
            if len(list(FruitName)) > 19:
                fontsize = 9
            FruitTitle = Label(FruitFrame, text=f" - {FruitName}({UserCart.count(fruit)}) - {FruitCost}", font=("Century Gothic", fontsize), bg=FrameBackground)
            FruitTitle.grid(row=0, column=0, sticky=W)
            
            FruitFrame.grid(row=index+1, column=0, sticky=W)
        
        TotalTotal = Label(TotalFrame, text=f"Total: {costHandler(sum([fruit.cost for fruit in UserCart]))}", font=("Century Gothic", 20, "bold"),  bg=FrameBackground)
        TotalTotal.grid(row=99, column=0, sticky=SW)
        
        TotalPadX = Label(TotalFrame, text="", bg=FrameBackground)
        TotalPadX.grid(row=98, column=0, padx=(240, 0), sticky=NW)
        
        TotalPadY = Label(TotalFrame, text="", bg=FrameBackground)
        TotalPadY.grid(row=0, column=1, pady=(503, 0), sticky=NW, rowspan=100)
    
        TotalFrame.grid(row=0, column=1, rowspan=4, sticky=NE, padx=(10, 0), pady=(10, 0))
    
    updateFruits()
    if Cart:
        updateTotal()
    
    ScrollFrame = Frame(CartFrame, bg=FrameBackground)
    
    PadXVal = 530
    if not Cart:
        PadXVal = 798
    
    ScrollUp = Button(ScrollFrame, text="^", font=("Century Gothic", 12, "bold"), width=2, bg=MainButtonColor, command=lambda: handleScroll(-1))
    ScrollUp.grid(row=0, column=0, padx=(PadXVal, 10))
    
    if CartNum == 0:
        ScrollUp["state"] = DISABLED

    ScrollDown = Button(ScrollFrame, text="v", font=("Century Gothic", 12, "bold"), width=2, bg=MainButtonColor, command=lambda: handleScroll(1))
    ScrollDown.grid(row=0, column=1, padx=(0, 5))
    
    if len(Cart) <= CartNum+3:
        ScrollDown["state"] = DISABLED
    
    ScrollFrame.grid(row=3, column=0, sticky=NW)
    FruitFrames.grid(row=2, column=0)
    CartFrame.grid(row=1, column=0, sticky=NW)
    
    MainCartFrame.grid(row=1, column=0, sticky=NW, padx=(20, 0))

# Topbar GUI
Topbar = Frame(screen, bg=TopbarColor)

Logo = Label(Topbar, text="Fantasy Fruits", bg=TopbarColor, fg="#e3cc8d", font=("Century Gothic", 25, "bold"))
Logo.grid(row=0, column=0, pady=20, padx=(10, 0))

Search = Entry(Topbar, font=("Century Gothic", 15), width=27)
Search.grid(row=0, column=1, sticky=E, padx=(130, 0))

SearchButton = Button(Topbar, text="Search", command=updateQuery, font=("Century Gothic", 13, "bold"), bg="#a18b50", fg="#f5db95", width=10)
SearchButton.grid(row=0, column=2, sticky=E, padx=20)

CartImage = PhotoImage(file='Cart.png') ### MAY NEED TO CHANGE!!!!!
CartCanvas = Canvas(Topbar, width=80, height=80, bg=TopbarColor, highlightbackground=TopbarColor)
CartButton = CartCanvas.create_image(40, 40, image=CartImage)
CartCanvas.tag_bind(CartButton, "<Button-1>", updateCart)
CartCanvas.grid(row=0, column=3, padx=(0, 20))

Topbar.grid(row=0, column=0, columnspan=3, sticky=NW)

# Sidebar GUI
Sidebar = Frame(screen, bg=SidebarColor)

Includelabel = Label(Sidebar, text="Include Regions:", font=("Century Gothic", 15, "bold"), bg=SidebarColor)
Includelabel.grid(row=1, column=0, padx=5, pady=(0, 5), columnspan=3)

NaVar = IntVar()
NaVar.set(1)
NaVar.name = "Na"
Na = Checkbutton(Sidebar, text="North America", font=("Century Gothic", 15), bg=SidebarColor, variable=NaVar, command=updateQuery)
Na.grid(row=2, column=0, sticky=W, pady=5)

SaVar = IntVar()
SaVar.set(1)
SaVar.name = "Sa"
Sa = Checkbutton(Sidebar, text="South America", font=("Century Gothic", 15), bg=SidebarColor, variable=SaVar, command=updateQuery)
Sa.grid(row=3, column=0, sticky=W, pady=5)

EuVar = IntVar()
EuVar.set(1)
EuVar.name = "Europe"
Eu = Checkbutton(Sidebar, text="Europe", font=("Century Gothic", 15), bg=SidebarColor, variable=EuVar, command=updateQuery)
Eu.grid(row=4, column=0, sticky=W, pady=5)

AfricaVar = IntVar()
AfricaVar.set(1)
AfricaVar.name = "Africa"
Africa = Checkbutton(Sidebar, text="Africa", font=("Century Gothic", 15), bg=SidebarColor, variable=AfricaVar, command=updateQuery)
Africa.grid(row=5, column=0, sticky=W, pady=5)

AsiaVar = IntVar()
AsiaVar.set(1)
AsiaVar.name = "Asia"
Asia = Checkbutton(Sidebar, text="Asia", font=("Century Gothic", 15), bg=SidebarColor, variable=AsiaVar, command=updateQuery)
Asia.grid(row=6, column=0, sticky=W, pady=5)

OceaniaVar = IntVar()
OceaniaVar.set(1)
OceaniaVar.name = "Oceania"
Oceania = Checkbutton(Sidebar, text="Oceania", font=("Century Gothic", 15), bg=SidebarColor, variable=OceaniaVar, command=updateQuery)
Oceania.grid(row=7, column=0, sticky=W, pady=(5, 170))

Continents = [NaVar, SaVar, EuVar, AfricaVar, AsiaVar, OceaniaVar]

# Page GUI
PageFrame = Frame(Sidebar, bg=SidebarColor)

PageLeft = Button(PageFrame, text="<", font=("Century Gothic", 18, "bold"), width=2, bg=MainButtonColor, command=lastPage)
PageLeft.grid(row=0, column=0, sticky=W)
PageLeft["state"] = DISABLED

PageRight = Button(PageFrame, text=">", font=("Century Gothic", 18, "bold"), width=2, bg=MainButtonColor, command=nextPage)
PageRight.grid(row=0, column=2, sticky=W)

PageNumLabel = Label(PageFrame, text=f"{PageNum}", font=("Century Gothic", 25, "bold"), bg=SidebarColor)
PageNumLabel.grid(row=0, column=1, padx=15)

PageFrame.grid(row=8, column=0, pady=(0, 40), sticky=S)

Sidebar.grid(row=1, column=0, rowspan=5, sticky=NW)

# Fruits
FileStart = "fruits/" ### MAY NEED TO CHANGE!!!!!

# Fruit Class
class Fruit:
    def __init__(self, name, displayname, continent, info, cost, picture):
        self.name = name
        self.displayname = displayname
        self.continent = continent
        self.info = info
        self.cost = cost
        self.picture = picture

# Fruit Info
# Na Fruits
Sapodilla_Info = {
    "Description": ["Has an exceptionally sweet, with flavors reminiscent of brown sugar", "Originates from Southern Mexico, but also grown in some Asian Regions", "Has skinny and long black seeds"],
    "Colors": ["Green", "Yellow", "Brown"],
    "Regions": ["Mexico", "India", "Guatemala", "Philippines"],
}

Guava_Info = {
    "Description": ["Tastes unique, sweet, and almost universally pleasant", "Green on outside, red on inside"],
    "Colors": ["Green", "Red"],
    "Regions": ["Mexico", "Brazil", "Hawaii"],
}

Royal_Tropical_Pineapple_Info = {
    "Description": ["Sweet and tart", "Has yellow flesh and skin that grows in cylindrical fashion"],
    "Colors": ["Yellow"],
    "Regions": ["Hawaii"],
}

# Sa Fruits
Passionfruit_Info = {
    "Description": ["Has a unique blend of sour and sweet with a very floral finish and citrussy taste", "Purple and yellow varieties are the most common"],
    "Colors": ["Green", "Red", "Purple"],
    "Regions": ["Hawaii", "Australia", "South Africa", "Venezuela", "Brazil", "Peru", "Ecuador", "Colombia"],
}

Araza_Info = {
    "Description": ["Has a very unique sweet and sour taste with a smooth and effervescent texture", "Very fragrant"],
    "Colors": ["Green", "Yellow"],
    "Regions": ["Brazil", "Colombia", "Ecuador"],
}

# Asia Fruits
Durian_Info = {
    "Description": ["Has a sweet flavour", "Pungent odor", "Spiky shape"],
    "Colors": ["Green", "Yellow", "Brown"],
    "Regions": ["Thailand", "Malaysia", "Philippines", "Indonesia"],
}

Carambola_Info = {
    "Description": ["Tastes like a mix of apple, pear, grape, and citrus fruits", "Star shape"],
    "Colors": ["Green", "Orange", "Yellow"],
    "Regions": ["China"],
}

Pomelo_Info = {
    "Description": ["Has taste similar to that of a grapefruit, with an intense tartness, sharp acidity,\n   and a prevailing sweetness", "Citrus fruit"],
    "Colors": ["Green", "Yellow", "Red"],
    "Regions": ["China", "Malaysia"],
}

Longan_Info = {
    "Description": ["Musky, sweet taste, which can be compared to the flavor of lychee fruit", "Has translucent flesh"],
    "Colors": ["Brown"],
    "Regions": ["China", "Malaysia", "Taiwan", "Indonesia", "Thailand"],
}

Akebi_Info = {
    "Description": ["Has a mildly bitter taste and added texture", "Has a semi-translucent white pulp"],
    "Colors": ["Purple"],
    "Regions": ["Japan"],
}

Mangosteen_Info = {
    "Description": ["Sweet and tangy flavor with notes of peach, cherry, and strawberry", "The fruit pulp is slightly acidic and sweet"],
    "Colors": ["Green to dark purple"],
    "Regions": ["Malaysia", "Indonesia"],
}

Rambutan_Info = {
    "Description": ["Has a sweet, fruity flavour with a hint of acidity reminiscent of strawberries and grapes", "A round or ellipsoid with a leathery skin densely covered in soft spines"],
    "Colors": ["Red", "Yellow"],
    "Regions": ["Malaysia", "Thailand", "Myanmar", "Sri Lanka", "Indonesia", "Singapore", "Philippines"],
}

Persimmon_Info = {
    "Description": ["Beautifully delicate flavor that almost has a cantaloupe quality to it,\n   both in color and sweetness", "Round and squat, it resembles a tomato"],
    "Colors": ["Red", "Orange"],
    "Regions": ["China", "Japan", "Korea", "India", "Indonesian"],
}

# Europe Fruits
Maracujá_dos_Açores_Info = {
    "Description": ["Has a sour flavor", "Has a particular and strong perfume"],
    "Colors": ["Purple"],
    "Regions": ["Portugal"],
}

# Africa Fruits
Kiwano_Info = {
    "Description": ["Mild and slightly sweet", "A spiky fruit"],
    "Colors": ["Orange"],
    "Regions": ["South Africa"],
}

Prickly_Pear_Info = {
    "Description": ["Has taste comparable to that of a melon or a kiwi, sometimes with a hint of bubblegum", "Comes from a melon"],
    "Colors": ["Red", "Orange", "Yellow", "Pink"],
    "Regions": ["Mexico", "Colombia", "Israel", "South Africa", "Italy", "Spain"],
}

# Oceania Fruits
Pandanus_Info = {
    "Description": ["Has a grassy vanilla with a hint of coconut taste", "Tough fibrous fruit"],
    "Colors": ["Green"],
    "Regions": ["Polynesia", "Australia"],
}

Quandong_Info = {
    "Description": ["A sweet taste with a balancing slightly sour and salty aftertaste", "Has a mild aroma of dry lentils with some earthy fermented touches"],
    "Colors": ["Red", "Green"],
    "Regions": ["Australia"],
}

# Initialize Fruits
# Na Fruits
Sapodilla = Fruit(["Sapodilla"], False, "Na", Sapodilla_Info, 7.99, f"{FileStart}Sapodilla.png")
Guava = Fruit(["Guava"], False, "Na", Guava_Info, 5.99, f"{FileStart}Guava.png")
Royal_Tropical_Pineapple = Fruit(["Royal Tropical Pineapple"], False, "Na", Royal_Tropical_Pineapple_Info, 5.99, f"{FileStart}Royal Tropical Pineapple.png")

# Sa Fruits
Passionfruit = Fruit(["Passionfruit"], False, "Sa", Passionfruit_Info, 5.99, f"{FileStart}Passionfruit.png")
Araza = Fruit(["Araza"], False, "Sa", Araza_Info, 5.99, f"{FileStart}Araza.png")

# Asia Fruits
Durian = Fruit(["Durian"], False, "Asia", Durian_Info, 7.99, f"{FileStart}Durian.png")
Carambola = Fruit(["Carambola"], False, "Asia", Carambola_Info, 5.99, f"{FileStart}Carambola.png")
Mangosteen = Fruit(["Mangosteen"], False, "Asia", Mangosteen_Info, 4.99, f"{FileStart}Mangosteen.png")
Rambutan = Fruit(["Rambutan"], False, "Asia", Rambutan_Info, 8.99, f"{FileStart}Rambutan.png")
Pomelo = Fruit(["Pomelo"], False, "Asia", Pomelo_Info, 6.99, f"{FileStart}Pomelo.png")
Longan = Fruit(["Longan"], False, "Asia", Longan_Info, 5.99, f"{FileStart}Longan.png")
Akebi = Fruit(["Akebi"], False, "Asia", Akebi_Info, 3.99, f"{FileStart}Akebi.png")
Persimmon = Fruit(["Persimmon"], False, "Asia", Persimmon_Info, 7.99, f"{FileStart}Persimmon.png")

# Europe Fruits
Maracujá_dos_AçoresList = ["Maracuja dos Acores", "Maracuja dos Açores", "Maracuja dos Açores", "Maracujá dos Açores"]
Maracujá_dos_Açores = Fruit(Maracujá_dos_AçoresList, "Maracujá dos Açores", "Europe", Maracujá_dos_Açores_Info, 6.99, f"{FileStart}Maracujá dos Açores.png")

# Africa Fruits
Kiwano = Fruit(["Kiwano"], False, "Africa", Kiwano_Info, 8.99, f"{FileStart}Kiwano.png")
Prickly_Pear = Fruit(["Prickly Pear"], False, "Africa", Prickly_Pear_Info, 4.99, f"{FileStart}Prickly Pear.png")

# Oceania Fruits
Pandanus = Fruit(["Pandanus"], False, "Oceania", Pandanus_Info, 8.99, f"{FileStart}Pandanus.png")
Quandong = Fruit(["Quandong"], False, "Oceania", Quandong_Info, 7.99, f"{FileStart}Quandong.png")

# Fruit Handlers
FruitList = []
for object in gc.get_objects():
    if isinstance(object, Fruit):
        FruitList.append(object)

FruitList = rearrangeFruits(FruitList)

FruitNameList = {}
for fruit in FruitList:
    if len(fruit.name) > 1:
        for FruitName in fruit.name:
            FruitNameList[FruitName] = fruit
    else:
        FruitNameList[fruit.name[0]] = fruit

loadFruits(FruitList)

screen.mainloop()