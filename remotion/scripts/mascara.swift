// Máscara de persona con Apple Vision (VNGeneratePersonSegmentationRequest).
// Lee un video, segmenta a la persona cuadro por cuadro y escribe por stdout
// cuadros en escala de grises (8 bits) de ANCHO x ALTO. ffmpeg los convierte en video.
// Uso: mascara <video> <ancho> <alto>
import AVFoundation
import CoreImage
import Foundation
import Vision

let args = CommandLine.arguments
guard args.count >= 4, let W = Int(args[2]), let H = Int(args[3]) else {
    FileHandle.standardError.write("uso: mascara <video> <ancho> <alto>\n".data(using: .utf8)!)
    exit(1)
}
let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let semaforo = DispatchSemaphore(value: 0)
var pistas: [AVAssetTrack] = []
Task {
    pistas = (try? await asset.loadTracks(withMediaType: .video)) ?? []
    semaforo.signal()
}
semaforo.wait()
guard let pista = pistas.first, let lector = try? AVAssetReader(asset: asset) else {
    FileHandle.standardError.write("no pude abrir el video\n".data(using: .utf8)!)
    exit(1)
}
let salida = AVAssetReaderTrackOutput(track: pista, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
salida.alwaysCopiesSampleData = false
lector.add(salida)
lector.startReading()

let pedido = VNGeneratePersonSegmentationRequest()
pedido.qualityLevel = .accurate
pedido.outputPixelFormat = kCVPixelFormatType_OneComponent8
let contexto = CIContext(options: [.useSoftwareRenderer: false])
var bytes = [UInt8](repeating: 0, count: W * H)
let out = FileHandle.standardOutput
var n = 0
while let muestra = salida.copyNextSampleBuffer() {
    autoreleasepool {
        guard let cuadro = CMSampleBufferGetImageBuffer(muestra) else { return }
        let handler = VNImageRequestHandler(cvPixelBuffer: cuadro, orientation: .up, options: [:])
        try? handler.perform([pedido])
        if let m = pedido.results?.first?.pixelBuffer {
            var img = CIImage(cvPixelBuffer: m)
            img = img.transformed(by: CGAffineTransform(scaleX: CGFloat(W) / img.extent.width, y: CGFloat(H) / img.extent.height))
            contexto.render(img, toBitmap: &bytes, rowBytes: W, bounds: CGRect(x: 0, y: 0, width: W, height: H), format: .L8, colorSpace: nil)
        } else {
            for i in 0..<bytes.count { bytes[i] = 0 }
        }
        out.write(Data(bytes))
        n += 1
        if n % 300 == 0 { FileHandle.standardError.write("  \(n) cuadros\n".data(using: .utf8)!) }
    }
}
FileHandle.standardError.write("listo: \(n) cuadros\n".data(using: .utf8)!)
