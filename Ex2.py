
# Exercise 2

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import pymysql


def start(bot, update):
    update.message.reply_text("Hello! Please issue commands in this format:\n")
    update.message.reply_text("1. /showTasks\n"
                              "2. /newTask <task to add>\n"
                              "3. /removeTask <task to remove>\n"
                              "4. /removeAllTasks <substring to use to remove all the tasks that contain it>\n")


def unknownMessage(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I'm sorry I can't do that.")


def showTasks(bot, update):
    """
    Show existing tasks
    :return:
    """
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("To do list:\n")
    sql = "SELECT todo from task order by todo"
    conn = pymysql.connect(user="root", password="root", host="localhost", database="todolist")
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    for task in results:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text(task[0], end="")


def buidString(words):
    ret = ""
    for word in words:
        ret = ret + " " + word
    return ret.strip()


def newTask(bot, update, args):
    """
    Add a new task to the list
    :return:
    """

    if args is not None:
        new = buidString(args)
        sql = "insert into task(todo) values (%s)"
        conn = pymysql.connect(user="root", password="root", host="localhost", database="todolist")
        cur = conn.cursor()
        cur.execute(sql, new)
        conn.commit()
        cur.close()
        conn.close()
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("New task added successfully")


def remove_all(bot, update, args):
    """
    Remove an existing task from the list
    :return:
    """
    if args is None:
        return

    to_be_removed = []

    task = buidString(args)
    sql = "SELECT * from task;"
    conn = pymysql.connect(user="root", password="root", host="localhost", database="todolist")
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    for (identifier, todo) in results:
        if task in todo:
            to_be_removed.append(identifier)

    if to_be_removed.__sizeof__() == 0:
        update.message.reply_text("Task %s is not in the list" % task)
    else:
        sql = "delete from task where id_task=%s;"
        conn = pymysql.connect(user="root", password="root", host="localhost", database="todolist")
        cur = conn.cursor()
        for element in to_be_removed:
            cur.execute(sql, element)
        conn.commit()
        cur.close()
        conn.close()
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Task(s) Removed")


def remove_task(bot, update, args):

    if args is None:
        return

    task = buidString(args)
    sql = "SELECT * from task;"
    conn = pymysql.connect(user="root", password="root", host="localhost", database="todolist")
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    for row in results:
        if task == row[1]:
            sql = "DELETE from task WHERE todo=%s;"
            conn = pymysql.connect(user="root", password="root", host="localhost", database="todolist")
            cur = conn.cursor()
            cur.execute(sql, task)
            conn.commit()
            cur.close()
            conn.close()
            bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
            update.message.reply_text("Task Removed")
            return

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("Task is not in the list")
    return


def main():
    """
    The bot will help you manage your tasks
    """

    updater = Updater(token='')

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", showTasks))
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", remove_task, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", remove_all, pass_args=True))
    dp.add_handler(MessageHandler(Filters.all, unknownMessage))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
