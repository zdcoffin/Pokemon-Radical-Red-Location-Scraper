import gspread
import pandas as pd

gc = gspread.service_account(filename= 'creds.json')

RR_sheet = gc.open("RR Locations Test")


def get_grass_and_caves_data(pokemon):
    
    grass_caves_worksheet = RR_sheet.get_worksheet(0)
    
    pokemon_location_cells = grass_caves_worksheet.findall(pokemon)

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
        
    return area_dict
    


def get_fishing_and_surfing_data(pokemon):

    fishing_surfing_worksheet = RR_sheet.get_worksheet(1)

    pokemon_location_cells = fishing_surfing_worksheet.findall(pokemon)

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
    
    return area_dict



print(get_fishing_and_surfing_data("Sealeo"))






