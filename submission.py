"""
Package submission script
Creates a .zip file with all necessary files for submission
"""

import os
import zipfile
from datetime import datetime

def create_submission_zip():
    """Create a zip file with all project files"""
    
    # Files to include in submission
    files_to_include = [
        'game.py',
        'expectimax_agent.py',
        'heuristics.py',
        'runner.py',
        'visualize.py',
        'demo.py',
        'requirements.txt',
        'README.md',
        # 'results.json',  # If it exists
    ]
    
    # Image files (if they exist)
    image_files = [
        'score_distributions.png',
        'max_tile_distribution.png',
        'performance_comparison.png',
        'tile_achievements.png',
    ]
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'2048_expectimax_submission_{timestamp}.zip'
    
    print(f"Creating submission package: {zip_filename}")
    print("="*60)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main files
        for filename in files_to_include:
            if os.path.exists(filename):
                zipf.write(filename)
                print(f"✓ Added: {filename}")
            else:
                print(f"✗ Not found: {filename}")
        
        # Add image files if they exist
        for filename in image_files:
            if os.path.exists(filename):
                zipf.write(filename)
                print(f"✓ Added: {filename}")
        
        # Add report.pdf if it exists
        if os.path.exists('report.pdf'):
            zipf.write('report.pdf')
            print(f"✓ Added: report.pdf")
        else:
            print(f"\n⚠ WARNING: report.pdf not found!")
            print("  Remember to add your report before final submission!")
    
    print("="*60)
    print(f"\n✓ Submission package created: {zip_filename}")
    
    # Get file size
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"  File size: {size_mb:.2f} MB")
    
    return zip_filename

def verify_submission():
    """Verify that all required files are present"""
    print("\nVerifying submission requirements...")
    print("="*60)
    
    required_files = {
        'Code files': ['game.py', 'expectimax_agent.py', 'heuristics.py', 
                       'runner.py', 'visualize.py'],
        'Documentation': ['README.md'],
        'Report': ['report.pdf'],
        'Dependencies': ['requirements.txt'],
        'Results': ['results.json']
    }
    
    all_present = True
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        for filename in files:
            exists = os.path.exists(filename)
            status = "✓" if exists else "✗"
            print(f"  {status} {filename}")
            if not exists:
                all_present = False
                if filename == 'report.pdf':
                    print(f"     → REQUIRED: Create your report!")
                elif filename == 'results.json':
                    print(f"     → Run: python runner.py")
    
    print("\n" + "="*60)
    if all_present:
        print("✓ All required files present!")
    else:
        print("⚠ Some files are missing. See above.")
    
    return all_present

def print_submission_checklist():
    """Print a checklist for final submission"""
    print("\n" + "="*60)
    print("FINAL SUBMISSION CHECKLIST")
    print("="*60)
    
    checklist = [
        "Run experiments: python runner.py",
        "Generate visualizations: python visualize.py",
        "Write report.pdf (2-3 pages)",
        "Include in report:",
        "  - All group member names",
        "  - Problem description & your contribution",
        "  - Literature review",
        "  - Software requirements",
        "  - Instructions to run",
        "  - Results with graphs",
        "Test that code runs: python demo.py",
        "Verify all files present",
        "Create submission zip",
        "Upload to course submission portal"
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"{i:2}. [ ] {item}")
    
    print("="*60)

def main():
    """Main submission packaging function"""
    print("\n" + "="*60)
    print("2048 EXPECTIMAX PROJECT - SUBMISSION PACKAGER")
    print("="*60)
    
    # Verify files
    all_present = verify_submission()
    
    if not all_present:
        print("\n⚠ Some required files are missing.")
        response = input("\nContinue creating zip anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("Aborted.")
            return
    
    # Create zip
    print()
    zip_filename = create_submission_zip()
    
    # Show checklist
    print_submission_checklist()
    
    print(f"\n✓ Submission package ready: {zip_filename}")
    print("\nNext steps:")
    print("1. Review the checklist above")
    print("2. Complete any missing items")
    print("3. Upload the .zip file to your course portal")
    print("4. Upload report.pdf separately if required")

if __name__ == "__main__":
    main()