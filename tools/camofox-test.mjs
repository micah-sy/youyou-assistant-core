import { chromium } from 'playwright';

console.log('🦊 启动 Camofox Browser 测试...');

// 使用临时用户数据
const userDataDir = '/tmp/camofox-test-' + Date.now();

const browser = await chromium.launchPersistentContext(userDataDir, {
  headless: true,
  executablePath: '/usr/bin/google-chrome',
  viewport: { width: 1920, height: 1080 },
  args: [
    '--disable-blink-features=AutomationControlled',
    '--no-sandbox',
    '--disable-dev-shm-usage'
  ]
});

const page = browser.pages()[0];

// 访问 Google
console.log('🌐 访问 Google...');
await page.goto('https://www.google.com/', { waitUntil: 'networkidle' });
await page.waitForTimeout(3000);

// 搜索
console.log('🔍 搜索：伊朗...');
const searchBox = await page.$('textarea[name="q"]');
await searchBox.click({ delay: 150 });
await searchBox.type('伊朗', { delay: 80 });
await page.keyboard.press('Enter');
await page.waitForTimeout(5000);

// 检查人机验证
const hasCaptcha = await page.evaluate(() => {
  const text = document.body.innerText.toLowerCase();
  return text.includes('captcha') || text.includes('robot') || text.includes('验证');
});

console.log('人机验证:', hasCaptcha ? '❌ 检测到' : '✅ 未检测到');

// 截图
await page.screenshot({ 
  path: '/home/tellice/.openclaw/workspace/tools/camofox-google-iran.png',
  fullPage: false 
});

console.log('✅ 测试完成！');
console.log('截图：camofox-google-iran.png');

await browser.close();
