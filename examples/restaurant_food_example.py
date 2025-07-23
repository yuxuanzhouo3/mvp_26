"""
Restaurant/Food module example demonstrating restaurant discovery and food recommendations.
"""

from morngpt import MornGPT

def main():
    """Demonstrate the restaurant/food module capabilities."""
    
    # Initialize mornGPT
    morngpt = MornGPT()
    
    print("🍽️ mornGPT Restaurant/Food Module Demo")
    print("=" * 50)
    
    # Example 1: Restaurant Discovery (u1)
    print("\n📍 Restaurant Discovery (u1)")
    print("-" * 30)
    
    u1_result = morngpt.restaurant_food.get_submodule(1).process({
        'location': 'San Francisco, CA',
        'radius': 3,
        'cuisine_preferences': ['Italian', 'Chinese', 'Mexican'],
        'price_range': [2, 4]
    })
    
    print(f"Found {u1_result['total_found']} restaurants")
    for i, restaurant in enumerate(u1_result['restaurants'][:3]):
        print(f"  {i+1}. {restaurant['name']} - {restaurant['cuisine']} (${restaurant['price_level']})")
    
    # Example 2: Food Recommendations (u2)
    print("\n🍕 Food Recommendations (u2)")
    print("-" * 30)
    
    u2_result = morngpt.restaurant_food.get_submodule(2).process({
        'user_preferences': {'spicy': 'medium', 'healthy': True},
        'dietary_restrictions': ['vegetarian'],
        'cuisine_type': 'Italian',
        'meal_type': 'dinner'
    })
    
    print(f"Generated {len(u2_result['recommendations'])} food recommendations")
    for i, rec in enumerate(u2_result['recommendations'][:3]):
        print(f"  {i+1}. {rec['dish_name']} - {rec['calories']} cal, ${rec['price']}")
    
    # Example 3: Order Management (u3)
    print("\n📱 Order Management (u3)")
    print("-" * 30)
    
    u3_result = morngpt.restaurant_food.get_submodule(3).process({
        'restaurant_id': 'restaurant_1',
        'order_items': [
            {'name': 'Margherita Pizza', 'price': 18},
            {'name': 'Caesar Salad', 'price': 14}
        ],
        'delivery_apps': ['uber_eats', 'doordash', 'grubhub']
    })
    
    print(f"Found {len(u3_result['order_options'])} delivery options")
    best_option = u3_result['best_option']
    print(f"Best option: {best_option['recommended_app']} - ${best_option['order_details']['total_cost']:.2f}")
    
    # Example 4: App Integration (u4)
    print("\n🔗 App Integration (u4)")
    print("-" * 30)
    
    u4_result = morngpt.restaurant_food.get_submodule(4).process({
        'apps': ['uber_eats', 'doordash', 'grubhub'],
        'integration_type': 'order_links'
    })
    
    print("App integration status:")
    for app, data in u4_result['integration_data'].items():
        print(f"  {data['display_name']}: {'✅' if data['api_available'] else '❌'}")
    
    # Example 5: Popularity Ranking (u5)
    print("\n🏆 Popularity Ranking (u5)")
    print("-" * 30)
    
    u5_result = morngpt.restaurant_food.get_submodule(5).process({
        'criteria': ['reviews', 'orders', 'ratings'],
        'location': 'San Francisco',
        'cuisine_filter': ''
    })
    
    print("Top 3 restaurants by popularity:")
    for i, restaurant in enumerate(u5_result['popularity_rankings'][:3]):
        print(f"  {restaurant['rank']}. {restaurant['name']} - Score: {restaurant['popularity_score']}")
    
    # Example 6: Menu Analysis (u6)
    print("\n📋 Menu Analysis (u6)")
    print("-" * 30)
    
    u6_result = morngpt.restaurant_food.get_submodule(6).process({
        'restaurant_id': 'pizza_palace',
        'focus': 'comprehensive'
    })
    
    analysis = u6_result['menu_analysis']
    print(f"Menu has {analysis['total_items']} items")
    print(f"Price range: {analysis['price_range']}")
    print(f"Average price: ${analysis['average_price']:.2f}")
    
    # Example 7: Delivery Optimization (u7)
    print("\n🚚 Delivery Optimization (u7)")
    print("-" * 30)
    
    u7_result = morngpt.restaurant_food.get_submodule(7).process({
        'delivery_address': '123 Main St, San Francisco, CA',
        'restaurant_locations': [
            {'name': 'Restaurant A', 'distance': 0.8},
            {'name': 'Restaurant B', 'distance': 1.2}
        ],
        'preferences': {'speed': 'fast', 'cost': 'reasonable'}
    })
    
    optimization = u7_result['delivery_optimization']
    print(f"Fastest delivery: {optimization['estimated_delivery_times']['fastest']}")
    print(f"Delivery fee range: ${optimization['delivery_fees']['minimum']} - ${optimization['delivery_fees']['maximum']}")
    
    # Example 8: Cuisine Specialization (u8)
    print("\n👨‍🍳 Cuisine Specialization (u8)")
    print("-" * 30)
    
    u8_result = morngpt.restaurant_food.get_submodule(8).process({
        'cuisine_type': 'Italian',
        'expertise_level': 'intermediate'
    })
    
    specialization = u8_result['cuisine_specialization']
    print(f"Signature dishes: {', '.join(specialization['signature_dishes'][:3])}")
    print(f"Authentic ingredients: {', '.join(specialization['authentic_ingredients'][:3])}")
    
    # Example 9: Food Trends (u9)
    print("\n📈 Food Trends (u9)")
    print("-" * 30)
    
    u9_result = morngpt.restaurant_food.get_submodule(9).process({
        'period': '6 months',
        'location': 'San Francisco',
        'focus': 'cuisine'
    })
    
    trends = u9_result['food_trends']
    print("Top trending cuisines:")
    for cuisine in trends['top_trending_cuisines'][:3]:
        print(f"  {cuisine['cuisine']}: {cuisine['growth_rate']}")
    
    print("\n✅ Restaurant/Food module demonstration completed!")
    print("\nKey features demonstrated:")
    print("• Restaurant discovery with location-based search")
    print("• Personalized food recommendations")
    print("• Multi-app order management")
    print("• Popularity rankings and trends")
    print("• Delivery optimization")
    print("• Cuisine expertise and menu analysis")

if __name__ == "__main__":
    main() 