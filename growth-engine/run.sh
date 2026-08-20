#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "🚀 PINTEREST -> WHATNOT GROWTH ENGINE"
echo "=================================================="

# 1. Run Python Engine Pipeline
python3 engine.py

# 2. Render Graphics for Ready-to-Post Batch (Pins 31-40)
echo ""
echo "🎨 Rendering 1000x1500px PNG Graphics for Next Batch..."

cat << 'SWIFT_EOF' > /tmp/render_next_batch.swift
import Foundation
import WebKit
import AppKit

let app = NSApplication.shared

struct PinJob {
    let htmlFile: String
    let outputFile: String
}

class BatchRenderer: NSObject, WKNavigationDelegate {
    var webView: WKWebView!
    var queue: [PinJob] = []
    var currentJob: PinJob?
    
    override init() {
        super.init()
        let config = WKWebViewConfiguration()
        let frame = NSRect(x: 0, y: 0, width: 1000, height: 1500)
        self.webView = WKWebView(frame: frame, configuration: config)
        self.webView.navigationDelegate = self
    }
    
    func start(jobs: [PinJob]) {
        self.queue = jobs
        processNext()
    }
    
    func processNext() {
        guard !queue.isEmpty else {
            print("✨ Batch graphics rendered successfully!")
            exit(0)
        }
        
        let job = queue.removeFirst()
        self.currentJob = job
        
        guard let html = try? String(contentsOfFile: job.htmlFile, encoding: .utf8) else {
            print("Could not read \(job.htmlFile)")
            processNext()
            return
        }
        
        webView.loadHTMLString(html, baseURL: URL(fileURLWithPath: "/tmp/pin_htmls/"))
    }
    
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.35) {
            guard let job = self.currentJob else { return }
            
            let snapConfig = WKSnapshotConfiguration()
            snapConfig.rect = NSRect(x: 0, y: 0, width: 1000, height: 1500)
            snapConfig.snapshotWidth = 1000
            
            webView.takeSnapshot(with: snapConfig) { (image, error) in
                if let image = image,
                   let tiff = image.tiffRepresentation,
                   let rep = NSBitmapImageRep(data: tiff),
                   let png = rep.representation(using: .png, properties: [:]) {
                    
                    try? png.write(to: URL(fileURLWithPath: job.outputFile))
                    print("RENDERED: \(URL(fileURLWithPath: job.outputFile).lastPathComponent)")
                }
                self.processNext()
            }
        }
    }
}

let fm = FileManager.default
let htmlDir = "/tmp/pin_htmls"
let exportDir = "/Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/ready-to-post/images"

var jobs: [PinJob] = []
if let files = try? fm.contentsOfDirectory(atPath: htmlDir) {
    let sorted = files.filter { $0.hasSuffix(".html") }.sorted()
    for f in sorted {
        let base = f.replacingOccurrences(of: ".html", with: ".png")
        jobs.append(PinJob(htmlFile: "\(htmlDir)/\(f)", outputFile: "\(exportDir)/\(base)"))
    }
}

if !jobs.isEmpty {
    let renderer = BatchRenderer()
    renderer.start(jobs: jobs)
    app.run()
} else {
    exit(0)
}
SWIFT_EOF

swift /tmp/render_next_batch.swift
rm -f /tmp/render_next_batch.swift

# 3. Ensure exact 1000x1500
sips -z 1500 1000 "$DIR/ready-to-post/images/"*.png > /dev/null 2>&1 || true

# 4. Generate visual contact sheet for ready-to-post batch
cat << 'PY_EOF' > /tmp/gen_ready_sheet.py
import os
from PIL import Image, ImageDraw, ImageFont

EXPORT_DIR = "/Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/ready-to-post/images"
files = sorted([f for f in os.listdir(EXPORT_DIR) if f.startswith("pin-") and f.endswith(".png")])

if files:
    COLS = 5
    ROWS = (len(files) + COLS - 1) // COLS
    THUMB_W = 360
    THUMB_H = 540
    PADDING = 24
    HEADER_H = 100

    SHEET_W = COLS * THUMB_W + (COLS + 1) * PADDING
    SHEET_H = ROWS * THUMB_H + (ROWS + 1) * PADDING + HEADER_H

    sheet = Image.new("RGB", (SHEET_W, SHEET_H), (15, 17, 21))
    draw = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 18)
        font_label = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 16)
    except:
        font_title = font_sub = font_label = ImageFont.load_default()

    draw.text((PADDING, 24), "READY-TO-POST BATCH (1000 × 1500 PX)", fill=(255, 255, 255), font=font_title)
    draw.text((PADDING, 68), "Compliant Evergreen Graphics • Ready for Pinterest Upload", fill=(156, 163, 175), font=font_sub)

    for idx, filename in enumerate(files):
        row = idx // COLS
        col = idx % COLS
        x = PADDING + col * (THUMB_W + PADDING)
        y = HEADER_H + PADDING + row * (THUMB_H + PADDING)
        
        img_path = os.path.join(EXPORT_DIR, filename)
        pin_img = Image.open(img_path).convert("RGB")
        pin_thumb = pin_img.resize((THUMB_W, THUMB_H), Image.Resampling.LANCZOS)
        
        sheet.paste(pin_thumb, (x, y))
        draw.rectangle([x, y, x + THUMB_W, y + THUMB_H], outline=(55, 65, 81), width=2)
        draw.rectangle([x, y + THUMB_H - 30, x + THUMB_W, y + THUMB_H], fill=(0, 0, 0))
        label_text = f"{filename}"
        draw.text((x + 10, y + THUMB_H - 24), label_text, fill=(255, 255, 255), font=font_label)

    sheet.save(os.path.join(EXPORT_DIR, "contact_sheet.jpg"), quality=92)
    print("✅ Created ready-to-post contact sheet!")
PY_EOF

python3 /tmp/gen_ready_sheet.py
rm -f /tmp/gen_ready_sheet.py

echo ""
echo "=================================================="
echo "✅ GROWTH ENGINE CYCLE COMPLETE"
echo "=================================================="
echo "📁 Ready-to-post files: growth-engine/ready-to-post/"
echo "📊 Visual Dashboard:   growth-engine/dashboard/index.html"
echo "📈 Weekly Report:       growth-engine/analysis/weekly-report.md"
