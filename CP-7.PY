import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_cp7_simulation(system_operations, recovery_time_objective, recovery_point_objective, alternate_processing_site_location, agreements_status, equipment_and_supplies, equivalent_controls_check, scenario=None):

    try:
        parameters = {
            "system_operations": system_operations,
            "recovery_time_objective": recovery_time_objective,
            "recovery_point_objective": recovery_point_objective,
            "alternate_processing_site_location": alternate_processing_site_location,
            "agreements_status": agreements_status,
            "equipment_and_supplies": equipment_and_supplies,
            "equivalent_controls_check": equivalent_controls_check
        }
        

        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the establishment of an alternate processing site for essential mission and business functions."},
                {
                    "role": "user",
                    "content": f"Start the CP-7 guidance with the following details: {parameters}."
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        assistant_message = response.choices[0].message["content"]
        print(f"\nGuidance: {assistant_message}\n")

        while True:

            user_input = input("Your response (type 'end' to exit): ").strip().lower()
            if user_input == "end":
                print("Alternate processing site guidance ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the CP-7 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the CP-7 guidance: {e}")

def main():
    system_operations = "Core banking operations, payroll systems."
    recovery_time_objective = "4 hours."
    recovery_point_objective = "1 hour of data loss tolerance."
    alternate_processing_site_location = "Backup Data Center, Miami."
    agreements_status = "Signed agreements with third-party vendor, effective Q2 2023."
    equipment_and_supplies = "Backup servers, network switches, storage devices."
    equivalent_controls_check = True

    scenario = None


    run_cp7_simulation(system_operations, recovery_time_objective, recovery_point_objective, alternate_processing_site_location, agreements_status, equipment_and_supplies, equivalent_controls_check, scenario)

if __name__ == "__main__":
    main()

