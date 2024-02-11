from aiogram import Bot, Dispatcher, executor, types
from transformers import pipeline

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

check_tox = pipeline("text-classification", model="cointegrated/rubert-tiny-toxicity")
replace_tox = pipeline("text2text-generation", model="s-nlp/ruT5-base-detox")

@dp.message_handler()
async def detox(message: types.Message):
    before = message.text

    check = check_tox(before.lower())

    if check[0]['label'] != "non-toxic":
        after_temp = replace_tox(before)
        after_t1 = f"'{after_temp[0]['generated_text']}"
        final = "".join(after_t1[1:])

        if final == before:
            await message.reply("[delete]")
        else:
            await message.reply(final)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)