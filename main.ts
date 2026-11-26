// News Image 20261125 entry (Node 22, standard library only).
//
// The entry image lives in this repository as entry.png: one 1024x1024 PNG
// summing up the world news of Wednesday 25 November 2026. This program
// copies it to the output directory and then verifies the copy by reading
// it back: the bytes must match the source exactly and the file must stay
// within the competition limit of 1 MiB (1048576 bytes).
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576;

const sourcePath = fileURLToPath(new URL("./entry.png", import.meta.url));
const sourceBytes = readFileSync(sourcePath);
if (sourceBytes.length === 0 || sourceBytes.length > MAX_BYTES) {
  throw new Error(
    `entry.png is ${sourceBytes.length} bytes, outside 1-${MAX_BYTES}`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
writeFileSync(target, sourceBytes);

// Read-back verification: the written file must be byte-identical to the
// repository image, so the judge sees exactly the bytes we shipped.
const writtenBytes = readFileSync(target);
if (writtenBytes.length > MAX_BYTES) {
  throw new Error(
    `output is ${writtenBytes.length} bytes, over the ${MAX_BYTES} limit`,
  );
}
if (!writtenBytes.equals(sourceBytes)) {
  throw new Error(
    `output bytes mismatch: ${writtenBytes.length} bytes written vs ${sourceBytes.length} in entry.png`,
  );
}

// PNG magic bytes (89 50 4E 47 0D 0A 1A 0A) must be present in the
// written file, otherwise the output is not a PNG at all.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (
  writtenBytes.length < PNG_SIGNATURE.length ||
  !writtenBytes.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)
) {
  throw new Error("output is missing the PNG signature");
}

// IHDR is the first chunk: length(4) + type(4) + width(4) + height(4).
// Verify the image dimensions stay within the 1024x1024 competition cap.
if (writtenBytes.length < 24 || writtenBytes.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("output is missing a valid IHDR chunk");
}
const width = writtenBytes.readUInt32BE(16);
const height = writtenBytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > 1024 || height > 1024) {
  throw new Error(`output dimensions ${width}x${height} exceed 1024x1024`);
}

// Determinism check: a second independent copy must be byte-identical
// to the first, so the result does not depend on filesystem quirks.
const target2 = join(outDir, "entry-check.png");
writeFileSync(target2, sourceBytes);
const writtenBytes2 = readFileSync(target2);
if (!writtenBytes2.equals(writtenBytes)) {
  throw new Error("second copy differs from first copy; output is not deterministic");
}

console.log(`wrote ${target} (${writtenBytes.length} bytes, ${width}x${height})`);
