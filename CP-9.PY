import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_cp9_simulation(disruption_type, recovery_time_objective, recovery_point_objective, known_state_description, recovery_steps, validation_process, scenario=None):

    try:
        parameters = {
            "disruption_type": disruption_type,
            "recovery_time_objective": recovery_time_objective,
            "recovery_point_objective": recovery_point_objective,
            "known_state_description": known_state_description,
            "recovery_steps": recovery_steps,
            "validation_process": validation_process
        }
        
        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the recovery and reconstitution of a system to a known state after a disruption or failure."},
                {
                    "role": "user",
                    "content": f"Start the CP-9 guidance with the following details: {parameters}."
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
                print("Recovery and reconstitution guidance ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the CP-9 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the CP-9 guidance: {e}")

def main():
    disruption_type = "Cyber attack resulting in data compromise."
    recovery_time_objective = "4 hours."
    recovery_point_objective = "30 minutes of data loss."
    known_state_description = "Last verified backup taken at 12:00 PM."
    recovery_steps = "1. Isolate compromised systems, 2. Restore data from backup, 3. Revalidate system integrity."
    validation_process = "Cross-check restored data with backup logs and perform system integrity checks."

    scenario = None

    run_cp9_simulation(disruption_type, recovery_time_objective, recovery_point_objective, known_state_description, recovery_steps, validation_process, scenario)

if __name__ == "__main__":
    main()

