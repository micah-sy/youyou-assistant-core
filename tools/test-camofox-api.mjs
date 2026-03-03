import fetch from 'node-fetch';

const BASE_URL = 'http://localhost:9377';

console.log('🦊 测试 Camofox Browser API...\n');

// 测试 1: 健康检查
console.log('1️⃣ 健康检查...');
const health = await fetch(`${BASE_URL}/health`);
console.log('   状态:', health.status === 200 ? '✅ OK' : '❌ FAIL');

// 测试 2: 创建标签页
console.log('\n2️⃣ 创建标签页...');
const createTab = await fetch(`${BASE_URL}/tabs`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userId: 'test',
    sessionKey: 'test1',
    url: 'https://www.google.com/'
  })
});
const tabData = await createTab.json();
console.log('   标签页 ID:', tabData.tabId);
const tabId = tabData.tabId;

// 等待页面加载
await new Promise(r => setTimeout(r, 3000));

// 测试 3: 获取快照
console.log('\n3️⃣ 获取页面快照...');
const snapshot = await fetch(`${BASE_URL}/tabs/${tabId}/snapshot?userId=test`);
const snapshotData = await snapshot.json();
console.log('   快照长度:', snapshotData.snapshot?.length || 0, '字符');
console.log('   页面标题:', snapshotData.title?.substring(0, 50) || 'N/A');

// 测试 4: 搜索
console.log('\n4️⃣ 执行搜索...');
await fetch(`${BASE_URL}/tabs/${tabId}/type`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userId: 'test',
    ref: 'search',
    text: '伊朗历史',
    pressEnter: true
  })
});
await new Promise(r => setTimeout(r, 5000));

// 测试 5: 截图
console.log('\n5️⃣ 截图...');
const screenshot = await fetch(`${BASE_URL}/tabs/${tabId}/screenshot?userId=test`);
const imgBuffer = await screenshot.buffer();
console.log('   截图大小:', (imgBuffer.length / 1024).toFixed(2), 'KB');

// 保存截图
import fs from 'fs';
fs.writeFileSync('/tmp/camofox-api-test.png', imgBuffer);
console.log('   已保存：/tmp/camofox-api-test.png');

// 测试 6: 检查人机验证
console.log('\n6️⃣ 检查人机验证...');
const snapshot2 = await fetch(`${BASE_URL}/tabs/${tabId}/snapshot?userId=test`);
const snapshotData2 = await snapshot2.json();
const hasCaptcha = snapshotData2.snapshot?.toLowerCase().includes('captcha') || 
                   snapshotData2.snapshot?.includes('验证');
console.log('   人机验证:', hasCaptcha ? '❌ 检测到' : '✅ 未检测到');

// 清理：关闭标签页
console.log('\n7️⃣ 关闭标签页...');
await fetch(`${BASE_URL}/tabs/${tabId}`, { method: 'DELETE' });
console.log('   已关闭');

console.log('\n✅ 全部测试完成!');
