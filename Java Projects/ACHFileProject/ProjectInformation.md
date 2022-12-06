# ACH File Transfer Project
The code in this project was built as a skeleton for a large software network crucial to the previous company I worked for, Fairmount Automation. 
The purpose of the code was to replace the time that employee's would spend figuring out which invoices to pay and write checks for. 
The solution that I wrote here, is an ACH File generator, that creates a text file that is possible to send to an ACH intermediary which would transfer money.
Currently, the code itself uses hard coded values as an example, however, once linked to existing databases within the network, it would be simple to replace these hard coded fields with that data.
The point of this code was so that Fairmount Automation employees would simply be able to press a checkbox, and it would send the correct amount of money owed to that company. This would save time writing checks every other week, which added up to a signifigant chunk of employee time.
What this code does is very similar to what money transfer apps like Venmo and Cashapp use. When you send money over Venmo, a prompt will show up asking you to choose between instant(1.5% fee) and normal(ACH). This is because ACH files are extremely cheap to use, but they generally take a few days to process. 
This program does the same thing, it writes an ACH file to the company that we owe money to, using ACH files. 
The text file achExample.txt is the output file that this program creates and it is an example of what a complete file looks like.
