#!/usr/bin/env python3
"""
Blog Build Script
Converts Markdown blog posts to HTML and updates the blog listing page.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
try:
    import markdown
    from markdown.extensions import codehilite, fenced_code, tables
except ImportError:
    print("Error: markdown library not found. Install it with: pip install markdown")
    exit(1)

# Configuration
BLOG_SRC_DIR = Path("blog_src")
BLOG_OUTPUT_DIR = Path("blog")
TEMPLATE_FILE = Path("blog/_template.html")
BLOG_LISTING_FILE = Path("blog/index.html")

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown file."""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        markdown_content = match.group(2)
        metadata = {}
        
        # Simple YAML parser for basic key-value pairs
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                metadata[key] = value
        
        return metadata, markdown_content
    else:
        # No frontmatter, use filename as title
        return {}, content

def markdown_to_html(markdown_text):
    """Convert markdown to HTML."""
    md = markdown.Markdown(extensions=[
        'codehilite',
        'fenced_code',
        'tables',
        'nl2br',
        'sane_lists'
    ])
    html = md.convert(markdown_text)
    return html

def generate_blog_post(metadata, html_content, slug, template_path):
    """Generate HTML file for a blog post."""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    title = metadata.get('title', slug.replace('-', ' ').title())
    description = metadata.get('description', '')
    date = metadata.get('date', datetime.now().strftime('%B %d, %Y'))
    
    # Format date if it's in ISO format
    try:
        if re.match(r'\d{4}-\d{2}-\d{2}', date):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date = date_obj.strftime('%B %d, %Y')
    except:
        pass
    
    html = template.replace('{{TITLE}}', title)
    html = html.replace('{{DESCRIPTION}}', description)
    html = html.replace('{{DATE}}', date)
    html = html.replace('{{SLUG}}', slug)
    html = html.replace('{{CONTENT}}', html_content)
    
    return html

def update_blog_listing(posts):
    """Update the blog listing page with all posts."""
    with open(BLOG_LISTING_FILE, 'r', encoding='utf-8') as f:
        listing_html = f.read()
    
    # Generate blog list HTML
    blog_list_html = ''
    if posts:
        # Sort posts by date (newest first)
        sorted_posts = sorted(posts, key=lambda x: x.get('date', ''), reverse=True)
        
        for post in sorted_posts:
            slug = post['slug']
            title = post['title']
            date = post['date']
            description = post.get('description', '')
            
            blog_list_html += f'''
          <div class="view-list-item" style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #e0e0e0;">
            <i class="far fa-file-alt pub-icon" aria-hidden="true"></i>
            <a href="/blog/{slug}/" style="font-size: 1.1rem; font-weight: 500;">{title}</a>
            <div class="article-metadata" style="margin-top: 0.5rem;">
              <span class="article-date">{date}</span>
            </div>
            {f'<p style="margin-top: 0.5rem; color: #666;">{description}</p>' if description else ''}
          </div>
'''
    else:
        blog_list_html = '<p>No blog posts yet. Check back soon!</p>'
    
    # Replace the blog list section
    listing_html = re.sub(
        r'<div id="blog-list">.*?</div>',
        f'<div id="blog-list">{blog_list_html}\n          </div>',
        listing_html,
        flags=re.DOTALL
    )
    
    with open(BLOG_LISTING_FILE, 'w', encoding='utf-8') as f:
        f.write(listing_html)

def main():
    """Main build function."""
    # Create directories if they don't exist
    BLOG_SRC_DIR.mkdir(exist_ok=True)
    BLOG_OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Find all markdown files
    md_files = list(BLOG_SRC_DIR.glob('*.md'))
    
    if not md_files:
        print(f"No markdown files found in {BLOG_SRC_DIR}/")
        print(f"Create markdown files in {BLOG_SRC_DIR}/ to generate blog posts.")
        return
    
    posts = []
    
    for md_file in md_files:
        print(f"Processing {md_file.name}...")
        
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        metadata, markdown_content = parse_frontmatter(content)
        
        # Generate slug from filename
        slug = md_file.stem
        
        # Get title from frontmatter or filename
        title = metadata.get('title', slug.replace('-', ' ').title())
        
        # Get date
        date = metadata.get('date', datetime.now().strftime('%B %d, %Y'))
        # Format date if it's in ISO format
        try:
            if re.match(r'\d{4}-\d{2}-\d{2}', date):
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                date = date_obj.strftime('%B %d, %Y')
        except:
            pass
        
        # Convert markdown to HTML
        html_content = markdown_to_html(markdown_content)
        
        # Generate blog post HTML
        post_html = generate_blog_post(metadata, html_content, slug, TEMPLATE_FILE)
        
        # Create output directory for this post
        post_dir = BLOG_OUTPUT_DIR / slug
        post_dir.mkdir(exist_ok=True)
        
        # Write HTML file
        output_file = post_dir / 'index.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(post_html)
        
        print(f"  Generated: {output_file}")
        
        # Store post metadata for listing
        posts.append({
            'slug': slug,
            'title': title,
            'date': date,
            'description': metadata.get('description', '')
        })
    
    # Update blog listing page
    print(f"\nUpdating blog listing page...")
    update_blog_listing(posts)
    print(f"  Updated: {BLOG_LISTING_FILE}")
    
    print(f"\n✓ Build complete! Generated {len(posts)} blog post(s).")

if __name__ == '__main__':
    main()

