# components/city_kpi_data.py

def get_kpis_for_city(city):
    sample_data = {
        "Pune": {
            "Air Quality Index": 42,
            "Renewable Energy Usage": "70%",
            "Waste Recycling Rate": "45%",
            "Water Conservation Score": 78,
            "Energy Efficiency Score": 85,
            "Green Space Coverage": "25%"
        },
        "Hyderabad": {
            "Air Quality Index": 60,
            "Renewable Energy Usage": "50%",
            "Waste Recycling Rate": "38%",
            "Water Conservation Score": 65,
            "Energy Efficiency Score": 75,
            "Green Space Coverage": "18%"
        },
        "Chennai": {
            "Air Quality Index": 55,
            "Renewable Energy Usage": "60%",
            "Waste Recycling Rate": "42%",
            "Water Conservation Score": 72,
            "Energy Efficiency Score": 78,
            "Green Space Coverage": "22%"
        },
        "Delhi": {
            "Air Quality Index": 150,
            "Renewable Energy Usage": "30%",
            "Waste Recycling Rate": "25%",
            "Water Conservation Score": 60,
            "Energy Efficiency Score": 65,
            "Green Space Coverage": "12%"
        },
        "Bangalore": {
            "Air Quality Index": 48,
            "Renewable Energy Usage": "68%",
            "Waste Recycling Rate": "50%",
            "Water Conservation Score": 82,
            "Energy Efficiency Score": 88,
            "Green Space Coverage": "28%"
        }
    }

    return sample_data.get(city)
