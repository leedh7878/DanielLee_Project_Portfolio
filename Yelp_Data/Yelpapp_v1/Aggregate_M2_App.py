import sys
from unicodedata import decimal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2
from PyQt5.QtWidgets import QMessageBox

qtCreatorFile = "Aggregate_YelpApp2.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class yelp_app(QMainWindow):
    def __init__(self):
        super(yelp_app, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged) # when item in state list is changed execute stateChanged function (pass in function result)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged) # when item in city list is changed execute cityChanged function
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.businessCategoryList.itemSelectionChanged.connect(self.businessSearch)
        self.ui.EnterName.textChanged.connect(self.enterUser)
        self.ui.SelectUser.itemSelectionChanged.connect(self.selectUser)
        # self.getname(self.businessChanged)
        self.ui.businessTable.cellClicked.connect(self.businessChanged)
        self.ui.EnterBusiness.textChanged.connect(self.enterBusiness)
        self.ui.businessTable.selectionModel().selectionChanged.connect(self.businessChanged)
        #self.ui.businessCategoryList.itemSelectionChanged.connect(self.getBusinessCategory)
        #self.ui.bname.textChanged.connect(self.getBusinessNames)
        #self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)

        # self.ui.SelectUser.itemSelectionChanged.connect(self.latestip_friend)
        # self.ui.SelectUser.itemSelectionChanged.connect(self.getFriends)
        # self.ui.SelectUser.itemSelectionChanged.connect(self.getFriends)


    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='project_451' user='postgres' host='localhost' password='laoemdk2anel'")
        except Exception as e: 
            print('Unable to connect to the database!',e)
        cur = conn.cursor()  
        cur.execute(sql_str)   
        conn.commit()
        result = cur.fetchall()   
        conn.close()
        return result


    def loadStateList(self):
        self.ui.stateList.clear() # remove everything from comboBox first
        sql_str = "SELECT distinct state FROM business ORDER BY state;"  
        try:
            results = self.executeQuery(sql_str)
            for row in results: # for each row in results add it to the list box
                self.ui.stateList.addItem(row[0])
        except Exception as e:
            print("Load state list query failed! Error message: ", e)   
        self.ui.stateList.setCurrentIndex(-1) # make sure there is no state selected and displayed before selection happens
        self.ui.stateList.clearEditText() 


    def stateChanged(self):
        self.ui.cityList.clear() # clear entries before selection
        #self.ui.zipcodeList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex()>=0): # if a state has been selected (index is >= 0)
            sql_str = "SELECT distinct city FROM business WHERE state ='{}' ORDER BY city;".format(state)
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
                
            except Exception as e:
                print("State changed query failed! Error message: ", e)  



    def cityChanged(self):
        self.ui.zipcodeList.clear() # clear entries before selection
        self.ui.numBusinessesZipcode.clear()
        self.ui.businessCategoryList.clear()
        self.ui.TopCategoriesZipcodeList.clear()

        state = self.ui.stateList.currentText() # retrieve current state
        city = self.ui.cityList.selectedItems()[0].text() # retrieve current city
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            sql_str = "SELECT distinct zipcode FROM business WHERE state ='{0}' AND city ='{1}';".format(state,city)
        
            try:
                results = self.executeQuery(sql_str)

                currentRowCount = 0
                for row in results:
                    self.ui.zipcodeList.addItem(str(row[0]))
                    currentRowCount += 1
            except Exception as e: 
                print("City changed query failed! Error message: ", e)



    def zipcodeChanged(self):
        self.ui.numBusinessesZipcode.clear()
        self.ui.businessCategoryList.clear()
        self.ui.TopCategoriesZipcodeList.clear()


        state = self.ui.stateList.currentText() # retrieve current state
        city = self.ui.cityList.selectedItems()[0].text() # retrieve current city
        zipcode = self.ui.zipcodeList.selectedItems()[0].text() # retrieve current zipcode

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) > 0):
            sql_str = "SELECT COUNT(business_id) FROM business WHERE state ='{0}' AND city ='{1}' AND zipcode ='{2}';".format(state,city,zipcode)
        
            try:
                results = self.executeQuery(sql_str)
                
                self.ui.numBusinessesZipcode.addItem(str(results[0][0]))

            except Exception as e: 
                print("Count Businesses in Zipcode query failed! Error message: ", e)



            sql_str2 = "SELECT distinct category_name FROM categories,business WHERE categories.business_id = business.business_id AND state ='{0}' AND city ='{1}' AND zipcode ='{2}' ORDER BY category_name;".format(state,city,zipcode)
            try:
                results2 = self.executeQuery(sql_str2)

                #self.ui.businessCategoryList.setColumnCount(len(results2[0]))
                #self.ui.businessCategoryList.setRowCount(len(results2))

                currentRowCount = 0

                for row in results2:

                    for colCount in range (0,len(results2[0])):
                        self.ui.businessCategoryList.addItem(str(row[colCount]))
                        #self.ui.businessCategoryList.addItem(currentRowCount, colCount,QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except Exception as e: 
                print("Get Business Category query failed! Error message: ", e)


            # show top categories (star rating >= 4.5) 
            sql_str3 = "SELECT COUNT(*), categories.category_name FROM business, categories WHERE business.business_id = categories.business_id AND zipcode ='{0}'  AND city ='{1}' GROUP BY categories.category_name ORDER BY COUNT(*) DESC;".format(zipcode,city)
            try:
                results3 = self.executeQuery(sql_str3)
                
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.TopCategoriesZipcodeList.horizontalHeader().setStyleSheet(style)

                self.ui.TopCategoriesZipcodeList.setColumnCount(len(results3[0])) # get first tuple and count entries
                self.ui.TopCategoriesZipcodeList.setRowCount(len(results3)) # count rows

                # add labels for header and set width to length of item
                self.ui.TopCategoriesZipcodeList.setHorizontalHeaderLabels(['# of Businesses', 'Top Categories'])
                self.ui.TopCategoriesZipcodeList.setColumnWidth(0, 200)
                self.ui.TopCategoriesZipcodeList.setColumnWidth(1, 300)


                currentRowCount = 0
                for row in results3:
                    for colCount in range (0,len(results3[0])):
                        #self.ui.TopCategoriesZipcodeList.Item(str(row[colCount]))
                        self.ui.TopCategoriesZipcodeList.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except Exception as e: 
                print("Get Business Category query failed! Error message: ", e)

                # self.ui.TopCategoriesZipcodeList.resizeColumnsToContents()

        

            sql_str4 = "SELECT name, address, city, state, stars, numTips, numCheckins FROM business WHERE zipcode ='{}' ORDER BY name;".format(zipcode)
            try:
                results4 = self.executeQuery(sql_str4)

                style = "::section {""background-color: #f3f3f3; }" # #faded8
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)

                self.ui.businessTable.setColumnCount(len(results4[0]))
                self.ui.businessTable.setRowCount(len(results4))

                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', '# of tips', 'total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()

                currentRowCount = 0
                for row in results4:
                    for colCount in range (0,len(results4[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e: 
                print("Show Businesses query failed! Error message: ", e)
            
            self.ui.popBList.clear()
            print(state, city, zipcode)

            sql_str5 = """\
                select temp.attribute_value, count(temp.attribute_value)
                from (select concat(attr_name, ' - ',  value) as attribute_value, attributes.business_id
                        from attributes, (select business_id
                                            from business
                                            where state = '{0}' AND  City ='{1}' AND Zipcode = '{2}'
                                                AND stars >=4.5) as recur
                        where value != 'False' AND value != 'no' AND value !='none'
                            and attributes.business_id = recur.business_id)as temp
                group by temp.attribute_value
                order by count desc;              
                """.format(state,city,zipcode)
            try:
                results5 = self.executeQuery(sql_str5)
                
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popBList.horizontalHeader().setStyleSheet(style)

                self.ui.popBList.setColumnCount(len(results5[0])) # get first tuple and count entries
                self.ui.popBList.setRowCount(len(results5)) # count rows

                # add labels for header and set width to length of item
                self.ui.popBList.setHorizontalHeaderLabels(['count', 'Attributes'])
                self.ui.popBList.setColumnWidth(0, 200)
                self.ui.popBList.setColumnWidth(1, 80)



                currentRowCount = 0
                for row in results5:
                    for colCount in range (0,len(results5[0])):
                        #self.ui.TopCategoriesZipcodeList.Item(str(row[colCount]))
                        self.ui.popBList.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except Exception as e: 
                print("Get attributes Category query failed! Error message: ", e)   


    def cellClicked(self, row, col):    
        item = self.businessTable.item(row, col)   
        self.SF = item.text()    
        self.label_2.setText(self.SF)

    def businessChanged(self, row, col):
        self.ui.CatBusinessList.clear()
        self.ui.AttrBusinessList.clear()
        business = self.ui.businessTable.selectedItems()[0].text()  # retrieve current business

        if (self.ui.businessTable.currentRow() >= 0):
            sql_str = "SELECT DISTINCT category_name FROM business, categories WHERE business.business_id = categories.business_id AND business.name ='{0}';". format(business)
            #sql_str = pd.DataFrame(columns=[sql_strr])
            #.format(business.row(), business.col())
            try:
                results = self.executeQuery(sql_str)

                currentRowCount = 0
                for row in results:
                    for colCount in range (0,len(results[0])):
                        #self.ui.TopCategoriesZipcodeList.Item(str(row[colCount]))
                        self.ui.CatBusinessList.addItem(row[colCount])
                    currentRowCount += 1

            except Exception as e:
                print("Add categories when select business query failed! Error message: ", e)

            sql_str2 = "SELECT DISTINCT attr_name FROM business, attributes WHERE business.business_id = attributes.business_id AND value != 'False' AND value != 'no' AND value !='none' AND business.name ='{0}';".format(business)
            #sql_str2 = pd.DataFrame(columns=[sql_strr2])
            #.format(business.row(), business.col())
            try:
                results2 = self.executeQuery(sql_str2)
                
                currentRowCount = 0
                for row in results2:
                    for colCount in range (0,len(results2[0])):
                        #self.ui.TopCategoriesZipcodeList.Item(str(row[colCount]))
                        self.ui.AttrBusinessList.addItem(row[colCount])
                    currentRowCount += 1

            except Exception as e:
                print("Add attributes when select business query failed! Error message: ", e)



    def businessSearch(self):
        self.ui.businessTable.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) > 0) and (len(self.ui.businessCategoryList.selectedItems()) > 0):
            # When user selects one or more categories, the search results will be filtered based on the selected business categories
        
            zipcode = self.ui.zipcodeList.selectedItems()[0].text() # retrieve current zipcode
            businessCategory = self.ui.businessCategoryList.selectedItems()[0].text() # retrieve current businessCategory
            city =  self.ui.cityList.selectedItems()[0].text()

            sql_str1 = "SELECT name, address, city, state, stars, numTips, numCheckins FROM business, categories  WHERE business.business_id = categories.business_id  AND zipcode ='{0}' and category_name = '{1}' and city = '{2}' ORDER BY name;".format(zipcode,businessCategory,city)

            try:
                results1 = self.executeQuery(sql_str1)

                style = "::section {""background-color: #f3f3f3; }" # #faded8
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)

                self.ui.businessTable.setColumnCount(len(results1[0]))
                self.ui.businessTable.setRowCount(len(results1))

                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', '# of tips', 'total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                
                currentRowCount = 0
                for row in results1:
                    for colCount in range (0,len(results1[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e:
                print("Filtering by businessCategory query failed Error message: ", e)
    



    def enterUser(self):
        self.ui.SelectUser.clear() # so that the list box gets cleared before, otherwise adds search to previous results
        userName = self.ui.EnterName.text() # get text from that box we enter

        sql_str = "SELECT user_id FROM users WHERE name LIKE '%{}%' ORDER BY name;".format(userName)
        try: 
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.SelectUser.addItem(row[0]) # add each rows data to list box
        except Exception as e:
            print("Get users names query failed! Error message: ", e)


    def selectUser(self):
        self.ui.Name.clear()
        self.ui.Stars.clear()
        self.ui.YelpingSince.clear()
        self.ui.Funny.clear()
        self.ui.Cool.clear()
        self.ui.Useful.clear()
        self.ui.Fans.clear()
        self.ui.TipCount.clear()
        self.ui.TotalLikes.clear()

        UserID = self.ui.SelectUser.selectedItems()[0].text() # get user name from entered text box, only first one selected
        if len(UserID) > 0: # when clear search, then just show all
        
            sql_str = "SELECT name, avg_stars, yelping_since, funny, cool, useful, fans, tipCount, totalLikes FROM users WHERE user_id = '{}' ;".format(UserID) # pass user name into query, filter by userName, should return single value
            try: 
                results = self.executeQuery(sql_str)
                #self.ui.bcity.setText(results[0]) # puts the results (city of business) into the bcity text box
                self.ui.Name.addItem(results[0][0])
                self.ui.Stars.addItem(str(results[0][1]))
                self.ui.YelpingSince.addItem(str(results[0][2]))
                #self.ui.Votes(str(results)[3])
                self.ui.Funny.addItem(str(results[0][3]))
                self.ui.Cool.addItem(str(results[0][4]))
                self.ui.Useful.addItem(str(results[0][5]))
                self.ui.Fans.addItem(str(results[0][6]))
                self.ui.TipCount.addItem(str(results[0][7]))
                self.ui.TotalLikes.addItem(str(results[0][8]))


            except Exception as e:
                print("Display user information query failed! Error message: ", e)

            self.ui.FriendsList.clear()

            sql_frined_list =  """\
                SELECT users.name, users.avg_stars, users.fans, users.tipCount, users.yelping_since
                FROM (SELECT distinct friend.friend_id
                    FROM friend 
                    WHERE friend.user_id = '{}')as temp, users
                WHERE temp.friend_id = users.user_id
                """.format(UserID)

            try: 
                results2 = self.executeQuery(sql_frined_list)
                # puts the results from query into the assigned text boxes
                #self.ui.Name.addItem(results[0][0])
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.FriendsList.horizontalHeader().setStyleSheet(style) # tipfriendllist = change to qlsit widget to qtable widget

                self.ui.FriendsList.setColumnCount(len(results2[0]))
                self.ui.FriendsList.setRowCount(len(results2))

                self.ui.FriendsList.setHorizontalHeaderLabels(['Friend Name', 'Avg Stars', 'Fans', 'tipCount', 'Yelping Since'])
                self.ui.FriendsList.resizeColumnsToContents()
            
                currentRowCount = 0
                for row in results2:
                    for colCount in range (0,len(results2[0])):
                        self.ui.FriendsList.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                

            except Exception as e:
                print("Display friends information query failed! Error message: ", e)




        self.ui.TipsFriendsList.clear()

        user_id = self.ui.SelectUser.selectedItems()[0].text()
        print(user_id)

        sql_str_latestip = """\
        select distinct users.name, business.name, business.city, Temp.date, tip.tipText
        from(select friend.friend_id, Max(tip.tipDate) as date
            from Users,friend, tip
            where users.user_id = '{}'
                AND users.user_id = friend.user_id
                AND friend.friend_id = tip.user_id 
            group by friend.friend_id)as temp, business, tip,users
        where Temp.friend_id = Users.user_id
            AND Temp.date = tip.tipDate
            AND tip.business_id = business.business_id;""".format(user_id)


        try:
            results1 = self.executeQuery(sql_str_latestip)
            print((results1))
            if results1:
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.TipsFriendsList.horizontalHeader().setStyleSheet(style) # tipfriendllist = change to qlsit widget to qtable widget

                self.ui.TipsFriendsList.setColumnCount(len(results1[0]))
                self.ui.TipsFriendsList.setRowCount(len(results1))

                self.ui.TipsFriendsList.setHorizontalHeaderLabels(['Friend Name', 'Business', 'City', 'Date', 'Review'])
                currentRowCount = 0
                for row in results1:
                    for colCount in range (0,len(results1[0])):
                        self.ui.TipsFriendsList.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                self.ui.TipsFriendsList.resizeColumnsToContents()

            else: 

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('No lastest review from friend ')
                msg.setWindowTitle("Error")
                msg.exec_()

        except Exception as e:
            print("Filtering by latest tip from friend query failed Error message: ", e)


        # user_id = self.ui.SelectUser.selectedItems()[0].text()
        
        self.ui.FFList.clear()  # remove everything from the list first
 
        sql_ff = """\
            (SELECT 1 as degree, users2.name, users.avg_stars, users.fans, users.tipCount, users.yelping_since 
            FROM friend,users , users as users2
            WHERE users.user_id IN (select friend_id
                                    from friend, users
                                    where users.user_id = '{0}'
                                        AND friend.user_id = users.user_id)
                    AND users.user_id = friend.user_id
                    AND users.user_id != '{1}'
                    AND users2.user_id = friend.friend_id)
            UNION

            (SELECT 2 as degree, users2.name, users.avg_stars, users.fans, users.tipCount, users.yelping_since
            FROM friend,users, users as users2
            WHERE users.user_id IN (SELECT friend.friend_id
                                    FROM friend,users
                                    WHERE users.user_id IN (select friend_id
                                                            from friend, users
                                                            where users.user_id = '{2}'
                                                                AND friend.user_id = users.user_id)
                                            AND users.user_id = friend.user_id)	
                AND users.user_id = friend.user_id
                AND users.user_id != '{3}'
                AND users2.user_id = friend.friend_id); """.format(user_id,user_id,user_id,user_id)

        try:
            results_ff = self.executeQuery(sql_ff)
            print((results_ff))
            print("DDDD")
            if results_ff:
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.FFList.horizontalHeader().setStyleSheet(style) 

                self.ui.FFList.setColumnCount(len(results_ff[0]))
                self.ui.FFList.setRowCount(len(results_ff))

                self.ui.FFList.setHorizontalHeaderLabels(['Degree', 'Friend Name', 'Avg Stars', 'Fans', 'Tip Count', 'Yelping Since'])
                currentRowCount = 0
                for row in results_ff:
                    for colCount in range (0,len(results_ff[0])):
                        self.ui.FFList.setItem(currentRowCount, colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                self.ui.FFList.resizeColumnsToContents()

        except Exception as e:
            print("Load friend of friends list query failed! Error message: ", e)

    def enterBusiness(self):
        self.ui.SelectBusiness.clear() # so that the list box gets cleared before, otherwise adds search to previous results
        businessName = self.ui.EnterBusiness.text() # get text from that box we enter

        sql_str = "SELECT name FROM business WHERE name LIKE '%{}%' ORDER BY name;".format(businessName)
        try: 
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.SelectBusiness.addItem(row[0]) # add each rows data to list box
        except Exception as e:
            print("Get users names query failed! Error message: ", e)



if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = yelp_app()
    #window.show()
    window.showMaximized()
    sys.exit(app.exec_())
