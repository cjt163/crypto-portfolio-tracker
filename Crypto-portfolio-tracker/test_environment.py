"""
Test script to verify environment setup
Run this BEFORE starting development
"""

import sys
import subprocess

def test_python_version():
    """Test Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (need 3.9+)")
        return False

def test_julia_installation():
    """Test Julia installation"""
    print("\nTesting Julia installation...")
    try:
        result = subprocess.run(["julia", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"  ✓ {version}")
            return True
        else:
            print(f"  ✗ Julia not found")
            return False
    except FileNotFoundError:
        print("  ✗ Julia not found in PATH")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_python_packages():
    """Test required Python packages"""
    print("\nTesting Python packages...")
    
    packages = [
        "eth_brownie",
        "web3",
        "pandas",
        "numpy",
        "requests",
        "matplotlib",
        "julia"
    ]
    
    all_good = True
    for package in packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            all_good = False
    
    return all_good

def test_julia_packages():
    """Test required Julia packages"""
    print("\nTesting Julia packages...")
    
    julia_test = '''
using Pkg
packages = ["CSV", "DataFrames", "MLJ", "MLJLinearModels", "Statistics", "JSON"]
all_installed = true
for pkg in packages
    try
        eval(Meta.parse("using " * pkg))
        println("✓ " * pkg)
    catch e
        println("✗ " * pkg * " - NOT INSTALLED")
        global all_installed = false
    end
end
exit(all_installed ? 0 : 1)
'''
    
    try:
        result = subprocess.run(["julia", "-e", julia_test],
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"  ✗ Error testing Julia packages: {e}")
        return False

def test_brownie():
    """Test Brownie installation"""
    print("\nTesting Brownie...")
    try:
        result = subprocess.run(["brownie", "--version"],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"  ✓ {result.stdout.strip()}")
            return True
        else:
            print("  ✗ Brownie not working")
            return False
    except FileNotFoundError:
        print("  ✗ Brownie not found")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_julia_executor():
    """Test JuliaExecutor"""
    print("\nTesting JuliaExecutor...")
    try:
        from JuliaExecutor import SimpleJuliaExecutor
        print("  ✓ JuliaExecutor imported")
        
        # Try to start Julia process
        executor = SimpleJuliaExecutor()
        if executor.is_running:
            print("  ✓ Julia process started")
            executor.cleanup()
            return True
        else:
            print("  ✗ Julia process failed to start")
            return False
    except ImportError:
        print("  ✗ JuliaExecutor.py not found")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("ENVIRONMENT VERIFICATION")
    print("="*60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Julia Installation", test_julia_installation),
        ("Python Packages", test_python_packages),
        ("Julia Packages", test_julia_packages),
        ("Brownie", test_brownie),
        ("JuliaExecutor", test_julia_executor),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{name:25} {status}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to start development.")
    else:
        print("\n⚠ Some tests failed. Fix issues before proceeding.")
        print("\nCommon fixes:")
        print("  - Activate conda environment: conda activate python-julia")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Install Julia packages: julia -e 'using Pkg; Pkg.add([...])'")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
