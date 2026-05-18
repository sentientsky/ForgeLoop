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
    timeout: 45000,
    windowsHide: true
  });
}

cli({
  site: 'forgeloop',
  name: 'doctor',
  description: 'Run the ForgeLoop health check from OpenCLI.',
  access: 'read',
  example: 'opencli forgeloop doctor --root . -f json',
  strategy: Strategy.LOCAL,
  browser: false,
  args: [
    { name: 'root', type: 'string', default: '.', help: 'Repository root.' }
  ],
  columns: ['check', 'status', 'message'],
  func: async (kwargs) => {
    const root = safeText(kwargs.root, '.');
    const result = runForgeLoop(['doctor', root, '--json']);
    if (result.status !== 0 && !result.stdout) {
      throw new Error((result.stderr || 'ForgeLoop doctor failed').trim());
    }
    const payload = JSON.parse(result.stdout);
    return payload.checks.map((check) => ({
      check: check.name,
      status: check.status,
      message: check.message
    }));
  }
});

