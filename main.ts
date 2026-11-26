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
console.log(`wrote ${target} (${writtenBytes.length} bytes)`);
