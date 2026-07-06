"""
Referral Incentive Optimizer
============================
Determines optimal referral rewards for businesses using mathematical optimization.

Author: Noor ul Huda
Reg No: Mtech-AI26058
Project: Referral Incentive Optimizer
Difficulty: Intermediate
"""

import sys

def check_dependencies():
    """Check if required packages are installed."""
    required = {
        'numpy': 'numpy',
        'PIL': 'Pillow',
        'matplotlib': 'matplotlib'
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print("❌ Missing dependencies. Please install them using:")
        print(f"   pip install {' '.join(missing)}")
        print("
Or install all at once:")
        print("   pip install -r requirements.txt")
        return False

    return True

def main():
    """Main entry point."""
    print("=" * 70)
    print("🎁 REFERRAL INCENTIVE OPTIMIZER")
    print("=" * 70)
    print("Determine Optimal Referral Rewards for Maximum Profit")
    print("Author: Noor ul Huda | Reg No: Mtech-AI26058")
    print("=" * 70)
    print()

    if not check_dependencies():
        sys.exit(1)

    print("✅ All dependencies satisfied!")
    print("🚀 Launching application...")
    print()

    try:
        from referral_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
