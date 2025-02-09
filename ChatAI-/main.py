# app id : 1337766870312292392
# public key : b0ebc4abac4ddbacf2e94f9eafd5a19aff470bfdf9b019c4ca628a244f2c0cbe
import discord
import os
import openai 


discord_token = os.getenv("SecretKey") 
openai_api_key = os.getenv("openai")  


if not openai_api_key:
    print("Error: OpenAI API key not found. Make sure you have set the environment variable 'openai'.")
    exit(1)


openai_client = openai.OpenAI(api_key=openai_api_key)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return  

        print(f'Message from {message.author}: {message.content}')
        channel = message.channel

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[{"role": "user", "content": message.content}],  
                temperature=1,
                max_tokens=200,  
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            bot_reply = response.choices[0].message.content
            await channel.send(bot_reply) 

        except Exception as e:
            print(f"Error: {e}")
            await channel.send("Sorry, an error occurred.")

intents = discord.Intents.default()
intents.message_content = True

discord_client = MyClient(intents=intents)  # Renamed to avoid conflict
discord_client.run(discord_token)  # Ensure token is correctly set
