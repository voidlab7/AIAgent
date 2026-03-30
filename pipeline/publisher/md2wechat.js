#!/usr/bin/env node

/**
 * Markdown to WeChat Official Account HTML Converter
 *
 * Usage:
 *   node md2wechat.js <input.md> [output.html]
 *
 * If output is omitted, writes to <input-name>-wechat.html
 * Open the output HTML in browser, Ctrl+A select all, Ctrl+C copy,
 * then paste into WeChat editor.
 */

const fs = require("fs");
const path = require("path");
const { marked } = require("marked");
const juice = require("juice");

// ============================================================
// WeChat-friendly CSS theme (clean, readable on mobile)
// ============================================================
const WECHAT_CSS = `
/* Base */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue",
    "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 15px;
  color: #3f3f3f;
  line-height: 1.75;
  padding: 20px;
  max-width: 680px;
  margin: 0 auto;
  background: #fff;
}

/* Headings */
h1 {
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  margin: 1.5em 0 1em;
  color: #1a1a1a;
}

h2 {
  font-size: 18px;
  font-weight: bold;
  margin: 1.8em 0 0.8em;
  color: #1a1a1a;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
}

h3 {
  font-size: 16px;
  font-weight: bold;
  margin: 1.5em 0 0.6em;
  color: #1a1a1a;
}

/* Paragraphs */
p {
  margin: 0 0 1.2em;
  text-align: justify;
}

/* Strong / Bold */
strong {
  color: #d4552b;
  font-weight: bold;
}

/* Emphasis / Italic */
em {
  font-style: italic;
  color: #666;
}

/* Links — WeChat strips <a> hrefs, show URL as footnote */
a {
  color: #576b95;
  text-decoration: none;
  word-break: break-all;
}

/* Blockquote */
blockquote {
  margin: 1.2em 0;
  padding: 12px 16px;
  border-left: 3px solid #e8a735;
  background: #fdf8ed;
  color: #666;
  font-size: 14px;
  line-height: 1.7;
}

blockquote p {
  margin: 0 0 0.5em;
}

blockquote p:last-child {
  margin-bottom: 0;
}

/* Horizontal Rule */
hr {
  border: none;
  border-top: 1px dashed #ddd;
  margin: 2em 0;
}

/* Inline Code */
code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 90%;
  color: #d4552b;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}

/* Code Block */
pre {
  background: #f8f8f8;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 12px 16px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.6;
  margin: 1.2em 0;
}

pre code {
  background: none;
  padding: 0;
  border-radius: 0;
  color: #333;
}

/* Lists */
ul, ol {
  margin: 0.8em 0;
  padding-left: 2em;
}

li {
  margin: 0.3em 0;
  line-height: 1.75;
}

/* Images */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
  border-radius: 4px;
}

/* Table */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 14px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px 12px;
  text-align: left;
}

th {
  background: #f5f5f5;
  font-weight: bold;
}
`;

// ============================================================
// Custom renderer: convert links to footnote-style references
// (WeChat strips external links from <a> tags)
// ============================================================
const linkMap = new Map();
let linkCounter = 0;

const renderer = new marked.Renderer();

// Override link rendering: show text + footnote number
renderer.link = function ({ href, title, text }) {
  // Skip anchor-only links
  if (href && href.startsWith("#")) {
    return text;
  }
  linkCounter++;
  linkMap.set(linkCounter, { text, href });
  return `${text}<sup style="color:#576b95;font-size:12px;">[${linkCounter}]</sup>`;
};

// ============================================================
// Main conversion
// ============================================================
function convert(markdownContent) {
  // Reset link tracking
  linkMap.clear();
  linkCounter = 0;

  // Configure marked
  marked.setOptions({
    renderer,
    breaks: false,
    gfm: true,
  });

  // 1. Markdown → HTML
  let html = marked.parse(markdownContent);

  // 2. Append footnote references if any links were found
  if (linkMap.size > 0) {
    html += `\n<hr style="border:none;border-top:1px dashed #ddd;margin:2em 0;">\n`;
    html += `<section style="font-size:13px;color:#999;line-height:1.8;">\n`;
    html += `<p style="font-weight:bold;color:#666;margin-bottom:0.5em;">🔗 参考链接</p>\n`;
    for (const [num, { text, href }] of linkMap) {
      html += `<p style="margin:0.2em 0;word-break:break-all;">[${num}] ${text}: ${href}</p>\n`;
    }
    html += `</section>\n`;
  }

  // 3. Wrap in full HTML with <style>
  const fullHtml = `<style>${WECHAT_CSS}</style>\n<section>${html}</section>`;

  // 4. Inline CSS (critical for WeChat — it strips <style> tags)
  const inlinedHtml = juice(fullHtml);

  // 5. Wrap in a complete HTML document for preview
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WeChat Preview</title>
  <style>
    /* Preview container styling */
    body {
      background: #f0f0f0;
      display: flex;
      justify-content: center;
      padding: 20px 0;
    }
    .phone-frame {
      width: 375px;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      padding: 20px;
      min-height: 600px;
    }
    .copy-hint {
      text-align: center;
      color: #999;
      font-size: 13px;
      margin-bottom: 16px;
      font-family: sans-serif;
    }
    .copy-btn {
      display: block;
      margin: 0 auto 20px;
      padding: 8px 24px;
      background: #07c160;
      color: #fff;
      border: none;
      border-radius: 6px;
      font-size: 14px;
      cursor: pointer;
    }
    .copy-btn:hover {
      background: #06ad56;
    }
  </style>
</head>
<body>
  <div>
    <p class="copy-hint">💡 点击按钮复制内容，然后粘贴到公众号编辑器</p>
    <button class="copy-btn" onclick="copyContent()">📋 一键复制</button>
    <div class="phone-frame" id="content">
      ${inlinedHtml}
    </div>
  </div>
  <script>
    function copyContent() {
      const content = document.getElementById('content');
      const range = document.createRange();
      range.selectNodeContents(content);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      document.execCommand('copy');
      selection.removeAllRanges();

      const btn = document.querySelector('.copy-btn');
      btn.textContent = '✅ 已复制！粘贴到公众号编辑器即可';
      setTimeout(() => { btn.textContent = '📋 一键复制'; }, 2000);
    }
  </script>
</body>
</html>`;
}

// ============================================================
// CLI entry
// ============================================================
function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log("Usage: node md2wechat.js <input.md> [output.html]");
    console.log("Example: node md2wechat.js article.md");
    process.exit(1);
  }

  const inputFile = args[0];
  const outputFile =
    args[1] ||
    path.join(
      path.dirname(inputFile),
      path.basename(inputFile, path.extname(inputFile)) + "-wechat.html"
    );

  if (!fs.existsSync(inputFile)) {
    console.error(`❌ File not found: ${inputFile}`);
    process.exit(1);
  }

  const markdown = fs.readFileSync(inputFile, "utf-8");
  const html = convert(markdown);
  fs.writeFileSync(outputFile, html, "utf-8");

  console.log(`✅ Converted successfully!`);
  console.log(`   Input:  ${inputFile}`);
  console.log(`   Output: ${outputFile}`);
  console.log(`\n📖 Open the HTML file in browser to preview.`);
  console.log(`   Click "一键复制" button, then paste into WeChat editor.`);
}

main();
