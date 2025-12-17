
import sys
from datetime import datetime

# פתיחת קבצי הפלט
output_file = open("output.txt", "w", encoding="utf-8")
log_file = open("detailed_log.txt", "w", encoding="utf-8")

def log_print(message, to_output=True, to_log=False):
    """
    מדפיסה הודעה למסך ולקבצים לפי הצורך
    """
    print(message)
    if to_output:
        output_file.write(message + "\n")
        output_file.flush()
    if to_log:
        log_file.write(message + "\n")
        log_file.flush()

def detailed_log(message):
    """
    כותבת רק ללוג המפורט
    """
    log_file.write(message + "\n")
    log_file.flush()

# כותרת ללוג המפורט
detailed_log("="*80)
detailed_log(f"Phragmen Budget Allocation - Detailed Log")
detailed_log(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
detailed_log("="*80 + "\n")

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

    # לוג: מצב התחלתי
    detailed_log("\n" + "-"*80)
    detailed_log("Current State Before Selection:")
    detailed_log(f"Number of remaining projects: {len(costs)}")
    detailed_log(f"Citizens balances: {[f'{b:.2f}' for b in balances]}")
    detailed_log(f"Total money in system: {sum(balances):.2f}")
    detailed_log("-"*80)

    #סידור הפרוייקטים לפי סדר אלפביתי
    costs = dict(sorted(costs.items()))
    
    # לוג: ניתוח כל פרויקט
    detailed_log("\nAnalyzing all projects:")
    detailed_log("="*80)
    
    # מעבר על כל הפרוייקטים
    for project in costs:

        # מציאת התומכים של הפרוייקט הזה
        supporters = []
        supporters = find_supporters(project, votes)

        detailed_log(f"\nProject: {project}")
        detailed_log(f"  Cost: {costs[project]:,.2f}")
        detailed_log(f"  Number of supporters: {len(supporters)}")
        
        if supporters == []:
            detailed_log(f"  Status: NO SUPPORTERS - Cannot be funded")
            log_print(f"Project {project} has no supporters.", to_log=False)
            continue  # אין תומכים, לא ניתן לממן את הפרוייקט הזה

        # הדפסת פרטי התומכים
        detailed_log(f"  Supporters: {[i+1 for i in supporters]}")
        for sup in supporters:
            detailed_log(f"    - Citizen {sup+1}: balance = {balances[sup]:.2f}")

        # חישוב התקציב של התומכים בפרוייקט הנוכחי
        B_j = find_the_budget_for_project(supporters, balances)
        detailed_log(f"  Total supporters' balance: {B_j:.2f}")
        
        #חישוב כמה כסף חסר עבור הפרוייקט הנוכחי
        D_j = costs[project] - B_j
        detailed_log(f"  Missing amount (D_j): {D_j:.2f}")
        
        #חישוב כמה זמן ייקח לממן אותו
        t_j = D_j / len(supporters)
        detailed_log(f"  Time needed (t_j): {t_j:.2f}")
        detailed_log(f"  Formula: t_j = (cost - total_balance) / num_supporters")
        detailed_log(f"           t_j = ({costs[project]:.2f} - {B_j:.2f}) / {len(supporters)} = {t_j:.2f}")

        if t_j < min_time:
            detailed_log(f"  >>> NEW MINIMUM! This project can be funded first <<<")
            min_time = t_j
            chosen_project = project
            missing_cost = t_j
        elif t_j == min_time:
            detailed_log(f"  >>> TIE detected! Comparing lexicographically with {chosen_project}")
            if project < chosen_project:
                detailed_log(f"  >>> {project} comes before {chosen_project} - NEW WINNER <<<")
                chosen_project = project
        else:
            detailed_log(f"  Not selected (t_j = {t_j:.2f} > min = {min_time:.2f})")

    detailed_log("\n" + "="*80)

    if chosen_project is None:
        # אין פרוייקט שניתן לממן כרגע
        msg = "No project can be selected."
        log_print(msg, to_output=True, to_log=True)
        return
    
    # לוג: הפרויקט שנבחר
    detailed_log(f"\nSELECTED PROJECT: {chosen_project}")
    detailed_log(f"Time to add to each citizen: {missing_cost:.2f}")
    detailed_log(f"Project cost: {costs[chosen_project]:.2f}")
    
    # הוספת הסכום הנדרש לכל אזרח
    detailed_log("\nUpdating balances:")
    for i in range(n):
        old_balance = balances[i]
        balances[i] += missing_cost
        detailed_log(f"  Citizen {i+1}: {old_balance:.2f} + {missing_cost:.2f} = {balances[i]:.2f}")
    
    # איפוס היתרות של התומכים של הפרוייקט שנבחר
    detailed_log(f"\nResetting balances of supporters of {chosen_project}:")
    supporters_of_chosen = find_supporters(chosen_project, votes)
    for i in range(n):
        if chosen_project in votes[i]:
            old_balance = balances[i]
            balances[i] -= missing_cost  # התומכים משלמים על הפרוייקט
            detailed_log(f"  Citizen {i+1} (supporter): {old_balance:.2f} - {missing_cost:.2f} = {balances[i]:.2f}")

    #מחיקת הפרוייקט הנבחר מהמילון של העלויות ומרשימת ההצבעות
    del costs[chosen_project]
    for i in range(n):
        if chosen_project in votes[i]:
            votes[i].remove(chosen_project)
    
    detailed_log(f"\nProject {chosen_project} removed from costs and votes lists")
    detailed_log(f"Remaining projects: {len(costs)}")

    # הדפסת התוצאות לפלט רגיל
    log_print(f"Chosen project: {chosen_project}", to_output=True, to_log=True)
    log_print(f"Amount added to each citizen: {missing_cost:.2f}", to_output=True, to_log=True)
    for i in range(len(balances)):
        log_print(f"Citizen {i+1} has {balances[i]:.2f} remaining balance.", to_output=True, to_log=True)
    log_print(f"After adding {missing_cost:.2f} to each citizen, \"{chosen_project}\" is chosen.", to_output=True, to_log=True)


# Example 5: Iterative run
log_print("\n\nExample 5: Iterative run with 10 citizens and 60 projects", to_output=True, to_log=True)
log_print("="*80, to_output=True, to_log=True)

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

balances5 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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

# לוג התחלתי
detailed_log("\n" + "="*80)
detailed_log("INITIAL SETUP:")
detailed_log("="*80)
detailed_log(f"Total number of citizens: {len(votes5)}")
detailed_log(f"Total number of projects: {len(costs5)}")
detailed_log(f"Initial balances: {balances5}")
detailed_log("\nCitizen preferences:")
for i, prefs in enumerate(votes5):
    detailed_log(f"  Citizen {i+1} supports {len(prefs)} projects: {sorted(list(prefs)[:5])}... (showing first 5)")

# הרצה איטרטיבית
round_num = 1
funded_projects = []

while costs5:
    header = f"\n{'='*70}\nRound {round_num}\n{'='*70}"
    log_print(header, to_output=True, to_log=True)
    detailed_log(f"\n\n{'#'*80}")
    detailed_log(f"ROUND {round_num}")
    detailed_log(f"{'#'*80}")
    
    elect_next_budget_item(votes5, balances5, costs5)
    
    round_num += 1
    if round_num > 60:  # למניעת לולאה אינסופית
        msg = "\nהגענו למקסימום סיבובים."
        log_print(msg, to_output=True, to_log=True)
        break

summary = f"\n{'='*70}\nFinal Summary: {round_num-1} projects were funded\n{'='*70}"
log_print(summary, to_output=True, to_log=True)

detailed_log("\n\n" + "="*80)
detailed_log("EXECUTION COMPLETED")
detailed_log(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
detailed_log(f"Total rounds executed: {round_num-1}")
detailed_log("="*80)

# סגירת הקבצים
output_file.close()
log_file.close()

print("\n✅ Execution completed!")
print("📄 Output saved to: output.txt")
print("📊 Detailed log saved to: detailed_log.txt")