from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram.constants import ParseMode
import logging
from config import TOKEN

class taskL:
    def __init__(self, descr = "empty"):
        self.descr = descr
        self.done = False
    def taskDone(self, done = True):
        self.done = done
    def getState(self):
        return bool(self.done)
    def getDescr(self):
        return str(self.descr)
    def clear(self):
        self.descr = ""
        self.done = False


TaskList = []
fclear = False

user_command = [
    BotCommand("start", "start bot"),
    BotCommand("list", "show list of tasks"),
    BotCommand("help", "show list of commands"),
    BotCommand("clear", "clear list")
]

# updater - получает сообщения
# dispatcher - обрабатывает сообщения
# Логи для ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# `update.effective_chat.id` - определяем `id` чата, откуда прилетело сообщение 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_my_commands(user_command)
    global fclear 
    fclear = False
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello! I'm a bot - TaskPlaner." + \
            "\nWith me, you will be able to make a list of your tasks and mark completed ones." +\
            "\nLet's try to make Your first list of tasks" + \
            "\n\n Commands:" +\
            "\n/add <description> - add 1 task" +\
            "\n/done <number of task> - set task as completed" +\
            "\n/not_done <number of task> - set task as uncompleted" +\
            "\n/list - show list of tasks"+\
            "\n/help - show list of commands" +\
            "\n/clear - clear the list"+\
            "\n\np.s.: use commands without <>"
        )
    

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    TaskList.clear()
    global fclear
    fclear = True

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="The list has been successfully cleared")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Commands:" +\
            "\n/add <description> - add 1 task" +\
            "\n/done <number of task> - set task as completed" +\
            "\n/not_done <number of task> - set task as uncompleted" +\
            "\n/list - show list of tasks"+\
            "\n/help - show list of commands" +\
            "\n/clear - clear the list"+\
            "\n\np.s.: use commands without <>"
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I can't talk to you."+\
            "\n(You can use the commands from the first message after /start)"
        )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Sorry, I didn't understand that command." +\
            "\n(try using the commands from the first message after /start)"
        )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    task = text.removeprefix("/add")
    taskinlist = taskL(task)
    res = ""
    if task == "" or task == " ":
        res = "Sorry, but the task is empty"
    else:
        res = "Your task was successfully added!"
        TaskList.append(taskinlist)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=res)

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    listoftask = "The list of your tasks is presented below \n"
    descr = ""
    tsakitem = ""
    don = False
    t = taskL()

    if len(TaskList) == 0:
        listoftask += "\nIt's empty"
    else:
        for i in range(0, len(TaskList)):
            t = TaskList[i]
            descr = t.getDescr()
            don = t.getState()
            taskitem = '*' + str(i+1) + ')*' + descr
            if don:
                listoftask += '~'+taskitem+'~'
                # for c in taskitem:
                #     listoftask += c + '\u0336'
            else:
                listoftask += taskitem
            listoftask += '\n'

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=listoftask, parse_mode=ParseMode.MARKDOWN_V2)

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = ""
    text = update.message.text
    numtext = text.removeprefix("/done ")
    fnum = not numtext.isnumeric()
    if fnum:
        res = "Incorrect number of task"
    else:
        num = int(numtext)
        t = taskL()
        fdone = False
        if num >= len(TaskList)+1:
            res = "You don't have a task with that number, check it with /list"
        else:
            t = TaskList[num-1]
            fdone = t.getState()
            if fdone:
                res = "The task has already been marked as done"
            else:
                res = "The task is marked as done!"
                t.taskDone()

    await context.bot.send_message(
    chat_id=update.effective_chat.id, 
    text=res)

async def not_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = ""
    text = update.message.text
    numtext = text.removeprefix("/not_done ")
    if not numtext.isnumeric():
        res = "Incorrect number of task"
    else:
        num = int(numtext)
        t = taskL()
        fdone = False
        if num >= len(TaskList)+1:
            res = "You don't have a task with that number, check it with /list"
        else:
            t = TaskList[num-1]
            fdone = t.getState()
            if not fdone:
                res = "The task has already been marked as not done"
            else:
                res = "The task is marked as not done!"
                t.taskDone(False)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=res)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    clear_handler = CommandHandler('clear', clear)
    application.add_handler(clear_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    add_handler = CommandHandler('add', add)
    application.add_handler(add_handler)

    list_handler = CommandHandler('list', list)
    application.add_handler(list_handler)

    done_handler = CommandHandler('done', done)
    application.add_handler(done_handler)
    not_done_handler = CommandHandler('not_done', not_done)
    application.add_handler(not_done_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # if (fclear == True):
    #     application.shutdown()
    # else:
    application.run_polling()




