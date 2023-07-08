import gspread
import pandas as pd
from time import sleep


gc = gspread.service_account(filename= 'creds.json')

RR_sheet = gc.open("RR Locations Test")

updated_sheet = gc.open("Potential Final RR")

#dictionary
def get_grass_and_caves_data(pokemon):
    
    grass_caves_worksheet = RR_sheet.get_worksheet(0)

    pokemon_location_cells = grass_caves_worksheet.findall(pokemon)
    
    if not pokemon_location_cells:
        return

    area_dict = {}

    for cell in pokemon_location_cells:
    
        row = cell.row
        column = cell.col
        name = cell.value
        day_night = ""

        location = grass_caves_worksheet.cell(3, (column - 1)).value
        
        if row <= 16:
            day_night = "Day"
        else:
            day_night = "Night"
        
        percent = int((grass_caves_worksheet.cell(row, (column - 2)).value)[:-1])

        if location not in area_dict:
            area_dict[location] = [day_night, percent]
        
        elif location in area_dict:
            if area_dict[location][0] == day_night:
                area_dict[location][1] += percent
            if area_dict[location][0] != day_night:
                area_dict[location][0] = "Day and Night"
        
    list_of_strings = []

    for location in area_dict:
        
        final_string = ""

        final_string += f"{location}:"

        for entry in area_dict[location]:
            if type(entry) == int:
                string_entry = str(entry)
                string_entry += "%  | "
                final_string += f" {string_entry}"
            else:
                final_string += f" {entry}"

        list_of_strings.append(final_string)
    
    return list_of_strings

#dictionary
def get_fishing_and_surfing_data(pokemon):

    fishing_surfing_worksheet = RR_sheet.get_worksheet(1)

    pokemon_location_cells = fishing_surfing_worksheet.findall(pokemon)

    if not pokemon_location_cells:
        return

    area_dict = {}

    for cell in pokemon_location_cells:
        
        row = cell.row
        column = cell.col
        name = cell.value

        location = fishing_surfing_worksheet.cell(3, (column - 1)).value

        which_rod_or_surf = ""

        if row < 7:
            which_rod_or_surf = "Old Rod"
        elif row > 9 and row < 13:
            which_rod_or_surf = "Good Rod"
        elif row > 15 and row < 21:
            which_rod_or_surf = "Super Rod"
        elif row > 23:
            which_rod_or_surf = "Surfing"
        

        percent = int((fishing_surfing_worksheet.cell(row, (column - 2)).value)[:-1])

        if location not in area_dict:
            area_dict[location] = [which_rod_or_surf, percent]
        elif location in area_dict and which_rod_or_surf in area_dict[location]:
            area_dict[location][(area_dict[location].index(which_rod_or_surf)) + 1] += percent
        elif location in area_dict and which_rod_or_surf not in area_dict[location]:
            area_dict[location].append(which_rod_or_surf)
            area_dict[location].append(percent)


    list_of_strings = []

    for location in area_dict:
        
        final_string = ""

        final_string += f"{location}:"

        for entry in area_dict[location]:
            if type(entry) == int:
                string_entry = str(entry)
                string_entry += "%  | "
                final_string += f" {string_entry}"
            else:
                final_string += f" {entry}"

        list_of_strings.append(final_string)
    
    return list_of_strings

#dictionary
def get_safari_zone_info(pokemon):

    safari_zone_worksheet = RR_sheet.get_worksheet(2)

    pokemon_location_cells = safari_zone_worksheet.findall(pokemon)

    if not pokemon_location_cells:
        return

    area_dict = {}

    for cell in pokemon_location_cells:
        
        row = cell.row
        column = cell.col
        name = cell.value

        location = ""

        if row < 18:
            location = "Center"
        elif row < 35:
            location = "East"
        elif row < 52:
            location = "North"
        else:
            location = "West"
        
        how_where = ""

        if column == 5:
            how_where = "Grass, Day"
        elif column == 10:
            how_where = "Grass, Night"
        elif column == 15:
            how_where = "Old Rod"
        elif column == 20:
            how_where = "Good Rod"
        elif column == 25:
            how_where = "Super Rod"
        elif column == 30:
            how_where = "Surfing"
        
        percent = int((safari_zone_worksheet.cell(row, (column - 2)).value)[:-1])

        if location not in area_dict:
            area_dict[location] = [how_where, percent]
        elif location in area_dict and how_where in area_dict[location]:
            area_dict[location][(area_dict[location].index(how_where)) + 1] += percent
        elif location in area_dict and how_where not in area_dict[location]:
            area_dict[location].append(how_where)
            area_dict[location].append(percent)
        
    list_of_strings = []

    for location in area_dict:
        
        final_string = ""

        final_string += f"{location}:"

        for entry in area_dict[location]:
            if type(entry) == int:
                string_entry = str(entry)
                string_entry += "%  | "
                final_string += f" {string_entry}"
            else:
                final_string += f" {entry}"

        list_of_strings.append(final_string)
    
    return list_of_strings

#list
def get_fossil_info(pokemon):

    fossil_worksheet = RR_sheet.get_worksheet(3)

    pokemon_location_cells = fossil_worksheet.findall(pokemon)

    if not pokemon_location_cells:
        return

    area_list = []

    for cell in pokemon_location_cells:

        row = cell.row
        column = cell.col
        name = cell.value

        shard_or_location = ""

        if row < 10:
            shard_or_location = (fossil_worksheet.cell(3, (column - 1)).value).title()
            shard_or_location += " - Trade with a hiker on 1F of Celadon City Mansion"
        else:
            shard_or_location = (fossil_worksheet.cell(10, (column - 1)).value).title()
        
        area_list.append(shard_or_location)
    
    return area_list

#list
def get_legendary_and_static_info(pokemon):

    legendary_and_static_worksheet = RR_sheet.get_worksheet(4)

    pokemon_location_cell = legendary_and_static_worksheet.find(pokemon)

    if not pokemon_location_cell:
        return

    area_list = []
    if pokemon_location_cell:
        row = pokemon_location_cell.row
        column = pokemon_location_cell.col
        name = pokemon_location_cell.value

        location = legendary_and_static_worksheet.cell(row, (column + 2)).value

        area_list.append(location)

    return area_list

#list
def get_raid_den_info(pokemon):

    raid_den_worksheet = RR_sheet.get_worksheet(5)

    pokemon_location_cells = raid_den_worksheet.findall(pokemon)

    if not pokemon_location_cells:
        return

    area_list = []

    for cell in pokemon_location_cells:

        row = cell.row
        column = cell.col
        name = cell.value

        location_and_star = "Raid Den, " + raid_den_worksheet.cell((row - 2), 2).value

        area_list.append(location_and_star)
    
    return(area_list)

#list
def get_egg_vendor_and_game_corner_info(pokemon):

    egg_and_gc_worksheet = RR_sheet.get_worksheet(6)

    pokemon_location_cells = egg_and_gc_worksheet.findall(pokemon)

    if not pokemon_location_cells:
        return

    area_list = []

    for cell in pokemon_location_cells:

        row = cell.row
        column = cell.col
        name = cell.value

        shard_or_gc = ""

        if row < 13:
            shard_or_gc = (egg_and_gc_worksheet.cell(3, (column - 1)).value).title()
            shard_or_gc += " - Trade shard in at Celadon City Mansion for an egg that MAY contain this Pokemon."
        else:
            shard_or_gc = "Buy at Celadon City Game Corner for 100,000"
        
        area_list.append(shard_or_gc)

        return area_list
    
#dictionary
def get_trade_info(pokemon):

    trade_worksheet = RR_sheet.get_worksheet(7)

    pokemon_location_cell = trade_worksheet.find(pokemon)

    if not pokemon_location_cell:
        return

    area_dict = {} 

    if pokemon_location_cell:
        row = pokemon_location_cell.row
        column = pokemon_location_cell.col
        name = pokemon_location_cell.value

        location = (trade_worksheet.cell((row - 2), (column - 1)).value).title()
        
        if column == 4:
            wanted_pokemon = (trade_worksheet.cell(row, (column + 2)).value)
        else:
            wanted_pokemon = (trade_worksheet.cell(row, (column + 3)).value)

        area_dict[location] = [f"Trade for a {wanted_pokemon}"]

    list_of_strings = []

    for location in area_dict:
        
        final_string = ""

        final_string += f"{location}:"

        for entry in area_dict[location]:
            if type(entry) == int:
                string_entry = str(entry)
                string_entry += "%  | "
                final_string += f" {string_entry}"
            else:
                final_string += f" {entry}"

        list_of_strings.append(final_string)
    
    return list_of_strings

#dictionary
def get_gift_info(pokemon):

    gift_worksheet = RR_sheet.get_worksheet(8)

    pokemon_location_cells = gift_worksheet.findall(pokemon)

    if not pokemon_location_cells:
        return

    area_dict = {}

    for cell in pokemon_location_cells:

        row = cell.row
        column = cell.col
        name = cell.value

        location = (gift_worksheet.cell((row - 2), (column - 1)).value).title()
        requirement = gift_worksheet.cell(row, (column + 1)).value

        area_dict[location] = [requirement]

    list_of_strings = []

    for location in area_dict:
        
        final_string = ""

        final_string += f"{location}:"

        for entry in area_dict[location]:
            if type(entry) == int:
                string_entry = str(entry)
                string_entry += "%  | "
                final_string += f" {string_entry}"
            else:
                final_string += f" {entry}"

        list_of_strings.append(final_string)
    
    return list_of_strings

#list
def get_mystery_gift_info(pokemon):
     
    mystery_gift_worksheet = RR_sheet.get_worksheet(9)

    pokemon_location_cell = mystery_gift_worksheet.find(pokemon)

    if not pokemon_location_cell:
        return

    area_list = []

    if pokemon_location_cell:
        row = pokemon_location_cell.row
        column = pokemon_location_cell.col

        code = mystery_gift_worksheet.cell(row, (column + 2)).value

        area_list.append(f"Can be obtained with mystery gift code [{code}] at any Pokemon Center by talking to the red nurse.")

    return area_list

#list
def get_unobtainable_info(pokemon):

    unobtainable_worksheet = RR_sheet.get_worksheet(10)

    area_list = []

    if unobtainable_worksheet.find(pokemon):
        area_list.append("This Pokemon is Unobtainable.")

    
    return area_list


    
pokemon = "Shinx"
pokemon1 = "Tentacool"


#print(get_grass_and_caves_data(pokemon))
#print("------------------------------")
#print("------------------------------")
#print(get_fishing_and_surfing_data(pokemon1))


final_worksheet = updated_sheet.get_worksheet(0)



def write_to_category(function, row_start, column):
    string_list = function
    if string_list:
        for entry in string_list:
            final_worksheet.update_cell(row_start, column, entry)
            row_start += 1





def write_all_info(pokemon, column):


    final_worksheet = updated_sheet.get_worksheet(0)

    final_worksheet.update_cell(1, column, pokemon)
        
    write_to_category(get_grass_and_caves_data(pokemon), 4, column)

    write_to_category(get_fishing_and_surfing_data(pokemon), 15, column)

    write_to_category(get_safari_zone_info(pokemon), 27, column)

    write_to_category(get_fossil_info(pokemon), 32, column)

    write_to_category(get_legendary_and_static_info(pokemon), 36, column)

    write_to_category(get_raid_den_info(pokemon), 39, column)

    write_to_category(get_trade_info(pokemon), 44, column)

    write_to_category(get_gift_info(pokemon), 45, column)

    write_to_category(get_mystery_gift_info(pokemon), 46, column)

    write_to_category(get_unobtainable_info(pokemon), 47, column)






    

write_all_info("Zapdos", 2)















            












        









        
        


        
        

        










