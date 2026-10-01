import AppKit
import Foundation

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let folder = root.appendingPathComponent("word-atlas-111-new/source/proofs")
let first = Int(CommandLine.arguments[1])!
let last = Int(CommandLine.arguments[2])!
let urls = try FileManager.default.contentsOfDirectory(at: folder, includingPropertiesForKeys: nil)
    .filter { $0.lastPathComponent.hasSuffix("-art-preview.png") }
    .filter { let id = Int($0.lastPathComponent.prefix(3))!; return first <= id && id <= last }
    .sorted { $0.lastPathComponent < $1.lastPathComponent }
let cols = 4, cellW = 500, cellH = 258, rows = (urls.count + cols - 1) / cols
precondition(!urls.isEmpty)
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: cols * cellW, pixelsHigh: rows * cellH,
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
    bytesPerRow: 0, bitsPerPixel: 0)!
let gc = NSGraphicsContext(bitmapImageRep: rep)!
gc.cgContext.translateBy(x: 0, y: CGFloat(rows * cellH)); gc.cgContext.scaleBy(x: 1, y: -1)
NSGraphicsContext.current = NSGraphicsContext(cgContext: gc.cgContext, flipped: true)
NSColor(srgbRed: 0.965, green: 0.948, blue: 0.92, alpha: 1).setFill()
NSBezierPath(rect: NSRect(x: 0, y: 0, width: cols * cellW, height: rows * cellH)).fill()
for (i, url) in urls.enumerated() {
    let x = (i % cols) * cellW, y = (i / cols) * cellH
    let art = NSImage(contentsOf: url)!
    art.draw(in: NSRect(x: x + 8, y: y + 8, width: 484, height: 215), from: .zero,
        operation: .sourceOver, fraction: 1, respectFlipped: true, hints: [.interpolation: NSImageInterpolation.high])
    let label = url.lastPathComponent.replacingOccurrences(of: "-art-preview.png", with: "")
    (label as NSString).draw(in: NSRect(x: x + 12, y: y + 229, width: 477, height: 25), withAttributes: [
        .font: NSFont(name: "HelveticaNeue", size: 18)!, .foregroundColor: NSColor.darkGray])
}
let output = folder.appendingPathComponent(String(format: "art-contact-%03d-%03d.png", first, last))
try rep.representation(using: .png, properties: [:])!.write(to: output)
print(output.path)
