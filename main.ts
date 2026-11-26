import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Copy the entry image into the output directory make.fun expects.
// Standard library only; refuses to ship an image over the 1 MiB cap.
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const size = statSync(src).size;
if (size > 1048576) {
  console.error(`entry.png is ${size} bytes, over the 1 MiB cap`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log(`wrote ${dest} (${size} bytes)`);
