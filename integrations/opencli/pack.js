import { cli, Strategy } from '@jackwener/opencli/registry';
import { spawnSync } from 'node:child_process';

function safeText(value, fallback) {
  const text = String(value ?? fallback);
  if (!text || text.length > 1000 || text.includes('\0')) {
    throw new Error('Unsafe argument');
  }
  return text;
}

function safeLimit(value) {
  const parsed = Number.parseInt(String(value ?? '5'), 10);
  if (!Number.isFinite(parsed)) {
    return '5';
  }
  return String(Math.max(1, Math.min(parsed, 25)));
}

function runForgeLoop(args) {
  const python = safeText(process.env.FORGELOOP_PYTHON, 'python');
  return spawnSync(python, ['-m', 'forgeloop', ...args], {
    encoding: 'utf8',
    maxBuffer: 1024 * 1024,
    shell: false,
    timeout: 30000,
    windowsHide: true
  });
}

cli({
  site: 'forgeloop',
  name: 'pack',
  description: 'Build a pointer-only ForgeLoop context packet.',
  access: 'read',
  example: 'opencli forgeloop pack --query "memory validation" --root . --limit 5 -f json',
  strategy: Strategy.LOCAL,
  browser: false,
  args: [
    { name: 'query', type: 'string', required: true, help: 'Task or memory query.' },
    { name: 'root', type: 'string', default: '.', help: 'Repository root.' },
    { name: 'limit', type: 'int', default: 5, help: 'Maximum records to return.' }
  ],
  columns: ['packet'],
  func: async (kwargs) => {
    const query = safeText(kwargs.query, '');
    const root = safeText(kwargs.root, '.');
    const limit = safeLimit(kwargs.limit);
    const result = runForgeLoop(['pack', query, root, '--limit', limit]);
    if (result.status !== 0) {
      throw new Error((result.stderr || result.stdout || 'ForgeLoop pack failed').trim());
    }
    return [{ packet: result.stdout.trim() }];
  }
});

