# CareBloom Disease Care Engine
# Provides treatment, prevention and health recommendations.

DISEASE_CARE = {
    "Early Blight": {
        "description": "A fungal disease that causes brown circular spots and damages older leaves.",
        "symptoms": [
            "Brown circular spots",
            "Yellowing of older leaves",
            "Leaf drying",
            "Reduced plant growth"
        ],
        "organic_remedies": [
            "Remove infected leaves",
            "Apply neem oil spray",
            "Avoid watering directly on leaves",
            "Improve air circulation"
        ],
        "treatment": [
            "Remove severely infected plant material",
            "Use an appropriate fungicide when necessary",
            "Keep foliage dry"
        ],
        "prevention": [
            "Use healthy planting material",
            "Maintain proper plant spacing",
            "Rotate crops",
            "Keep the growing area clean"
        ]
    },

    "Late Blight": {
        "description": "A rapidly spreading disease that can damage leaves, stems and fruits.",
        "symptoms": [
            "Dark water-soaked leaf lesions",
            "Brown or black patches",
            "White fungal growth under humid conditions",
            "Rapid leaf collapse"
        ],
        "organic_remedies": [
            "Remove infected leaves immediately",
            "Avoid overhead watering",
            "Improve ventilation around plants"
        ],
        "treatment": [
            "Isolate severely affected plants",
            "Apply a recommended fungicide when required",
            "Remove heavily infected plant material"
        ],
        "prevention": [
            "Avoid prolonged leaf wetness",
            "Maintain adequate spacing",
            "Inspect plants regularly",
            "Use disease-free planting material"
        ]
    },

    "Bacterial Spot": {
        "description": "A bacterial infection that produces spots on leaves and may affect fruits.",
        "symptoms": [
            "Small dark leaf spots",
            "Yellow halos around lesions",
            "Leaf damage",
            "Fruit spotting in severe infections"
        ],
        "organic_remedies": [
            "Remove infected leaves",
            "Avoid splashing water between plants",
            "Disinfect gardening tools"
        ],
        "treatment": [
            "Remove badly infected plant material",
            "Use an appropriate bactericidal treatment when recommended"
        ],
        "prevention": [
            "Use clean seeds and seedlings",
            "Avoid handling wet plants",
            "Sanitize tools",
            "Maintain good field hygiene"
        ]
    },

    "Powdery Mildew": {
        "description": "A fungal disease characterized by powder-like growth on plant surfaces.",
        "symptoms": [
            "White powdery patches",
            "Leaf curling",
            "Yellow leaves",
            "Reduced growth"
        ],
        "organic_remedies": [
            "Apply neem oil",
            "Remove heavily infected leaves",
            "Improve airflow"
        ],
        "treatment": [
            "Apply a suitable fungicide when infection becomes severe",
            "Remove heavily affected plant parts"
        ],
        "prevention": [
            "Avoid overcrowding",
            "Provide adequate sunlight",
            "Maintain good airflow",
            "Inspect plants regularly"
        ]
    },

    "Healthy": {
        "description": "No obvious disease symptoms were identified.",
        "symptoms": [],
        "organic_remedies": [],
        "treatment": [],
        "prevention": [
            "Continue regular watering",
            "Maintain balanced nutrition",
            "Inspect the plant regularly",
            "Keep the growing area clean"
        ]
    }
}


def calculate_health_score(disease: str, confidence: float) -> int:
    """
    Simple explainable health score for UI display.
    """

    if disease.lower() == "healthy":
        return max(85, min(100, round(80 + confidence * 0.20)))

    # Higher disease confidence -> lower estimated health score.
    score = round(80 - confidence * 0.50)

    return max(20, min(80, score))


def get_disease_care(disease: str, confidence: float = 0):
    """
    Return disease-care information.

    confidence is expected as a percentage: 0-100.
    """

    clean_name = disease.replace("_", " ").strip()

    care = DISEASE_CARE.get(clean_name)

    if care is None:
        care = {
            "description":
                f"{clean_name} was detected. Detailed CareBloom guidance "
                "for this disease is being expanded.",

            "symptoms": [],

            "organic_remedies": [
                "Remove visibly damaged plant material",
                "Keep the growing area clean",
                "Avoid unnecessary moisture on leaves"
            ],

            "treatment": [
                "Monitor the plant closely",
                "Consult an agricultural expert before applying chemical treatment"
            ],

            "prevention": [
                "Inspect plants regularly",
                "Maintain proper spacing",
                "Use clean gardening tools"
            ]
        }

    return {
        "disease": clean_name,
        "health_score": calculate_health_score(
            clean_name,
            confidence
        ),
        **care
    }