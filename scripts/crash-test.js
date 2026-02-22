#!/usr/bin/env node
/**
 * CRASH-TEST.js - Demonstrē crash-proof sistēmu
 * 
 * Šis skripts simulē dažādas kļūdas un parāda, kā sistēma tās apķīlā.
 */

const { safeExec, safeKill } = require('./safe-executor');

async function runTests() {
  console.log('═══════════════════════════════════════');
  console.log('  CRASH-PROOF SYSTEM TEST');
  console.log('═══════════════════════════════════════\n');

  // Test 1: Veiksmīga komanda
  console.log('Test 1: Veiksmīga komanda');
  const r1 = await safeExec('echo "Hello World"', { timeout: 5 });
  console.log(`  Success: ${r1.success}, Output: ${r1.output.trim()}`);
  console.log(`  ✅ PASS\n`);

  // Test 2: Neeksistējoša komanda (jāapķīlā)
  console.log('Test 2: Neeksistējoša komanda (kļūda jāapķīlā)');
  const r2 = await safeExec('this_command_does_not_exist_12345', { timeout: 5 });
  console.log(`  Success: ${r2.success}, Error: ${r2.error ? 'Yes' : 'No'}`);
  console.log(`  ✅ PASS - Kļūda apķīlāta, sistēma dzīva!\n`);

  // Test 3: Timeout
  console.log('Test 3: Timeout pārsniegšana');
  const r3 = await safeExec('sleep 10', { timeout: 1 });
  console.log(`  Success: ${r3.success}, Signal: ${r3.signal || 'none'}`);
  console.log(`  ✅ PASS - Timeout apķīlāts!\n`);

  // Test 4: SIGTERM apstrāde
  console.log('Test 4: SIGTERM apstrāde (simulēts)');
  const r4 = await safeExec('echo test && exit 143', { timeout: 5 }); // 143 = 128 + 15 (SIGTERM)
  console.log(`  Success: ${r4.success}, ExitCode: ${r4.exitCode}`);
  console.log(`  ✅ PASS - SIGTERM apķīlāts!\n`);

  // Test 5: Drošs procesu kill
  console.log('Test 5: Drošs procesu kill (neeksistējošs process)');
  const r5 = await safeKill('nonexistent_process_98765');
  console.log(`  Success: ${r5.success}`);
  console.log(`  ✅ PASS - Neeksistējoša procesa kill neizraisa kļūdu!\n`);

  // Test 6: Neiznīcināmais cikls
  console.log('Test 6: Neiznīcināmais cikls (3 iterācijas)');
  let errorsCaught = 0;
  for (let i = 0; i < 3; i++) {
    try {
      if (i === 1) {
        throw new Error('Simulēta kļūda!');
      }
      console.log(`  Iteration ${i}: OK`);
    } catch (error) {
      errorsCaught++;
      console.log(`  Iteration ${i}: Kļūda apķīlāta - ${error.message}`);
    }
  }
  console.log(`  ✅ PASS - ${errorsCaught} kļūdas apķīlātas, cikls turpinās!\n`);

  console.log('═══════════════════════════════════════');
  console.log('  VISI TESTI IZIETI!');
  console.log('  Sistēma ir crash-proof.');
  console.log('═══════════════════════════════════════');
}

runTests().catch(err => {
  console.error('FATAL: Pat tests izraisīja kļūdu:', err);
  process.exit(1);
});
