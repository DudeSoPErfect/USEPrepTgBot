# USEPrepTgBot

### The essence of the program
Telegram bot, that helps to prepair for United State Exam in Mathematics and Russian language. Uses SQLite3.
Sends theory files, creates tests for cheking knowledges in accents, trigonometric formulas.

### File Description
* **main.py** - The main program file. 
Calls functions from other files, main logic is based here.
* **paronimy_data_base.py** - Auxiliary program file.
Contains paronims to generate appropriate tests.
* **udar.db** - data program file.
Contains data and correct answers for accents test.
* **Паронимы.docx** - theory file.
Contains a theory for the paronyms
* **triga** - folder consist of formulas images.
Contains images of formulas to generate visually convenient formulas tests.

### How to launch
1. Upload files in one directory.
2. Create a telegram bot and get a unique token (you can read about it on the official website)
3. Insert the token into the required field at the beginning of the interpreted code.
4. Launch the bot.
5. Enjoy and get prepaired for the USE :)
