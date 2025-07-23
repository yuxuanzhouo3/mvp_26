"""
Personalized Housing module example demonstrating hotel, rental, and real estate advice.
"""

from morngpt import MornGPT

def main():
    """Demonstrate the personalized housing module capabilities."""
    
    # Initialize mornGPT
    morngpt = MornGPT()
    
    print("🏠 mornGPT Personalized Housing Module Demo")
    print("=" * 50)
    
    # Example 1: Housing Analysis (o1)
    print("\n📊 Housing Analysis (o1)")
    print("-" * 30)
    
    o1_result = morngpt.personalized_housing.get_submodule(1).process({
        'user_profile': {'income': 80000, 'family_size': 2},
        'budget': {'min': 2000, 'max': 3500},
        'location_preferences': {'city': 'San Francisco', 'neighborhood': 'downtown'},
        'housing_type': 'rent'
    })
    
    analysis = o1_result['housing_analysis']
    print(f"Recommended type: {analysis['recommended_type']}")
    print(f"Affordable range: {analysis['budget_analysis']['affordable_range']}")
    print(f"Confidence score: {o1_result['confidence_score']}")
    
    # Example 2: Hotel Recommendations (o2)
    print("\n🏨 Hotel Recommendations (o2)")
    print("-" * 30)
    
    o2_result = morngpt.personalized_housing.get_submodule(2).process({
        'destination': 'New York City',
        'dates': {'check_in': '2024-06-15', 'check_out': '2024-06-18'},
        'budget': 'medium',
        'preferences': {'location': 'downtown', 'amenities': ['gym', 'restaurant']},
        'travelers': 2
    })
    
    hotels = o2_result['hotel_recommendations']
    print(f"Found {len(hotels)} hotel recommendations")
    for i, hotel in enumerate(hotels[:2]):
        print(f"  {i+1}. {hotel['name']} - ${hotel['price_per_night']}/night, Rating: {hotel['rating']}")
    
    # Example 3: Rental Search (o3)
    print("\n🔍 Rental Search (o3)")
    print("-" * 30)
    
    o3_result = morngpt.personalized_housing.get_submodule(3).process({
        'location': 'Austin, TX',
        'budget': {'min': 1500, 'max': 2500},
        'property_type': 'apartment',
        'bedrooms': 2,
        'move_in_date': '2024-07-01'
    })
    
    properties = o3_result['rental_properties']
    print(f"Found {len(properties)} rental properties")
    for i, prop in enumerate(properties[:2]):
        print(f"  {i+1}. {prop['address']} - ${prop['monthly_rent']}/month, {prop['bedrooms']}BR")
    
    # Example 4: Real Estate Advice (o4)
    print("\n🏡 Real Estate Advice (o4)")
    print("-" * 30)
    
    o4_result = morngpt.personalized_housing.get_submodule(4).process({
        'location': 'Denver, CO',
        'budget': {'min': 400000, 'max': 600000},
        'property_type': 'single_family',
        'timeline': '6-12 months'
    })
    
    market = o4_result['market_analysis']
    print(f"Current market: {market['current_market']}")
    print(f"Average price: ${market['average_price']:,}")
    print(f"Price trend: {market['price_trend']}")
    
    # Example 5: Neighborhood Research (o5)
    print("\n🏘️ Neighborhood Research (o5)")
    print("-" * 30)
    
    o5_result = morngpt.personalized_housing.get_submodule(5).process({
        'neighborhoods': ['downtown', 'suburbs', 'midtown'],
        'criteria': ['safety', 'schools', 'amenities']
    })
    
    neighborhoods = o5_result['neighborhood_analysis']
    for name, data in neighborhoods.items():
        print(f"{name.title()}: Score {data['overall_score']}, Safety {data['safety_rating']}")
    
    # Example 6: Financing Guidance (o6)
    print("\n💰 Financing Guidance (o6)")
    print("-" * 30)
    
    o6_result = morngpt.personalized_housing.get_submodule(6).process({
        'purchase_price': 450000,
        'down_payment': 90000,
        'credit_score': 750,
        'income': 85000
    })
    
    financing = o6_result['financing_analysis']
    print(f"Loan amount: ${financing['loan_amount']:,}")
    print(f"Down payment percentage: {financing['down_payment_percentage']:.1f}%")
    print(f"Affordability score: {financing['affordability_score']}")
    
    # Example 7: Property Inspection (o7)
    print("\n🔍 Property Inspection (o7)")
    print("-" * 30)
    
    o7_result = morngpt.personalized_housing.get_submodule(7).process({
        'property_type': 'single_family',
        'age': 15,
        'size': 2000
    })
    
    inspection = o7_result['inspection_checklist']
    print("Structural inspection items:")
    for item in inspection['structural'][:3]:
        print(f"  • {item}")
    
    # Example 8: Moving Planning (o8)
    print("\n📦 Moving Planning (o8)")
    print("-" * 30)
    
    o8_result = morngpt.personalized_housing.get_submodule(8).process({
        'move_type': 'local',
        'distance': 25,
        'household_size': 3,
        'timeline': '1 month'
    })
    
    timeline = o8_result['moving_timeline']
    print("8 weeks before move:")
    for task in timeline['8_weeks_before'][:3]:
        print(f"  • {task}")
    
    # Example 9: Housing Integration (o9)
    print("\n🔗 Housing Integration (o9)")
    print("-" * 30)
    
    o9_result = morngpt.personalized_housing.get_submodule(9).process({
        'type': 'hotels',
        'location': 'Los Angeles',
        'dates': {'check_in': '2024-08-01', 'check_out': '2024-08-05'}
    })
    
    platforms = o9_result['platform_integration']
    print("Hotel platform features:")
    for platform, features in platforms['hotels'].items():
        print(f"  {platform}: {'✅' if features['availability'] else '❌'} available")
    
    print("\n✅ Personalized Housing module demonstration completed!")
    print("\nKey features demonstrated:")
    print("• Housing needs analysis and recommendations")
    print("• Hotel recommendations with booking links")
    print("• Rental property search and evaluation")
    print("• Real estate market analysis and advice")
    print("• Neighborhood research and comparison")
    print("• Mortgage and financing guidance")
    print("• Property inspection checklists")
    print("• Moving planning and logistics")
    print("• Multi-platform housing integration")

if __name__ == "__main__":
    main() 