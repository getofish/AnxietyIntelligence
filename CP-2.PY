import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_cp2_simulation(mission_functions, recovery_objectives, contingency_roles, system_restoration, contingency_information_sharing, approval_personnel, key_contingency_personnel, frequency_review, contingency_updates, lessons_learned, unauthorized_access_protection, scenario=None):

    try:
        parameters = {
            "mission_functions": mission_functions,
            "recovery_objectives": recovery_objectives,
            "contingency_roles": contingency_roles,
            "system_restoration": system_restoration,
            "contingency_information_sharing": contingency_information_sharing,
            "approval_personnel": approval_personnel,
            "key_contingency_personnel": key_contingency_personnel,
            "frequency_review": frequency_review,
            "contingency_updates": contingency_updates,
            "lessons_learned": lessons_learned,
            "unauthorized_access_protection": unauthorized_access_protection
        }
        
        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the development of a contingency plan for a system based on provided details."},
                {
                    "role": "user",
                    "content": f"Start the CP-2 guidance with the following details: {parameters}."
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
                print("Contingency plan guidance ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the CP-2 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the CP-2 guidance: {e}")

def main():
    mission_functions = "Ensure continuous network availability and security."
    recovery_objectives = "Restore all mission-critical services within 4 hours; minimize data loss."
    contingency_roles = "IT Director, Security Officer, Network Administrator."
    system_restoration = "Restore all systems with original security controls and without compromising availability."
    contingency_information_sharing = "Share contingency status with the executive team and IT stakeholders."
    approval_personnel = "Executive leadership, IT governance board."
    key_contingency_personnel = "IT team, Security personnel, Key managers."
    frequency_review = "Quarterly review and after significant changes."
    contingency_updates = "Update following system changes, incidents, or regulatory changes."
    lessons_learned = "Incorporate lessons from prior tests and real-world incidents into the plan."
    unauthorized_access_protection = "Limit access to the plan via role-based permissions and encryption."

    scenario = None

    run_cp2_simulation(mission_functions, recovery_objectives, contingency_roles, system_restoration, contingency_information_sharing, approval_personnel, key_contingency_personnel, frequency_review, contingency_updates, lessons_learned, unauthorized_access_protection, scenario)

if __name__ == "__main__":
    main()

