print("OpenHavroniya\n      by Andrey Daniluk and TideSoft!\nLoading...")
print("Import modules...")
import os, os.path, sys, random, sqlite3, configparser
from vkbottle.bot import Bot, rules, Message


print("Connect to database...")
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS openhavroniya (inttxt, outtxt)")


print("Inzialite libs to work...")
config = configparser.ConfigParser()
if not os.path.exists("config.ini"):
    print("Error: Config not found. Let`s to create it!")
    intk = input("Your VK token: ")
    with open("config.ini", "w") as wicicnf:
        wicicnf.write("[vk]\ntoken = " + intk)
config.read("config.ini")
bot = Bot(config.get("vk", "token"))


print("Inzialite vkbottle commands, and try to start bot")

@bot.on.message(text="/delete-reply <wtext>\n<wttext>")
async def antxt(message: Message, wtext, wttext):
    cursor.execute("DELETE FROM openhavroniya WHERE inttxt='" + wtext + "' AND outtxt='" + wttext +"'")
    conn.commit()
    delout = cursor.fetchall()
    await message.answer("Фраза удалена из БД")

@bot.on.message(text="/create-reply <wtext>\n<wttext>")
async def antxt(message: Message, wtext, wttext):
    cursor.execute("INSERT INTO openhavroniya (inttxt, outtxt) VALUES ('" + wtext + "', '" + wttext +"')")
    conn.commit()
    await message.answer("Добавленно!")

@bot.on.message(text="/reply <reqoutp>")
async def antxt(message: Message, reqoutp):
    outpt = ""
    cursor.execute("SELECT outtxt FROM 'openhavroniya' WHERE inttxt='" + reqoutp +"'")
    outp = cursor.fetchall()
    for i in outp:
        ii = i[0]
        outpt = outpt + str(ii) + "\n"
    if str(outpt) != "":
        await message.answer(str("Ниже приведены варианты ответа на сообщение с текстом \"" + reqoutp + "\" (" + str(len(outp)) +"шт.):\n" + str(outpt)))
    else:
        await message.answer("В базе ответов нет ответа на \"" + reqoutp +"\"")

@bot.on.message(text="/help")
async def antxt(message: Message):
    await message.answer("Простые примеры:\n\nСоздание ответа:\n/create-reply 300\nОтсоси у тракториста!\n\n Просмотр всех ответов на этот запрос: /reply 300\n\nУдаление ответа на входящее сообщение:\n/delete-reply 300\n Отсоси у тракториста!")

@bot.on.message(text="<anytext>")
async def antxt(message: Message, anytext):
    cursor.execute("SELECT outtxt FROM 'openhavroniya' WHERE inttxt='" + anytext +"'")
    outp = cursor.fetchall()
    outpp = []
    for i in outp:
        outpp.append(i[0])
    try:
        await message.answer(random.choice(outpp))
    except:
        None
bot.run_forever()