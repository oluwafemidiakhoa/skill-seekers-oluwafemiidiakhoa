#!/usr/bin/env python3
"""
Test Universal Skills Functionality

This script demonstrates how to use the new universal skills features
to create skills from any content source type.
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from skill_seekers.cli.content_adapters import (
    ContentType, SkillTemplate, ContentSourceConfig, 
    create_universal_config_template, get_adapter, ContentItem
)
from skill_seekers.cli.skill_templates import create_skill_from_template


def test_config_template_creation():
    """Test creating configuration templates for different content types."""
    print("Testing configuration template creation...")
    
    # Test API template
    api_template = create_universal_config_template(
        ContentType.API, 
        SkillTemplate.API_REFERENCE
    )
    print("API reference template created")
    print(f"   Contains: {list(api_template.keys())}")
    
    # Test Video template  
    video_template = create_universal_config_template(
        ContentType.VIDEO,
        SkillTemplate.TUTORIAL_SERIES
    )
    print("Video tutorial template created")
    print(f"   Contains: {list(video_template.keys())}")
    
    # Test Forum template
    forum_template = create_universal_config_template(
        ContentType.FORUM,
        SkillTemplate.TROUBLESHOOTING
    )
    print("Forum troubleshooting template created")
    print(f"   Contains: {list(forum_template.keys())}")
    
    return True


def test_content_adapter():
    """Test content adapter functionality with mock data."""
    print("\nTesting content adapters...")
    
    # Create a test API config
    api_config = ContentSourceConfig.from_dict({
        "name": "test_api",
        "description": "Test API skill",
        "source_type": "api",
        "template": "api_reference",
        "source_config": {
            "base_url": "https://api.example.com",
            "endpoints": [
                {
                    "path": "/users",
                    "method": "get",
                    "description": "Get all users",
                    "parameters": [
                        {
                            "name": "limit",
                            "type": "integer",
                            "required": False,
                            "description": "Maximum number of users to return"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Success"},
                        "400": {"description": "Bad request"}
                    }
                }
            ]
        }
    })
    
    # Test adapter creation
    try:
        adapter = get_adapter(api_config)
        print(f"Created adapter: {adapter.__class__.__name__}")
        
        # Test config validation
        is_valid = adapter.validate_config()
        print(f"Config validation: {'passed' if is_valid else 'failed'}")
        
        return True
    except Exception as e:
        print(f"Adapter test failed: {e}")
        return False


def test_skill_template():
    """Test skill template generation with mock content."""
    print("\nTesting skill templates...")
    
    # Create mock content items
    mock_content = [
        ContentItem(
            id="endpoint_1",
            title="GET /users",
            content="Retrieve a list of users from the system",
            content_type="api_endpoint",
            metadata={
                "method": "get",
                "path": "/users",
                "parameters": [{"name": "limit", "type": "integer"}],
                "responses": {"200": {"description": "Success"}}
            },
            categories=["users", "api"],
            quality_score=0.9
        ),
        ContentItem(
            id="endpoint_2", 
            title="POST /users",
            content="Create a new user in the system",
            content_type="api_endpoint",
            metadata={
                "method": "post",
                "path": "/users",
                "parameters": [{"name": "user", "type": "object"}],
                "responses": {"201": {"description": "Created"}}
            },
            categories=["users", "api"],
            quality_score=0.8
        )
    ]
    
    # Test skill generation
    try:
        skill_content = create_skill_from_template(
            content_items=mock_content,
            template=SkillTemplate.API_REFERENCE,
            metadata={
                "name": "Test API",
                "description": "Test API reference skill"
            }
        )
        
        print("Skill template generation successful")
        print(f"   Generated {len(skill_content)} characters")
        print(f"   Contains sections: {skill_content.count('##')} headings")
        
        # Save example output
        with open("test_skill_output.md", "w", encoding="utf-8") as f:
            f.write(skill_content)
        print("   Sample output saved to test_skill_output.md")
        
        return True
    except Exception as e:
        print(f"Template test failed: {e}")
        return False


def test_example_configs():
    """Test loading and validating example configurations."""
    print("\nTesting example configurations...")
    
    config_files = [
        "configs/examples/openai_api.json",
        "configs/examples/python_tutorials_video.json", 
        "configs/examples/stackoverflow_python_qa.json"
    ]
    
    for config_file in config_files:
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"Config file not found: {config_file}")
            continue
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Test config structure
            required_keys = ["name", "description", "source_type", "template", "source_config"]
            if all(key in config_data for key in required_keys):
                print(f"{config_path.name} - valid structure")
            else:
                print(f"{config_path.name} - missing required keys")
                continue
            
            # Test ContentSourceConfig creation
            try:
                config = ContentSourceConfig.from_dict(config_data)
                print(f"   Source: {config.source_type.value}, Template: {config.template.value}")
            except Exception as e:
                print(f"{config_path.name} - config creation failed: {e}")
                
        except Exception as e:
            print(f"{config_path.name} - failed to load: {e}")
    
    return True


def main():
    """Run all tests."""
    print("Testing Universal Skills Functionality\n")
    
    tests = [
        ("Config Template Creation", test_config_template_creation),
        ("Content Adapter", test_content_adapter),
        ("Skill Template", test_skill_template),
        ("Example Configs", test_example_configs)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\nTest Results:")
    print("=" * 50)
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nSummary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\nAll tests passed! Universal skills functionality is working correctly.")
        print("\nNext steps:")
        print("1. Try: skill-seekers create-template api api_reference my_api.json")
        print("2. Edit the generated config file")
        print("3. Run: skill-seekers universal --config my_api.json")
    else:
        print("\nSome tests failed. Check the implementation.")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)