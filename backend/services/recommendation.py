def get_recommendation(plant: str, disease: str):

    recommendations = {

        # =====================================================
        # TOMATO
        # =====================================================

        ("Tomato", "Target Spot"): {
            "organic_remedy": (
                "Remove infected leaves and spray neem oil regularly."
            ),
            "chemical_treatment": (
                "Use a suitable fungicide recommended for tomato fungal diseases."
            ),
            "prevention": (
                "Avoid overhead watering, improve air circulation, "
                "and remove infected plant debris."
            )
        },

        ("Tomato", "Early Blight"): {
            "organic_remedy": (
                "Remove infected lower leaves and apply neem oil or compost tea."
            ),
            "chemical_treatment": (
                "Use an appropriate fungicide after consulting an agriculture expert."
            ),
            "prevention": (
                "Rotate crops, avoid wetting leaves, and keep the growing area clean."
            )
        },

        ("Tomato", "Late Blight"): {
            "organic_remedy": (
                "Remove infected leaves and destroy severely affected plant material."
            ),
            "chemical_treatment": (
                "Use a recommended fungicide for late blight under expert guidance."
            ),
            "prevention": (
                "Avoid excess moisture, improve spacing, and monitor plants regularly."
            )
        },

        ("Tomato", "Bacterial Spot"): {
            "organic_remedy": (
                "Remove infected leaves and disinfect tools after handling plants."
            ),
            "chemical_treatment": (
                "Use a copper-based bactericide only if recommended by an expert."
            ),
            "prevention": (
                "Use disease-free seeds and avoid overhead watering."
            )
        },

        ("Tomato", "Leaf Mold"): {
            "organic_remedy": (
                "Remove affected leaves and improve ventilation around the plant."
            ),
            "chemical_treatment": (
                "Use a suitable fungicide under agriculture expert guidance."
            ),
            "prevention": (
                "Reduce humidity, avoid overcrowding, and keep leaves dry."
            )
        },

        ("Tomato", "Septoria Leaf Spot"): {
            "organic_remedy": (
                "Remove infected leaves and apply neem oil regularly."
            ),
            "chemical_treatment": (
                "Use a suitable fungicide if infection becomes severe."
            ),
            "prevention": (
                "Avoid overhead watering and remove infected plant debris."
            )
        },

        ("Tomato", "Tomato Mosaic Virus"): {
            "organic_remedy": (
                "Remove infected plants and disinfect hands and tools."
            ),
            "chemical_treatment": (
                "There is no direct chemical cure for viral infection."
            ),
            "prevention": (
                "Use healthy seedlings and avoid handling healthy plants "
                "after touching infected plants."
            )
        },

        ("Tomato", "Tomato Yellow Leaf Curl Virus"): {
            "organic_remedy": (
                "Remove badly infected plants and control whiteflies using neem spray."
            ),
            "chemical_treatment": (
                "Use an approved insecticide for whitefly control only under expert guidance."
            ),
            "prevention": (
                "Control whiteflies early and use virus-resistant varieties when available."
            )
        },

        # =====================================================
        # BELL PEPPER
        # =====================================================

        ("Bell Pepper", "Bacterial Spot"): {
            "organic_remedy": (
                "Remove infected leaves, avoid splashing water on leaves, "
                "and keep tools clean."
            ),
            "chemical_treatment": (
                "Use a copper-based bactericide only as recommended "
                "by an agriculture expert."
            ),
            "prevention": (
                "Use disease-free seeds, avoid overhead irrigation, "
                "and remove infected plant debris."
            )
        },

        ("Bell Pepper", "Healthy"): {
            "organic_remedy": (
                "No treatment is required. Continue regular plant care."
            ),
            "chemical_treatment": (
                "No chemical treatment is required."
            ),
            "prevention": (
                "Maintain proper watering, sunlight, nutrition, and routine monitoring."
            )
        },

        # =====================================================
        # BLACKGRAM
        # =====================================================

        ("Blackgram", "Yellow Mosaic"): {
            "organic_remedy": (
                "Remove severely infected plants and control whiteflies "
                "using neem-based spray."
            ),
            "chemical_treatment": (
                "Use an approved whitefly-control insecticide only under expert guidance."
            ),
            "prevention": (
                "Use resistant varieties, control whiteflies early, "
                "and remove infected plants from the field."
            )
        },

        ("Blackgram", "Healthy"): {
            "organic_remedy": (
                "No treatment is required. Continue regular plant care."
            ),
            "chemical_treatment": (
                "No chemical treatment is required."
            ),
            "prevention": (
                "Maintain healthy soil, proper irrigation, and regular field monitoring."
            )
        },

        # =====================================================
        # POTATO
        # =====================================================

        ("Potato", "Early Blight"): {
            "organic_remedy": (
                "Remove infected leaves and use neem-based spray when appropriate."
            ),
            "chemical_treatment": (
                "Use a suitable fungicide under expert guidance."
            ),
            "prevention": (
                "Rotate crops, avoid excess leaf moisture, and remove infected debris."
            )
        },

        ("Potato", "Late Blight"): {
            "organic_remedy": (
                "Remove infected foliage and destroy heavily infected plant material."
            ),
            "chemical_treatment": (
                "Use an approved fungicide for late blight under expert supervision."
            ),
            "prevention": (
                "Avoid prolonged wet conditions and use healthy planting material."
            )
        },

        ("Potato", "Healthy"): {
            "organic_remedy": (
                "No treatment is required."
            ),
            "chemical_treatment": (
                "No chemical treatment is required."
            ),
            "prevention": (
                "Maintain good drainage, balanced nutrition, and routine crop monitoring."
            )
        },

        # =====================================================
        # WHEAT
        # =====================================================

        ("Wheat", "Leaf Rust"): {
            "organic_remedy": (
                "Remove severely infected leaves where practical and improve field sanitation."
            ),
            "chemical_treatment": (
                "Use a recommended fungicide for rust only under expert advice."
            ),
            "prevention": (
                "Use resistant varieties and avoid excessive nitrogen fertilizer."
            )
        },

        ("Wheat", "Stem Rust"): {
            "organic_remedy": (
                "Remove heavily infected crop residue after harvest."
            ),
            "chemical_treatment": (
                "Use a recommended fungicide if disease pressure is high."
            ),
            "prevention": (
                "Plant resistant varieties and monitor fields regularly."
            )
        },

        ("Wheat", "Stripe Rust"): {
            "organic_remedy": (
                "Remove heavily infected leaves where practical and maintain field sanitation."
            ),
            "chemical_treatment": (
                "Use a suitable fungicide under agriculture expert guidance."
            ),
            "prevention": (
                "Grow resistant varieties and monitor during cool, humid conditions."
            )
        },

        ("Wheat", "Powdery Mildew"): {
            "organic_remedy": (
                "Improve airflow and remove heavily infected plant material."
            ),
            "chemical_treatment": (
                "Use a suitable fungicide when infection becomes severe."
            ),
            "prevention": (
                "Avoid overcrowding and excessive nitrogen application."
            )
        },

        ("Wheat", "Septoria Blotch"): {
            "organic_remedy": (
                "Remove infected crop residue and maintain good field sanitation."
            ),
            "chemical_treatment": (
                "Use an approved fungicide under expert guidance."
            ),
            "prevention": (
                "Rotate crops and use healthy seed material."
            )
        },

        ("Wheat", "Loose Smut"): {
            "organic_remedy": (
                "Remove infected seed heads before spores spread."
            ),
            "chemical_treatment": (
                "Use properly treated certified seed for future planting."
            ),
            "prevention": (
                "Use certified disease-free seed and resistant varieties."
            )
        },

        # =====================================================
        # ZUCCHINI
        # =====================================================

        ("Zucchini", "Powdery Mildew"): {
            "organic_remedy": (
                "Remove badly infected leaves and use neem oil where appropriate."
            ),
            "chemical_treatment": (
                "Use a recommended fungicide for powdery mildew if necessary."
            ),
            "prevention": (
                "Improve air circulation, avoid overcrowding, and monitor humidity."
            )
        }
    }

    # =========================================================
    # HEALTHY CLASS FALLBACK
    # =========================================================

    if "healthy" in disease.lower():
        return {
            "organic_remedy": (
                "No treatment is required. The plant appears healthy."
            ),
            "chemical_treatment": (
                "No chemical treatment is required."
            ),
            "prevention": (
                "Continue proper watering, balanced nutrition, "
                "good sunlight, and regular monitoring."
            )
        }

    # =========================================================
    # LOOK FOR EXACT DISEASE RECOMMENDATION
    # =========================================================

    recommendation = recommendations.get((plant, disease))

    if recommendation:
        return recommendation

    disease_lower = disease.lower()

    if "bacterial" in disease_lower:
        return {
            "organic_remedy": "Remove infected leaves and keep tools clean.",
            "chemical_treatment": "Use a suitable bactericide only with expert guidance.",
            "prevention": "Avoid overhead watering and use disease-free planting material."
        }

    if any(word in disease_lower for word in [
        "rust",
        "blight",
        "mildew",
        "spot",
        "rot"
    ]):
        return {
            "organic_remedy": "Remove infected leaves and keep the plant area clean.",
            "chemical_treatment": "Use a suitable fungicide only with expert guidance.",
            "prevention": "Avoid excess moisture and improve air circulation."
        }

    if any(word in disease_lower for word in [
        "virus",
        "mosaic",
        "tungro"
    ]):
        return {
            "organic_remedy": "Remove severely infected plants and control insect vectors.",
            "chemical_treatment": "There is no direct chemical cure for viral diseases.",
            "prevention": "Use healthy planting material and control insect vectors."
        }
        # Pest-related diseases
    if any(word in disease_lower for word in [
        "pest", "hispa", "mites", "beetle"
    ]):
        return {
            "organic_remedy": "Remove heavily affected leaves and use neem-based pest control.",
            "chemical_treatment": "Use an approved insecticide only under expert guidance.",
            "prevention": "Inspect plants regularly and control insect pests early."
        }

    # Wilt / Dead Heart
    if any(word in disease_lower for word in [
        "wilt", "dead heart"
    ]):
        return {
            "organic_remedy": "Remove severely affected plant parts and maintain good field hygiene.",
            "chemical_treatment": "Use suitable treatment only after confirming the cause with an agriculture expert.",
            "prevention": "Use healthy planting material and avoid waterlogging."
        }

    # Nutrition deficiency
    if "nutrition deficiency" in disease_lower:
        return {
            "organic_remedy": "Apply well-decomposed compost and maintain balanced soil nutrition.",
            "chemical_treatment": "Use balanced fertilizer based on soil-test recommendations.",
            "prevention": "Perform regular soil testing and maintain balanced nutrients."
        }

    # Smut / Blast
    if any(word in disease_lower for word in [
        "smut", "blast"
    ]):
        return {
            "organic_remedy": "Remove infected plant parts and keep the field clean.",
            "chemical_treatment": "Use an approved fungicide or seed treatment under expert guidance.",
            "prevention": "Use disease-free seed and resistant varieties where available."
        }

    # Leaf Curl / Leaf Crinkle / Bunchy Top
    if any(word in disease_lower for word in [
        "leaf curl", "leaf crinkle", "bunchy top"
    ]):
        return {
            "organic_remedy": "Remove severely infected plants and control insect vectors.",
            "chemical_treatment": "There is usually no direct chemical cure; control insect vectors under expert guidance.",
            "prevention": "Use healthy planting material and control vector insects early."
        }

    return {
        "organic_remedy": "Remove affected leaves and keep the plant area clean.",
        "chemical_treatment": "Consult an agriculture expert before applying any chemical treatment.",
        "prevention": "Maintain proper watering, spacing, field hygiene, and regular disease monitoring."
    }