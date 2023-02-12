import openai
from pyrogram import Client, filters
import info
from deep_translator import GoogleTranslator

openai.api_key = "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"  # supply your API key however you choose

app = Client("my_bot", api_id=info.api_id, api_hash=info.api_hash, bot_token=info.bot_token)

@app.on_message(filters.private & filters.command('start'))
async def hello(client, msg):
  await client.send_message(msg.chat.id, f'welcome {msg.from_user.username} to bot **OpenAI GPT**')


@app.on_message(filters.private & filters.text)
async def sendphoto(client, msg):
    await client.send_message(msg.chat.id,f'جاري البحث...')
    translated = GoogleTranslator(source='auto', target='en').translate(msg.text)  # output -> Weiter so, du bist großartig
    print(translated)
    image_resp = openai.Image.create(prompt=translated , n=4, size="512x512")
    for i in image_resp['data']:
        #print(i['url'])
        await app.delete_messages(msg.chat.id, msg.id + 1)
        await client.send_photo(msg.chat.id, i['url'], f"@P6SBOT,")

app.run()
