import { cli, Strategy } from '@jackwener/opencli/registry';
import { spawnSync } from 'node:child_process';

function safeText(value, fallback) {
  const text = String(value ?? fallback);
  if (!text || text.length > 500 || text.includes('\0')) {
    throw new Error('Unsafe argument');
  }
  return text;
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
  name: 'status',
  description: 'Show local ForgeLoop project status.',
  access: 'read',
  example: 'opencli forgeloop status --root . -f json',
  strategy: Strategy.LOCAL,
  browser: false,
  args: [
    { name: 'root', type: 'string', default: '.', help: 'Repository root.' }
  ],
  columns: ['metric', 'value'],
  func: async (kwargs) => {
    const root = safeText(kwargs.root, '.');
    const result = runForgeLoop(['status', root, '--json']);
    if (result.status !== 0) {
      throw new Error((result.stderr || result.stdout || 'ForgeLoop status failed').trim());
    }
    const payload = JSON.parse(result.stdout);
    return Object.entries(payload).map(([metric, value]) => ({
      metric,
      value: String(value)
    }));
  }
});

