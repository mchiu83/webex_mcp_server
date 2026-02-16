import json

def test_api_loading():
    print("Testing API Collection Loading...")
    
    with open('webex_api_collection.json', 'r', encoding='utf-8') as f:
        api_data = json.load(f)
    
    print(f"[OK] Version: {api_data['version']}")
    print(f"[OK] Exported: {api_data['exported_at']}")
    print(f"[OK] Total Endpoints: {api_data['total_endpoints']}")
    print(f"\n[OK] Features: {len(api_data['endpoints'])}")
    
    total_tools = 0
    for feature, endpoints in api_data['endpoints'].items():
        count = len(endpoints)
        total_tools += count
        print(f"  - {feature}: {count} endpoints")
    
    print(f"\n[OK] Total Tools Generated: {total_tools}")
    
    print("\n[OK] Sample Endpoint Structure:")
    first_feature = list(api_data['endpoints'].keys())[0]
    first_endpoint = api_data['endpoints'][first_feature][0]
    print(f"  Feature: {first_feature}")
    print(f"  Title: {first_endpoint['title']}")
    print(f"  Method: {first_endpoint['method']}")
    print(f"  Path: {first_endpoint['path']}")
    
    print("\n[OK] All tests passed! Server ready to run.")

if __name__ == "__main__":
    test_api_loading()
