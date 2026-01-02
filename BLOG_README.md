# Blog System Guide

This website now includes a blog system that allows you to easily create blog posts using Markdown files.

## Viewing the Website Locally

### Option 1: Python HTTP Server (Recommended)

1. **Start a local server:**
   ```bash
   python3 -m http.server 8000
   ```

2. **Open your browser and visit:**
   ```
   http://localhost:8000
   ```

3. **To stop the server:** Press `Ctrl+C` in the terminal

### Option 2: Using Node.js (if you have it installed)

```bash
npx http-server -p 8000
```

### Option 3: Using PHP (if you have it installed)

```bash
php -S localhost:8000
```

## Creating New Blog Posts

1. **Create a new Markdown file** in the `blog_src/` directory with a `.md` extension.

2. **Add frontmatter** at the top of your file:
   ```markdown
   ---
   title: "Your Blog Post Title"
   date: "2024-01-15"
   description: "A brief description of your post"
   ---
   
   Your blog content here...
   ```

3. **Write your content** in Markdown format below the frontmatter.

4. **Build the blog** by running:
   ```bash
   python3 build_blog.py
   ```

5. **Refresh your browser** to see the new post!

## Example Blog Post Structure

```markdown
---
title: "My First Blog Post"
date: "2024-01-15"
description: "This is my first blog post about machine learning."
---

# My First Blog Post

This is the content of my blog post. I can use **bold**, *italic*, and other Markdown features.

## Code Example

```python
def hello():
    print("Hello, World!")
```

## Lists

- Item 1
- Item 2
- Item 3
```

## Markdown Features Supported

- Headers (#, ##, ###, etc.)
- **Bold** and *italic* text
- Code blocks with syntax highlighting
- Lists (ordered and unordered)
- Links and images
- Tables
- Blockquotes

## File Structure

```
.
├── blog_src/              # Source Markdown files (create posts here)
│   └── example-post.md
├── blog/                  # Generated HTML files
│   ├── index.html         # Blog listing page
│   ├── _template.html     # Template for individual posts
│   └── example-post/      # Generated post directory
│       └── index.html
└── build_blog.py          # Build script
```

## Workflow

1. Write your blog post in `blog_src/your-post-name.md`
2. Run `python3 build_blog.py` to generate HTML
3. Commit and push to GitHub
4. Your blog post will appear on your website!

## Requirements

- Python 3
- `markdown` library (install with: `pip3 install markdown`)

## Tips

- Use descriptive filenames (they become the URL slug)
- Always include frontmatter with title, date, and description
- Dates can be in format `YYYY-MM-DD` or full text like `January 15, 2024`
- The build script automatically sorts posts by date (newest first)

