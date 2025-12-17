
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
            balances[i] -= missing_cost  #  התומכים משלמים על רק על הפרוייקט והיתרה שלהם לא מתאפסת

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
Citizen 3 has 64000.00 remaining balance.
Citizen 4 has 24800.00 remaining balance.
Citizen 5 has 64000.00 remaining balance.
Citizen 6 has 24800.00 remaining balance.
Citizen 7 has 64000.00 remaining balance.
Citizen 8 has 88800.00 remaining balance.
Citizen 9 has 64000.00 remaining balance.
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
Citizen 3 has 101360.00 remaining balance.
Citizen 4 has 24800.00 remaining balance.
Citizen 5 has 101360.00 remaining balance.
Citizen 6 has 24800.00 remaining balance.
Citizen 7 has 101360.00 remaining balance.
Citizen 8 has 88800.00 remaining balance.
Citizen 9 has 101360.00 remaining balance.
Citizen 10 has 24800.00 remaining balance.
After adding 37360.00 to each citizen, "Dog_Park" is chosen.

======================================================================
Round 4
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Chosen project: Skate_Park
Amount added to each citizen: 8912.00
Citizen 1 has 71072.00 remaining balance.
Citizen 2 has 0.00 remaining balance.
Citizen 3 has 101360.00 remaining balance.
Citizen 4 has 33712.00 remaining balance.
Citizen 5 has 101360.00 remaining balance.
Citizen 6 has 33712.00 remaining balance.
Citizen 7 has 101360.00 remaining balance.
Citizen 8 has 97712.00 remaining balance.
Citizen 9 has 101360.00 remaining balance.
Citizen 10 has 33712.00 remaining balance.
After adding 8912.00 to each citizen, "Skate_Park" is chosen.

======================================================================
Round 5
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Chosen project: Farmers_Market
Amount added to each citizen: 21140.00
Citizen 1 has 92212.00 remaining balance.
Citizen 2 has 21140.00 remaining balance.
Citizen 3 has 101360.00 remaining balance.
Citizen 4 has 54852.00 remaining balance.
Citizen 5 has 101360.00 remaining balance.
Citizen 6 has 54852.00 remaining balance.
Citizen 7 has 101360.00 remaining balance.
Citizen 8 has 118852.00 remaining balance.
Citizen 9 has 101360.00 remaining balance.
Citizen 10 has 54852.00 remaining balance.
After adding 21140.00 to each citizen, "Farmers_Market" is chosen.

======================================================================
Round 6
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Chosen project: Urban_Garden
Amount added to each citizen: 12374.40
Citizen 1 has 92212.00 remaining balance.
Citizen 2 has 33514.40 remaining balance.
Citizen 3 has 101360.00 remaining balance.
Citizen 4 has 54852.00 remaining balance.
Citizen 5 has 113734.40 remaining balance.
Citizen 6 has 54852.00 remaining balance.
Citizen 7 has 113734.40 remaining balance.
Citizen 8 has 131226.40 remaining balance.
Citizen 9 has 113734.40 remaining balance.
Citizen 10 has 54852.00 remaining balance.
After adding 12374.40 to each citizen, "Urban_Garden" is chosen.

======================================================================
Round 7
======================================================================
Project Basketball_Courts has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Green_Roof_Project
Amount added to each citizen: 21415.20
Citizen 1 has 92212.00 remaining balance.
Citizen 2 has 33514.40 remaining balance.
Citizen 3 has 122775.20 remaining balance.
Citizen 4 has 54852.00 remaining balance.
Citizen 5 has 135149.60 remaining balance.
Citizen 6 has 54852.00 remaining balance.
Citizen 7 has 135149.60 remaining balance.
Citizen 8 has 131226.40 remaining balance.
Citizen 9 has 135149.60 remaining balance.
Citizen 10 has 54852.00 remaining balance.
After adding 21415.20 to each citizen, "Green_Roof_Project" is chosen.

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
Amount added to each citizen: 5912.80
Citizen 1 has 92212.00 remaining balance.
Citizen 2 has 39427.20 remaining balance.
Citizen 3 has 122775.20 remaining balance.
Citizen 4 has 60764.80 remaining balance.
Citizen 5 has 135149.60 remaining balance.
Citizen 6 has 60764.80 remaining balance.
Citizen 7 has 135149.60 remaining balance.
Citizen 8 has 137139.20 remaining balance.
Citizen 9 has 135149.60 remaining balance.
Citizen 10 has 60764.80 remaining balance.
After adding 5912.80 to each citizen, "Bike_Lanes_Main_St" is chosen.

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
Chosen project: Animal_Shelter
Amount added to each citizen: 11912.80
Citizen 1 has 92212.00 remaining balance.
Citizen 2 has 51340.00 remaining balance.
Citizen 3 has 122775.20 remaining balance.
Citizen 4 has 72677.60 remaining balance.
Citizen 5 has 135149.60 remaining balance.
Citizen 6 has 72677.60 remaining balance.
Citizen 7 has 135149.60 remaining balance.
Citizen 8 has 149052.00 remaining balance.
Citizen 9 has 135149.60 remaining balance.
Citizen 10 has 72677.60 remaining balance.
After adding 11912.80 to each citizen, "Animal_Shelter" is chosen.

======================================================================
Round 10
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Cultural_Festival
Amount added to each citizen: 23678.40
Citizen 1 has 92212.00 remaining balance.
Citizen 2 has 75018.40 remaining balance.
Citizen 3 has 122775.20 remaining balance.
Citizen 4 has 96356.00 remaining balance.
Citizen 5 has 135149.60 remaining balance.
Citizen 6 has 96356.00 remaining balance.
Citizen 7 has 158828.00 remaining balance.
Citizen 8 has 172730.40 remaining balance.
Citizen 9 has 135149.60 remaining balance.
Citizen 10 has 96356.00 remaining balance.
After adding 23678.40 to each citizen, "Cultural_Festival" is chosen.

======================================================================
Round 11
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Chess_Club
Amount added to each citizen: 20456.80
Citizen 1 has 112668.80 remaining balance.
Citizen 2 has 95475.20 remaining balance.
Citizen 3 has 143232.00 remaining balance.
Citizen 4 has 116812.80 remaining balance.
Citizen 5 has 155606.40 remaining balance.
Citizen 6 has 96356.00 remaining balance.
Citizen 7 has 179284.80 remaining balance.
Citizen 8 has 172730.40 remaining balance.
Citizen 9 has 155606.40 remaining balance.
Citizen 10 has 116812.80 remaining balance.
After adding 20456.80 to each citizen, "Chess_Club" is chosen.

======================================================================
Round 12
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Recycling_Center
Amount added to each citizen: 6720.32
Citizen 1 has 112668.80 remaining balance.
Citizen 2 has 102195.52 remaining balance.
Citizen 3 has 143232.00 remaining balance.
Citizen 4 has 123533.12 remaining balance.
Citizen 5 has 155606.40 remaining balance.
Citizen 6 has 103076.32 remaining balance.
Citizen 7 has 179284.80 remaining balance.
Citizen 8 has 179450.72 remaining balance.
Citizen 9 has 155606.40 remaining balance.
Citizen 10 has 123533.12 remaining balance.
After adding 6720.32 to each citizen, "Recycling_Center" is chosen.

======================================================================
Round 13
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Chosen project: Youth_Center
Amount added to each citizen: 16376.67
Citizen 1 has 112668.80 remaining balance.
Citizen 2 has 118572.19 remaining balance.
Citizen 3 has 143232.00 remaining balance.
Citizen 4 has 123533.12 remaining balance.
Citizen 5 has 171983.07 remaining balance.
Citizen 6 has 103076.32 remaining balance.
Citizen 7 has 195661.47 remaining balance.
Citizen 8 has 195827.39 remaining balance.
Citizen 9 has 155606.40 remaining balance.
Citizen 10 has 139909.79 remaining balance.
After adding 16376.67 to each citizen, "Youth_Center" is chosen.

======================================================================
Round 14
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Butterfly_Garden
Amount added to each citizen: 17241.90
Citizen 1 has 129910.70 remaining balance.
Citizen 2 has 135814.10 remaining balance.
Citizen 3 has 160473.90 remaining balance.
Citizen 4 has 140775.02 remaining balance.
Citizen 5 has 189224.98 remaining balance.
Citizen 6 has 120318.22 remaining balance.
Citizen 7 has 212903.38 remaining balance.
Citizen 8 has 213069.30 remaining balance.
Citizen 9 has 155606.40 remaining balance.
Citizen 10 has 139909.79 remaining balance.
After adding 17241.90 to each citizen, "Butterfly_Garden" is chosen.

======================================================================
Round 15
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Public_Park_North
Amount added to each citizen: 3515.45
Citizen 1 has 129910.70 remaining balance.
Citizen 2 has 139329.55 remaining balance.
Citizen 3 has 160473.90 remaining balance.
Citizen 4 has 144290.47 remaining balance.
Citizen 5 has 189224.98 remaining balance.
Citizen 6 has 123833.67 remaining balance.
Citizen 7 has 212903.38 remaining balance.
Citizen 8 has 216584.75 remaining balance.
Citizen 9 has 159121.85 remaining balance.
Citizen 10 has 139909.79 remaining balance.
After adding 3515.45 to each citizen, "Public_Park_North" is chosen.

======================================================================
Round 16
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Rain_Garden
Amount added to each citizen: 8987.39
Citizen 1 has 138898.09 remaining balance.
Citizen 2 has 148316.93 remaining balance.
Citizen 3 has 169461.29 remaining balance.
Citizen 4 has 153277.86 remaining balance.
Citizen 5 has 198212.36 remaining balance.
Citizen 6 has 132821.06 remaining balance.
Citizen 7 has 212903.38 remaining balance.
Citizen 8 has 225572.13 remaining balance.
Citizen 9 has 159121.85 remaining balance.
Citizen 10 has 148897.18 remaining balance.
After adding 8987.39 to each citizen, "Rain_Garden" is chosen.

======================================================================
Round 17
======================================================================
Project Animal_Shelter has no supporters, or is already funded.
Project Basketball_Courts has no supporters, or is already funded.
Project Bike_Lanes_Main_St has no supporters, or is already funded.
Project Butterfly_Garden has no supporters, or is already funded.
Project Chess_Club has no supporters, or is already funded.
Project Cultural_Festival has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Community_Center
Amount added to each citizen: 369.46
Citizen 1 has 138898.09 remaining balance.
Citizen 2 has 148316.93 remaining balance.
Citizen 3 has 169830.75 remaining balance.
Citizen 4 has 153277.86 remaining balance.
Citizen 5 has 198581.82 remaining balance.
Citizen 6 has 132821.06 remaining balance.
Citizen 7 has 213272.83 remaining balance.
Citizen 8 has 225572.13 remaining balance.
Citizen 9 has 159491.31 remaining balance.
Citizen 10 has 148897.18 remaining balance.
After adding 369.46 to each citizen, "Community_Center" is chosen.

======================================================================
Round 18
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
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Music_School
Amount added to each citizen: 13920.02
Citizen 1 has 138898.09 remaining balance.
Citizen 2 has 162236.95 remaining balance.
Citizen 3 has 169830.75 remaining balance.
Citizen 4 has 153277.86 remaining balance.
Citizen 5 has 212501.84 remaining balance.
Citizen 6 has 132821.06 remaining balance.
Citizen 7 has 227192.85 remaining balance.
Citizen 8 has 225572.13 remaining balance.
Citizen 9 has 173411.33 remaining balance.
Citizen 10 has 162817.20 remaining balance.
After adding 13920.02 to each citizen, "Music_School" is chosen.

======================================================================
Round 19
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
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Emergency_Shelter
Amount added to each citizen: 13751.85
Citizen 1 has 138898.09 remaining balance.
Citizen 2 has 175988.81 remaining balance.
Citizen 3 has 169830.75 remaining balance.
Citizen 4 has 167029.71 remaining balance.
Citizen 5 has 212501.84 remaining balance.
Citizen 6 has 146572.91 remaining balance.
Citizen 7 has 227192.85 remaining balance.
Citizen 8 has 239323.99 remaining balance.
Citizen 9 has 187163.18 remaining balance.
Citizen 10 has 162817.20 remaining balance.
After adding 13751.85 to each citizen, "Emergency_Shelter" is chosen.

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
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Food_Bank
Amount added to each citizen: 17768.42
Citizen 1 has 156666.51 remaining balance.
Citizen 2 has 193757.23 remaining balance.
Citizen 3 has 187599.17 remaining balance.
Citizen 4 has 167029.71 remaining balance.
Citizen 5 has 212501.84 remaining balance.
Citizen 6 has 164341.34 remaining balance.
Citizen 7 has 244961.28 remaining balance.
Citizen 8 has 257092.41 remaining balance.
Citizen 9 has 187163.18 remaining balance.
Citizen 10 has 180585.62 remaining balance.
After adding 17768.42 to each citizen, "Food_Bank" is chosen.

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
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: New_Library
Amount added to each citizen: 13421.20
Citizen 1 has 156666.51 remaining balance.
Citizen 2 has 193757.23 remaining balance.
Citizen 3 has 201020.37 remaining balance.
Citizen 4 has 167029.71 remaining balance.
Citizen 5 has 225923.04 remaining balance.
Citizen 6 has 164341.34 remaining balance.
Citizen 7 has 258382.47 remaining balance.
Citizen 8 has 257092.41 remaining balance.
Citizen 9 has 200584.38 remaining balance.
Citizen 10 has 180585.62 remaining balance.
After adding 13421.20 to each citizen, "New_Library" is chosen.

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
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Coastal_Cleanup
Amount added to each citizen: 8370.04
Citizen 1 has 165036.55 remaining balance.
Citizen 2 has 202127.27 remaining balance.
Citizen 3 has 209390.40 remaining balance.
Citizen 4 has 175399.75 remaining balance.
Citizen 5 has 225923.04 remaining balance.
Citizen 6 has 172711.37 remaining balance.
Citizen 7 has 258382.47 remaining balance.
Citizen 8 has 265462.44 remaining balance.
Citizen 9 has 200584.38 remaining balance.
Citizen 10 has 188955.66 remaining balance.
After adding 8370.04 to each citizen, "Coastal_Cleanup" is chosen.

======================================================================
Round 23
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
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Daycare_Center
Amount added to each citizen: 11759.01
Citizen 1 has 176795.56 remaining balance.
Citizen 2 has 213886.27 remaining balance.
Citizen 3 has 209390.40 remaining balance.
Citizen 4 has 175399.75 remaining balance.
Citizen 5 has 237682.05 remaining balance.
Citizen 6 has 172711.37 remaining balance.
Citizen 7 has 270141.48 remaining balance.
Citizen 8 has 265462.44 remaining balance.
Citizen 9 has 212343.39 remaining balance.
Citizen 10 has 200714.67 remaining balance.
After adding 11759.01 to each citizen, "Daycare_Center" is chosen.

======================================================================
Round 24
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
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Veterans_Memorial
Amount added to each citizen: 6911.44
Citizen 1 has 183707.00 remaining balance.
Citizen 2 has 220797.72 remaining balance.
Citizen 3 has 216301.85 remaining balance.
Citizen 4 has 182311.20 remaining balance.
Citizen 5 has 244593.49 remaining balance.
Citizen 6 has 179622.82 remaining balance.
Citizen 7 has 277052.92 remaining balance.
Citizen 8 has 265462.44 remaining balance.
Citizen 9 has 219254.83 remaining balance.
Citizen 10 has 200714.67 remaining balance.
After adding 6911.44 to each citizen, "Veterans_Memorial" is chosen.

======================================================================
Round 25
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
Chosen project: Streetlight_Upgrade
Amount added to each citizen: 4176.79
Citizen 1 has 187883.79 remaining balance.
Citizen 2 has 224974.51 remaining balance.
Citizen 3 has 220478.64 remaining balance.
Citizen 4 has 186487.99 remaining balance.
Citizen 5 has 244593.49 remaining balance.
Citizen 6 has 183799.61 remaining balance.
Citizen 7 has 277052.92 remaining balance.
Citizen 8 has 269639.24 remaining balance.
Citizen 9 has 223431.62 remaining balance.
Citizen 10 has 204891.46 remaining balance.
After adding 4176.79 to each citizen, "Streetlight_Upgrade" is chosen.

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
Project Daycare_Center has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Pedestrian_Bridge
Amount added to each citizen: 9442.97
Citizen 1 has 187883.79 remaining balance.
Citizen 2 has 224974.51 remaining balance.
Citizen 3 has 229921.61 remaining balance.
Citizen 4 has 186487.99 remaining balance.
Citizen 5 has 254036.46 remaining balance.
Citizen 6 has 183799.61 remaining balance.
Citizen 7 has 286495.90 remaining balance.
Citizen 8 has 269639.24 remaining balance.
Citizen 9 has 232874.59 remaining balance.
Citizen 10 has 214334.43 remaining balance.
After adding 9442.97 to each citizen, "Pedestrian_Bridge" is chosen.

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
Project Music_School has no supporters, or is already funded.
Project New_Library has no supporters, or is already funded.
Project Pedestrian_Bridge has no supporters, or is already funded.
Project Playground_East has no supporters, or is already funded.
Project Public_Park_North has no supporters, or is already funded.
Project Rain_Garden has no supporters, or is already funded.
Project Recycling_Center has no supporters, or is already funded.
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Science_Lab
Amount added to each citizen: 21322.22
Citizen 1 has 187883.79 remaining balance.
Citizen 2 has 246296.73 remaining balance.
Citizen 3 has 229921.61 remaining balance.
Citizen 4 has 186487.99 remaining balance.
Citizen 5 has 275358.68 remaining balance.
Citizen 6 has 183799.61 remaining balance.
Citizen 7 has 307818.12 remaining balance.
Citizen 8 has 269639.24 remaining balance.
Citizen 9 has 254196.82 remaining balance.
Citizen 10 has 214334.43 remaining balance.
After adding 21322.22 to each citizen, "Science_Lab" is chosen.

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
Project Youth_Center has no supporters, or is already funded.
Chosen project: Vocational_School
Amount added to each citizen: 7281.61
Citizen 1 has 195165.40 remaining balance.
Citizen 2 has 246296.73 remaining balance.
Citizen 3 has 229921.61 remaining balance.
Citizen 4 has 193769.60 remaining balance.
Citizen 5 has 275358.68 remaining balance.
Citizen 6 has 191081.22 remaining balance.
Citizen 7 has 307818.12 remaining balance.
Citizen 8 has 276920.84 remaining balance.
Citizen 9 has 254196.82 remaining balance.
Citizen 10 has 221616.04 remaining balance.
After adding 7281.61 to each citizen, "Vocational_School" is chosen.

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
Chosen project: Homeless_Support
Amount added to each citizen: 11004.28
Citizen 1 has 206169.68 remaining balance.
Citizen 2 has 246296.73 remaining balance.
Citizen 3 has 240925.89 remaining balance.
Citizen 4 has 193769.60 remaining balance.
Citizen 5 has 286362.96 remaining balance.
Citizen 6 has 202085.49 remaining balance.
Citizen 7 has 318822.40 remaining balance.
Citizen 8 has 276920.84 remaining balance.
Citizen 9 has 265201.09 remaining balance.
Citizen 10 has 232620.31 remaining balance.
After adding 11004.28 to each citizen, "Homeless_Support" is chosen.

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
Amount added to each citizen: 20735.57
Citizen 1 has 226905.25 remaining balance.
Citizen 2 has 267032.30 remaining balance.
Citizen 3 has 240925.89 remaining balance.
Citizen 4 has 193769.60 remaining balance.
Citizen 5 has 307098.53 remaining balance.
Citizen 6 has 202085.49 remaining balance.
Citizen 7 has 339557.97 remaining balance.
Citizen 8 has 276920.84 remaining balance.
Citizen 9 has 285936.67 remaining balance.
Citizen 10 has 232620.31 remaining balance.
After adding 20735.57 to each citizen, "Historic_Preservation" is chosen.

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
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
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
Amount added to each citizen: 7252.68
Citizen 1 has 234157.93 remaining balance.
Citizen 2 has 274284.99 remaining balance.
Citizen 3 has 248178.57 remaining balance.
Citizen 4 has 201022.28 remaining balance.
Citizen 5 has 314351.22 remaining balance.
Citizen 6 has 209338.18 remaining balance.
Citizen 7 has 339557.97 remaining balance.
Citizen 8 has 284173.53 remaining balance.
Citizen 9 has 285936.67 remaining balance.
Citizen 10 has 239873.00 remaining balance.
After adding 7252.68 to each citizen, "Robotics_Workshop" is chosen.

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
Chosen project: Dental_Clinic
Amount added to each citizen: 15730.09
Citizen 1 has 249888.02 remaining balance.
Citizen 2 has 274284.99 remaining balance.
Citizen 3 has 263908.66 remaining balance.
Citizen 4 has 216752.37 remaining balance.
Citizen 5 has 314351.22 remaining balance.
Citizen 6 has 225068.27 remaining balance.
Citizen 7 has 355288.06 remaining balance.
Citizen 8 has 284173.53 remaining balance.
Citizen 9 has 301666.75 remaining balance.
Citizen 10 has 255603.09 remaining balance.
After adding 15730.09 to each citizen, "Dental_Clinic" is chosen.

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
Project Dental_Clinic has no supporters, or is already funded.
Project Dog_Park has no supporters, or is already funded.
Project Emergency_Shelter has no supporters, or is already funded.
Project Farmers_Market has no supporters, or is already funded.
Project Food_Bank has no supporters, or is already funded.
Project Green_Roof_Project has no supporters, or is already funded.
Project Historic_Preservation has no supporters, or is already funded.
Project Homeless_Support has no supporters, or is already funded.
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
Chosen project: Language_Center
Amount added to each citizen: 10111.69
Citizen 1 has 259999.72 remaining balance.
Citizen 2 has 284396.68 remaining balance.
Citizen 3 has 274020.36 remaining balance.
Citizen 4 has 226864.06 remaining balance.
Citizen 5 has 324462.91 remaining balance.
Citizen 6 has 235179.96 remaining balance.
Citizen 7 has 365399.75 remaining balance.
Citizen 8 has 284173.53 remaining balance.
Citizen 9 has 311778.45 remaining balance.
Citizen 10 has 255603.09 remaining balance.
After adding 10111.69 to each citizen, "Language_Center" is chosen.

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
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Theater_Renovation
Amount added to each citizen: 8963.83
Citizen 1 has 259999.72 remaining balance.
Citizen 2 has 284396.68 remaining balance.
Citizen 3 has 282984.18 remaining balance.
Citizen 4 has 226864.06 remaining balance.
Citizen 5 has 333426.74 remaining balance.
Citizen 6 has 235179.96 remaining balance.
Citizen 7 has 374363.58 remaining balance.
Citizen 8 has 284173.53 remaining balance.
Citizen 9 has 320742.28 remaining balance.
Citizen 10 has 255603.09 remaining balance.
After adding 8963.83 to each citizen, "Theater_Renovation" is chosen.

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
Chosen project: Autism_Center
Amount added to each citizen: 7155.80
Citizen 1 has 267155.52 remaining balance.
Citizen 2 has 291552.48 remaining balance.
Citizen 3 has 290139.99 remaining balance.
Citizen 4 has 234019.86 remaining balance.
Citizen 5 has 333426.74 remaining balance.
Citizen 6 has 242335.76 remaining balance.
Citizen 7 has 374363.58 remaining balance.
Citizen 8 has 291329.33 remaining balance.
Citizen 9 has 320742.28 remaining balance.
Citizen 10 has 262758.89 remaining balance.
After adding 7155.80 to each citizen, "Autism_Center" is chosen.

======================================================================
Round 36
======================================================================
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
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Women_Shelter
Amount added to each citizen: 7858.67
Citizen 1 has 275014.19 remaining balance.
Citizen 2 has 299411.16 remaining balance.
Citizen 3 has 297998.66 remaining balance.
Citizen 4 has 241878.54 remaining balance.
Citizen 5 has 341285.41 remaining balance.
Citizen 6 has 242335.76 remaining balance.
Citizen 7 has 382222.25 remaining balance.
Citizen 8 has 291329.33 remaining balance.
Citizen 9 has 328600.95 remaining balance.
Citizen 10 has 262758.89 remaining balance.
After adding 7858.67 to each citizen, "Women_Shelter" is chosen.

======================================================================
Round 37
======================================================================
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
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Amphitheater
Amount added to each citizen: 24973.18
Citizen 1 has 299987.37 remaining balance.
Citizen 2 has 324384.34 remaining balance.
Citizen 3 has 297998.66 remaining balance.
Citizen 4 has 266851.72 remaining balance.
Citizen 5 has 341285.41 remaining balance.
Citizen 6 has 267308.94 remaining balance.
Citizen 7 has 382222.25 remaining balance.
Citizen 8 has 316302.51 remaining balance.
Citizen 9 has 328600.95 remaining balance.
Citizen 10 has 287732.07 remaining balance.
After adding 24973.18 to each citizen, "Amphitheater" is chosen.

======================================================================
Round 38
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
Project Skate_Park has no supporters, or is already funded.
Project Streetlight_Upgrade has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Senior_Home
Amount added to each citizen: 6238.84
Citizen 1 has 299987.37 remaining balance.
Citizen 2 has 324384.34 remaining balance.
Citizen 3 has 304237.50 remaining balance.
Citizen 4 has 266851.72 remaining balance.
Citizen 5 has 347524.25 remaining balance.
Citizen 6 has 267308.94 remaining balance.
Citizen 7 has 388461.09 remaining balance.
Citizen 8 has 316302.51 remaining balance.
Citizen 9 has 334839.79 remaining balance.
Citizen 10 has 287732.07 remaining balance.
After adding 6238.84 to each citizen, "Senior_Home" is chosen.

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
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Medical_Clinic
Amount added to each citizen: 39062.39
Citizen 1 has 299987.37 remaining balance.
Citizen 2 has 363446.73 remaining balance.
Citizen 3 has 304237.50 remaining balance.
Citizen 4 has 266851.72 remaining balance.
Citizen 5 has 386586.64 remaining balance.
Citizen 6 has 267308.94 remaining balance.
Citizen 7 has 427523.48 remaining balance.
Citizen 8 has 316302.51 remaining balance.
Citizen 9 has 373902.18 remaining balance.
Citizen 10 has 326794.46 remaining balance.
After adding 39062.39 to each citizen, "Medical_Clinic" is chosen.

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
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Swimming_Pool
Amount added to each citizen: 9710.72
Citizen 1 has 299987.37 remaining balance.
Citizen 2 has 363446.73 remaining balance.
Citizen 3 has 313948.22 remaining balance.
Citizen 4 has 276562.44 remaining balance.
Citizen 5 has 386586.64 remaining balance.
Citizen 6 has 277019.66 remaining balance.
Citizen 7 has 427523.48 remaining balance.
Citizen 8 has 326013.23 remaining balance.
Citizen 9 has 373902.18 remaining balance.
Citizen 10 has 336505.18 remaining balance.
After adding 9710.72 to each citizen, "Swimming_Pool" is chosen.

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
Project Swimming_Pool has no supporters, or is already funded.
Project Theater_Renovation has no supporters, or is already funded.
Project Urban_Garden has no supporters, or is already funded.
Project Veterans_Memorial has no supporters, or is already funded.
Project Vocational_School has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Wetlands_Restoration
Amount added to each citizen: 16637.57
Citizen 1 has 316624.95 remaining balance.
Citizen 2 has 380084.30 remaining balance.
Citizen 3 has 330585.79 remaining balance.
Citizen 4 has 276562.44 remaining balance.
Citizen 5 has 403224.21 remaining balance.
Citizen 6 has 277019.66 remaining balance.
Citizen 7 has 444161.05 remaining balance.
Citizen 8 has 342650.80 remaining balance.
Citizen 9 has 390539.75 remaining balance.
Citizen 10 has 336505.18 remaining balance.
After adding 16637.57 to each citizen, "Wetlands_Restoration" is chosen.

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
Amount added to each citizen: 73494.82
Citizen 1 has 390119.76 remaining balance.
Citizen 2 has 453579.12 remaining balance.
Citizen 3 has 404080.61 remaining balance.
Citizen 4 has 350057.26 remaining balance.
Citizen 5 has 476719.03 remaining balance.
Citizen 6 has 350514.48 remaining balance.
Citizen 7 has 517655.87 remaining balance.
Citizen 8 has 416145.62 remaining balance.
Citizen 9 has 464034.57 remaining balance.
Citizen 10 has 336505.18 remaining balance.
After adding 73494.82 to each citizen, "Meditation_Garden" is chosen.

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
Amount added to each citizen: 27916.75
Citizen 1 has 390119.76 remaining balance.
Citizen 2 has 453579.12 remaining balance.
Citizen 3 has 431997.36 remaining balance.
Citizen 4 has 350057.26 remaining balance.
Citizen 5 has 504635.78 remaining balance.
Citizen 6 has 350514.48 remaining balance.
Citizen 7 has 545572.62 remaining balance.
Citizen 8 has 416145.62 remaining balance.
Citizen 9 has 491951.32 remaining balance.
Citizen 10 has 364421.94 remaining balance.
After adding 27916.75 to each citizen, "Art_Museum" is chosen.

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
Amount added to each citizen: 27144.63
Citizen 1 has 390119.76 remaining balance.
Citizen 2 has 480723.75 remaining balance.
Citizen 3 has 431997.36 remaining balance.
Citizen 4 has 377201.89 remaining balance.
Citizen 5 has 504635.78 remaining balance.
Citizen 6 has 377659.11 remaining balance.
Citizen 7 has 545572.62 remaining balance.
Citizen 8 has 443290.25 remaining balance.
Citizen 9 has 491951.32 remaining balance.
Citizen 10 has 391566.57 remaining balance.
After adding 27144.63 to each citizen, "Sports_Complex" is chosen.

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
Chosen project: School_Expansion
Amount added to each citizen: 26201.05
Citizen 1 has 390119.76 remaining balance.
Citizen 2 has 480723.75 remaining balance.
Citizen 3 has 458198.41 remaining balance.
Citizen 4 has 377201.89 remaining balance.
Citizen 5 has 530836.83 remaining balance.
Citizen 6 has 377659.11 remaining balance.
Citizen 7 has 571773.67 remaining balance.
Citizen 8 has 443290.25 remaining balance.
Citizen 9 has 518152.37 remaining balance.
Citizen 10 has 417767.61 remaining balance.
After adding 26201.05 to each citizen, "School_Expansion" is chosen.

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
Chosen project: Innovation_Lab
Amount added to each citizen: 33520.28
Citizen 1 has 423640.05 remaining balance.
Citizen 2 has 514244.03 remaining balance.
Citizen 3 has 491718.69 remaining balance.
Citizen 4 has 377201.89 remaining balance.
Citizen 5 has 564357.12 remaining balance.
Citizen 6 has 377659.11 remaining balance.
Citizen 7 has 605293.96 remaining balance.
Citizen 8 has 443290.25 remaining balance.
Citizen 9 has 551672.65 remaining balance.
Citizen 10 has 417767.61 remaining balance.
After adding 33520.28 to each citizen, "Innovation_Lab" is chosen.

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
Project Innovation_Lab has no supporters, or is already funded.
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
Amount added to each citizen: 41032.84
Citizen 1 has 423640.05 remaining balance.
Citizen 2 has 514244.03 remaining balance.
Citizen 3 has 532751.54 remaining balance.
Citizen 4 has 377201.89 remaining balance.
Citizen 5 has 605389.96 remaining balance.
Citizen 6 has 377659.11 remaining balance.
Citizen 7 has 646326.80 remaining balance.
Citizen 8 has 443290.25 remaining balance.
Citizen 9 has 592705.50 remaining balance.
Citizen 10 has 417767.61 remaining balance.
After adding 41032.84 to each citizen, "Tech_Hub" is chosen.

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
Project Innovation_Lab has no supporters, or is already funded.
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
Chosen project: Police_Station
Amount added to each citizen: 41716.44
Citizen 1 has 465356.48 remaining balance.
Citizen 2 has 514244.03 remaining balance.
Citizen 3 has 532751.54 remaining balance.
Citizen 4 has 418918.32 remaining balance.
Citizen 5 has 605389.96 remaining balance.
Citizen 6 has 419375.55 remaining balance.
Citizen 7 has 646326.80 remaining balance.
Citizen 8 has 485006.69 remaining balance.
Citizen 9 has 592705.50 remaining balance.
Citizen 10 has 459484.05 remaining balance.
After adding 41716.44 to each citizen, "Police_Station" is chosen.

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
Chosen project: Makerspace
Amount added to each citizen: 12754.63
Citizen 1 has 478111.11 remaining balance.
Citizen 2 has 526998.66 remaining balance.
Citizen 3 has 545506.17 remaining balance.
Citizen 4 has 431672.95 remaining balance.
Citizen 5 has 618144.59 remaining balance.
Citizen 6 has 432130.18 remaining balance.
Citizen 7 has 659081.43 remaining balance.
Citizen 8 has 485006.69 remaining balance.
Citizen 9 has 605460.13 remaining balance.
Citizen 10 has 459484.05 remaining balance.
After adding 12754.63 to each citizen, "Makerspace" is chosen.

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
Chosen project: Solar_Farm
Amount added to each citizen: 64432.73
Citizen 1 has 478111.11 remaining balance.
Citizen 2 has 526998.66 remaining balance.
Citizen 3 has 609938.89 remaining balance.
Citizen 4 has 431672.95 remaining balance.
Citizen 5 has 682577.31 remaining balance.
Citizen 6 has 432130.18 remaining balance.
Citizen 7 has 723514.16 remaining balance.
Citizen 8 has 485006.69 remaining balance.
Citizen 9 has 669892.85 remaining balance.
Citizen 10 has 459484.05 remaining balance.
After adding 64432.73 to each citizen, "Solar_Farm" is chosen.

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
Chosen project: Fire_Station
Amount added to each citizen: 51464.63
Citizen 1 has 478111.11 remaining balance.
Citizen 2 has 578463.29 remaining balance.
Citizen 3 has 609938.89 remaining balance.
Citizen 4 has 483137.58 remaining balance.
Citizen 5 has 682577.31 remaining balance.
Citizen 6 has 483594.81 remaining balance.
Citizen 7 has 723514.16 remaining balance.
Citizen 8 has 536471.32 remaining balance.
Citizen 9 has 721357.48 remaining balance.
Citizen 10 has 510948.68 remaining balance.
After adding 51464.63 to each citizen, "Fire_Station" is chosen.

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
Chosen project: Water_Treatment
Amount added to each citizen: 56829.77
Citizen 1 has 534940.89 remaining balance.
Citizen 2 has 578463.29 remaining balance.
Citizen 3 has 609938.89 remaining balance.
Citizen 4 has 539967.36 remaining balance.
Citizen 5 has 682577.31 remaining balance.
Citizen 6 has 540424.58 remaining balance.
Citizen 7 has 723514.16 remaining balance.
Citizen 8 has 593301.09 remaining balance.
Citizen 9 has 721357.48 remaining balance.
Citizen 10 has 567778.45 remaining balance.
After adding 56829.77 to each citizen, "Water_Treatment" is chosen.

======================================================================
Round 53
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
Project Water_Treatment has no supporters, or is already funded.
Project Wetlands_Restoration has no supporters, or is already funded.
Project Women_Shelter has no supporters, or is already funded.
Project Youth_Center has no supporters, or is already funded.
Chosen project: Business_Incubator
Amount added to each citizen: 67564.18
Citizen 1 has 602505.07 remaining balance.
Citizen 2 has 646027.47 remaining balance.
Citizen 3 has 677503.07 remaining balance.
Citizen 4 has 607531.54 remaining balance.
Citizen 5 has 750141.50 remaining balance.
Citizen 6 has 607988.76 remaining balance.
Citizen 7 has 723514.16 remaining balance.
Citizen 8 has 660865.27 remaining balance.
Citizen 9 has 721357.48 remaining balance.
Citizen 10 has 635342.63 remaining balance.
After adding 67564.18 to each citizen, "Business_Incubator" is chosen.

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
Chosen project: Public_Transport
Amount added to each citizen: 196291.26
Citizen 1 has 798796.33 remaining balance.
Citizen 2 has 646027.47 remaining balance.
Citizen 3 has 677503.07 remaining balance.
Citizen 4 has 803822.80 remaining balance.
Citizen 5 has 750141.50 remaining balance.
Citizen 6 has 804280.03 remaining balance.
Citizen 7 has 723514.16 remaining balance.
Citizen 8 has 857156.53 remaining balance.
Citizen 9 has 721357.48 remaining balance.
Citizen 10 has 831633.90 remaining balance.
After adding 196291.26 to each citizen, "Public_Transport" is chosen.

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
Chosen project: Convention_Center
Amount added to each citizen: 203558.95
Citizen 1 has 1002355.28 remaining balance.
Citizen 2 has 646027.47 remaining balance.
Citizen 3 has 881062.02 remaining balance.
Citizen 4 has 803822.80 remaining balance.
Citizen 5 has 953700.45 remaining balance.
Citizen 6 has 804280.03 remaining balance.
Citizen 7 has 927073.11 remaining balance.
Citizen 8 has 1060715.49 remaining balance.
Citizen 9 has 924916.43 remaining balance.
Citizen 10 has 831633.90 remaining balance.
After adding 203558.95 to each citizen, "Convention_Center" is chosen.

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
Chosen project: Hospital_Wing
Amount added to each citizen: 93444.10
Citizen 1 has 1095799.38 remaining balance.
Citizen 2 has 646027.47 remaining balance.
Citizen 3 has 881062.02 remaining balance.
Citizen 4 has 897266.90 remaining balance.
Citizen 5 has 953700.45 remaining balance.
Citizen 6 has 897724.13 remaining balance.
Citizen 7 has 927073.11 remaining balance.
Citizen 8 has 1154159.59 remaining balance.
Citizen 9 has 924916.43 remaining balance.
Citizen 10 has 925078.00 remaining balance.
After adding 93444.10 to each citizen, "Hospital_Wing" is chosen.

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
Project Hospital_Wing has no supporters, or is already funded.
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
Amount added to each citizen: 275002.78
Citizen 1 has 1370802.17 remaining balance.
Citizen 2 has 921030.26 remaining balance.
Citizen 3 has 1156064.81 remaining balance.
Citizen 4 has 1172269.69 remaining balance.
Citizen 5 has 1228703.23 remaining balance.
Citizen 6 has 1172726.91 remaining balance.
Citizen 7 has 1202075.89 remaining balance.
Citizen 8 has 1429162.37 remaining balance.
Citizen 9 has 924916.43 remaining balance.
Citizen 10 has 925078.00 remaining balance.
After adding 275002.78 to each citizen, "Observatory" is chosen.

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
Amount added to each citizen: 117924.11
Citizen 1 has 1488726.28 remaining balance.
Citizen 2 has 1038954.37 remaining balance.
Citizen 3 has 1273988.92 remaining balance.
Citizen 4 has 1290193.80 remaining balance.
Citizen 5 has 1346627.34 remaining balance.
Citizen 6 has 1290651.02 remaining balance.
Citizen 7 has 1202075.89 remaining balance.
Citizen 8 has 1547086.48 remaining balance.
Citizen 9 has 1042840.55 remaining balance.
Citizen 10 has 1043002.11 remaining balance.
After adding 117924.11 to each citizen, "Addiction_Treatment" is chosen.

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

[Done] exited with code=0 in 0.08 seconds
"""
