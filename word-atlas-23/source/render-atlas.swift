import AppKit
import CoreGraphics
import Foundation
import PDFKit

struct Section: Decodable { let heading: String; let text: String }
struct Entry: Decodable {
    let index: Int
    let slug: String
    let word: String
    let pronunciation: String
    let tagline: String
    let definition: String
    let etymology: String
    let sections: [Section]
    let literary: String
    let art_caption: String
    let accent: String
    let theme: String
    var stem: String { String(format: "%02d", index) + "-" + slug }
}

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let atlas = root.appendingPathComponent("word-atlas-23")
let manifestURL = atlas.appendingPathComponent("catalog.json")
let args = Array(CommandLine.arguments.dropFirst())
let previewOnly = args.contains("--preview-only")
let exportPDF = args.contains("--pdf")
let exportContact = args.contains("--contact-sheet")
let selected: Set<Int>? = args.first(where: { $0.hasPrefix("--ids=") }).map {
    Set($0.dropFirst(6).split(separator: ",").compactMap { Int($0) })
}
let allEntries = try JSONDecoder().decode([Entry].self, from: Data(contentsOf: manifestURL)).sorted { $0.index < $1.index }
let entries = allEntries.filter { selected == nil || selected!.contains($0.index) }
let width: CGFloat = 2000
let height: CGFloat = 2500
var overflow: [String] = []
var adjustments: [String] = []

func color(_ hex: String) -> NSColor {
    let n = UInt32(hex.replacingOccurrences(of: "#", with: ""), radix: 16)!
    return NSColor(srgbRed: CGFloat((n >> 16) & 255) / 255,
                   green: CGFloat((n >> 8) & 255) / 255,
                   blue: CGFloat(n & 255) / 255, alpha: 1)
}
let paper = color("F4F5F6")
let ink = color("243342")
let muted = color("576574")
let mist = color("D6DAE3")

func attributes(font: String, size: CGFloat, fill: NSColor, line: CGFloat?,
                align: NSTextAlignment, tracking: CGFloat) -> [NSAttributedString.Key: Any] {
    let p = NSMutableParagraphStyle()
    p.alignment = align
    p.lineBreakMode = .byWordWrapping
    p.hyphenationFactor = 0
    if let line = line { p.minimumLineHeight = line; p.maximumLineHeight = line }
    return [.font: NSFont(name: font, size: size)!, .foregroundColor: fill,
            .paragraphStyle: p, .kern: tracking]
}

func text(_ value: String, _ box: NSRect, font: String = "HelveticaNeue", size: CGFloat,
          fill: NSColor = ink, line: CGFloat? = nil, align: NSTextAlignment = .left,
          tracking: CGFloat = 0, minimum: CGFloat? = nil) {
    var actual = size
    var rendered: NSAttributedString!
    var bounds = CGRect.zero
    repeat {
        let actualLine = line.map { $0 * actual / size }
        rendered = NSAttributedString(string: value,
            attributes: attributes(font: font, size: actual, fill: fill,
                                   line: actualLine, align: align, tracking: tracking))
        bounds = rendered.boundingRect(with: NSSize(width: box.width, height: 10000),
            options: [.usesLineFragmentOrigin, .usesFontLeading])
        if bounds.height <= box.height + 1 { break }
        if let minimum = minimum, actual > minimum { actual -= 0.5 } else { break }
    } while true
    if bounds.height > box.height + 1 {
        overflow.append("\(value.prefix(45)): \(bounds.height) > \(box.height)")
    }
    if actual < size { adjustments.append("\(value.prefix(28)): \(size) → \(actual)") }
    rendered.draw(with: box, options: [.usesLineFragmentOrigin, .usesFontLeading])
}

func rect(_ box: NSRect, _ fill: NSColor) {
    fill.setFill(); NSBezierPath(rect: box).fill()
}

func line(_ y: CGFloat) {
    let p = NSBezierPath()
    p.move(to: NSPoint(x: 120, y: y)); p.line(to: NSPoint(x: 1880, y: y))
    p.lineWidth = 1.5; color("CCD3DB").setStroke(); p.stroke()
}

func draw(_ entry: Entry, art: NSImage, context cg: CGContext, scale: CGFloat) {
    cg.saveGState()
    cg.translateBy(x: 0, y: height * scale)
    cg.scaleBy(x: scale, y: -scale)
    cg.setShouldAntialias(true); cg.setShouldSmoothFonts(true); cg.interpolationQuality = .high
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: true)
    rect(NSRect(x: 0, y: 0, width: width, height: height), paper)
    rect(NSRect(x: 0, y: 660, width: width, height: 860), color(entry.theme))

    text("The difficult word atlas", NSRect(x: 120, y: 65, width: 1100, height: 36), size: 23, fill: muted)
    text(String(format: "%02d / 23", entry.index), NSRect(x: 1530, y: 65, width: 350, height: 36),
         size: 23, fill: muted, align: .right)
    var titleSize: CGFloat = 250
    while (entry.word as NSString).size(withAttributes: [.font: NSFont(name: "Didot", size: titleSize)!, .kern: -3.5]).width > 1760 {
        titleSize -= 1
    }
    text(entry.word, NSRect(x: 108, y: 113, width: 1790, height: 320),
         font: "Didot", size: titleSize, tracking: -3.5)
    text(entry.tagline, NSRect(x: 122, y: 409, width: 1756, height: 71),
         font: "Baskerville-Italic", size: 48, minimum: 43)
    text("noun     " + entry.pronunciation, NSRect(x: 123, y: 481, width: 1740, height: 39),
         size: 23, fill: muted)
    text(entry.definition, NSRect(x: 123, y: 542, width: 1754, height: 99),
         font: "Baskerville", size: 34, line: 44, minimum: 31)

    art.draw(in: NSRect(x: 120, y: 671, width: 1760, height: 782.222),
             from: .zero, operation: .sourceOver, fraction: 1, respectFlipped: true,
             hints: [.interpolation: NSImageInterpolation.high])
    if entry.slug == "hysteresis" {
        text("response", NSRect(x: 1040, y: 733, width: 260, height: 34), size: 23, fill: mist)
        text("input", NSRect(x: 1720, y: 1090, width: 155, height: 34), size: 23, fill: mist)
    }
    text(entry.art_caption, NSRect(x: 120, y: 1464, width: 1760, height: 51),
         size: 23, fill: mist, line: 29, align: .center, minimum: 21)

    text("Inside the word", NSRect(x: 120, y: 1560, width: 335, height: 53),
         font: "Baskerville", size: 37)
    text(entry.etymology, NSRect(x: 495, y: 1554, width: 1385, height: 123),
         font: "Baskerville", size: 29, fill: muted, line: 37, minimum: 27)
    line(1700)
    for (i, section) in entry.sections.enumerated() {
        let x: CGFloat = i % 2 == 0 ? 120 : 1050
        let y: CGFloat = i < 2 ? 1737 : 2036
        text(section.heading, NSRect(x: x, y: y, width: 830, height: 51),
             font: "Baskerville", size: 39, line: 45, minimum: 34)
        text(section.text, NSRect(x: x, y: y + 62, width: 830, height: 224),
             font: "Baskerville", size: 29, line: 36, minimum: 26.5)
    }
    text(entry.literary, NSRect(x: 120, y: 2343, width: 1760, height: 85),
         font: "Baskerville-Italic", size: 30.5, line: 38, minimum: 28)
    text("An original literary sentence. Full explanation and reading notes: " + entry.stem + ".md",
         NSRect(x: 120, y: 2443, width: 1760, height: 28), size: 18, fill: muted)

    NSGraphicsContext.restoreGraphicsState()
    cg.restoreGState()
}

func bitmap(_ entry: Entry, art: NSImage, width: Int, height: Int, output: URL, dpi: CGFloat) throws {
    overflow = []; adjustments = []
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    rep.setProperty(.colorSyncProfileData, withValue: NSColorSpace.sRGB.iccProfileData!)
    let gc = NSGraphicsContext(bitmapImageRep: rep)!
    draw(entry, art: art, context: gc.cgContext, scale: CGFloat(width) / 2000)
    rep.size = NSSize(width: CGFloat(width) * 72 / dpi, height: CGFloat(height) * 72 / dpi)
    if !overflow.isEmpty {
        for issue in overflow { FileHandle.standardError.write(Data((entry.stem + ": " + issue + "\n").utf8)) }
        let path = URL(fileURLWithPath: "/tmp/memoryx-word-atlas23/overflow-" + entry.stem + ".png")
        try rep.representation(using: .png, properties: [:])!.write(to: path)
        throw NSError(domain: "Typography overflow", code: entry.index)
    }
    try rep.representation(using: .png, properties: [:])!.write(to: output, options: .atomic)
    print("SAVED \(output.lastPathComponent) \(width)×\(height); fit adjustments \(adjustments.count)")
    fflush(stdout)
}

func artFor(_ entry: Entry) -> NSImage {
    let path = atlas.appendingPathComponent("source/art/" + entry.stem + ".png")
    return NSImage(contentsOf: path)!
}

if exportPDF {
    let target = root.appendingPathComponent("word-atlas-23-print.pdf")
    let temporary = URL(fileURLWithPath: "/tmp/memoryx-word-atlas23/book-unindexed.pdf")
    var page = CGRect(x: 0, y: 0, width: 1440, height: 1800)
    let consumer = CGDataConsumer(url: temporary as CFURL)!
    let pdf = CGContext(consumer: consumer, mediaBox: &page, [
        kCGPDFContextTitle: "The difficult word atlas — 23 illustrated inquiries",
        kCGPDFContextAuthor: "Locally rendered illustrated word studies",
        kCGPDFContextSubject: "Language, philosophy, perception and systems"
    ] as CFDictionary)!
    for entry in allEntries {
        autoreleasepool {
            let art = artFor(entry)
            pdf.beginPDFPage(nil)
            draw(entry, art: art, context: pdf, scale: 0.72)
            pdf.endPDFPage()
        }
    }
    pdf.closePDF()
    let book = PDFDocument(url: temporary)!
    let outline = PDFOutline()
    for (i, entry) in allEntries.enumerated() {
        let chapter = PDFOutline()
        chapter.label = String(format: "%02d", entry.index) + "  " + entry.word
        chapter.destination = PDFDestination(page: book.page(at: i)!, at: NSPoint(x: 0, y: 1800))
        outline.insertChild(chapter, at: i)
    }
    book.outlineRoot = outline
    guard book.write(to: target) else { fatalError("Failed to save PDF") }
    print("SAVED \(target.lastPathComponent), \(allEntries.count) bookmarked pages")
} else if exportContact {
    let cols = 5, rows = (entries.count + 4) / 5
    let cellW = 300, cellH = 405
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: cols * cellW, pixelsHigh: rows * cellH,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    let gc = NSGraphicsContext(bitmapImageRep: rep)!
    gc.cgContext.translateBy(x: 0, y: CGFloat(rows * cellH))
    gc.cgContext.scaleBy(x: 1, y: -1)
    NSGraphicsContext.current = NSGraphicsContext(cgContext: gc.cgContext, flipped: true)
    rect(NSRect(x: 0, y: 0, width: cols * cellW, height: rows * cellH), color("DDE2E7"))
    for (i, entry) in entries.enumerated() {
        let image = NSImage(contentsOf: atlas.appendingPathComponent("previews/" + entry.stem + ".png"))!
        image.draw(in: NSRect(x: (i % cols) * cellW + 8, y: (i / cols) * cellH + 6, width: 284, height: 355),
            from: .zero, operation: .sourceOver, fraction: 1, respectFlipped: true, hints: [.interpolation:NSImageInterpolation.high])
        text(entry.stem, NSRect(x: (i % cols) * cellW + 12, y: (i / cols) * cellH + 369, width: 280, height: 30), size: 17)
    }
    try rep.representation(using: .png, properties: [:])!.write(to: atlas.appendingPathComponent("contact-sheet.png"))
    print("SAVED contact-sheet.png")
} else {
    for entry in entries {
        try autoreleasepool {
            let art = artFor(entry)
            let preview = atlas.appendingPathComponent("previews/" + entry.stem + ".png")
            try bitmap(entry, art: art, width: 1200, height: 1500, output: preview, dpi: 72)
            if !previewOnly {
                let target = root.appendingPathComponent("atlas-" + entry.stem + "-8000x10000.png")
                guard !FileManager.default.fileExists(atPath: target.path) else {
                    print("EXISTS \(target.lastPathComponent), preserved")
                    return
                }
                try bitmap(entry, art: art, width: 8000, height: 10000, output: target, dpi: 400)
            }
        }
    }
}
