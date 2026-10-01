import Foundation
import PDFKit

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let catalog = try JSONSerialization.jsonObject(with: Data(contentsOf: root.appendingPathComponent("word-atlas-23/catalog.json"))) as! [[String: Any]]
let pdf = PDFDocument(url: root.appendingPathComponent("word-atlas-23-print.pdf"))!
precondition(pdf.pageCount == 23)
precondition(pdf.outlineRoot?.numberOfChildren == 23)
func normalize(_ string: String) -> String {
    string.decomposedStringWithCompatibilityMapping
        .replacingOccurrences(of: "([-–‑])[ \\t]*[\\r\\n]+[ \\t]*", with: "$1", options: .regularExpression)
        .replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression)
        .trimmingCharacters(in: .whitespacesAndNewlines)
}
for (i, entry) in catalog.enumerated() {
    let page = pdf.page(at: i)!
    let value = normalize(page.string ?? "")
    let word = entry["word"] as! String
    precondition(value.contains(normalize(word)), "Missing title: \(word)")
    precondition(page.bounds(for: .mediaBox).size == NSSize(width: 1440, height: 1800))
    for section in entry["sections"] as! [[String: String]] {
        precondition(value.contains(normalize(section["heading"]!)), "Missing section: \(word)")
        precondition(value.contains(normalize(section["text"]!)), "Incomplete paragraph: \(word)")
    }
    precondition(value.contains(normalize(entry["literary"] as! String)), "Incomplete literary sentence: \(word)")
}
print("PDF verified: 23 pages, 23 bookmarks, all section paragraphs and literary sentences present, 20×25 inch pages.")
