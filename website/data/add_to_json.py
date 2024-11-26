import json
import os

# Path to the JSON file
json_path = r"C:\Users\eric-\SoftwareProjects\Personal\auth_note_app_flask\website\data\nfl_teams.json"

# Folder containing team logos
logo_folder = '/static/logos/'

try:
    # Step 1: Read the existing JSON file
    with open(json_path, 'r') as file:
        teams = json.load(file)

    # Step 2: Add a logo path for each team
    for team in teams:
        # Generate the logo filename based on team name
        team_logo = f"{team['name'].lower().replace(' ', '_')}.png"
        # Add the logo path to the team object
        team['logo'] = os.path.join(logo_folder, team_logo)

    # Step 3: Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(teams, file, indent=4)
    print("Logo paths added successfully!")

except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
except json.JSONDecodeError:
    print("Error: Invalid JSON file.")