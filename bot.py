from random import randrange
import discord
from discord_slash import SlashCommand


token = 'token'   # bot token
client = discord.Client()

slash = SlashCommand(client, sync_commands=True)


@slash.slash(name="wordle", description="generates a game of wordle!")
async def wordle(ctx):

    """
    Starts a wordle game and calls the wordle generator.
    """


    won = 0 # logs whether the game is over

    iteration = 0 # logs whether the game iterationed


    guess = [['1', '2', '3', '4', '5']] # logs guesses stripped into individual letters

    wordlist = open('wordlist.txt').readlines() # read from file containing all possible correct words
    number = randrange(len(wordlist) + 1)   
    correct_word = list(wordlist[number][:-1])  # pick a random word
    print(correct_word)

    print_guesses = '' # logs the wordle square block thingy 


    playerid = ctx.author.id
    id = ctx.channel.id


    while won != 1:

        if iteration == 0:

            embed = discord.Embed(color=discord.Colour.green())
            embed.add_field(name='Wordle', value='Start making guesses!')
            await ctx.send(embed=embed)


        won, guess, print_guesses = await wordle_generator(ctx, id, guess, correct_word, print_guesses, playerid)


        iteration += 1


        if iteration == 6 and won == 0:
            embed = discord.Embed(color=discord.Colour.green())
            embed.add_field(name='Wordle', value=f'<@{ctx.author.id}> lost! \n{print_guesses}')
            await ctx.send(embed=embed)


        if won == 1:
            break          


async def wordle_generator(ctx, CHANNEL_ID, guess, correct_word, print_guesses, playerid):

    """
    Generates a game of wordle.
    """


    with open('validguesses.txt', 'r') as file:
        validguesses = file.read().replace('\n', '')    # read all possible valid guesses from a file


    msg = await client.wait_for(event="message")   # get word


    if msg.channel.id != CHANNEL_ID or msg.author.id != playerid:
        return -1, guess, print_guesses
    if msg.content not in validguesses:
        await ctx.send(f'{msg.content} is not a valid guess!') 
        return -1, guess, print_guesses

    else:
        check_guess = list(msg.content)


    # check if guess os correct and update the block thingy accordingly
    string = list('⬛⬛⬛⬛⬛\n')
    for key, _ in enumerate(guess[-1]):
        if check_guess[key] == correct_word[key]:
            string[key] = '🟩'
        elif check_guess[key] in correct_word:
            string[key] = '🟨'

    print_guesses = print_guesses + ''.join(string)


        # send messages with the block thingy
    if check_guess == correct_word:
        
        embed = discord.Embed(color=discord.Colour.green())
        embed.add_field(
            name='Wordle',
            value=f"<@{playerid}> won:\nThe word was: {''.join(correct_word)}\n{print_guesses}",
        )

        await ctx.send(embed=embed)
        return 1, guess, print_guesses

    else:

        embed = discord.Embed(color=discord.Colour.green())
        embed.add_field(name='Wordle', value=f'<@{msg.author.id}> guessed:\n{print_guesses}')
        await ctx.send(embed=embed)
        return 0, guess, print_guesses


client.run(token)   # run the bot
