"""
Personalized Clothing module example demonstrating fashion advice and shopping integration.
"""

from morngpt import MornGPT

def main():
    """Demonstrate the personalized clothing module capabilities."""
    
    # Initialize mornGPT
    morngpt = MornGPT()
    
    print("👗 mornGPT Personalized Clothing Module Demo")
    print("=" * 50)
    
    # Example 1: Fashion Analysis (t1)
    print("\n📸 Fashion Analysis (t1)")
    print("-" * 30)
    
    t1_result = morngpt.personalized_clothing.get_submodule(1).process({
        'photos': ['user_photo_1.jpg', 'user_photo_2.jpg'],
        'style_preferences': {'casual': True, 'professional': False},
        'body_type': 'athletic',
        'occasion': 'casual'
    })
    
    analysis = t1_result['analysis']
    print(f"Current style: {analysis['current_style']}")
    print(f"Color palette: {', '.join(analysis['color_palette'])}")
    print(f"Confidence score: {t1_result['confidence_score']}")
    
    # Example 2: Outfit Recommendations (t2)
    print("\n👕 Outfit Recommendations (t2)")
    print("-" * 30)
    
    t2_result = morngpt.personalized_clothing.get_submodule(2).process({
        'occasion': 'professional',
        'weather': 'moderate',
        'budget': 'medium',
        'style': 'modern'
    })
    
    outfits = t2_result['outfits']
    print(f"Generated {len(outfits)} outfit recommendations")
    for i, outfit in enumerate(outfits[:2]):
        print(f"  {i+1}. {outfit['top']} + {outfit['bottom']} + {outfit['shoes']}")
    
    # Example 3: Style Consultation (t3)
    print("\n💼 Style Consultation (t3)")
    print("-" * 30)
    
    t3_result = morngpt.personalized_clothing.get_submodule(3).process({
        'type': 'wardrobe_audit',
        'goals': ['professional look', 'versatile pieces'],
        'current_wardrobe': ['jeans', 't-shirts', 'sneakers']
    })
    
    consultation = t3_result['consultation_results']
    print(f"Wardrobe gaps: {', '.join(consultation['wardrobe_gaps'][:3])}")
    print(f"Investment pieces: {', '.join(consultation['investment_pieces'][:3])}")
    
    # Example 4: Shopping Assistance (t4)
    print("\n🛍️ Shopping Assistance (t4)")
    print("-" * 30)
    
    t4_result = morngpt.personalized_clothing.get_submodule(4).process({
        'item_type': 'tops',
        'budget_range': [50, 200],
        'preferred_brands': ['Everlane', 'Madewell'],
        'size_preferences': {'tops': 'M', 'bottoms': '28'}
    })
    
    items = t4_result['recommended_items']
    print(f"Found {len(items)} recommended items")
    for i, item in enumerate(items[:2]):
        print(f"  {i+1}. {item['name']} by {item['brand']} - ${item['price']}")
    
    # Example 5: Trend Analysis (t5)
    print("\n📈 Trend Analysis (t5)")
    print("-" * 30)
    
    t5_result = morngpt.personalized_clothing.get_submodule(5).process({
        'season': 'current',
        'category': 'all',
        'location': 'global'
    })
    
    trends = t5_result['current_trends']
    print(f"Current colors: {', '.join(trends['colors'])}")
    print(f"Popular patterns: {', '.join(trends['patterns'])}")
    
    # Example 6: Fit Optimization (t6)
    print("\n📏 Fit Optimization (t6)")
    print("-" * 30)
    
    t6_result = morngpt.personalized_clothing.get_submodule(6).process({
        'measurements': {'chest': 40, 'waist': 32, 'hips': 38},
        'fit_issues': ['wide shoulders', 'narrow waist'],
        'preferred_fit': 'comfortable'
    })
    
    fit_analysis = t6_result['fit_analysis']
    print(f"Body proportions: {fit_analysis['body_proportions']}")
    print(f"Recommended top fit: {fit_analysis['recommended_fits']['tops']}")
    
    # Example 7: Accessory Styling (t7)
    print("\n💍 Accessory Styling (t7)")
    print("-" * 30)
    
    t7_result = morngpt.personalized_clothing.get_submodule(7).process({
        'outfit': {'top': 'White blouse', 'bottom': 'Black pants'},
        'occasion': 'professional',
        'budget': 'medium',
        'style': 'minimalist'
    })
    
    accessories = t7_result['accessory_recommendations']
    print("Jewelry recommendations:")
    for jewelry in accessories['jewelry'][:2]:
        print(f"  {jewelry['type']}: {jewelry['style']} - {jewelry['price_range']}")
    
    # Example 8: Seasonal Wardrobe (t8)
    print("\n🌤️ Seasonal Wardrobe (t8)")
    print("-" * 30)
    
    t8_result = morngpt.personalized_clothing.get_submodule(8).process({
        'season': 'spring',
        'climate': 'temperate',
        'lifestyle': 'professional'
    })
    
    wardrobe = t8_result['seasonal_wardrobe']
    print(f"Spring essentials: {', '.join(wardrobe['essentials'][:3])}")
    print(f"Spring colors: {', '.join(wardrobe['colors'])}")
    
    # Example 9: Shopping Integration (t9)
    print("\n🔗 Shopping Integration (t9)")
    print("-" * 30)
    
    t9_result = morngpt.personalized_clothing.get_submodule(9).process({
        'items': ['white button-down', 'high-waisted jeans'],
        'platforms': ['amazon', 'nordstrom', 'revolve'],
        'budget': {'min': 50, 'max': 200},
        'location': 'US'
    })
    
    platforms = t9_result['shopping_platforms']
    print("Platform availability:")
    for platform, data in platforms['hotels'].items():
        print(f"  {platform}: {'✅' if data['availability'] else '❌'}")
    
    print("\n✅ Personalized Clothing module demonstration completed!")
    print("\nKey features demonstrated:")
    print("• Fashion analysis from user photos")
    print("• Personalized outfit recommendations")
    print("• Style consultation and wardrobe planning")
    print("• Shopping assistance with product recommendations")
    print("• Trend analysis and forecasting")
    print("• Fit optimization and sizing advice")
    print("• Accessory styling recommendations")
    print("• Seasonal wardrobe planning")
    print("• Multi-platform shopping integration")

if __name__ == "__main__":
    main() 