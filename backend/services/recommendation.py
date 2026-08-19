def get_recommendation(plant: str, disease: str):

    recommendations = {
        ("Tomato", "Target Spot"): {
            "organic_remedy": "Remove infected leaves and spray neem oil regularly.",
            "chemical_treatment": "Use a suitable fungicide recommended for tomato fungal diseases.",
            "prevention": "Avoid overhead watering, improve air circulation, and remove infected plant debris."
        }
    }

    return recommendations.get(
        (plant, disease),
        {
            "organic_remedy": "Remove affected leaves and keep the plant area clean.",
            "chemical_treatment": "Consult an agriculture expert before applying chemicals.",
            "prevention": "Maintain proper watering, spacing, and regular plant monitoring."
        }
    )