*****************************************************
CPE 466                  Alex Dekhtyar, Jacob Verburg
Cal Poly		  Computer Science Department
San Luis Obispo                College of Engineering 
California                   dekhtyar@csc.calpoly.edu   
*****************************************************
		  EXTENDED BAKERY DATASET
               Version 1.0
             April 1, 2009
*****************************************************
Sources:  this is a synthesized dataset. 

******************************************************

This file describes the contents of the  EXTENDED BAKERY
dataset developed for CPE 466, Knowledge Discovery in Data,
course at Cal Poly.

The dataset contains information about one year worth
of sales information for a couple of small bakery shops.
The sales are made by employees. The dataset contains
information about the different store locations, the assortments of
baked goods offered for sale and the purchases made.


General Conventions.

 1. Setup, insert, build, and cleanup scripts are provided.


  The dataset consists of the following files:

   - EB-build-location.sql : information about the bakery's locations
   - EB-build-employee.sql : information about the bakery's employees
   - EB-build-goods.sql    : information about the baked goods offered
                             for sale by the bakery
   - EB-build-items.sql    : itemized reciept infromation for purchases
   - EB-build-reciepts.sql : general reciept information for purchases


 EB-build-reciepts.sql stores information about individual reciepts
(purchases by customers). Each purchase may contain from
one to eight items, items.sql contains itemized reciept information.


 Individual files have the following formats.

**************************************************************************

 EB-build-location.sql

     City: City the store is located in
    State: State the store is located in
      Zip: Zip the store is located in
   Street: Street the store is located on
 StoreNum: unique identifier of the store

**************************************************************************

 EB-build-employee.sql

     Last: last name of the employee
    First: first name of the employee
 HireDate: date employee was hired
 FireDate: date employee was fired
 Position: job title (e.g., Shift Manager, Barista, Cashier)
 FullTime: true for full time, false for part time
 StoreNum: store they work at (see location.StoreNum)
    EmpId: unique identifier for the employee



**************************************************************************


 EB-build-goods.sql

     Id : unique identifier of the baked good
  Flavor: flavor/type of the good (e.g., "chocolate", "lemon")
    Food: category of the good (e.g., "cake", "tart")
   Price: price (in dollars) 
    Type: Food or Drink



**************************************************************************

 EB-build-items.sql

    Reciept : reciept number (see reciepts.RecieptNumber)
   Quantity : amount of this item purchased, (e.g. 2 for two chocolate cakes)
    Item    : identifier of the item purchased (see goods.Id)
    


**************************************************************************

 EB-build-receipts.sql

RecieptNumber : unique identifier of the reciept
     SaleDate : date of the purchase. The date is
                in  DD-Mon-YYY format, which is the
                default Oracle's format for DATE data type.
      Weekend : true for if this was a saturday or sunday
	    isCash: true they paid in cash, false they paid with credit
         EmpId: Employee who made the sale, (see employee.EmpId)
	  StoreNum: Store this receipt came from, (see location.StoreNum)

**************************************************************************
**************************************************************************

Permission granted to use and distribute this dataset in its current form, 
provided this file  is kept unchanged and is distributed together with the 
data.

Permission granted to modify and expand this dataset, provided this
file is updated accordingly with new information.

**************************************************************************
**************************************************************************

