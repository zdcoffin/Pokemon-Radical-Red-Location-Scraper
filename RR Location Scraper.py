import gspread
import pandas as pd

gc = gspread.service_account(filename= 'creds.json')

RR_sheet = gc.open("RR Locations Test")

grass_caves_worksheet = RR_sheet.get_worksheet(0)

def get_grass_and_caves_data(pokemon):
    
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
    

print(get_grass_and_caves_data("Dragapult"))








