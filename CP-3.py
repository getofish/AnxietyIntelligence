import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_cp3_simulation(contingency_roles, training_time_period, system_changes_trigger, training_frequency, training_update_frequency, event_triggers, scenario=None):

    try:
        parameters = {
            "contingency_roles": contingency_roles,
            "training_time_period": training_time_period,
            "system_changes_trigger": system_changes_trigger,
            "training_frequency": training_frequency,
            "training_update_frequency": training_update_frequency,
            "event_triggers": event_triggers
        }
        
        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the management of contingency training for system users based on the provided details."},
                {
                    "role": "user",
                    "content": f"Start the CP-3 guidance with the following details: {parameters}."
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
                print("Contingency training guidance ended. Thank you for participating.")
                break
            

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the CP-3 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )


            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the CP-3 guidance: {e}")

def main():

    contingency_roles = "System Administrator, Backup Specialist, Incident Response Lead."
    training_time_period = "Within 30 days of assuming the contingency role."
    system_changes_trigger = "When there are changes to system architecture or key personnel."
    training_frequency = "Annually."
    training_update_frequency = "Bi-annually."
    event_triggers = "Following significant incidents, system upgrades, or audit results."


    scenario = None

 
    run_cp3_simulation(contingency_roles, training_time_period, system_changes_trigger, training_frequency, training_update_frequency, event_triggers, scenario)

if __name__ == "__main__":
    main()

