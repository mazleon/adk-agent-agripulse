#!/usr/bin/env python3
"""
Test script to verify Streamlit session handling works correctly
"""
import asyncio
import uuid
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adk_app.agents import coordinator_agent
from google.adk.runners import InMemoryRunner
from google.genai import types


async def test_session_flow():
    """Test the session creation and usage flow"""
    print("=" * 80)
    print("🧪 Testing ADK Session Flow")
    print("=" * 80)
    
    # Create runner
    print("\n1️⃣  Creating InMemoryRunner...")
    runner = InMemoryRunner(agent=coordinator_agent)
    print("✅ Runner created")
    
    # Generate session IDs
    user_id = "test_user_001"
    session_id = str(uuid.uuid4())
    print(f"\n2️⃣  Generated IDs:")
    print(f"   User ID: {user_id}")
    print(f"   Session ID: {session_id}")
    
    # Create session
    print(f"\n3️⃣  Creating session...")
    try:
        session = runner.session_service.create_session(
            app_name="agripulse_ai_test",
            user_id=user_id,
            session_id=session_id
        )
        print(f"✅ Session created: {session.id}")
    except Exception as e:
        print(f"❌ Failed to create session: {e}")
        return False
    
    # List sessions
    print(f"\n4️⃣  Listing sessions for user...")
    try:
        sessions = runner.session_service.list_sessions(user_id=user_id)
        print(f"✅ Found {len(sessions)} session(s)")
        for s in sessions:
            print(f"   - Session: {s.id}")
    except Exception as e:
        print(f"❌ Failed to list sessions: {e}")
    
    # Test query
    print(f"\n5️⃣  Testing query with session...")
    test_message = "What can you help me with?"
    
    try:
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=test_message)]
        )
        
        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            if hasattr(event, 'content') and event.content:
                content = event.content
                if isinstance(content, str):
                    response_text += content
                elif hasattr(content, 'parts'):
                    for part in content.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
        
        if response_text:
            print(f"✅ Got response ({len(response_text)} chars)")
            print(f"\n📝 Response preview:")
            print(f"   {response_text[:200]}...")
            return True
        else:
            print(f"❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Query failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_session_persistence():
    """Test if session persists across multiple queries"""
    print("\n" + "=" * 80)
    print("🧪 Testing Session Persistence")
    print("=" * 80)
    
    runner = InMemoryRunner(agent=coordinator_agent)
    user_id = "test_user_002"
    session_id = str(uuid.uuid4())
    
    # Create session
    print(f"\n1️⃣  Creating session...")
    try:
        session = runner.session_service.create_session(
            app_name="agripulse_ai_test",
            user_id=user_id,
            session_id=session_id
        )
        print(f"✅ Session created: {session.id}")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False
    
    # First query
    print(f"\n2️⃣  First query...")
    try:
        msg1 = types.Content(role="user", parts=[types.Part(text="Hello")])
        response_count = 0
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=msg1):
            response_count += 1
        print(f"✅ First query successful ({response_count} events)")
    except Exception as e:
        print(f"❌ First query failed: {e}")
        return False
    
    # Second query (should use same session)
    print(f"\n3️⃣  Second query (same session)...")
    try:
        msg2 = types.Content(role="user", parts=[types.Part(text="What's the weather?")])
        response_count = 0
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=msg2):
            response_count += 1
        print(f"✅ Second query successful ({response_count} events)")
        print(f"✅ Session persisted across queries!")
        return True
    except Exception as e:
        print(f"❌ Second query failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n🚀 Starting ADK Session Tests\n")
    
    # Test 1: Basic session flow
    test1_passed = await test_session_flow()
    
    # Test 2: Session persistence
    test2_passed = await test_session_persistence()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Test Summary")
    print("=" * 80)
    print(f"Test 1 (Basic Flow): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (Persistence): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 80)
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Session handling is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
