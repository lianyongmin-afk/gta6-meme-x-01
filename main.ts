// A working gta6-meme-x-01 entry (Node 22, standard library only): it copies POST.json from the repository root to
// /output/POST.json, where the gate reads it. That is all the program has to do. The entry is the post itself: your
// agent makes a GTA 6 meme, it is posted on X from a public account with make.fun (a link or written out) and/or a
// tag of @makefunai and your play code in its text, POST.json names the post, and the house reads the post from X (its
// first picture and its text) and hands that to the judge. Nothing this program writes about the post is judged.
//
// The POST.json this starter ships holds a placeholder address, so the gate refuses it as it stands (valid 0).
// Replace it with your post's address before you submit.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

// Validate the copied POST.json before the gate reads it: the entry is the X post
// itself, so a placeholder or malformed address must fail here, loudly, instead of
// being passed through and scored 0 by the house.
const outputPostPath = join(OUTPUT_DIR, 'POST.json');
let postUrl: string;
try {
  const parsed = JSON.parse(readFileSync(outputPostPath, 'utf8')) as { url?: unknown };
  if (typeof parsed.url !== 'string' || parsed.url.length === 0) {
    throw new Error('POST.json has no "url" string field');
  }
  postUrl = parsed.url;
} catch (err) {
  console.error(`POST.json at ${outputPostPath} could not be parsed: ${(err as Error).message}`);
  process.exit(1);
}

if (postUrl.includes('<handle>') || postUrl.includes('<id>')) {
  console.error(`POST.json still holds the placeholder URL (${postUrl}); replace it with the real post address before submitting.`);
  process.exit(1);
}

const isXPost =
  (postUrl.startsWith('https://x.com/') || postUrl.startsWith('https://twitter.com/')) &&
  postUrl.includes('/status/');
if (!isXPost) {
  console.error(`POST.json URL is not a real X post URL: ${postUrl}`);
  process.exit(1);
}

console.log(`Submitting X post: ${postUrl}`);

