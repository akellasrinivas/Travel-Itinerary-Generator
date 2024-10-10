import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json  # Import json module
import sys  # Import sys module for command line arguments

# Load the enriched dataset (replace with the path to your enriched CSV file)
data = pd.read_csv('scripts\modified_travel_data.csv')  # Use forward slashes

# Mapping 'vibe' values to numeric values and vice versa for easy lookup
vibe_mapping = {
    'Adventure': 1,
    'Relaxation': 2,
    'Socializing': 3,
    'Budget': 4,
    'Cultural': 5,
    'Luxury': 6
}
reverse_vibe_mapping = {v: k for k, v in vibe_mapping.items()}
data['vibe'] = data['vibe'].map(vibe_mapping)

# Handle missing values
data['expenses'].fillna(0, inplace=True)  # Replace NaNs with 0 for expenses
data['total_package_amount'].fillna(0, inplace=True)  # Replace NaNs with 0 for package amount
data['vibe'].fillna(0, inplace=True)  # Replace NaNs with 0 for vibe

# Ensure the columns are of the correct type
data['total_package_amount'] = data['total_package_amount'].astype(float)

# Function to generate filtered trips based on place and create a detailed itinerary
def generate_filtered_itineraries(place):
    try:
        # Filter data based on users who visited the specified place
        filtered_data = data[
            (data['previous_destinations'].str.contains(place, case=False, na=False))
        ]
        
        if filtered_data.empty:
            return {"Error": f"No trips available for the place: {place}"}
        
        # Selecting relevant features for clustering
        features = filtered_data[['expenses', 'vibe', 'total_package_amount']]
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        # Apply KMeans clustering to the filtered data
        num_clusters = min(4, len(filtered_data))  # Avoid having more clusters than data points
        if num_clusters < 1:
            return {"Error": "Not enough data to form clusters."}
        
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        filtered_data.loc[:, 'cluster'] = kmeans.fit_predict(scaled_features)

        # Generate itineraries for each cluster
        itineraries = {}
        for cluster in range(num_clusters):
            cluster_data = filtered_data[filtered_data['cluster'] == cluster]
            
            if not cluster_data.empty:
                # Randomly select an itinerary from this cluster
                itinerary = cluster_data.sample(n=1, random_state=42)  # Select a random entry for the itinerary
                
                # Prepare the itinerary details
                total_package = itinerary['total_package_amount'].values[0]
                vibes = reverse_vibe_mapping.get(int(itinerary['vibe'].values[0]), "General")
                famous_places = itinerary['famous_places_to_visit'].values[0].split(', ')
                activities = itinerary['favorite_activities'].values[0].split(', ')
                
                # Determine the number of days for the itinerary (fixed or based on data)
                # Here we're assuming a fixed number of days, adjust as needed
                days_by_travel = 3  # Example: 3 days, you can change this value as needed
                
                # Generate a detailed itinerary for each day based on the number of days
                itinerary_details = {}
                for day in range(1, days_by_travel + 1):
                    itinerary_details[f"Day {day}"] = (
                        f"Morning: Relax at hotel.\n"
                        f"Afternoon: Visit {famous_places[day % len(famous_places)]}.\n"  # Cycle through famous places
                        f"Evening: Enjoy activities like {activities[day % len(activities)]}.\n"  # Cycle through activities
                        f"Total Package Amount: {total_package} USD."
                    )

                itineraries[f"Cluster {cluster + 1}"] = {
                    "Vibe": vibes,
                    "Details": itinerary_details
                }
        
        return itineraries

    except Exception as e:
        return {"Error": str(e)}  # Handle any unexpected errors

# Main function to get user input from command line arguments
if __name__ == "__main__":
    try:
        # Get user input from command line arguments
        user_place = sys.argv[1]  # Only take place as input

        # Generate the filtered itineraries and print as JSON
        itineraries_info = generate_filtered_itineraries(user_place)
        
        # Ensure the output is JSON serializable
        print(json.dumps(itineraries_info))  # Ensure this outputs a JSON string
    except Exception as e:
        print(json.dumps({"Error": str(e)}))  # Handle any unexpected errors
