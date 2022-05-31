from scam.bot import *

referal = input("Entrez votre lien d'affiliation : ")

while Bot.nb_error < 5:
    bot = Bot(referal)
    bot.scam()

log(f"Scam run finished with {Bot.nb_scam} success Scam",Type.Success)