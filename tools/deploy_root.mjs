import { cp, mkdir, rm } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = resolve(root, 'dist');

const targets = [
  ['index.html', 'index.html'],
  ['assets', 'assets'],
  ['songs.sqlite', 'songs.sqlite'],
  ['CNAME', 'CNAME'],
  ['.nojekyll', '.nojekyll'],
];

await mkdir(root, { recursive: true });
await rm(resolve(root, 'assets'), { recursive: true, force: true });

for (const [source, target] of targets) {
  await cp(resolve(dist, source), resolve(root, target), {
    recursive: true,
    force: true,
  });
}
