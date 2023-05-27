import discord
import re

bot = discord.Bot()

@bot.slash_command()
async def rgb(ctx, color: str):
    # only hex codes match (with or without the #)
    is_hex = re.search("\A#?[a-fA-F0-9]{6}\Z", color)
    role_list = await ctx.guild.fetch_roles()
    selected_role = None

    for role in role_list:
        if role.name == str(ctx.author.id):
            selected_role = role
            break

    # if we have a proper color code
    if is_hex:
        print("is_hex")
        # create role with name == author id
        if selected_role is None:
            selected_role = await ctx.guild.create_role(name=ctx.author.id)
            await selected_role.edit(position=len(role_list)-1)
            print(f"Created role {ctx.author.id}")
        else:
            print(f"Found role {ctx.author.id}")
        
        rgb = hexToRgb(color)
        await selected_role.edit(color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]))
        print(f"Color edited to {color}")
    else:
        await ctx.respond("Please set color to a hex code. Format: #ffffff")
        return
    
    # if the author doesn't have their role, add it
    if not ctx.author in selected_role.members:
        await ctx.author.add_roles(selected_role)
        print(f"Added role to {ctx.author.id}")

    await ctx.respond(f"Successfully set your role color to {color}!")a

def hexToRgb(hex: str):
    hex = hex.lstrip("#")
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def grab_token():
    ''' Only returns if the file can be read '''
    with open("token.txt", "r") as file:
        return file.read()

bot.run(grab_token())