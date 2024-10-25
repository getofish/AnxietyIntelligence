import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_c6_simulation(primary_site_controls, alternate_site_location, agreements_status, equivalent_controls_check, scenario=None):

    try:
        parameters = {
            "primary_site_controls": primary_site_controls,
            "alternate_site_location": alternate_site_location,
            "agreements_status": agreements_status,
            "equivalent_controls_check": equivalent_controls_check
        }
        
        if scenario:
            parameters["scenario"] = scenario

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant guiding the establishment of an alternate storage site for system backups."},
                {
                    "role": "user",
                    "content": f"Start the C-6 guidance with the following details: {parameters}."
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
                print("Alternate storage site guidance ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the C-6 guidance based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the C-6 guidance: {e}")

def main():
    primary_site_controls = "Encryption, access control, and monitoring."
    alternate_site_location = "Data Center B, Springfield."
    agreements_status = "Signed and active as of Q3 2023."
    equivalent_controls_check = True

    scenario = None

    run_c6_simulation(primary_site_controls, alternate_site_location, agreements_status, equivalent_controls_check, scenario)

if __name__ == "__main__":
    main()

