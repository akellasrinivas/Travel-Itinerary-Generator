import subprocess
import json

def test_generate_filtered_itineraries(place):
    try:
        # Call the main itinerary generation script with the specified place
        result = subprocess.run(
            ['python', 'scripts\itinerary.py', place],  # Adjust the path if necessary
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        # Print the output from the script
        print(f"Output for place '{place}':")
        print(result.stdout)

        # Optionally, parse the JSON output to check specific details
        itineraries_info = json.loads(result.stdout)
        
        # Perform assertions or checks based on expected output
        if "Error" in itineraries_info:
            print(itineraries_info["Error"])
        else:
            # Example checks: print the number of clusters generated
            print(f"Generated {len(itineraries_info)} clusters.")
            for cluster, itinerary in itineraries_info.items():
                print(f"{cluster} itineraries:")
                for day, activities in itinerary.items():
                    print(f"{day}: {activities}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")

if __name__ == "__main__":
    # Example test cases
    test_places = [ "agra", "shimla", "kerala"]  # Include some known and unknown places
    for place in test_places:
        test_generate_filtered_itineraries(place)
