"""
Basic usage example for mornGPT system with model version management.
"""

from morngpt import MornGPT

def main():
    """Demonstrate basic usage of mornGPT modules with model versions."""
    
    # Initialize mornGPT with default configuration
    morngpt = MornGPT()
    
    print("🤖 mornGPT - Multi-Module AI System (with Model Versions)")
    print("=" * 60)
    
    # Example 1: Multi-GPT Prompts (h1) with v9 (best model)
    print("\n📝 Multi-GPT Prompts Module (h1) - v9 Best Model")
    print("-" * 40)
    
    # Use h1 - Prompt Orchestration with v9
    h1_result = morngpt.process_request('h', 1, {
        'prompt': 'Explain quantum computing',
        'complexity': 'intermediate',
        'audience': 'technical'
    }, model_version=9)
    print(f"h1 Result (v9): {h1_result['orchestrated_prompt'][:100]}...")
    
    # Example 2: AI Teacher/Coach (q1) with v7 (ultimate)
    print("\n👨‍🏫 AI Teacher/Coach Module (q1) - v7 Ultimate")
    print("-" * 40)
    
    # Use q1 - Personalized Learning with v7
    q1_result = morngpt.process_request('q', 1, {
        'learning_goal': 'Master Python programming',
        'current_level': 'beginner',
        'preferred_style': 'hands-on'
    }, model_version=7)
    print(f"q1 Result (v7): {q1_result['learning_plan']['curriculum'][:100]}...")
    
    # Example 3: AI Coder (c1) with v8 (perfect)
    print("\n💻 AI Coder Module (c1) - v8 Perfect")
    print("-" * 40)
    
    # Use c1 - Code Generation with v8
    c1_result = morngpt.process_request('c', 1, {
        'requirements': 'Create a simple calculator',
        'language': 'python',
        'complexity': 'basic'
    }, model_version=8)
    print(f"c1 Result (v8): Generated {c1_result['word_count']} words of code")
    
    # Example 4: Content Generation (w1) with v9 (best)
    print("\n🎨 Content Generation Module (w1) - v9 Best")
    print("-" * 40)
    
    # Use w1 - Text Generation with v9
    w1_result = morngpt.process_request('w', 1, {
        'content_type': 'article',
        'topic': 'Artificial Intelligence',
        'length': 'medium',
        'style': 'professional'
    }, model_version=9)
    print(f"w1 Result (v9): Generated {w1_result['word_count']} words")
    
    # Example 5: Content Detection (d1) with v6 (master)
    print("\n🔍 Content Detection Module (d1) - v6 Master")
    print("-" * 40)
    
    # Use d1 - Text Detection with v6
    d1_result = morngpt.process_request('d', 1, {
        'text': 'This is a sample text for analysis',
        'method': 'comprehensive',
        'confidence': 0.8
    }, model_version=6)
    print(f"d1 Result (v6): Fake probability: {d1_result['fake_probability']:.1f}%")
    
    # Example 6: Person Matching (p1) with v5 (expert)
    print("\n👥 Person Matching Module (p1) - v5 Expert")
    print("-" * 40)
    
    # Use p1 - Person Search with v5
    p1_result = morngpt.process_request('p', 1, {
        'criteria': {'skills': ['Python', 'AI'], 'location': 'San Francisco'},
        'search_type': 'comprehensive',
        'limit': 5
    }, model_version=5)
    print(f"p1 Result (v5): Found {p1_result['total_found']} people")
    
    # Example 7: Interview/Job (b1) with v7 (ultimate)
    print("\n💼 Interview/Job Module (b1) - v7 Ultimate")
    print("-" * 40)
    
    # Use b1 - Interview Preparation with v7
    b1_result = morngpt.process_request('b', 1, {
        'position': 'Software Engineer',
        'company': 'Tech Corp',
        'interview_type': 'technical'
    }, model_version=7)
    print(f"b1 Result (v7): {len(b1_result['practice_questions'])} practice questions generated")
    
    # Example 8: Medical Advice (e1) with v8 (perfect)
    print("\n🏥 Medical Advice Module (e1) - v8 Perfect")
    print("-" * 40)
    
    # Use e1 - Symptom Analysis with v8
    e1_result = morngpt.process_request('e', 1, {
        'symptoms': ['headache', 'fever'],
        'duration': '2 days',
        'severity': 'moderate'
    }, model_version=8)
    print(f"e1 Result (v8): {e1_result['assessment']['condition']}")
    
    # Example 9: Growth Advisory (a1) with v6 (master)
    print("\n📈 Growth Advisory Module (a1) - v6 Master")
    print("-" * 40)
    
    # Use a1 - Customer Acquisition with v6
    a1_result = morngpt.process_request('a', 1, {
        'business_type': 'SaaS',
        'target_audience': 'small businesses',
        'budget': 'medium'
    }, model_version=6)
    print(f"a1 Result (v6): {len(a1_result['strategies'])} strategies recommended")
    
    # Example 10: Product Search (s1) with v5 (expert)
    print("\n🛒 Product Search Module (s1) - v5 Expert")
    print("-" * 40)
    
    # Use s1 - Product Search with v5
    s1_result = morngpt.process_request('s', 1, {
        'product': 'laptop',
        'budget': 1000,
        'preferences': ['performance', 'battery life']
    }, model_version=5)
    print(f"s1 Result (v5): Found {s1_result['total_results']} products")
    
    # Example 11: Restaurant/Food (u1) with v7 (ultimate)
    print("\n🍽️ Restaurant/Food Module (u1) - v7 Ultimate")
    print("-" * 40)
    
    # Use u1 - Restaurant Discovery with v7
    u1_result = morngpt.process_request('u', 1, {
        'location': 'San Francisco, CA',
        'radius': 3,
        'cuisine_preferences': ['Italian', 'Chinese'],
        'price_range': [2, 4]
    }, model_version=7)
    print(f"u1 Result (v7): Found {u1_result['total_found']} restaurants")
    
    # Example 12: Personalized Clothing (t1) with v6 (master)
    print("\n👗 Personalized Clothing Module (t1) - v6 Master")
    print("-" * 40)
    
    # Use t1 - Fashion Analysis with v6
    t1_result = morngpt.process_request('t', 1, {
        'photos': ['user_photo_1.jpg'],
        'style_preferences': {'casual': True},
        'body_type': 'athletic',
        'occasion': 'casual'
    }, model_version=6)
    print(f"t1 Result (v6): Style confidence: {t1_result['confidence_score']}")
    
    # Example 13: Personalized Housing (o1) with v8 (perfect)
    print("\n🏠 Personalized Housing Module (o1) - v8 Perfect")
    print("-" * 40)
    
    # Use o1 - Housing Analysis with v8
    o1_result = morngpt.process_request('o', 1, {
        'user_profile': {'income': 80000, 'family_size': 2},
        'budget': {'min': 2000, 'max': 3500},
        'location_preferences': {'city': 'San Francisco'},
        'housing_type': 'rent'
    }, model_version=8)
    print(f"o1 Result (v8): Confidence score: {o1_result['confidence_score']}")
    
    # Example 14: Personalized Traveling (r1) with v9 (best)
    print("\n✈️ Personalized Traveling Module (r1) - v9 Best")
    print("-" * 40)
    
    # Use r1 - Travel Planning with v9
    r1_result = morngpt.process_request('r', 1, {
        'destination': 'Tokyo, Japan',
        'duration': 7,
        'budget': 'medium',
        'travel_style': 'balanced',
        'interests': ['culture', 'food', 'technology']
    }, model_version=9)
    print(f"r1 Result (v9): Budget breakdown: {r1_result['budget_breakdown']['accommodation']}")
    
    # Show model version information
    print("\n📊 Model Version Summary")
    print("-" * 40)
    print("Module | Submodule | Version | Quality Level")
    print("-" * 50)
    modules_used = [
        ('h', 1, 9, 'Best'),
        ('q', 1, 7, 'Ultimate'),
        ('c', 1, 8, 'Perfect'),
        ('w', 1, 9, 'Best'),
        ('d', 1, 6, 'Master'),
        ('p', 1, 5, 'Expert'),
        ('b', 1, 7, 'Ultimate'),
        ('e', 1, 8, 'Perfect'),
        ('a', 1, 6, 'Master'),
        ('s', 1, 5, 'Expert'),
        ('u', 1, 7, 'Ultimate'),
        ('t', 1, 6, 'Master'),
        ('o', 1, 8, 'Perfect'),
        ('r', 1, 9, 'Best')
    ]
    
    for module, submodule, version, quality in modules_used:
        print(f"{module:6} | {submodule:9} | v{version:6} | {quality}")
    
    print("\n✅ Basic usage demonstration completed!")
    print("\nKey features demonstrated:")
    print("• Model version management (v1-v9)")
    print("• Different quality levels for different use cases")
    print("• All 14 modules with optimized versions")
    print("• New API with model version specification")

if __name__ == "__main__":
    main() 