
def find_supporters(project: str, votes: list[set[str]]) -> list[int]:
    """
    Finds the indices of citizens who support a given project.

    Args:
    - project: The project to find supporters for.
    - votes: List of sets, where each set contains the projects a citizen supports.

    Returns:
    - List of indices of citizens who support the given project.
    """
    supporters = []
    for i in range(len(votes)):
        if project in votes[i]:
            supporters.append(i)
    return supporters

def find_the_budget_for_project(supporters: list[int], balances: list[float]) -> float:
    """
    Calculates the total balance of the supporters for a given project.

    Args:
    - supporters: List of indices of citizens who support the project.
    - balances: List of current virtual balances for each citizen.

    Returns:
    - Total balance of the supporters.
    """
    total_balance = 0.0
    for i in supporters:
        total_balance += balances[i]
    return total_balance


def elect_next_budget_item(
    votes: list[set[str]], #רשימת ההצבעות של האזרחים
    balances: list[float], #היתרה הוירטואלית הנוכחית של כל אזרח
    costs: dict[str, float] #העלות של כל אחד מהפרוייקטים
):
    
    n = len(votes)  # מספר האזרחים
    min_time = float('inf')  # אתחול למציאת הזמן המינימלי
    chosen_project = None    # הפרוייקט שייבחר הכי מהר
    missing_cost = 0.0  # הסכום החסר למימון הפרוייקט שייקח הכי פחות זמן לממן

    #סידור הפרוייקטים לפי סדר אלפביתי
    costs = dict(sorted(costs.items()))
    
    # מעבר על כל הפרוייקטים
    for project in costs:

        # מציאת התומכים של הפרוייקט הזה
        supporters = []
        supporters = find_supporters(project, votes)

        if supporters == []:
            print(f"Project {project} has no supporters, or is already funded.")
            continue  # אין תומכים, לא ניתן לממן את הפרוייקט הזה

        # חישוב התקציב של התומכים בפרוייקט הנוכחי
        B_j = find_the_budget_for_project(supporters, balances)
        
        #חישוב כמה כסף חסר עבור הפרוייקט הנוכחי
        D_j = costs[project] - B_j
        
        #חישוב כמה זמן ייקח לממן אותו
        t_j = D_j / len(supporters)

        
        if t_j < min_time:
            min_time = t_j
            chosen_project = project
            missing_cost = t_j

    if chosen_project is None:
        # אין פרוייקט שניתן לממן כרגע
        print("No project can be selected.")
        return
    # הוספת הסכום הנדרש לכל אזרח
    for i in range(n):
        balances[i] += missing_cost
    # איפוס היתרות של התומכים של הפרוייקט שנבחר
    for i in range(n):
        if chosen_project in votes[i]:
            balances[i] = 0.0

    #מחיקת הפרוייקט הנבחר מהמילון של העלויות ומרשימת ההצבעות
    del costs[chosen_project]
    for i in range(n):
        if chosen_project in votes[i]:
            votes[i].remove(chosen_project)
    

    # הדפסת התוצאות
    print(f"Chosen project: {chosen_project}")
    print(f"Amount added to each citizen: {missing_cost:.2f}")
    for i in range(len(balances)):
        print(f"Citizen {i+1} has {balances[i]:.2f} remaining balance.")
    # הדפסת התוצאות
    print(f"After adding {missing_cost:.2f} to each citizen, \"{chosen_project}\" is chosen.")


# Example 1: Simple case
votes1 = [
    {"A", "B"},
    {"B", "C"},
    {"C"}
]
balances1 = [0.0, 0.0, 0.0]
costs1 = {
    "A": 1.0,
    "B": 1.0,
    "C": 1.0
}

print("Example 1:")
elect_next_budget_item(votes1, balances1, costs1)



# Example 2: Different project costs
votes2 = [
    {"X"},
    {"Y"},
    {"Y", "Z"}
]
balances2 = [0.0, 0.0, 0.0]
costs2 = {
    "X": 500.0,
    "Y": 1000.0,
    "Z": 750.0
}

print("\n\nExample 2 (Variable costs):")
elect_next_budget_item(votes2, balances2, costs2)



# Example 3: No possible selection
votes3 = [
    {"D"},
    {"E"},
]
balances3 = [0.0, 0.0]
costs3 = {
    "D": 5.0,
    "E": 10.0
}

print("\n\nExample 3:")
elect_next_budget_item(votes3, balances3, costs3)

# Example 4: Lexicographical tie-break
votes4 = [
    {"Apple", "Banana"},    
    {"Banana", "Cherry"},   
    {"Cherry", "Apple"}     
]
balances4 = [0.0, 0.0, 0.0]
costs4  = {
    "Apple": 300.0,
    "Banana": 300.0,
    "Cherry": 300.0
}
print("\n\nExample 4: Lexicographical tie-break")
elect_next_budget_item(votes4, balances4, costs4)


# Example 5: Iterative run
print("\n\nExample 5: Iterative run")
votes5 = [
    {"Public_Park_North", "New_Library", "Sports_Complex", "Community_Center", "Bike_Lanes_Main_St", "Solar_Farm", "Youth_Center", "Senior_Home", "Art_Museum", "Science_Lab", "Playground_East", "Swimming_Pool", "Music_School", "Theater_Renovation", "Emergency_Shelter", "Green_Roof_Project", "Urban_Garden", "Tech_Hub", "Medical_Clinic", "Recycling_Center", "Pedestrian_Bridge", "Cultural_Festival", "School_Expansion", "Fire_Station", "Animal_Shelter"},
    
    {"New_Library", "Community_Center", "Hospital_Wing", "Solar_Farm", "Basketball_Courts", "Senior_Home", "Art_Museum", "Public_Transport", "Playground_East", "Swimming_Pool", "Skate_Park", "Theater_Renovation", "Homeless_Support", "Green_Roof_Project", "Vocational_School", "Tech_Hub", "Dental_Clinic", "Water_Treatment", "Pedestrian_Bridge", "Convention_Center", "School_Expansion", "Police_Station", "Dog_Park"},
    
    {"Public_Park_North", "Sports_Complex", "Hospital_Wing", "Bike_Lanes_Main_St", "Youth_Center", "Basketball_Courts", "Science_Lab", "Public_Transport", "Music_School", "Skate_Park", "Emergency_Shelter", "Vocational_School", "Urban_Garden", "Medical_Clinic", "Recycling_Center", "Water_Treatment", "Cultural_Festival", "Fire_Station", "Police_Station", "Animal_Shelter", "Historic_Preservation", "Farmers_Market", "Daycare_Center", "Amphitheater"},
    
    {"New_Library", "Community_Center", "Solar_Farm", "Youth_Center", "Senior_Home", "Art_Museum", "Science_Lab", "Playground_East", "Music_School", "Theater_Renovation", "Homeless_Support", "Green_Roof_Project", "Urban_Garden", "Tech_Hub", "Medical_Clinic", "Pedestrian_Bridge", "Convention_Center", "School_Expansion", "Dog_Park", "Historic_Preservation", "Food_Bank", "Daycare_Center", "Innovation_Lab", "Wetlands_Restoration"},
    
    {"Public_Park_North", "Sports_Complex", "Hospital_Wing", "Bike_Lanes_Main_St", "Basketball_Courts", "Public_Transport", "Swimming_Pool", "Skate_Park", "Emergency_Shelter", "Vocational_School", "Dental_Clinic", "Recycling_Center", "Water_Treatment", "Cultural_Festival", "Fire_Station", "Police_Station", "Animal_Shelter", "Farmers_Market", "Food_Bank", "Amphitheater", "Streetlight_Upgrade", "Coastal_Cleanup", "Autism_Center"},
    
    {"New_Library", "Community_Center", "Solar_Farm", "Youth_Center", "Senior_Home", "Art_Museum", "Science_Lab", "Playground_East", "Music_School", "Theater_Renovation", "Green_Roof_Project", "Urban_Garden", "Tech_Hub", "Medical_Clinic", "Pedestrian_Bridge", "Convention_Center", "School_Expansion", "Dog_Park", "Historic_Preservation", "Daycare_Center", "Innovation_Lab", "Wetlands_Restoration", "Women_Shelter", "Chess_Club"},
    
    {"Public_Park_North", "Sports_Complex", "Hospital_Wing", "Bike_Lanes_Main_St", "Basketball_Courts", "Public_Transport", "Swimming_Pool", "Skate_Park", "Emergency_Shelter", "Vocational_School", "Recycling_Center", "Water_Treatment", "Fire_Station", "Police_Station", "Animal_Shelter", "Farmers_Market", "Amphitheater", "Streetlight_Upgrade", "Coastal_Cleanup", "Autism_Center", "Robotics_Workshop", "Rain_Garden", "Business_Incubator", "Addiction_Treatment"},
    
    {"New_Library", "Community_Center", "Solar_Farm", "Senior_Home", "Art_Museum", "Science_Lab", "Music_School", "Theater_Renovation", "Homeless_Support", "Green_Roof_Project", "Tech_Hub", "Dental_Clinic", "Medical_Clinic", "Pedestrian_Bridge", "School_Expansion", "Dog_Park", "Historic_Preservation", "Daycare_Center", "Innovation_Lab", "Women_Shelter", "Chess_Club", "Language_Center", "Makerspace", "Veterans_Memorial"},
    
    {"Sports_Complex", "Hospital_Wing", "Bike_Lanes_Main_St", "Youth_Center", "Basketball_Courts", "Public_Transport", "Swimming_Pool", "Skate_Park", "Vocational_School", "Recycling_Center", "Water_Treatment", "Cultural_Festival", "Police_Station", "Animal_Shelter", "Farmers_Market", "Food_Bank", "Amphitheater", "Coastal_Cleanup", "Autism_Center", "Robotics_Workshop", "Rain_Garden", "Business_Incubator", "Observatory", "Butterfly_Garden"},
    
    {"Public_Park_North", "New_Library", "Community_Center", "Solar_Farm", "Senior_Home", "Science_Lab", "Playground_East", "Theater_Renovation", "Emergency_Shelter", "Green_Roof_Project", "Urban_Garden", "Tech_Hub", "Convention_Center", "Dog_Park", "Historic_Preservation", "Innovation_Lab", "Wetlands_Restoration", "Women_Shelter", "Language_Center", "Makerspace", "Veterans_Memorial", "Observatory", "Butterfly_Garden", "Meditation_Garden"}
]

balances5 = [0,0,0,0,0,0,0,0,0,0]

costs5 = {
    "Public_Park_North": 850000.0,
    "New_Library": 1200000.0,
    "Sports_Complex": 2500000.0,
    "Community_Center": 950000.0,
    "Hospital_Wing": 4800000.0,
    "Bike_Lanes_Main_St": 650000.0,
    "Solar_Farm": 3200000.0,
    "Youth_Center": 720000.0,
    "Basketball_Courts": 380000.0,
    "Senior_Home": 1800000.0,
    "Art_Museum": 2100000.0,
    "Science_Lab": 1400000.0,
    "Public_Transport": 4500000.0,
    "Playground_East": 320000.0,
    "Swimming_Pool": 1900000.0,
    "Music_School": 890000.0,
    "Skate_Park": 450000.0,
    "Theater_Renovation": 1600000.0,
    "Emergency_Shelter": 980000.0,
    "Homeless_Support": 750000.0,
    "Green_Roof_Project": 550000.0,
    "Vocational_School": 1350000.0,
    "Urban_Garden": 420000.0,
    "Tech_Hub": 2800000.0,
    "Dental_Clinic": 920000.0,
    "Medical_Clinic": 1650000.0,
    "Recycling_Center": 780000.0,
    "Water_Treatment": 3600000.0,
    "Pedestrian_Bridge": 1100000.0,
    "Convention_Center": 3900000.0,
    "Cultural_Festival": 580000.0,
    "School_Expansion": 2200000.0,
    "Fire_Station": 2700000.0,
    "Police_Station": 3100000.0,
    "Animal_Shelter": 680000.0,
    "Dog_Park": 350000.0,
    "Historic_Preservation": 1250000.0,
    "Farmers_Market": 490000.0,
    "Food_Bank": 620000.0,
    "Daycare_Center": 870000.0,
    "Amphitheater": 1450000.0,
    "Innovation_Lab": 1750000.0,
    "Wetlands_Restoration": 940000.0,
    "Streetlight_Upgrade": 530000.0,
    "Coastal_Cleanup": 710000.0,
    "Autism_Center": 1050000.0,
    "Women_Shelter": 820000.0,
    "Chess_Club": 310000.0,
    "Robotics_Workshop": 640000.0,
    "Rain_Garden": 390000.0,
    "Business_Incubator": 1580000.0,
    "Addiction_Treatment": 1320000.0,
    "Language_Center": 560000.0,
    "Makerspace": 970000.0,
    "Veterans_Memorial": 480000.0,
    "Observatory": 2400000.0,
    "Butterfly_Garden": 330000.0,
    "Meditation_Garden": 410000.0
}

# הרצה איטרטיבית
round_num = 1
while costs5:
    print(f"\n{'='*70}")
    print(f"Round {round_num}")
    print(f"{'='*70}")
    elect_next_budget_item(votes5, balances5, costs5)
    round_num += 1
    if round_num > 60:  # למניעת לולאה אינסופית
        print("\nהגענו למקסימום סיבובים.")
        break

print(f"\n{'='*70}")
print(f"Final Summary: {round_num-1} projects were funded")
print(f"{'='*70}")



########################################################################################################
##נעזרתי בקוד שלי ספיר דהאן משנה שעברה אך שיניתי אותו כי הבחנתי בלוגיקה שאני חושב שהיא לא נכונה##
########################################################################################################

"""
[Running] python -u "c:\Users\user\Documents\Computer Science\2026\סמסטר א\אלגוריתמים כלכליים\מטלות\Economic-Algorithms\EX7\EX7Q4.py"
Example 1:
Chosen project: B
Amount added to each citizen: 0.50
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.50 remaining balance.
After adding 0.50 to each citizen, "B" is chosen.


Example 2 (Variable costs):
Chosen project: X
Amount added to each citizen: 500.00
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 500.00 remaining balance.
Citizen 3 has 500.00 remaining balance.
After adding 500.00 to each citizen, "X" is chosen.


Example 3:
Chosen project: D
Amount added to each citizen: 5.00
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 5.00 remaining balance.
After adding 5.00 to each citizen, "D" is chosen.


Example 4: Lexicographical tie-break
Chosen project: Apple
Amount added to each citizen: 150.00
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 150.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
After adding 150.00 to each citizen, "Apple" is chosen.


Example 5: Iterative run

======================================================================
Round 1
======================================================================
Chosen project: Playground_East
Amount added to each citizen: 64000.00
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 64000.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 64000.00 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 64000.00 remaining balance.
Citizen 8 has 64000.00 remaining balance.
Citizen 9 has 64000.00 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 64000.00 to each citizen, "Playground_East" is chosen.

======================================================================
Round 2
======================================================================
Project Playground_East has no supporters, or is already funded.
Chosen project: Basketball_Courts
Amount added to each citizen: 24800.00
Citizen 1 has 24800.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 24800.00 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 24800.00 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 88800.00 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 24800.00 remaining balance.
After adding 24800.00 to each citizen, "Basketball_Courts" is chosen.

======================================================================
Round 3
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Chosen project: Dog_Park
Amount added to each citizen: 37360.00
Citizen 1 has 62160.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 37360.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 37360.00 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 37360.00 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 37360.00 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 37360.00 to each citizen, "Dog_Park" is chosen.

======================================================================
Round 4
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Chosen project: Skate_Park
Amount added to each citizen: 60112.00
Citizen 1 has 122272.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 60112.00 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 60112.00 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 60112.00 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 60112.00 remaining balance.
After adding 60112.00 to each citizen, "Skate_Park" is chosen.

======================================================================
Round 5
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Chosen project: Urban_Garden
Amount added to each citizen: 23478.40
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 23478.40 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 23478.40 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 23478.40 remaining balance.
Citizen 8 has 83590.40 remaining balance.
Citizen 9 has 23478.40 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 23478.40 to each citizen, "Urban_Garden" is chosen.

======================================================================
Round 6
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Green_Roof_Project
Amount added to each citizen: 73821.87
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 73821.87 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 97300.27 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 97300.27 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 97300.27 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 73821.87 to each citizen, "Green_Roof_Project" is chosen.

======================================================================
Round 7
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Farmers_Market
Amount added to each citizen: 31069.33
Citizen 1 has 31069.33 remaining balance.
Citizen 2 has 31069.33 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 31069.33 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 31069.33 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 31069.33 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 31069.33 remaining balance.
After adding 31069.33 to each citizen, "Farmers_Market" is chosen.

======================================================================
Round 8
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Bike_Lanes_Main_St
Amount added to each citizen: 123786.13
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 154855.47 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 154855.47 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 154855.47 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 154855.47 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 154855.47 remaining balance.
After adding 123786.13 to each citizen, "Bike_Lanes_Main_St" is chosen.

======================================================================
Round 9
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Chess_Club
Amount added to each citizen: 144.53
Citizen 1 has 144.53 remaining balance.
Citizen 2 has 155000.00 remaining balance.
Citizen 3 has 144.53 remaining balance.
Citizen 4 has 155000.00 remaining balance.
Citizen 5 has 144.53 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 144.53 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 144.53 remaining balance.
Citizen 10 has 155000.00 remaining balance.
After adding 144.53 to each citizen, "Chess_Club" is chosen.

======================================================================
Round 10
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Community_Center
Amount added to each citizen: 80809.24
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 80953.78 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 80953.78 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 80953.78 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 80953.78 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 80809.24 to each citizen, "Community_Center" is chosen.

======================================================================
Round 11
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Animal_Shelter
Amount added to each citizen: 71236.98
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 71236.98 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 71236.98 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 71236.98 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 71236.98 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 71236.98 remaining balance.
After adding 71236.98 to each citizen, "Animal_Shelter" is chosen.

======================================================================
Round 12
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Youth_Center
Amount added to each citizen: 115505.21
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 186742.19 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 115505.21 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 115505.21 remaining balance.
Citizen 8 has 186742.19 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 186742.19 remaining balance.
After adding 115505.21 to each citizen, "Youth_Center" is chosen.

======================================================================
Round 13
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Veterans_Memorial
Amount added to each citizen: 53257.81
Citizen 1 has 53257.81 remaining balance.
Citizen 2 has 240000.00 remaining balance.
Citizen 3 has 53257.81 remaining balance.
Citizen 4 has 53257.81 remaining balance.
Citizen 5 has 168763.02 remaining balance.
Citizen 6 has 53257.81 remaining balance.
Citizen 7 has 168763.02 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 53257.81 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 53257.81 to each citizen, "Veterans_Memorial" is chosen.

======================================================================
Round 14
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Recycling_Center
Amount added to each citizen: 56540.10
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 296540.10 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 109797.92 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 109797.92 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 56540.10 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 56540.10 remaining balance.
After adding 56540.10 to each citizen, "Recycling_Center" is chosen.

======================================================================
Round 15
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: New_Library
Amount added to each citizen: 95130.64
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 95130.64 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 95130.64 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 95130.64 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 95130.64 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 95130.64 to each citizen, "New_Library" is chosen.

======================================================================
Round 16
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Cultural_Festival
Amount added to each citizen: 73652.02
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 73652.02 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 73652.02 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 73652.02 remaining balance.
Citizen 7 has 168782.66 remaining balance.
Citizen 8 has 73652.02 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 73652.02 remaining balance.
After adding 73652.02 to each citizen, "Cultural_Festival" is chosen.

======================================================================
Round 17
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Rain_Garden
Amount added to each citizen: 110608.67
Citizen 1 has 110608.67 remaining balance.
Citizen 2 has 184260.69 remaining balance.
Citizen 3 has 110608.67 remaining balance.
Citizen 4 has 184260.69 remaining balance.
Citizen 5 has 110608.67 remaining balance.
Citizen 6 has 184260.69 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 184260.69 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 184260.69 remaining balance.
After adding 110608.67 to each citizen, "Rain_Garden" is chosen.

======================================================================
Round 18
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Music_School
Amount added to each citizen: 23200.12
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 207460.81 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 133808.79 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 23200.12 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 23200.12 remaining balance.
Citizen 10 has 207460.81 remaining balance.
After adding 23200.12 to each citizen, "Music_School" is chosen.

======================================================================
Round 19
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Butterfly_Garden
Amount added to each citizen: 49669.54
Citizen 1 has 49669.54 remaining balance.
Citizen 2 has 257130.34 remaining balance.
Citizen 3 has 49669.54 remaining balance.
Citizen 4 has 49669.54 remaining balance.
Citizen 5 has 183478.33 remaining balance.
Citizen 6 has 49669.54 remaining balance.
Citizen 7 has 72869.66 remaining balance.
Citizen 8 has 49669.54 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 49669.54 to each citizen, "Butterfly_Garden" is chosen.

======================================================================
Round 20
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Public_Park_North
Amount added to each citizen: 98862.59
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 355992.93 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 148532.13 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 148532.13 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 148532.13 remaining balance.
Citizen 9 has 98862.59 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 98862.59 to each citizen, "Public_Park_North" is chosen.

======================================================================
Round 21
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Homeless_Support
Amount added to each citizen: 32314.27
Citizen 1 has 32314.27 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 32314.27 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 32314.27 remaining balance.
Citizen 6 has 180846.40 remaining balance.
Citizen 7 has 32314.27 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 131176.86 remaining balance.
Citizen 10 has 32314.27 remaining balance.
After adding 32314.27 to each citizen, "Homeless_Support" is chosen.

======================================================================
Round 22
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Food_Bank
Amount added to each citizen: 152169.62
Citizen 1 has 184483.89 remaining balance.
Citizen 2 has 152169.62 remaining balance.
Citizen 3 has 184483.89 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 333016.02 remaining balance.
Citizen 7 has 184483.89 remaining balance.
Citizen 8 has 152169.62 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 184483.89 remaining balance.
After adding 152169.62 to each citizen, "Food_Bank" is chosen.

======================================================================
Round 23
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Emergency_Shelter
Amount added to each citizen: 48412.88
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 200582.51 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 48412.88 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 381428.90 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 200582.51 remaining balance.
Citizen 9 has 48412.88 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 48412.88 to each citizen, "Emergency_Shelter" is chosen.

======================================================================
Round 24
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Pedestrian_Bridge
Amount added to each citizen: 53798.64
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 53798.64 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 53798.64 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 53798.64 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 102211.52 remaining balance.
Citizen 10 has 53798.64 remaining balance.
After adding 53798.64 to each citizen, "Pedestrian_Bridge" is chosen.

======================================================================
Round 25
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Coastal_Cleanup
Amount added to each citizen: 166730.40
Citizen 1 has 166730.40 remaining balance.
Citizen 2 has 166730.40 remaining balance.
Citizen 3 has 220529.04 remaining balance.
Citizen 4 has 166730.40 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 166730.40 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 166730.40 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 220529.04 remaining balance.
After adding 166730.40 to each citizen, "Coastal_Cleanup" is chosen.

======================================================================
Round 26
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Daycare_Center
Amount added to each citizen: 37319.94
Citizen 1 has 204050.34 remaining balance.
Citizen 2 has 204050.34 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 37319.94 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 37319.94 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 37319.94 remaining balance.
Citizen 10 has 257848.98 remaining balance.
After adding 37319.94 to each citizen, "Daycare_Center" is chosen.

======================================================================
Round 27
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Language_Center
Amount added to each citizen: 151075.51
Citizen 1 has 355125.85 remaining balance.
Citizen 2 has 355125.85 remaining balance.
Citizen 3 has 151075.51 remaining balance.
Citizen 4 has 151075.51 remaining balance.
Citizen 5 has 188395.45 remaining balance.
Citizen 6 has 151075.51 remaining balance.
Citizen 7 has 188395.45 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 188395.45 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 151075.51 to each citizen, "Language_Center" is chosen.

======================================================================
Round 28
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Vocational_School
Amount added to each citizen: 55722.46
Citizen 1 has 410848.31 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 206797.97 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 206797.97 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 55722.46 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 55722.46 remaining balance.
After adding 55722.46 to each citizen, "Vocational_School" is chosen.

======================================================================
Round 29
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Science_Lab
Amount added to each citizen: 77351.81
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 77351.81 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 77351.81 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 77351.81 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 77351.81 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 77351.81 to each citizen, "Science_Lab" is chosen.

======================================================================
Round 30
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Streetlight_Upgrade
Amount added to each citizen: 187648.19
Citizen 1 has 187648.19 remaining balance.
Citizen 2 has 265000.00 remaining balance.
Citizen 3 has 187648.19 remaining balance.
Citizen 4 has 187648.19 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 187648.19 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 187648.19 remaining balance.
Citizen 9 has 265000.00 remaining balance.
Citizen 10 has 187648.19 remaining balance.
After adding 187648.19 to each citizen, "Streetlight_Upgrade" is chosen.

======================================================================
Round 31
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Historic_Preservation
Amount added to each citizen: 62351.81
Citizen 1 has 250000.00 remaining balance.
Citizen 2 has 327351.81 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 62351.81 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 62351.81 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 327351.81 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 62351.81 to each citizen, "Historic_Preservation" is chosen.

======================================================================
Round 32
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Robotics_Workshop
Amount added to each citizen: 125148.19
Citizen 1 has 375148.19 remaining balance.
Citizen 2 has 452500.00 remaining balance.
Citizen 3 has 125148.19 remaining balance.
Citizen 4 has 125148.19 remaining balance.
Citizen 5 has 187500.00 remaining balance.
Citizen 6 has 125148.19 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 125148.19 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 125148.19 remaining balance.
After adding 125148.19 to each citizen, "Robotics_Workshop" is chosen.

======================================================================
Round 33
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Theater_Renovation
Amount added to each citizen: 45293.17
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 170441.37 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 232793.17 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 45293.17 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 45293.17 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 45293.17 to each citizen, "Theater_Renovation" is chosen.

======================================================================
Round 34
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Dental_Clinic
Amount added to each citizen: 229068.94
Citizen 1 has 229068.94 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 399510.31 remaining balance.
Citizen 4 has 229068.94 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 229068.94 remaining balance.
Citizen 7 has 274362.12 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 274362.12 remaining balance.
Citizen 10 has 229068.94 remaining balance.
After adding 229068.94 to each citizen, "Dental_Clinic" is chosen.

======================================================================
Round 35
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Wetlands_Restoration
Amount added to each citizen: 84264.39
Citizen 1 has 313333.33 remaining balance.
Citizen 2 has 84264.39 remaining balance.
Citizen 3 has 483774.70 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 84264.39 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 358626.51 remaining balance.
Citizen 8 has 84264.39 remaining balance.
Citizen 9 has 358626.51 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 84264.39 to each citizen, "Wetlands_Restoration" is chosen.

======================================================================
Round 36
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Amphitheater
Amount added to each citizen: 41176.97
Citizen 1 has 354510.31 remaining balance.
Citizen 2 has 125441.37 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 41176.97 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 41176.97 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 125441.37 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 41176.97 remaining balance.
After adding 41176.97 to each citizen, "Amphitheater" is chosen.

======================================================================
Round 37
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Senior_Home
Amount added to each citizen: 178512.67
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 178512.67 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 178512.67 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 178512.67 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 178512.67 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 178512.67 to each citizen, "Senior_Home" is chosen.

======================================================================
Round 38
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Autism_Center
Amount added to each citizen: 171487.33
Citizen 1 has 171487.33 remaining balance.
Citizen 2 has 171487.33 remaining balance.
Citizen 3 has 350000.00 remaining balance.
Citizen 4 has 171487.33 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 171487.33 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 171487.33 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 171487.33 remaining balance.
After adding 171487.33 to each citizen, "Autism_Center" is chosen.

======================================================================
Round 39
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Women_Shelter
Amount added to each citizen: 101846.01
Citizen 1 has 273333.33 remaining balance.
Citizen 2 has 273333.33 remaining balance.
Citizen 3 has 451846.01 remaining balance.
Citizen 4 has 273333.33 remaining balance.
Citizen 5 has 101846.01 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 101846.01 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 101846.01 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 101846.01 to each citizen, "Women_Shelter" is chosen.

======================================================================
Round 40
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Medical_Clinic
Amount added to each citizen: 130297.47
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 403630.80 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 232143.47 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 232143.47 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 232143.47 remaining balance.
Citizen 10 has 130297.47 remaining balance.
After adding 130297.47 to each citizen, "Medical_Clinic" is chosen.

======================================================================
Round 41
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Swimming_Pool
Amount added to each citizen: 159987.76
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 159987.76 remaining balance.
Citizen 4 has 159987.76 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 159987.76 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 159987.76 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 290285.22 remaining balance.
After adding 159987.76 to each citizen, "Swimming_Pool" is chosen.

======================================================================
Round 42
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Meditation_Garden
Amount added to each citizen: 119714.78
Citizen 1 has 119714.78 remaining balance.
Citizen 2 has 119714.78 remaining balance.
Citizen 3 has 279702.53 remaining balance.
Citizen 4 has 279702.53 remaining balance.
Citizen 5 has 119714.78 remaining balance.
Citizen 6 has 279702.53 remaining balance.
Citizen 7 has 119714.78 remaining balance.
Citizen 8 has 279702.53 remaining balance.
Citizen 9 has 119714.78 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 119714.78 to each citizen, "Meditation_Garden" is chosen.

======================================================================
Round 43
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Art_Museum
Amount added to each citizen: 204292.57
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 483995.10 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 324007.35 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 324007.35 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 324007.35 remaining balance.
Citizen 10 has 204292.57 remaining balance.
After adding 204292.57 to each citizen, "Art_Museum" is chosen.

======================================================================
Round 44
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Sports_Complex
Amount added to each citizen: 208796.57
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 208796.57 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 208796.57 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 208796.57 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 208796.57 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 413089.14 remaining balance.
After adding 208796.57 to each citizen, "Sports_Complex" is chosen.

======================================================================
Round 45
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Makerspace
Amount added to each citizen: 174057.14
Citizen 1 has 174057.14 remaining balance.
Citizen 2 has 382853.72 remaining balance.
Citizen 3 has 174057.14 remaining balance.
Citizen 4 has 382853.72 remaining balance.
Citizen 5 has 174057.14 remaining balance.
Citizen 6 has 382853.72 remaining balance.
Citizen 7 has 174057.14 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 174057.14 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 174057.14 to each citizen, "Makerspace" is chosen.

======================================================================
Round 46
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: School_Expansion
Amount added to each citizen: 175476.34
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 349533.49 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 349533.49 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 349533.49 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 349533.49 remaining balance.
Citizen 10 has 175476.34 remaining balance.
After adding 175476.34 to each citizen, "School_Expansion" is chosen.

======================================================================
Round 47
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Police_Station
Amount added to each citizen: 340373.21
Citizen 1 has 340373.21 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 340373.21 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 340373.21 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 340373.21 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 515849.55 remaining balance.
After adding 340373.21 to each citizen, "Police_Station" is chosen.

======================================================================
Round 48
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Innovation_Lab
Amount added to each citizen: 53257.70
Citizen 1 has 393630.91 remaining balance.
Citizen 2 has 53257.70 remaining balance.
Citizen 3 has 53257.70 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 53257.70 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 53257.70 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 53257.70 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 53257.70 to each citizen, "Innovation_Lab" is chosen.

======================================================================
Round 49
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Tech_Hub
Amount added to each citizen: 392185.23
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 445442.93 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 445442.93 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 445442.93 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 445442.93 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 392185.23 to each citizen, "Tech_Hub" is chosen.

======================================================================
Round 50
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Fire_Station
Amount added to each citizen: 340917.80
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 340917.80 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 340917.80 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 340917.80 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 340917.80 remaining balance.
Citizen 9 has 786360.73 remaining balance.
Citizen 10 has 340917.80 remaining balance.
After adding 340917.80 to each citizen, "Fire_Station" is chosen.

======================================================================
Round 51
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Solar_Farm
Amount added to each citizen: 249235.17
Citizen 1 has 0.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 249235.17 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 249235.17 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 249235.17 remaining balance.
Citizen 8 has 0.00 remaining balance.
Citizen 9 has 1035595.90 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 249235.17 to each citizen, "Solar_Farm" is chosen.

======================================================================
Round 52
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Business_Incubator
Amount added to each citizen: 147584.47
Citizen 1 has 147584.47 remaining balance.
Citizen 2 has 147584.47 remaining balance.
Citizen 3 has 396819.63 remaining balance.
Citizen 4 has 147584.47 remaining balance.
Citizen 5 has 396819.63 remaining balance.
Citizen 6 has 147584.47 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 147584.47 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 147584.47 remaining balance.
After adding 147584.47 to each citizen, "Business_Incubator" is chosen.

======================================================================
Round 53
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Water_Treatment
Amount added to each citizen: 531755.25
Citizen 1 has 679339.72 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 679339.72 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 679339.72 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 679339.72 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 679339.72 remaining balance.
After adding 531755.25 to each citizen, "Water_Treatment" is chosen.

======================================================================
Round 54
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Convention_Center
Amount added to each citizen: 465495.21
Citizen 1 has 1144834.93 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 465495.21 remaining balance.
Citizen 4 has 0.00 remaining balance.
Citizen 5 has 465495.21 remaining balance.
Citizen 6 has 0.00 remaining balance.
Citizen 7 has 465495.21 remaining balance.
Citizen 8 has 1144834.93 remaining balance.
Citizen 9 has 465495.21 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 465495.21 to each citizen, "Convention_Center" is chosen.

======================================================================
Round 55
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Convention_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Public_Transport
Amount added to each citizen: 527603.83
Citizen 1 has 1672438.76 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 527603.83 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 527603.83 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 1672438.76 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 527603.83 remaining balance.
After adding 527603.83 to each citizen, "Public_Transport" is chosen.

======================================================================
Round 56
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Convention_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Public_Transport has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Observatory
Amount added to each citizen: 936198.08
Citizen 1 has 2608636.85 remaining balance.
Citizen 2 has 936198.08 remaining balance.
Citizen 3 has 936198.08 remaining balance.
Citizen 4 has 1463801.92 remaining balance.
Citizen 5 has 936198.08 remaining balance.
Citizen 6 has 1463801.92 remaining balance.
Citizen 7 has 936198.08 remaining balance.
Citizen 8 has 2608636.85 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 0.00 remaining balance.
After adding 936198.08 to each citizen, "Observatory" is chosen.

======================================================================
Round 57
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Convention_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Observatory has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Public_Transport has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Hospital_Wing
Amount added to each citizen: 211041.53
Citizen 1 has 2819678.38 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 0.00 remaining balance.
Citizen 4 has 1674843.45 remaining balance.
Citizen 5 has 0.00 remaining balance.
Citizen 6 has 1674843.45 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 2819678.38 remaining balance.
Citizen 9 has 0.00 remaining balance.
Citizen 10 has 211041.53 remaining balance.
After adding 211041.53 to each citizen, "Hospital_Wing" is chosen.

======================================================================
Round 58
======================================================================
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Convention_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Hospital_Wing has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Observatory has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Public_Transport has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Addiction_Treatment
Amount added to each citizen: 1320000.00
Citizen 1 has 4139678.38 remaining balance.
Citizen 2 has 1320000.00 remaining balance.
Citizen 3 has 1320000.00 remaining balance.
Citizen 4 has 2994843.45 remaining balance.
Citizen 5 has 1320000.00 remaining balance.
Citizen 6 has 2994843.45 remaining balance.
Citizen 7 has 0.00 remaining balance.
Citizen 8 has 4139678.38 remaining balance.
Citizen 9 has 1320000.00 remaining balance.
Citizen 10 has 1531041.53 remaining balance.
After adding 1320000.00 to each citizen, "Addiction_Treatment" is chosen.

======================================================================
Round 59
======================================================================
Project Addiction_Treatment has no supporters, or is already funded.
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Convention_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Hospital_Wing has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Observatory has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Public_Transport has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
No project can be selected.

======================================================================
Round 60
======================================================================
Project Addiction_Treatment has no supporters, or is already funded.
Project Amphitheater has no supporters, or is already funded.
Project Animal_Shelter has no supporters, or is already funded.
Project Art_Museum has no supporters, or is already funded.
Project Autism_Center has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Business_Incubator has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Coastal_Cleanup has no supporters, or is already funded.
Project Community_Center has no supporters, or is already funded.
Project Convention_Center has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Daycare_Center has no supporters, or is already funded.
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Fire_Station has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
Project Hospital_Wing has no supporters, or is already funded.
Project Innovation_Lab has no supporters, or is already funded.
Project Language_Center has no supporters, or is already funded.
Project Makerspace has no supporters, or is already funded.
Project Medical_Clinic has no supporters, or is already funded.
Project Meditation_Garden has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Observatory has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Police_Station has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Public_Transport has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Robotics_Workshop has no supporters, or is already funded.
Project School_Expansion has no supporters, or is already funded.
Project Science_Lab has no supporters, or is already funded.
Project Senior_Home has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Solar_Farm has no supporters, or is already funded.
Project Sports_Complex has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Swimming_Pool has no supporters, or is already funded.
Project Tech_Hub has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
No project can be selected.

����� �������� �������.

======================================================================
Final Summary: 60 projects were funded
======================================================================

[Done] exited with code=0 in 0.078 seconds
"""
