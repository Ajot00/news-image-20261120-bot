import { createHash } from 'node:crypto';
import { copyFile, mkdir, readFile, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const source = join(scriptDir, 'entry.png');
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR || '/output');
const destination = join(outputDir, 'entry.png');

async function hash(path: string): Promise<string> {
  return createHash('sha256').update(await readFile(path)).digest('hex');
}

try {
  const info = await stat(source);
  if (!info.isFile() || info.size === 0 || info.size > 1048576) {
    throw new Error(`source must be a non-empty file no larger than 1 MiB (got ${info.size} bytes)`);
  }
  const sourceBytes = await readFile(source);
  if (sourceBytes[0] !== 0xff || sourceBytes[1] !== 0xd8 || sourceBytes[2] !== 0xff) {
    throw new Error('source entry.png does not contain a JPEG image');
  }
  await mkdir(outputDir, { recursive: true });
  await copyFile(source, destination);
  const [sourceHash, destinationHash] = await Promise.all([hash(source), hash(destination)]);
  console.log(`saved ${destination} (${info.size} bytes) sha256=${destinationHash}`);
  if (sourceHash !== destinationHash) throw new Error('source and copied image SHA-256 hashes differ');
} catch (error) {
  console.error(`news-image-20261120-bot: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
}
