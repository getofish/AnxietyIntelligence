import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_cp8_simulation(user_level_components, user_backup_frequency, system_level_components, system_backup_frequency, documentation_backup_frequency, confidentiality_protection, integrity_protection, availability_protection, scenario=None):

    try:
        parameters = {
            "user_level_components": user_level_components,
            "user_backup_frequency": user_backup_frequency,
            "system_level_components": system_level_components,
            "system_backup_frequency": system_backup_frequency,
            "documentation_backup_frequency": documentation_backup_frequency,
            "confidentiality_protection": confidentiality_protection,
            "integrity_protection": integrity_protection,
            "availability_protection": availability_protection
        }
        
        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the management of backups for user-level, system-level, and documentation information."},
                {
                    "role": "user",
                    "content": f"Start the CP-8 guidance with the following details: {parameters}."
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
                print("Backup guidance ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the CP-8 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the CP-8 guidance: {e}")

def main():
    user_level_components = "Workstations, user directories."
    user_backup_frequency = "Daily."
    system_level_components = "Database servers, application servers."
    system_backup_frequency = "Weekly."
    documentation_backup_frequency = "Monthly."
    confidentiality_protection = True
    integrity_protection = True
    availability_protection = True

    scenario = None

    run_cp8_simulation(user_level_components, user_backup_frequency, system_level_components, system_backup_frequency, documentation_backup_frequency, confidentiality_protection, integrity_protection, availability_protection, scenario)

if __name__ == "__main__":
    main()

