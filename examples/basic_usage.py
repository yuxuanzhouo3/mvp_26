"""
Basic usage example for mornGPT system.
"""

from morngpt import MornGPT

def main():
    """Demonstrate basic usage of mornGPT modules."""
    
    # Initialize mornGPT with default configuration
    morngpt = MornGPT()
    
    print("🤖 mornGPT - Multi-Module AI System")
    print("=" * 50)
    
    # Example 1: Multi-GPT Prompts (h1-h9)
    print("\n📝 Multi-GPT Prompts Module (h1-h9)")
    print("-" * 30)
    
    # Use h1 - Prompt Orchestration
    h1_result = morngpt.multi_gpt.get_submodule(1).process({
        'prompt': 'Explain quantum computing',
        'complexity': 'intermediate',
        'audience': 'technical'
    })
    print(f"h1 Result: {h1_result['orchestrated_prompt'][:100]}...")
    
    # Example 2: AI Teacher/Coach (q1-q9)
    print("\n👨‍🏫 AI Teacher/Coach Module (q1-q9)")
    print("-" * 30)
    
    # Use q1 - Personalized Learning
    q1_result = morngpt.teacher_coach.get_submodule(1).process({
        'learning_goal': 'Master Python programming',
        'current_level': 'beginner',
        'preferred_style': 'hands-on'
    })
    print(f"q1 Result: {q1_result['learning_plan']['curriculum'][:100]}...")
    
    # Example 3: AI Coder (c1-c9)
    print("\n💻 AI Coder Module (c1-c9)")
    print("-" * 30)
    
    # Use c1 - Code Generation
    c1_result = morngpt.coder.get_submodule(1).process({
        'requirements': 'Create a simple calculator',
        'language': 'python',
        'complexity': 'basic'
    })
    print(f"c1 Result: Generated {c1_result['word_count']} words of code")
    
    # Example 4: Content Generation (w1-w9)
    print("\n🎨 Content Generation Module (w1-w9)")
    print("-" * 30)
    
    # Use w1 - Text Generation
    w1_result = morngpt.content_generation.get_submodule(1).process({
        'content_type': 'article',
        'topic': 'Artificial Intelligence',
        'length': 'medium',
        'style': 'professional'
    })
    print(f"w1 Result: Generated {w1_result['word_count']} words")
    
    # Example 5: Content Detection (d1-d9)
    print("\n🔍 Content Detection Module (d1-d9)")
    print("-" * 30)
    
    # Use d1 - Text Detection
    d1_result = morngpt.content_detection.get_submodule(1).process({
        'text': 'This is a sample text for analysis',
        'method': 'comprehensive',
        'confidence': 0.8
    })
    print(f"d1 Result: Fake probability: {d1_result['fake_probability']:.1f}%")
    
    # Example 6: Person Matching (p1-p9)
    print("\n👥 Person Matching Module (p1-p9)")
    print("-" * 30)
    
    # Use p1 - Person Search
    p1_result = morngpt.person_matching.get_submodule(1).process({
        'criteria': {'skills': ['Python', 'AI'], 'location': 'San Francisco'},
        'search_type': 'comprehensive',
        'limit': 5
    })
    print(f"p1 Result: Found {p1_result['total_found']} people")
    
    # Example 7: Interview/Job (b1-b9)
    print("\n💼 Interview/Job Module (b1-b9)")
    print("-" * 30)
    
    # Use b1 - Interview Preparation
    b1_result = morngpt.interview_job.get_submodule(1).process({
        'position': 'Software Engineer',
        'company': 'Tech Corp',
        'interview_type': 'technical'
    })
    print(f"b1 Result: {len(b1_result['practice_questions'])} practice questions generated")
    
    # Example 8: Medical Advice (e1-e9)
    print("\n🏥 Medical Advice Module (e1-e9)")
    print("-" * 30)
    
    # Use e1 - Symptom Analysis
    e1_result = morngpt.medical_advice.get_submodule(1).process({
        'symptoms': ['headache', 'fatigue'],
        'duration': '2 days',
        'severity': 'mild'
    })
    print(f"e1 Result: Urgency level: {e1_result['urgency_level']}")
    
    # Example 9: Growth Advisory (a1-a9)
    print("\n📈 Growth Advisory Module (a1-a9)")
    print("-" * 30)
    
    # Use a1 - Customer Acquisition
    a1_result = morngpt.growth_advisory.get_submodule(1).process({
        'business_type': 'SaaS',
        'target_audience': {'age': '25-40', 'interests': ['technology']},
        'budget': 'medium'
    })
    print(f"a1 Result: Expected {a1_result['acquisition_strategy']['expected_outcomes']}")
    
    # Example 10: Product Search (s1-s9)
    print("\n🛍️ Product Search Module (s1-s9)")
    print("-" * 30)
    
    # Use s1 - Product Search
    s1_result = morngpt.product_search.get_submodule(1).process({
        'query': 'laptop',
        'category': 'electronics',
        'filters': {'price_range': [500, 1500]}
    })
    print(f"s1 Result: Found {s1_result['total_results']} products")
    
    print("\n✅ All modules demonstrated successfully!")
    print("\nFor more detailed examples, check the documentation.")

if __name__ == "__main__":
    main() 