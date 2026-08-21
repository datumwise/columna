// /llms.txt — the agent orientation index.
//
// WAS a static asset at public/llms.txt. It is a ROUTE now because nine of its lines are publication
// facts and a static file cannot read the registry. Same URL, same bytes for every ratified line,
// same content type. See src/lib/llmsIndex.ts for what is composed and why.
import { LLMS_INDEX } from '../lib/llmsIndex';

export const prerender = true;

export function GET() {
  return new Response(`${LLMS_INDEX}\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
