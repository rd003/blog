import os
import re
import sys

def find_first_image(content_after_frontmatter):
    """Find the first markdown image in content"""
    # Pattern to match ![alt text](image_path)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    match = re.search(pattern, content_after_frontmatter)
    if match:
        return match.group(0), match.group(2)  # full match and image path
    return None, None

def process_markdown_file(filepath, dry_run=True):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has TOML front matter
        if not content.startswith('+++'):
            print(f"⚠️  Skipping {filepath}: No TOML front matter found")
            return False
        
        # Split front matter and content
        parts = content.split('+++', 2)
        if len(parts) < 3:
            print(f"⚠️  Skipping {filepath}: Invalid front matter format")
            return False
        
        front_matter = parts[1]
        body_content = parts[2]
        
        # Check if image already exists in front matter
        if re.search(r"image\s*=\s*['\"]", front_matter):
            print(f"⏭️  Skipping {filepath}: Already has image in front matter")
            return False
        
        # Find first image in content
        image_markdown, image_path = find_first_image(body_content)
        
        if not image_markdown:
            print(f"⚠️  Skipping {filepath}: No image found in content")
            return False
        
        # Add image to front matter (before the closing +++)
        new_front_matter = front_matter.rstrip() + f"\nimage = '{image_path}'\n"
        
        # Comment out the first image in content
        new_body_content = body_content.replace(image_markdown, f"<!-- {image_markdown} -->", 1)
        
        # Reconstruct the file
        new_content = f"+++{new_front_matter}+++{new_body_content}"
        
        if dry_run:
            print(f"\n✅ {filepath}")
            print(f"   📷 Image found: {image_path}")
            print(f"   ➡️  Will add to front matter")
            print(f"   ➡️  Will comment out: {image_markdown[:50]}...")
            return True
        else:
            # Write the changes
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"\n✅ Modified: {filepath}")
            print(f"   📷 Added image: {image_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Hugo Blog Image Migrator")
    print("=" * 60)
    
    # Get content directory
    content_dir = input("\nEnter your content directory path (e.g., content/posts): ").strip()
    
    if not os.path.exists(content_dir):
        print(f"❌ Directory not found: {content_dir}")
        return
    
    # Ask for dry run
    dry_run_input = input("\nRun in dry-run mode first? (y/n, default: y): ").strip().lower()
    dry_run = dry_run_input != 'n'
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified")
    else:
        confirm = input("\n⚠️  This will modify your files! Continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("❌ Aborted")
            return
    
    print("\n" + "=" * 60)
    print("Processing files...")
    print("=" * 60)
    
    # Find all .md files
    modified_count = 0
    skipped_count = 0
    
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                result = process_markdown_file(filepath, dry_run)
                if result:
                    modified_count += 1
                else:
                    skipped_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if dry_run:
        print(f"📊 Files that WOULD BE modified: {modified_count}")
        print(f"📊 Files that would be skipped: {skipped_count}")
        print("\n💡 Run again and choose 'n' for dry-run to make actual changes")
    else:
        print(f"✅ Files modified: {modified_count}")
        print(f"⏭️  Files skipped: {skipped_count}")
        print("\n✅ Done! Check your files in Git to verify changes.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)