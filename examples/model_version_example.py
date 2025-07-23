"""
Model Version Example demonstrating how to upgrade from v1 to v9 for optimal performance.
"""

from morngpt import MornGPT

def main():
    """Demonstrate the model version system and upgrades."""
    
    # Initialize mornGPT
    morngpt = MornGPT()
    
    print("🚀 mornGPT Model Version System Demo")
    print("=" * 50)
    
    # Example 1: Check current model version (default is v1)
    print("\n📊 Current Model Version (v1)")
    print("-" * 30)
    
    # Get model info for h1 (Multi-GPT Prompts)
    h1_info = morngpt.get_model_info('h', 1)
    print(f"Current version: {h1_info['current_version']}")
    print(f"Current quality: {h1_info['current_quality']}")
    print(f"Best available version: {h1_info['best_version']}")
    
    # Example 2: Process request with v1 (basic performance)
    print("\n🔧 Processing with v1 (Basic)")
    print("-" * 30)
    
    v1_result = morngpt.process_request('h', 1, {
        'prompt': 'Write a creative story about AI',
        'style': 'creative',
        'length': 'short'
    }, model_version=1)
    
    print(f"v1 Response quality: Basic")
    print(f"Response length: {len(str(v1_result))} characters")
    
    # Example 3: Upgrade to v5 (Expert level)
    print("\n⬆️ Upgrading to v5 (Expert)")
    print("-" * 30)
    
    upgrade_result = morngpt.upgrade_model('h', 1, 5)
    print(f"Upgrade result: {upgrade_result['message']}")
    print(f"Quality improvement: {upgrade_result['quality_improvement']}")
    
    # Example 4: Process same request with v5 (expert performance)
    print("\n🎯 Processing with v5 (Expert)")
    print("-" * 30)
    
    v5_result = morngpt.process_request('h', 1, {
        'prompt': 'Write a creative story about AI',
        'style': 'creative',
        'length': 'short'
    }, model_version=5)
    
    print(f"v5 Response quality: Expert")
    print(f"Response length: {len(str(v5_result))} characters")
    print(f"Improvement: {len(str(v5_result)) - len(str(v1_result))} characters more detailed")
    
    # Example 5: Upgrade to v9 (Best performance)
    print("\n🚀 Upgrading to v9 (Best)")
    print("-" * 30)
    
    upgrade_to_best = morngpt.upgrade_model('h', 1, 9)
    print(f"Upgrade result: {upgrade_to_best['message']}")
    print(f"Quality improvement: {upgrade_to_best['quality_improvement']}")
    
    # Example 6: Process with v9 (optimal performance)
    print("\n💎 Processing with v9 (Best)")
    print("-" * 30)
    
    v9_result = morngpt.process_request('h', 1, {
        'prompt': 'Write a creative story about AI',
        'style': 'creative',
        'length': 'short'
    }, model_version=9)
    
    print(f"v9 Response quality: Best")
    print(f"Response length: {len(str(v9_result))} characters")
    print(f"Total improvement: {len(str(v9_result)) - len(str(v1_result))} characters more detailed")
    
    # Example 7: Compare all versions
    print("\n📈 Version Comparison")
    print("-" * 30)
    
    versions = [1, 3, 5, 7, 9]
    results = {}
    
    for version in versions:
        result = morngpt.process_request('h', 1, {
            'prompt': 'Explain quantum computing',
            'style': 'educational',
            'length': 'medium'
        }, model_version=version)
        
        results[version] = {
            'length': len(str(result)),
            'quality': morngpt.get_model_info('h', 1)['current_quality']
        }
    
    print("Version | Quality Level | Response Length")
    print("-" * 45)
    for version, data in results.items():
        print(f"v{version:2d}     | {data['quality'][:15]:15} | {data['length']:6d} chars")
    
    # Example 8: Upgrade multiple modules
    print("\n🔄 Batch Module Upgrades")
    print("-" * 30)
    
    modules_to_upgrade = [
        ('q', 1, 7),  # Teacher/Coach to v7
        ('c', 1, 8),  # Coder to v8
        ('w', 1, 9),  # Content Generation to v9
        ('t', 1, 6),  # Clothing to v6
        ('r', 1, 5),  # Traveling to v5
    ]
    
    for module_code, submodule_id, target_version in modules_to_upgrade:
        try:
            result = morngpt.upgrade_model(module_code, submodule_id, target_version)
            print(f"✅ {module_code}{submodule_id} upgraded to v{target_version}")
        except Exception as e:
            print(f"❌ Failed to upgrade {module_code}{submodule_id}: {e}")
    
    # Example 9: Get all modules info with versions
    print("\n📋 All Modules Version Status")
    print("-" * 30)
    
    all_info = morngpt.get_all_modules_info()
    for module_code, module_info in all_info.items():
        print(f"\n{module_code.upper()} Module: {module_info['name']}")
        for submodule_id in range(1, 4):  # Show first 3 submodules
            try:
                submodule = morngpt.get_submodule(module_code, submodule_id)
                print(f"  {module_code}{submodule_id}: v{submodule.model_version} - {submodule.model_quality[submodule.model_version]}")
            except:
                pass
    
    print("\n✅ Model Version System demonstration completed!")
    print("\nKey features demonstrated:")
    print("• Model version management (v1-v9)")
    print("• Quality improvements with version upgrades")
    print("• Performance comparison across versions")
    print("• Batch module upgrades")
    print("• Version status tracking")
    print("\n💡 Tips:")
    print("• Start with v1 for basic functionality")
    print("• Upgrade to v5+ for professional use")
    print("• Use v9 for optimal performance")
    print("• Different modules can have different versions")

if __name__ == "__main__":
    main() 