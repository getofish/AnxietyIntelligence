import sqlite3
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_device_info():

    try:
        conn = sqlite3.connect('anxiety_intelligence.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT device_name, risk_level, device_owner, primary_site, secondary_site, function FROM devices;")
        devices = cursor.fetchall()
        conn.close()

        device_list = []
        for index, device in enumerate(devices, start=1):
            device_info = {
                "device_name": device[0],
                "risk_level": device[1].lower(),
                "device_owner": device[2] if device[1].lower() in ['moderate', 'high'] else None,
                "primary_site": device[3] if device[1].lower() == 'high' else None,
                "secondary_site": device[4] if device[1].lower() == 'high' else None,
                "function": device[5]
            }
            device_list.append(device_info)
            print(f"{index}. Device: {device_info['device_name']}, Risk Level: {device_info['risk_level']}")

        return device_list

    except Exception as e:
        print(f"An error occurred while fetching device information: {e}")
        return []

def run_cp4_simulation(device_info):

    try:
        parameters = {
            "device_name": device_info['device_name'],
            "risk_level": device_info['risk_level']
        }
        
        if device_info['risk_level'] in ['moderate', 'high']:
            parameters['device_owner'] = device_info['device_owner']
        if device_info['risk_level'] == 'high':
            parameters['primary_site'] = device_info['primary_site']
            parameters['secondary_site'] = device_info['secondary_site']
        
        if device_info['function']:
            parameters['function'] = device_info['function']

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant running a disaster recovery tabletop simulation. Provide the initial scenario and respond dynamically based on the user's inputs."},
                {
                    "role": "user",
                    "content": f"Start the tabletop simulation with the following details: {parameters}."
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        assistant_message = response.choices[0].message["content"]
        print(f"\nScenario: {assistant_message}\n")

        while True:
            user_input = input("Your response (type 'end' to exit): ").strip().lower()
            if user_input == "end":
                print("Tabletop exercise ended. Thank you for participating.")
                break
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Continue the tabletop simulation based on the latest user response."},
                    {"role": "assistant", "content": assistant_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            assistant_message = response.choices[0].message["content"]
            print(f"\nUpdate: {assistant_message}\n")

    except Exception as e:
        print(f"An error occurred while running the tabletop simulation: {e}")

def main():
    devices = get_device_info()

    if not devices:
        print("No devices found in the database.")
        return

    selected_index = input("\nEnter the number of the device to run the simulation on (e.g., 1, 2, ...): ").strip()

    try:
        selected_device = devices[int(selected_index) - 1]
    except (IndexError, ValueError):
        print("Invalid selection. Please enter a valid device number.")
        return

    run_cp4_simulation(selected_device)

if __name__ == "__main__":
    main()

