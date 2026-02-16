from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
from learning_path import Base, LearningPath




def create_test_db():
    """Create an in-memory test database."""
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session()


def test_learning_path_creation():
    """Test: Can we create a learning path?"""
    print("Testing learning path creation...", end=" ")
    try:
        engine, session = create_test_db()
        
        path = LearningPath.create(
            name="Test Path",
            description="Testing",
            estimated_duration_days=30
        )
        session.add(path)
        session.commit()
        
        assert path.id is not None
        assert path.name == "Test Path"
        assert path.is_active is True
        
        print("✓ PASSED")
        session.close()
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_learning_path_query():
    """Test: Can we query learning paths?"""
    print("Testing learning path query...", end=" ")
    try:
        engine, session = create_test_db()
        
        #Create paths
        path1 = LearningPath.create(name="Path 1")
        path2 = LearningPath.create(name="Path 2")
        session.add_all([path1, path2])
        session.commit()
        
        #Query
        results = session.query(LearningPath).all()
        assert len(results) == 2
        
        #Query by name
        result = session.query(LearningPath).filter_by(name="Path 1").first()
        assert result is not None
        assert result.name == "Path 1"
        
        print("✓ PASSED")
        session.close()
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_learning_path_archive():
    """Test: Can we archive a learning path?"""
    print("Testing learning path archiving...", end=" ")
    try:
        engine, session = create_test_db()
        path = LearningPath.create(name="Path to Archive")
        session.add(path)
        session.commit()
        
        assert path.is_active is True
        
        #Archive it
        path.archive()
        session.commit()
        
        assert path.is_active is False
        
        print("PASSED")
        session.close()
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_learning_path_update():
    """Test: Can we update learning path info?"""
    print("Testing learning path updates...", end=" ")
    try:
        engine, session = create_test_db()
        
        path = LearningPath.create(name="Original Name")
        session.add(path)
        session.commit()
        
        # Update
        path.update_info(
            name="Updated Name",
            description="New description"
        )
        session.commit()
        
        # Verify
        assert path.name == "Updated Name"
        assert path.description == "New description"
        
        print("PASSED")
        session.close()
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_learning_path_to_dict():
    """Test: Can we serialize to dict?"""
    print("Testing to_dict serialization...", end=" ")
    try:
        engine, session = create_test_db()
        
        path = LearningPath.create(
            name="Test Path",
            description="Test",
            estimated_duration_days=45
        )
        session.add(path)
        session.commit()
        
        result = path.to_dict()
        assert isinstance(result, dict)
        assert result['name'] == "Test Path"
        assert 'id' in result
        assert 'created_at' in result
        
        print("PASSED")
        session.close()
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_learning_path_relationships():
    """Test: Do relationships work? (requires Module model)"""
    print("Testing relationships...", end=" ")
    try:
        engine, session = create_test_db()
        
        path = LearningPath.create(name="Path with Modules")
        session.add(path)
        session.commit()
        
        assert path.module_count == 0
        assert path.total_resources == 0
        
        print("SKIPPED (needs Module model)")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("QUICK MODEL TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_learning_path_creation,
        test_learning_path_query,
        test_learning_path_archive,
        test_learning_path_update,
        test_learning_path_to_dict,
        test_learning_path_relationships,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed!")
        return 0
    else:
        print(f"{total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())