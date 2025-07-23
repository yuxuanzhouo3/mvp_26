"""
Personalized Traveling module example demonstrating travel planning and cultural insights.
"""

from morngpt import MornGPT

def main():
    """Demonstrate the personalized traveling module capabilities."""
    
    # Initialize mornGPT
    morngpt = MornGPT()
    
    print("✈️ mornGPT Personalized Traveling Module Demo")
    print("=" * 50)
    
    # Example 1: Travel Planning (r1)
    print("\n🗺️ Travel Planning (r1)")
    print("-" * 30)
    
    r1_result = morngpt.personalized_traveling.get_submodule(1).process({
        'destination': 'Tokyo, Japan',
        'duration': 7,
        'budget': 'medium',
        'travel_style': 'balanced',
        'interests': ['culture', 'food', 'technology']
    })
    
    itinerary = r1_result['travel_itinerary']
    print(f"Day 1: {itinerary['day_1']['morning']}")
    print(f"Budget breakdown: {r1_result['budget_breakdown']['accommodation']}")
    
    # Example 2: Transportation Advice (r2)
    print("\n🚗 Transportation Advice (r2)")
    print("-" * 30)
    
    r2_result = morngpt.personalized_traveling.get_submodule(2).process({
        'origin': 'San Francisco, CA',
        'destination': 'New York, NY',
        'date': '2024-07-15',
        'passengers': 2,
        'preferences': {'speed': 'fast', 'cost': 'reasonable'}
    })
    
    options = r2_result['transportation_options']
    print(f"Found {len(options)} transportation options")
    for i, option in enumerate(options[:2]):
        print(f"  {i+1}. {option['mode']}: {option['duration']}, ${option['cost']}")
    
    # Example 3: Cultural Insights (r3)
    print("\n🌍 Cultural Insights (r3)")
    print("-" * 30)
    
    r3_result = morngpt.personalized_traveling.get_submodule(3).process({
        'destination': 'Paris, France',
        'focus_areas': ['customs', 'food', 'language']
    })
    
    culture = r3_result['cultural_overview']
    print(f"Primary language: {culture['language']['primary']}")
    print(f"Greeting custom: {culture['customs']['greetings']}")
    
    # Example 4: Accommodation Booking (r4)
    print("\n🏨 Accommodation Booking (r4)")
    print("-" * 30)
    
    r4_result = morngpt.personalized_traveling.get_submodule(4).process({
        'destination': 'Barcelona, Spain',
        'dates': {'check_in': '2024-09-01', 'check_out': '2024-09-05'},
        'guests': 2,
        'budget': 'medium',
        'preferences': {'location': 'city center', 'amenities': ['wifi', 'breakfast']}
    })
    
    accommodations = r4_result['accommodation_options']
    print(f"Found {len(accommodations)} accommodation options")
    for i, acc in enumerate(accommodations[:2]):
        print(f"  {i+1}. {acc['name']} - ${acc['price_per_night']}/night, Rating: {acc['rating']}")
    
    # Example 5: Local Attractions (r5)
    print("\n🎯 Local Attractions (r5)")
    print("-" * 30)
    
    r5_result = morngpt.personalized_traveling.get_submodule(5).process({
        'destination': 'Rome, Italy',
        'interests': ['history', 'art', 'food'],
        'duration': 4,
        'budget': 'medium'
    })
    
    attractions = r5_result['top_attractions']
    print(f"Found {len(attractions)} top attractions")
    for i, attraction in enumerate(attractions[:2]):
        print(f"  {i+1}. {attraction['name']} - {attraction['duration']}, ${attraction['cost']}")
    
    # Example 6: Travel Insurance (r6)
    print("\n🛡️ Travel Insurance (r6)")
    print("-" * 30)
    
    r6_result = morngpt.personalized_traveling.get_submodule(6).process({
        'trip_details': {'destination': 'Thailand', 'duration': 14},
        'destination': 'Thailand',
        'duration': 14,
        'activities': ['beach', 'temple_visits', 'street_food'],
        'travelers': 2
    })
    
    insurance = r6_result['insurance_recommendations']
    print(f"Found {len(insurance)} insurance options")
    for i, plan in enumerate(insurance[:2]):
        print(f"  {i+1}. {plan['provider']} - ${plan['cost']}, Rating: {plan['rating']}")
    
    # Example 7: Packing Guidance (r7)
    print("\n🧳 Packing Guidance (r7)")
    print("-" * 30)
    
    r7_result = morngpt.personalized_traveling.get_submodule(7).process({
        'destination': 'London, UK',
        'duration': 10,
        'climate': 'temperate',
        'activities': ['sightseeing', 'museums', 'dining'],
        'luggage_type': 'checked'
    })
    
    checklist = r7_result['packing_checklist']
    print("Clothing essentials:")
    for item in checklist['clothing'][:3]:
        print(f"  • {item}")
    
    # Example 8: Safety Advice (r8)
    print("\n🛡️ Safety Advice (r8)")
    print("-" * 30)
    
    r8_result = morngpt.personalized_traveling.get_submodule(8).process({
        'destination': 'Mexico City, Mexico',
        'travel_type': 'leisure',
        'solo_travel': False
    })
    
    safety = r8_result['safety_overview']
    print(f"Overall safety: {safety['overall_safety']}")
    print(f"Crime level: {safety['crime_level']}")
    
    # Example 9: Travel Integration (r9)
    print("\n🔗 Travel Integration (r9)")
    print("-" * 30)
    
    r9_result = morngpt.personalized_traveling.get_submodule(9).process({
        'type': 'flights',
        'destination': 'Tokyo, Japan',
        'dates': {'departure': '2024-10-01', 'return': '2024-10-08'}
    })
    
    platforms = r9_result['platform_integration']
    print("Flight platform features:")
    for platform, features in platforms['flights'].items():
        print(f"  {platform}: {'✅' if features['availability'] else '❌'} available")
    
    print("\n✅ Personalized Traveling module demonstration completed!")
    print("\nKey features demonstrated:")
    print("• Personalized travel itineraries and planning")
    print("• Transportation recommendations from A to B")
    print("• Cultural insights and local customs")
    print("• Accommodation recommendations and booking")
    print("• Local attractions and must-see destinations")
    print("• Travel insurance advice and recommendations")
    print("• Packing guidance and checklists")
    print("• Travel safety advice and emergency info")
    print("• Multi-platform travel integration")

if __name__ == "__main__":
    main() 