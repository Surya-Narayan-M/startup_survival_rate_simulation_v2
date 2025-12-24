"""
Startup Simulation Launcher
Provides menu to configure policies or run simulation directly
"""

import subprocess
import sys
import os
from pathlib import Path


def print_banner():
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║        STARTUP FUNDING DYNAMICS SIMULATION - LAUNCHER                 ║
    ║        Agent-Based Model using Mesa Framework                         ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)


def main():
    print_banner()
    
    config_exists = Path('policy_config.json').exists()
    
    if config_exists:
        print("\n✓ Saved policy configuration found: policy_config.json")
    else:
        print("\n⚠ No saved policy configuration found")
    
    print("\n" + "="*70)
    print("SELECT AN OPTION:")
    print("="*70)
    print("\n1. 🎛️  CONFIGURE POLICIES & PARAMETERS (GUI Interface)")
    print("   → Customize all simulation parameters with a user-friendly interface")
    print("   → Save/load configurations")
    print("   → View all parameters organized by category")
    
    if config_exists:
        print("\n2. ▶️  RUN SIMULATION (with saved configuration)")
        print("   → Execute simulation using last saved policies")
        print("   → Skip configuration step")
    else:
        print("\n2. ▶️  RUN SIMULATION (with defaults)")
        print("   → Execute simulation using default parameters")
        print("   → Run 'Option 1' first to customize")
    
    print("\n3. 📊 VIEW LAST RESULTS")
    print("   → Open last generated analysis plots")
    
    print("\n4. ❌ EXIT")
    print("\n" + "="*70)
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n🎛️  Launching Policy Configuration GUI...")
            print("(This window will remain open while GUI is active)\n")
            try:
                subprocess.run([sys.executable, 'policy_gui.py'], check=True)
                print("\n✓ Configuration completed. You can now run the simulation.")
            except subprocess.CalledProcessError:
                print("\n❌ Error launching GUI. Please ensure tkinter is installed.")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
            break
        
        elif choice == '2':
            print("\n▶️  Launching Simulation...")
            print("(Running with", end="")
            if config_exists:
                print(" saved configuration)\n")
            else:
                print(" default configuration)\n")
            try:
                subprocess.run([sys.executable, 'run_simulation.py'], check=True)
            except subprocess.CalledProcessError:
                print("\n❌ Error running simulation.")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
            break
        
        elif choice == '3':
            print("\n📊 Opening results directory...")
            results_path = Path('results')
            if results_path.exists():
                try:
                    if sys.platform == 'win32':
                        os.startfile(str(results_path.absolute()))
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', str(results_path.absolute())])
                    else:
                        subprocess.run(['xdg-open', str(results_path.absolute())])
                    print(f"✓ Opened: {results_path.absolute()}")
                except Exception as e:
                    print(f"Could not open results folder: {str(e)}")
                    print(f"Results are in: {results_path.absolute()}")
            else:
                print("⚠ No results directory found. Run a simulation first.")
            break
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
