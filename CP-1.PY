import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_cp1_simulation(personnel_roles, contingency_policy_level, official_designate, review_frequency, trigger_events, compliance_requirements, scenario=None):

    try:
        parameters = {
            "personnel_roles": personnel_roles,
            "contingency_policy_level": contingency_policy_level,
            "official_designate": official_designate,
            "review_frequency": review_frequency,
            "trigger_events": trigger_events,
            "compliance_requirements": compliance_requirements
        }
        
        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the development, documentation, and dissemination of contingency planning policy and procedures based on provided details."},
                {
                    "role": "user",
                    "content": f"Start the CP-1 guidance with the following details: {parameters}."
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
                print("Contingency planning guidance ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the CP-1 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the CP-1 guidance: {e}")

def main():
    personnel_roles = "IT Manager, Security Officer"
    contingency_policy_level = "organization-level"
    official_designate = "Contingency Planning Officer"
    review_frequency = "annually"
    trigger_events = "after a significant incident"
    compliance_requirements = "NIST guidelines, executive orders, company policies"
    scenario = None 

    run_cp1_simulation(personnel_roles, contingency_policy_level, official_designate, review_frequency, trigger_events, compliance_requirements, scenario)

if __name__ == "__main__":
    main()

